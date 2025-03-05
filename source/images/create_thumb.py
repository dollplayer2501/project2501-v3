#! /usr/bin/env python3
# -*- coding: utf-8 -*-

help_message ='''
  Before)                         After)
   hoge..large.png                 hoge..thumb.png
  +--------------------+  ---     +--------------------+                  ---
  |01 +++              |   |      |01 +++              |                   |
  |02 ++               | top      |02 ++           ----| ---    ---       top height
  |03 +                |  height  |03 +        ----    |  |      | gap     |
  |04                  |   |      |04      ----    ----|  | --- --- height |  ---
  |05                  |   |      |05  ----    ----    | margin diagonal   |   |
  |06                  |  ---     |----    ----       *| --- |            ---  |
  |07                  |   |      |    ----          **|     |                 |
  |08                  |   |      |----             ***|    ---         bottom height
  |09                  |   |      |22              ****|                       |
  M 10                 M -----    +--------------------+                      ---
  |11                  |   |
  |12                  | middle
  |13                  |  height (if you need)
  |14                  |   |
  |15                  | -----    M: location of middle
  |16                  |   |
  |17                  |  ---
  |18                  |   |
  |19                 *|   |
  |20                **| bottom
  |21               ***|  height
  |22              ****|   |
  +--------------------+  ---
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
    return subprocess.check_output(_exec_args, encoding = 'utf-8')
  except:
    subprocess_error_message('subprocess.check_output', _exec_args)
    sys.exit()


def subprocess_run(_exec_args:list):
  try:
    # raise ValueError()
    return subprocess.run(_exec_args, encoding = 'utf-8')
  except:
    subprocess_error_message('subprocess.run', _exec_args)
    sys.exit()


def subprocess_pipe_run(_exec_args:list):
  try:
    return subprocess.run(_exec_args, stdout = subprocess.PIPE, encoding = 'utf-8')
  except:
    subprocess_error_message('subprocess.pipe.run', _exec_args)
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
    metavar = 'Input file',
    help = message_yellow('Input image file, the file name MUST be xxx..large.png'))
  parser.add_argument('output_path',
    metavar = 'Output path',
    help = message_yellow('Output path'))

  parser.add_argument('--top',
    required = True,
    metavar = 'Top height', default=0, type=int,
    help = message_yellow('Height to crop the image from the top'))
  parser.add_argument('--bottom',
    required = True,
    metavar = 'Bottom height', default=0, type=int,
    help = message_yellow('Height to crop the image from the bottom'))
  parser.add_argument('--margin_diagonal',
    required = True,
    metavar = 'Diagonal margin', default=0, type=int,
    help = message_yellow('Diagonal margin'))
  parser.add_argument('--gap_height',
    required = True,
    metavar = 'Gap height', default=0, type=int,
    help = message_yellow('Gap, between the top and bottom of the generated image'))

  parser.add_argument('-mh', '--middle_height',
    metavar = 'Middle height', default=0, type=int,
    help = message_yellow('Height to crop the image from the middle'))
  parser.add_argument('-ml', '--middle_location',
    metavar = 'Middle location height', default=0, type=int,
    help = message_yellow('Location at crop the image from the middle'))

  parser.add_argument('-bc', '--background_color',
    metavar = 'Background color', default='#00000000', type=str,
    help = message_yellow('Background color, default is #00000000'))

  parser.add_argument('-r', '--resize',
    metavar = 'Resize', default='', type=str,
    help = message_yellow('Arguments to give to -resize in the convert command'))

  args = parser.parse_args()

  output_normal_file = os.path.join(args.output_path,
    os.path.basename(args.input_file).replace('large.png', 'normal.png'))
  output_resize_file = os.path.join(args.output_path,
    os.path.basename(args.input_file).replace('large.png', 'resize.png'))

  print('\033[32m' + args.input_file + ' - Start' + '\033[0m')


  #
  # get file's width and height
  #

  ret_width_height = subprocess_check_output([
      'identify', '-format', '%w %h', args.input_file
    ])

  ret_width = int(ret_width_height.split(' ')[0])
  ret_height = int(ret_width_height.split(' ')[1])


  #
  # mask
  #

  polygon_template = 'polygon' + \
    ' {top_left_x},{top_left_y}' + \
    ' {bottom_left_x},{bottom_left_y}' + \
    ' {bottom_right_x},{bottom_right_y}' + \
    ' {top_right_x},{top_right_y}'

  def _create_mask(_size, _polygon, _output_file):
    return subprocess_run([
        'magick', '-size', _size, 'xc:#00000000',
        '-fill', '#ff00ffff', '-draw', _polygon,
        _output_file
      ])

  # mask: top
  polygon_str = textwrap.dedent(polygon_template).format(
      top_left_x = 0,
      top_left_y = 0,
      bottom_left_x = 0,
      bottom_left_y = args.top,
      bottom_right_x = ret_width,
      bottom_right_y = args.top - args.margin_diagonal,
      top_right_x = ret_width,
      top_right_y = 0,
    ).strip()
  size_str_top = '%sx%s' % (ret_width, args.top)
  ret = _create_mask(size_str_top, polygon_str, 'mask_top.mpc')

  # mask: bottom
  polygon_str = textwrap.dedent(polygon_template).format(
      top_left_x = 0,
      top_left_y = args.margin_diagonal,
      bottom_left_x = 0,
      bottom_left_y = args.bottom,
      bottom_right_x = ret_width,
      bottom_right_y = args.bottom,
      top_right_x = ret_width,
      top_right_y = 0,
    ).strip()
  size_str_bottom = '%sx%s' % (ret_width, args.bottom)
  ret = _create_mask(size_str_bottom, polygon_str, 'mask_bottom.mpc')

  # mask: middle
  if 0 < args.middle_height:
    polygon_str = textwrap.dedent(polygon_template).format(
        top_left_x = 0,
        top_left_y = args.margin_diagonal,
        bottom_left_x = 0,
        bottom_left_y = args.middle_height,
        bottom_right_x = ret_width,
        bottom_right_y = args.middle_height - args.margin_diagonal,
        top_right_x = ret_width,
        top_right_y = 0,
      ).strip()
    size_str_middle = '%sx%s' % (ret_width, args.middle_height)
    ret = _create_mask(size_str_middle, polygon_str, 'mask_middle.mpc')


  #
  # crop
  #

  def _create_crop(_input_file, _crop, _output_file):
    return subprocess_run([
        'magick', _input_file, '-crop', _crop, _output_file
      ])

  # crop: top
  crop_top = size_str_top + '+0+0'
  ret = _create_crop(args.input_file, crop_top, 'crop_top.mpc')

  # crop: bottom
  crop_bottom = size_str_bottom + '+0+' + str(ret_height - args.bottom)
  ret = _create_crop(args.input_file, crop_bottom, 'crop_bottom.mpc')

  # crop: middle
  if 0 < args.middle_height:
    crop_middle = size_str_middle + '+0+' + str(args.middle_location)
    ret = _create_crop(args.input_file, crop_middle, 'crop_middle.mpc')


  #
  # combine
  #

  def _create_combine_parts(_input_file_1, _input_file_2, _output_file):
    return subprocess_run([
        'magick', 'composite', '-compose', 'dst-in', _input_file_1, _input_file_2,
        '-alpha', 'on', _output_file
      ])

  # combine mask and crop: top
  ret = _create_combine_parts('mask_top.mpc', 'crop_top.mpc', 'parts_top.mpc')

  # combine mask and crop: bottom
  ret = _create_combine_parts('mask_bottom.mpc', 'crop_bottom.mpc', 'parts_bottom.mpc')

  # combine mask and crop: middle
  if 0 < args.middle_height:
    ret = _create_combine_parts('mask_middle.mpc', 'crop_middle.mpc', 'parts_middle.mpc')


  #
  # paste: create base image
  #

  size_str_base = ''
  if 0 < args.middle_height:
    size_str_base = '%sx%s' % (ret_width, str(
          args.top - args.margin_diagonal
        + args.gap_height + args.margin_diagonal
        + args.middle_height - args.margin_diagonal - args.margin_diagonal
        + args.gap_height + args.margin_diagonal
        + args.bottom - args.margin_diagonal
      ))
  else:
    size_str_base = '%sx%s' % (ret_width, str(
          args.top - args.margin_diagonal
        + args.margin_diagonal + args.gap_height
        + args.bottom - args.margin_diagonal
      ))

  ret = subprocess_run([
      'magick', '-size', size_str_base, 'xc:' + args.background_color, 'base.mpc'
    ])


  #
  # paste: top and bottom
  #

  def _create_combine_between(_gravity, _geometry, _input_file_1, _input_file_2, _output_file):
    return subprocess_run([
        'composite', '-gravity', _gravity,
        '-geometry', _geometry, '-compose', 'over',
        _input_file_1, _input_file_2, _output_file
      ])


  # paste: top
  ret = _create_combine_between('north', size_str_top + '+0+0',
    'parts_top.mpc', 'base.mpc', 'base_1.mpc')

  tmp_output_file = output_normal_file if 0 == len(args.resize) else 'finish.mpc'

  if 0 == args.middle_height:

    # paste: bottom  ==> DONE?
    ret = _create_combine_between('south', size_str_bottom + '+0+0',
        'parts_bottom.mpc', 'base_1.mpc', tmp_output_file)

  else:

    # paste: middle
    ret = _create_combine_between('north',
        size_str_middle + '+0+' + str(args.top - args.margin_diagonal + args.gap_height),
        'parts_middle.mpc', 'base_1.mpc', 'base_2.mpc')

    # paste: bottom  ==> DONE?
    ret = _create_combine_between('south', size_str_bottom + '+0+0',
        'parts_bottom.mpc', 'base_2.mpc', tmp_output_file)


  #
  # Resize
  #

  if 0 < len(args.resize):
    ret = subprocess_run([
        'magick', tmp_output_file, '-resize', args.resize, output_resize_file
      ])

  ret = subprocess_run([
      'magick', tmp_output_file, output_normal_file
    ])


  #
  # delete temporary files
  #

  def _exec_delete(_files):
    for filename in glob.glob(_files):
      os.remove(filename)

  _exec_delete('*.mpc')
  _exec_delete('*.cache')


  #
  #
  #

  ret_normal = subprocess_pipe_run([
      'magick', 'identify', '-format', '%wx%h', output_normal_file
    ])
  print('\033[32m' + args.input_file + ' - End    - Normal: ' + ret_normal.stdout + '\033[0m')

  if 0 < len(args.resize):
    ret_resize = subprocess_pipe_run([
        'magick', 'identify', '-format', '%wx%h', output_resize_file
      ])
    print('\033[32m' + args.input_file + ' - End    - Resize: ' + ret_resize.stdout + '\033[0m')


  sys.exit()
