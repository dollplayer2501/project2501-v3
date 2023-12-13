'use strict';

import gulpMode from 'gulp-mode';


export const mode = gulpMode({
    modes: ['product', 'develop'],
    default: 'develop',
    verbose: false
});

export const outputPath = mode.product() ? './_product' : './_develop';

export const path = {
    'scss': {
        'source': [
            './source/assets/styles/pico.classless.CUSTOM.scss',
            './source/assets/styles/fontawesome-free.scss',
            './source/assets/styles/site.scss',
        ],
        'watch': './source/assets/styles/**/*.{scss,sass}',
    },
    'javascript': [
        './source/assets/scripts/minimal-theme-switcher.js',
        './source/assets/scripts/modal.js',
    ],
    'image': [
        './source/images/**/*.{jpg,jpeg,png,webp}'
    ],
};
