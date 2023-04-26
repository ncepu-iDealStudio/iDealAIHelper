# about
this project fork from https://github.com/moeakwak/chatgpt-web-share 
A web application that allows multiple users to share one ChatGPT account at the same time, developed using unofficial ChatGPT API & fastapi & vue3. Supports GPT-4! 共享 ChatGPT 账号给多用户同时使用，可用于朋友之间共享或合租 ChatGPT 账号。

使用 FastAPI + Vue3 开发。支持 ChatGPT Plus / 使用 GPT-4 / 用户请求限制等功能。

在原项目前后端的基础上，我们做了相当大的改变和扩展；具体包括：
 1. 增加了前端的prompt提示功能；
 2. 增强了PC和移动端访问的兼容性；
 3. 用户可以独立使用自己的key；也可以共享给他人使用；
 4. 更好的私有化部署；
 5. 更好的代理方式，以避免国内网络对openai接口的屏蔽；
 6. 扩充为智能助手，增加了其他AI产品的对接和支持；

# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support For `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
   1. Run `Extensions: Show Built-in Extensions` from VSCode's command palette
   2. Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## How to devlope in local？


## How to deploy this project?
