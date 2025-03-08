'use strict';

import gulp from 'gulp';
import webp from 'gulp-webp';

import { mode, outputPath, path } from './_config.mjs'

// MEMO:
//  - develop: pass through, not convert webp
//  - product: convert to webp
//  Operate image file extensions with 11ty.
//
// MEMO:
// Gulp 5 - Copied images using .src and .dest are corrupt · Issue #2777 · gulpjs/gulp
// https://github.com/gulpjs/gulp/issues/2777#issuecomment-2036776560

export const imageWebp_task = function(done) {
  gulp.src(path.image, {
      encoding: false,
      since: gulp.lastRun(imageWebp_task)
    })
    .pipe(mode.product(webp()))
    .pipe(gulp.dest(outputPath + '/images'));
  done();
}
