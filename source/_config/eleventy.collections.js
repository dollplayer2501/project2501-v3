'use strict';
//
//
//

module.exports = {
    //
    // I don't understand the following.
    //  - Why `collectionApi` is needed.
    //  - How to add your own arguments.
    //    For example, pass the pathname as an argument.
    //
    contentsSectionWorks: function (collectionApi) {
        return collectionApi
            .getFilteredByGlob('./source/sections/works/**/*.md')
            .sort((a, b) => Number(a.data.order) > Number(b.data.order) ? 1 : -1);
    },
    //
    contentsSectionRecent: function (collectionApi) {
        return collectionApi
            .getFilteredByGlob('./source/sections/recent.md');
    },
};
