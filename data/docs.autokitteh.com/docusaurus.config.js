// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config
require("dotenv").config();
import { themes as prismThemes } from "prism-react-renderer";

import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "AutoKitteh",
  tagline: "Complex automation made simple",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://docs.autokitteh.com",

  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",
  
  // Control trailing slash - set to 'false' to remove trailing slashes or 'true' to add them
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "autokitteh", // Usually your GitHub org/user name.
  projectName: "autokitteh", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: "./sidebars.js",
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: false, // Optional: disable the blog plugin
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: "img/autokitteh-social-card.png",
      navbar: {
        title: "AutoKitteh",
        logo: {
          alt: "AutoKitteh",
          src: "img/autokitteh_512.png",
          href: "https://autokitteh.com",
          target: "_self",
        },
        items: [
          {
            type: "doc",
            position: "left",
            docId: "intro",
            label: "Overview",
          },
          {
            type: "doc",
            position: "left",
            docId: "/tutorials",
            label: "Tutorials",
          },
          {
            type: "doc",
            position: "left",
            docId: "/integrations",
            label: "Integrations",
          },
          {
            href: "https://discord.gg/UhnJuBarZQ",
            label: "Discord",
            position: "right",
          },
          {
            href: "https://github.com/autokitteh/autokitteh",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [],
        copyright: `Copyright © ${new Date().getFullYear()} AutoKitteh, Inc.`,
      },
      prism: {
        additionalLanguages: ["bash", "json", "powershell", "sql"],
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      algolia: {
        appId: process.env.ALGOLIA_APP_ID,
        apiKey: process.env.ALGOLIA_API_KEY,
        indexName: process.env.ALGOLIA_INDEX_NAME,
        contextualSearch: false,
      },
    }),

  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css",
      type: "text/css",
      integrity:
        "sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM",
      crossorigin: "anonymous",
    },
  ],
};

export default config;
