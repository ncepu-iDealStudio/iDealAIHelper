import MarkdownIt from "markdown-it";
import markdownItHighlight from "markdown-it-highlightjs";
import markdownItKatex from "@traptitech/markdown-it-katex";
import hljs from "highlight.js";

const md = new MarkdownIt({
  html: true,
  linkify: false,
  typographer: true,
})
  .use(markdownItKatex)
  .use(markdownItHighlight, { hljs })

export default md;
