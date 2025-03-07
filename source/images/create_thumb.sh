#!/bin/bash

#
# This script is assumed to be executed from package.json.
#


option_margin_diagonal=60
option_gap_height=40
option_background_color='#00000000'


#
# screenshot..Eleventy-netlify-V2..main.png
# screenshot..Eleventy-netlify-V2..sub.png
#

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..Eleventy-netlify-V2..main.png \
  ./source/images/screenshot..Eleventy-netlify-V2..main..large.png \
  --top 700 \
  --bottom 1000 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 1000 \
  --middle_location 400 \
  --background_color $option_background_color

magick ./source/images/screenshot..Eleventy-netlify-V2..main..large.png -resize 768x \
  ./source/images/screenshot..Eleventy-netlify-V2..main..thumb.png


python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..Eleventy-netlify-V2..sub.png \
  ./source/images/screenshot..Eleventy-netlify-V2..sub..large.png \
  --top 700 \
  --bottom 700 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 1300 \
  --middle_location 300 \
  --background_color $option_background_color

magick ./source/images/screenshot..Eleventy-netlify-V2..sub..large.png -resize 768x \
  ./source/images/screenshot..Eleventy-netlify-V2..sub..thumb.png


#
# screenshot..Eleventy-test-bed.png
#

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..Eleventy-test-bed.png \
  ./source/images/screenshot..Eleventy-test-bed..large.png \
  --top 1200 \
  --bottom 700 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --background_color $option_background_color

magick ./source/images/screenshot..Eleventy-test-bed..large.png -resize 768x \
  ./source/images/screenshot..Eleventy-test-bed..thumb.png

#
# screenshot..project2501-v3-dark.png
# screenshot..project2501-v3-light.png
#

python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..project2501-v3-dark.png \
  ./source/images/screenshot..project2501-v3-dark..large.png \
  --top 1200 \
  --bottom 800 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 800 \
  --middle_location 1800 \
  --background_color $option_background_color

magick ./source/images/screenshot..project2501-v3-dark..large.png -resize 768x \
  ./source/images/screenshot..project2501-v3-dark..thumb.png


python3 ./source/images/create_thumb.py \
  ./source/images/raw/screenshot..project2501-v3-light.png \
  ./source/images/screenshot..project2501-v3-light..large.png \
  --top 1200 \
  --bottom 800 \
  --margin_diagonal $option_margin_diagonal \
  --gap_height $option_gap_height \
  --middle_height 800 \
  --middle_location 1800 \
  --background_color $option_background_color

magick ./source/images/screenshot..project2501-v3-light..large.png -resize 768x \
  ./source/images/screenshot..project2501-v3-light..thumb.png
