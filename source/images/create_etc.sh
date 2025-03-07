#!/bin/bash


cp ./source/images/raw/screenshot..project2501-v2.png ./source/images/screenshot..project2501-v2..large.png
magick ./source/images/screenshot..project2501-v2..large.png -resize 768x \
  ./source/images/screenshot..project2501-v2..thumb.png

cp ./source/images/raw/screenshot..raleway_love.png ./source/images/screenshot..raleway_love..large.png
magick ./source/images/screenshot..raleway_love..large.png -resize 768x \
  ./source/images/screenshot..raleway_love..thumb.png
