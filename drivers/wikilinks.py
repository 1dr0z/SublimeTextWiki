import sublime, os, re

class Link():

  def __init__(self, view, region):
    self.view   = view
    self.valid  = False
    self.window = view.window()

    # Get the link text surrounding our point
    region = view.extract_scope(region.a)
    if ('wikilinks.link' not in view.scope_name(region.a)):
      return

    # Get the link text
    link = view.substr(region)
    if (not link):
      return

    # Parse the link target our of link string
    match = re.match('^\[\[([^\]]+)\]\]$', link)

    if (not match):
      return

    name = match.group(1).strip()
    if (not name):
      return

    self.name  = '{name}.{ext}'.format(name=name, ext='wiki')
    self.valid = True

  def is_valid(self):
    return self.valid

  def open(self):
    # If we can find the file on disk then just open it
    page = self.find()
    if page:
      return self.window.open_file(page)

    path = os.path.dirname(self.name)
    name = os.path.basename(self.name)

    # If there is only one folder then create the file
    folders = self.window.folders()
    if len(folders) == 1:
      basedir = os.path.join(folders[0], path)
      if path and not os.path.exists(basedir):
        os.makedirs(basedir)

      with open(os.path.join(folders[0], self.name), 'a') as target:
        view    = self.window.open_file(self.name)
        sublime.status_message('Creating {file} on disk'.format(file=self.name))
        return view

    # If the target is ambigous open without saving
    view = self.window.new_file()
    view.set_name(name)
    view.set_syntax_file(self.view.settings().get('syntax'))

    message = 'File "{file}" does not exist on disk'.format(file=self.name)
    sublime.status_message(message)
    return view

  def find(self):
    for folder in self.window.folders():
      page = os.path.join(folder, self.name)
      if (os.path.exists(page)):
        return page
    return None