'use strict';

import gulpMode from 'gulp-mode';


export const mode = gulpMode({
  modes: ['product', 'develop'],
  default: 'develop',
  verbose: false
});

export const outputPath = mode.product() ? './_product' : './_develop';

export const path = {
  //
  'scss': {
    'source': [
      './source/assets/styles/site.scss',
    ],
    'watch': './source/assets/styles/**/*.{scss,sass}',
  },
  //
  'javascript': [
    './source/assets/scripts/minimal-theme-switcher.js',
    './source/assets/scripts/modal.js',
  ],
  //
  'image': [
    './source/images/**/*.{jpg,jpeg,png,webp}'
  ],
  //
  'filePaths': [
    {
      'source': './source/static/**/*',
      'destination': '',
    },
    //
    {
      'source': 'node_modules/@fortawesome/fontawesome-free/webfonts/fa-brands-400.ttf',
      'destination': '/assets/webfonts',
    },
    //
    {
      'source': 'node_modules/@fortawesome/fontawesome-free/webfonts/fa-brands-400.woff2',
      'destination': '/assets/webfonts',
    },
    {
      'source': 'node_modules/@fortawesome/fontawesome-free/css/brands.min.css',
      'destination': '/assets/styles',
    },
    {
      'source': 'node_modules/@fortawesome/fontawesome-free/css/fontawesome.min.css',
      'destination': '/assets/styles',
    },
    //
    {
      'source': 'node_modules/@picocss/pico/css/pico.min.css',
      'destination': '/assets/styles',
    },
    //
    {
      'source': 'node_modules/bootstrap/dist/css/bootstrap-grid.min.css',
      'destination': '/assets/styles',
    },
  ],
};
