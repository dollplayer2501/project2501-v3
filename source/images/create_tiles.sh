#!/bin/bash

#
# This script is assumed to be executed from package.json.
#

#  +-----+---+
#  |     |   |
#  |  5  | 1 |
#  |     |   |
#  |     +---+
#  +--+--+   |
#  |4 |3 | 2 |
#  |  |  |   |
#  +--+--+---+


python3 ./source/images/create_tiles.py \
    ./source/images/raw/EndeavourOS_Qtile_2023-12-12_14-49-23.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-12-18_15-47-06.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-11-19_04-08-40.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-12-21_22-02-03.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-12-12_13-59-40.png \
    ./source/images/screenshot..EndeavourOS_Qtile..thumb.png \
    --tyling_type 5tiles \
    --gap 20 \
    --resize 1920x


python3 ./source/images/create_tiles.py \
    ./source/images/raw/EndeavourOS_Qtile_2023-11-04_23-39-07.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-11-04_23-42-54.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-11-04_23-39-48.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-11-04_23-42-04.png \
    ./source/images/raw/EndeavourOS_Qtile_2023-11-04_23-39-02.png \
    ./source/images/screenshot..angle_minus_five_degrees..thumb.png \
    --tyling_type 5tiles \
    --gap 20 \
    --resize 1920x
