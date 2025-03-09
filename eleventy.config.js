'use strict';
//
//
//

//
const directoryOutputPlugin = require('@11ty/eleventy-plugin-directory-output');
//
const markdownIt = require('markdown-it');
const markdownItDeflist = require('markdown-it-deflist');
const htmlmin = require('html-minifier');
//
const collections = require('./source/_config/eleventy.collections.js');
const shortcodes = require('./source/_config/eleventy.shortcodes.js');
//
const isProduction = process.env.NODE_ENV === 'product' ? true: false;


//
//
//
module.exports = function (eleventyConfig) {

  //
  eleventyConfig.setQuietMode(false);

  //
  // eleventy-plugin-directory-output
  //
  eleventyConfig.addPlugin(directoryOutputPlugin, {
    columns: {
      filesize: true,
      benchmark: true,
    },
    warningFileSize: 400 * 1000,
  });

  //
  // 11ty - Collections
  //
  eleventyConfig.addCollection('contentsSectionWorks', collections.contentsSectionWorks);
  eleventyConfig.addCollection('contentsSectionRecent', collections.contentsSectionRecent);

  //
  // 11ty - Shortcodes
  //
  eleventyConfig.addShortcode('set_image_extension', shortcodes.set_image_extension);
  eleventyConfig.addShortcode('set_image_lightbox2_large', shortcodes.set_image_lightbox2_large);


  //
  // 11ty - Included Nunjucks
  //
  eleventyConfig.setNunjucksEnvironmentOptions({
    throwOnUndefined: true,
    autoescape: false,
  });

  //
  // Markdown
  //
  let markdownIt_options = {
    html: true,
    breaks: true,
    linkify: true,
  };
  //
  let markdownLib = markdownIt(markdownIt_options).use(markdownItDeflist);
  //
  eleventyConfig.setLibrary('md', markdownLib);


  //
  // 11ty - Watch
  //
  eleventyConfig.addWatchTarget('./source/assets/styles/');
  eleventyConfig.addWatchTarget('./source/assets/scripts/');
  eleventyConfig.setWatchThrottleWaitTime(3000);

  //
  if (isProduction) {
    //
    // HTML minify
    //
    eleventyConfig.addTransform('htmlmin', function(content) {
      if (this.page.outputPath && this.page.outputPath.endsWith('.html')) {
        let minified = htmlmin.minify(content, {
          useShortDoctype: true,
          removeComments: true,
          collapseWhitespace: true,
          minifyCSS: true,
          minifyJS: true,
        });
        return minified;
      }
      return content;
    });
  } else {
    //
    // 11ty - eleventy-dev-server, included in 11ty's install
    //
    eleventyConfig.setServerOptions({
      liveReload: true,
      domDiff: true,
      port: 8080,
      watch: [],
      showAllHosts: false,
      https: {},
      encoding: 'utf-8',
      showVersion: false,
    });
  }


  //
  if (! isProduction) {
    eleventyConfig.on('eleventy.beforeWatch', async function () {
      console.log('----  eleventy.beforeWatch  ----');
    });

    eleventyConfig.on('eleventy.before', async function () {
      console.log('----  eleventy.before       ----');
    });

    eleventyConfig.on('eleventy.after', async function () {
      console.log('----  eleventy.after        ----');
    });
  }


  //
  return {
    markdownTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dir: {
      input: './source',
      layouts: './_includes',
      output: isProduction ? './_product' : './_develop'
    }
  };
};
