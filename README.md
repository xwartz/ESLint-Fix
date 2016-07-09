## ESLint-Fix

Sublime Text 3 Plugin to fix eslint errors automatically.

Inspired by https://github.com/TheSavior/ESLint-Formatter.

*Use local `eslint` and `eslintrc` first, if not available, then use the settings config.*

[中文](./README-ZHCN.md)

## Installation

### Linter installation

ESLint (with autoformatting) must be installed on your system before this plugin will work. To install eslint, follow the getting started guide: http://eslint.org/docs/user-guide/getting-started.

### Plugin installation

First, clone the repo via git to Sublime's package directory.
And restart the Sublime.

## Commands
**Command palette:**

- ESLintFix: Format this file

**Shortcut key:**

* Linux/Windows: [Ctrl + Shift + H]
* Mac: [Cmd + Shift + H]


## Settings

By default, ESLintFix will supply the following settings:

```javascript
{
  // The Nodejs installation path
  "node_path": {
    "windows": "node.exe",
    "linux": "/usr/bin/nodejs",
    "osx": "/usr/local/bin/node"
  },

  // The location of the the globally installed eslint package
  "eslint_path": {
    "windows": "%APPDATA%/npm/node_modules/eslint/bin/eslint",
    "linux": "/usr/bin/eslint",
    "osx": "/usr/local/bin/eslint"
  },

  // Specify this path to a ESLint config file to override the default behavior.
  // Passed to ESLint as --config. Read more here:
  http://eslint.org/docs/user-guide/command-line-interface#c---config
  "config_path": "",

  // Automatically format when a file is saved.
  "format_on_save": false,

  // Only attempt to format files with whitelisted extensions on save.
  // Leave empty to disable the check
  "format_on_save_extensions": [
    "js",
    "jsx",
    "es",
    "es6",
    "babel"
  ]
}
```

* Modify any settings within the `Preferences -> Package Settings -> ESLint-Fix -> Settings - User` file.

**Project-specific settings override**

To override global plugin configuration for a specific project, add a settings object with a `ESLint-Fix` key in your `.sublime-project`. This file is accessible via `Project -> Edit Project`.

For example:

```
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "ESLint-Fix": {
      "format_on_save": true
    }
  }
}
```

## Contributing

If you find any bugs feel free to report them [here](https://github.com/xwartz/ESLint-Fix/issues).

Pull requests are also encouraged.
