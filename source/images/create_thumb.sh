#!/bin/bash

#
# This script is assumed to be executed from package.json.
#


margin_diagonal=400
margin_height=20


# ./raw/screenshot..Eleventy-netlify-V2..main..large.png
# ./raw/screenshot..Eleventy-netlify-V2..sub..large.png
python3 ./source/images/create_thumb.py ./source/images/raw/screenshot..Eleventy-netlify-V2..main..large.png \
    ./source/images/ \
    1200 1000 $margin_diagonal $margin_height
python3 ./source/images/create_thumb.py ./source/images/raw/screenshot..Eleventy-netlify-V2..sub..large.png \
    ./source/images/ \
    1200 1000 $margin_diagonal $margin_height


# screenshot..Eleventy-test-bed..large.png
python3 ./source/images/create_thumb.py ./source/images/raw/screenshot..Eleventy-test-bed..large.png \
    ./source/images/ \
    1000 900 $margin_diagonal $margin_height


# screenshot..project2501-v3..large.png
python3 ./source/images/create_thumb.py ./source/images/raw/screenshot..project2501-v3..large.png \
    ./source/images/ \
    1200 750 $margin_diagonal $margin_height
