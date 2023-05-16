import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import UnoCSS from "@unocss/vite";
import presetUno from "@unocss/preset-uno";
import { join } from "path";
import Components from "unplugin-vue-components/vite";
import { NaiveUiResolver } from "unplugin-vue-components/resolvers";
import { transformerDirectives } from "unocss";
import { fileURLToPath, URL } from "node:url";
import fs from "fs"
// https://vitejs.dev/config/
export default defineConfig({
  base: "/",
  plugins: [
    vue(),
    UnoCSS({
      presets: [
        /* no presets by default */
        presetUno(),
      ],
      /* options */
      transformers: [transformerDirectives()],
    }),
    Components({
      resolvers: [NaiveUiResolver()],
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  define: {
    "import.meta.env.PACKAGE_VERSION": JSON.stringify(process.env.npm_package_version),
  },
  mode: "development",
  server: {
    host: "0.0.0.0",
    port: 5173,
    fs: {
      strict: true,
    },
    open: true,
    https: {
      // 主要是下面两行的配置文件，不要忘记引入 fs 和 path 两个对象
      cert: fs.readFileSync(fileURLToPath(new URL("src/config/ssl/cert.crt", import.meta.url))),
      key: fs.readFileSync(fileURLToPath(new URL("src/config/ssl/cert.key", import.meta.url)))
    },
    proxy: {
      "/api": {
        // target: "http://127.0.0.1:8000",        
        target: "http://ai.quwancode.com/api",
        changeOrigin: true,
        ws: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  }
});
