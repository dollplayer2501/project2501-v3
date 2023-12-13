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
    //
    set_image_extension: function (fileName) {
        if (process.env.NODE_ENV === 'product') {
            var tmp = fileName.lastIndexOf('.');
            return fileName.slice(0, tmp) + '.webp';
        } else {
            return fileName;
        }
    },

    //
    //
    //
    set_picocss_tooltips: function (text, url, tooltiip, placement) {
        return `
            <a herf="${url}" data-tooltip="${tooltiip}" data-placement="${placement}">${text}</a>
        `;
    },
};
