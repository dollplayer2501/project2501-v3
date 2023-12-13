'use strict';

import gulp from 'gulp';

import webp from 'gulp-webp';

import { mode, outputPath, path } from './_config.mjs'


export const imageWebp_task = function() {
    return gulp.src(path.image, {since: gulp.lastRun(imageWebp_task)})
        .pipe(mode.product(webp()))
        .pipe(gulp.dest(outputPath + '/images'));
}
