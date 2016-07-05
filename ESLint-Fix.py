# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sublime, sublime_plugin
import platform
import os, sys, subprocess, codecs, webbrowser, re
from subprocess import Popen, PIPE


PROJECT_NAME = "ESLint-Fix"
SETTINGS_FILE = PROJECT_NAME + ".sublime-settings"
KEYMAP_FILE = "Default ($PLATFORM).sublime-keymap"

IS_WINDOWS = platform.system() == 'Windows'

class FixEslintCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    # Save the current viewport position to scroll to it after formatting.
    previous_selection = list(self.view.sel()) # Copy.
    previous_position = self.view.viewport_position()

    # Save the already folded code to refold it after formatting.
    # Backup of folded code is taken instead of regions because the start and end pos
    # of folded regions will change once formatted.
    folded_regions_content = [self.view.substr(r) for r in self.view.folded_regions()]

    # Get the current text in the buffer and save it in a temporary file.
    # This allows for scratch buffers and dirty files to be linted as well.
    entire_buffer_region = sublime.Region(0, self.view.size())

    buffer_text = self.get_buffer_text(entire_buffer_region)

    output = self.run_script_on_file(self.view.file_name())

    # return
    # eslint currently does not print the fixed file to stdout, it just modifies the file.

    # If the prettified text length is nil, the current syntax isn't supported.
    if output == None or len(output) < 1:
      return

    # Replace the text only if it's different.
    if output != buffer_text:
      self.view.replace(edit, entire_buffer_region, output)

    self.refold_folded_regions(folded_regions_content, output)
    self.view.set_viewport_position((0, 0), False)
    self.view.set_viewport_position(previous_position, False)
    self.view.sel().clear()

    # Restore the previous selection if formatting wasn't performed only for it.
    # if not is_formatting_selection_only:
    for region in previous_selection:
      self.view.sel().add(region)

  def get_buffer_text(self, region):
    buffer_text = self.view.substr(region)
    return buffer_text

  def run_script_on_file(self, data):
    try:
      node_path = PluginUtils.get_node_path()
      eslint_path = PluginUtils.get_eslint_path()

      if eslint_path == False:
        sublime.error_message('ESLint could not be found on your path')
        return

      cmd = [node_path, eslint_path, '--fix', data]

      # cmd = ['npm run', 'eslint', '--fix', data]
      config_path = PluginUtils.get_config_path()
      if config_path:
        print("Using configuration from {0}".format(config_path))
        cmd.extend(["--config", config_path])

      if self.view.file_name():
          cdir = os.path.dirname(self.view.file_name())
      else:
          cdir = "/"

      # output = PluginUtils.get_output(cmd, cdir, data)
      file = open(data, 'w')
      file.write(self.view.substr(sublime.Region(0, self.view.size())))
      file.close()
      eslint_log = PluginUtils.get_output(cmd, cdir, data)
      output = open(data, 'r').read()

      return output

    except:
      # Something bad happened.
      msg = str(sys.exc_info()[1])
      print("Unexpected error({0}): {1}".format(sys.exc_info()[0], msg))
      sublime.error_message(msg)

  def refold_folded_regions(self, folded_regions_content, entire_file_contents):
    self.view.unfold(sublime.Region(0, len(entire_file_contents)))
    region_end = 0

    for content in folded_regions_content:
      region_start = entire_file_contents.index(content, region_end)
      if region_start > -1:
        region_end = region_start + len(content)
        self.view.fold(sublime.Region(region_start, region_end))


class ESLintFixEventListeners(sublime_plugin.EventListener):
  @staticmethod
  def on_pre_save(view):
    if PluginUtils.get_pref("format_on_save"):
      extensions = PluginUtils.get_pref("format_on_save_extensions")
      extension = os.path.splitext(view.file_name())[1][1:]

      # Default to using filename if no extension
      if not extension:
        extension = os.path.basename(view.file_name())

      # Skip if extension is not whitelisted
      if extensions and not extension in extensions:
        return

      view.run_command("fix_eslint")

class PluginUtils:
  @staticmethod
  def get_pref(key):
    global_settings = sublime.load_settings(SETTINGS_FILE)
    value = global_settings.get(key)

    # Load active project settings
    project_settings = sublime.active_window().active_view().settings()

    # Overwrite global config value if it's defined
    if project_settings.has(PROJECT_NAME):
      value = project_settings.get(PROJECT_NAME).get(key, value)

    return value

  @staticmethod
  def get_node_path():
    platform = sublime.platform()
    node = PluginUtils.get_pref("node_path").get(platform)
    print("Using node.js path on '" + platform + "': " + node)
    return node

  @staticmethod
  def get_config_path():
    cwd = os.getcwd()
    folders = cwd.split('/')
    return PluginUtils.get_eslint_config(cwd, folders)

  @staticmethod
  def get_eslint_config(root, folders):
    cfs = ['.eslintrc.js', '.eslintrc.yaml', '.eslintrc.yml', '.eslintrc.json', '.eslintrc']
    dir = None
    for cf in cfs:
      fd = os.path.join(root, cf)
      if os.path.isfile(fd):
        dir = fd
        return dir

    if dir == None:
      f = folders.pop()
      if f:
        d = root.split(f)[0]
        if d:
          dir = PluginUtils.get_eslint_config(d, folders)
          return dir

    return False

  @staticmethod
  def get_eslint(root, folders):
    # get from local node_modules first
    ePath = 'node_modules/.bin/eslint'
    eslint = os.path.join(root, ePath)

    if os.path.isfile(eslint):
      return eslint
    else:
      fp = folders.pop()
      if fp:
        fd = root.split(fp)[0]
        if fd:
          eslint = PluginUtils.get_eslint(fd, folders)
          return eslint

    return False


  @staticmethod
  def get_eslint_path():
    platform = sublime.platform()
    cwd = os.getcwd()
    folders = cwd.split('/')

    esl = PluginUtils.get_eslint(cwd, folders)

    # if not available, then using the settings config
    if esl == False:
      esl = PluginUtils.get_pref("eslint_path").get(platform)

    print("Using eslint path on '" + platform + "': " + esl)
    return esl


  @staticmethod
  def get_output(cmd, cdir, data):
    try:
      p = Popen(cmd,
        stdout=PIPE, stdin=PIPE, stderr=PIPE,
        cwd=cdir, shell=IS_WINDOWS)
    except OSError:
      raise Exception('Couldn\'t find Node.js. Make sure it\'s in your $PATH by running `node -v` in your command-line.')
    stdout, stderr = p.communicate(input=data.encode('utf-8'))
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    if stderr:
      raise Exception('Error: %s' % stderr)
    else:
      return stdout
