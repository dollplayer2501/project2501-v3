#!/bin/bash

#
# This script is assumed to be executed from package.json.
#


option_margin_diagonal=60
option_gap_height=40
option_background_color='#00000000'
option_resize='30%'


#
# screenshot..Eleventy-netlify-V2..main..large.png
# screenshot..Eleventy-netlify-V2..sub..large.png
#

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..Eleventy-netlify-V2..main..large.png \
  ./source/images/ \
  --top 700 \
  --bottom 1000 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 1000 \
  --middle_location 400 \
  --background_color $option_background_color \
  --resize $option_resize

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..Eleventy-netlify-V2..sub..large.png \
  ./source/images/ \
  --top 700 \
  --bottom 700 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 1300 \
  --middle_location 300 \
  --background_color $option_background_color \
  --resize $option_resize


#
# screenshot..Eleventy-test-bed..large.png
#

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..Eleventy-test-bed..large.png \
  ./source/images/ \
  --top 1200 \
  --bottom 700 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --background_color $option_background_color \
  --resize $option_resize


#
# screenshot..project2501-v3-dark..large.png
# screenshot..project2501-v3-light..large.png
#

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..project2501-v3-dark..large.png \
  ./source/images/ \
  --top 1200 \
  --bottom 800 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 800 \
  --middle_location 1800 \
  --background_color $option_background_color \
  --resize $option_resize

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..project2501-v3-light..large.png \
  ./source/images/ \
  --top 1200 \
  --bottom 800 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 800 \
  --middle_location 1800 \
  --background_color $option_background_color \
  --resize $option_resize
