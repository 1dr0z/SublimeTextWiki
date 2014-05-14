from WikiLinks.drivers import wikilinks
import os, re, sublime
from pprint import pprint

class Link(wikilinks.Link):

  def __init__(self, view, selection):
    self.view   = view
    self.valid  = False
    self.window = view.window()

    # There's probably a better way to do this, but at least it's acurate
    regions = view.find_by_selector('meta.link.inline.markdown')
    link    = None

    for region in regions:
      if region.contains(selection):
        link = view.substr(region)
        break

    if not link:
      return

    # Determine the page/header to link to
    match = re.match('\[([^\]]+)\]\(([^\)]*)\)', link)
    if not match:
      return

    if not match.group(2):
      name    = match.group(1)
      heading = '';
    else:
      if '#' in match.group(2):
        name, heading = match.group(2).split('#')
      else:
        name    = match.group(2)
        heading = ''

    if name:
      name = '{name}.{ext}'.format(name=name, ext='md')
    else:
      name = view.file_name()

    self.name    = name
    self.heading = heading
    self.valid   = True

  def open(self):
    # Open the file
    view = super().open()

    # Go to the header position
    if self.heading:
      self._open_heading(view, self.heading)

    return view

  def _open_heading(self, view, heading):
    if view.is_loading():
      # Wait for view to finish loading (async)
      sublime.set_timeout(lambda: self._open_heading(view, heading), 100)
    else:
      symbols = view.indexed_symbols() # markdown headings
      for region, symbol in symbols:
        if symbol.strip(' #').lower() == heading.lower():
          view.show(region)