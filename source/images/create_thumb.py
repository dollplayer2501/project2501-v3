#! /usr/bin/env python3
# -*- coding: utf-8 -*-

help_message ='''
  Before)                   After)
   hoge..large.png           hoge..thumb.png
  +-------------+  ---      +-------------+
  |+++          |   |       |+++          |
  |++           | top       |++       ----| --- ---
  |+            |  (height) |+     ----   |  |   | gap_height
  |             |   |       |   ----  ----|  |  ---
  |             |  ---      |----  ----   | margin_diagonal
  |             |   |       |   ----     *|  |
  |             |  CUT!     |----       **| ---
  |             |   |       |          ***|
  |             |   |       |         ****|
  |             |  ---      +-------------+
  |            *|   |
  |           **| bottom
  |          ***|  (height)
  |         ****|   |
  +-------------+  ---
'''

import os
import sys
import argparse
import subprocess
import textwrap
import glob




def subprocess_check_output(_exec_args:list):
    try:
        # raise ValueError()
        return subprocess.check_output(_exec_args, encoding='utf-8')
    except:
        subprocess_error_message('subprocess.check_output', _exec_args)
        sys.exit()


def subprocess_run(_exec_args:list):
    try:
        # raise ValueError()
        return subprocess.run(_exec_args, encoding='utf-8')
    except:
        subprocess_error_message('subprocess.run', _exec_args)
        sys.exit()


def subprocess_error_message(message:str, _exec_args:list):
    print('\033[31m' + 'Something wrong: ' + message + '\033[0m')
    print('\033[31m' + str(_exec_args) + '\033[0m')


def message_yellow(message:str) -> str:
    return '\033[33m' + message + '\033[0m'




if __name__ == "__main__":

    #
    # handling arguments
    #

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=message_yellow('Delete the middle of an extremely tall image.'),
        epilog=textwrap.dedent(message_yellow(help_message)))

    parser.add_argument('input_file',
        metavar='Input file',
        help=message_yellow('Input image file, the file name MUST be xxx..large.png'))
    parser.add_argument('output_path',
        metavar='Output path',
        help=message_yellow('Output path'))
    parser.add_argument('top',
        metavar='Top height',
        help=message_yellow('Height to crop the image from the top'))
    parser.add_argument('bottom',
        metavar='Bottom height',
        help=message_yellow('Height to crop the image from the bottom'))
    parser.add_argument('margin_diagonal',
        metavar='Diagonal margin',
        help=message_yellow('Diagonal margin'))
    parser.add_argument('gap_height',
        metavar='Gap height',
        help=message_yellow('Gap, between the top and bottom of the generated image'))

    args = parser.parse_args()

    output_file = os.path.join(args.output_path,
        os.path.basename(args.input_file).replace('large.png', 'thumb.png'))

    print('\033[32m' + args.input_file + ' - Start' + '\033[0m')


    #
    # get file's width and height
    #

    ret_width_height = subprocess_check_output([
            'identify', '-format', '%w %h', args.input_file
        ])

    ret_width = ret_width_height.split(' ')[0]
    ret_height = ret_width_height.split(' ')[1]


    #
    # mask
    #

    polygon_str = 'polygon' + \
        ' {top_left_x},{top_left_y}' + \
        ' {bottom_left_x},{bottom_left_y}' + \
        ' {bottom_right_x},{bottom_right_y}' + \
        ' {top_right_x},{top_right_y}'

    def _create_mask(_size, _polygon, _output_file):
        return subprocess_run([
                'convert', '-size', _size, 'xc:#00000000',
                '-fill', '#ff00ffff', '-draw', _polygon,
                _output_file
            ])

    # mask: top
    polygon_top = textwrap.dedent(polygon_str).format(
            top_left_x = 0,
            top_left_y = 0,
            bottom_left_x = 0,
            bottom_left_y = args.top,
            bottom_right_x = ret_width,
            bottom_right_y = int(args.top) - int(args.margin_diagonal),
            top_right_x = ret_width,
            top_right_y = 0,
        ).strip()
    size_top = ret_width + 'x' + args.top
    ret = _create_mask(size_top, polygon_top, 'mask_top.mpc')

    # mask: bottom
    polygon_bottom = textwrap.dedent(polygon_str).format(
            top_left_x = 0,
            top_left_y = args.margin_diagonal,
            bottom_left_x = 0,
            bottom_left_y = args.bottom,
            bottom_right_x = ret_width,
            bottom_right_y = args.bottom,
            top_right_x = ret_width,
            top_right_y = 0,
        ).strip()
    size_bottom = ret_width + 'x' + args.bottom
    ret = _create_mask(size_bottom, polygon_bottom, 'mask_bottom.mpc')


    #
    # crop
    #

    def _create_crop(_input_file, _crop, _output_file):
        return subprocess_run([
                'convert', _input_file, '-crop', _crop, _output_file
            ])

    # crop: top
    crop_top = size_top + '+0+0'
    ret = _create_crop(args.input_file, crop_top, 'crop_top.mpc')

    # crop: bottom
    crop_bottom = size_bottom + '+0+' + str(int(ret_height) - int( args.bottom))
    ret = _create_crop(args.input_file, crop_bottom, 'crop_bottom.mpc')


    #
    # combine
    #

    def _create_combine_parts(_input_file_1, _input_file_2, _output_file):
        return subprocess_run([
                'composite', '-compose', 'dst-in', _input_file_1, _input_file_2,
                '-alpha', 'on', _output_file
            ])

    # combine mask and crop: top
    ret = _create_combine_parts('mask_top.mpc', 'crop_top.mpc', 'parts_top.mpc')

    # combine mask and crop: bottom
    ret = _create_combine_parts('mask_bottom.mpc', 'crop_bottom.mpc', 'parts_bottom.mpc')


    #
    # paste: create base image
    #

    size_base = ret_width + 'x' + str(
            int(args.top) - int(args.margin_diagonal)
            + int( args.margin_diagonal) + int(args.gap_height)
            + int(args.bottom) - int(args.margin_diagonal)
        )
    ret = subprocess_run([
            'convert', '-size', size_base, 'xc:#00000000', 'base.mpc'
        ])


    #
    # paste: top and bottom
    #

    def _create_combine_between(_gravity, _input_file_1, _input_file_2, _output_file):
        return subprocess_run([
                'composite', '-gravity', _gravity, '-compose', 'over',
                _input_file_1, _input_file_2, _output_file
            ])

    # paste: top
    ret = _create_combine_between('north', 'parts_top.mpc', 'base.mpc', 'base_1.mpc')

    # paste: bottom  ==> DONE!
    ret = _create_combine_between('south', 'parts_bottom.mpc', 'base_1.mpc', output_file)


    #
    # delete temporary files
    #

    def _exec_delete(_files):
        for filename in glob.glob(_files):
            os.remove(filename)

    _exec_delete('*.mpc')
    _exec_delete('*.cache')




    print('\033[32m' + args.input_file + ' - End' + '\033[0m')
    sys.exit()
