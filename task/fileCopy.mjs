'use strict';

import gulp from 'gulp';

import { mode, outputPath, path } from './_config.mjs';


export const fileCopy_task = function(done) {
  (path.filePaths).forEach(function(path) {
    gulp.src(path.source, {
        encoding: false,
      })
      .pipe(gulp.dest(outputPath + path.destination));
  });
  done();
};
