#!/bin/bash

#
# This script is assumed to be executed from package.json.
#


margin_diagonal=500
margin_height=20


#
# screenshot..Eleventy-netlify-V2..main..large.png
# screenshot..Eleventy-netlify-V2..sub..large.png
#

python3 ./source/images/create_thumb.py \
    ./source/images/raw/screenshot..Eleventy-netlify-V2..main..large.png \
    ./source/images/ \
    700 1000 $margin_diagonal $margin_height \
    --middle_height 1000 --middle_location 400 \
    --background_color '#00000000'

python3 ./source/images/create_thumb.py \
    ./source/images/raw/screenshot..Eleventy-netlify-V2..sub..large.png \
    ./source/images/ \
    700 700 $margin_diagonal $margin_height \
    --middle_height 1300 --middle_location 300 \
    --background_color '#00000000'


#
# screenshot..Eleventy-test-bed..large.png
#

python3 ./source/images/create_thumb.py \
    ./source/images/raw/screenshot..Eleventy-test-bed..large.png \
    ./source/images/ \
    1200 1300 $margin_diagonal $margin_height \
    --background_color '#00000000'


#
# screenshot..project2501-v3-dark..large.png
# screenshot..project2501-v3-light..large.png
#

python3 ./source/images/create_thumb.py \
    ./source/images/raw/screenshot..project2501-v3-dark..large.png \
    ./source/images/ \
    1200 800 $margin_diagonal $margin_height \
    --middle_height 1200 --middle_location 2000 \
    --background_color '#00000000'

python3 ./source/images/create_thumb.py \
    ./source/images/raw/screenshot..project2501-v3-light..large.png \
    ./source/images/ \
    1200 800 $margin_diagonal $margin_height \
    --middle_height 1200 --middle_location 2000 \
    --background_color '#00000000'
