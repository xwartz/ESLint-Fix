## ESLint-Fix

Sublime Text 3 插件，自动修复 `eslint` 检测出的错误。

在 [ESLint-Formatter](https://github.com/TheSavior/ESLint-Formatter) 增加使用 local 的 eslint 和 eslint config 之前推荐使用这个插件

首先会逐层查找项目下的 `eslint` 和 `eslintrc`，如果没有找到使用设置里的。

## 安装

clone 到 sublime 的 package 目录，重启 sublime

## 命令

**Command palette:**

- ESLintFix: Format this file

**Shortcut key:**

* Linux/Windows: [Ctrl + Shift + H]
* Mac: [Cmd + Shift + H]

## 设置

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

## 参与

欢迎提交 [issue](https://github.com/xwartz/ESLint-Fix/issues) 和 pr。



