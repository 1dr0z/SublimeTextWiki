import sublime, sublime_plugin, os
from . import drivers

class WikiLinkCommand(sublime_plugin.TextCommand):

  def __init__(self, view):
    self.view = view

  def run(self, edit):
    # Find an appropriate driver for this file syntax
    syntax    = self.view.settings().get('syntax')
    syntax, _ = os.path.splitext(os.path.basename(syntax))
    driver    = getattr(drivers, syntax.lower(), None)

    if not driver:
      return

    # Open a link for each selection
    for region in self.view.sel():
      link = driver.Link(self.view, region)
      if link.is_valid():
        link.open()

  def is_enabled(self):
    settings = self.view.settings()
    return settings.get('wiki_links_enable', False)