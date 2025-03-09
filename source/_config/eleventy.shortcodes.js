'use strict';
//
//
//

module.exports = {
  //
  // Image file's extension is
  //   - Case development: As is
  //   - Case production:  Forced to 'webp'
  //   To implement this rule, it is necessary to apply 'webp' to
  //   image files only in the production environment.
  //   The image file name setting for YAML-Markdown is "HOGE..thumb.png".
  //

  set_image_extension: function (fileName) {
    if ('product' === process.env.NODE_ENV) {
      var tmp = fileName.lastIndexOf('.');
      return fileName.slice(0, tmp) + '.webp';
    } else {
      return fileName;
    }
  },

  set_image_lightbox2_large: function(fileName) {
    // MEMO: I want to call `set_image_extension`,but I have no skill...

    var tmp1 = fileName.replace('thumb', 'large')

    if ('product' === process.env.NODE_ENV) {
      var tmp2 = tmp1.lastIndexOf('.');
      return tmp1.slice(0, tmp2) + '.webp';
    } else {
      return tmp1;
    }
  },
};
