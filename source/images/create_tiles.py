#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The size of each image is assumed to be Full HD, 1920x1080
"""

import os
import sys
import argparse
import subprocess
import textwrap
import glob
import pprint




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
    # Handling arguments
    #

  parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter,
    description = message_yellow('Arrange image files in tiles.'))

  parser.add_argument('input_files',
    nargs = '+',
    metavar = 'Input files',
    help = message_yellow('Input image files'))
  parser.add_argument('output_file',
    metavar = 'Output file',
    help = message_yellow('Output image file'))

  parser.add_argument('-tt', '--tyling_type',
    choices = [ 'landscape', 'portrait', '4tiles', '5tiles', '6tiles',],
    help = message_yellow('Tyling type'))
  parser.add_argument('-gs', '--gap_size',
    default = 10,
    type = int,
    help = message_yellow('Spacing between images'))
  parser.add_argument('-gc', '--gap_color',
    default = '#00000000',
    type = str,
    help = message_yellow('Spacing between images'))

  args = parser.parse_args()


  #
  # Check file's width and height
  #

  save_width = save_height = -1
  for in_file in args.input_files:
    ret = subprocess_check_output([
        'identify', '-format', '%w %h', in_file
      ])
    if -1 == save_width and -1 == save_height:
      save_width = ret.split(' ')[0]
      save_height = ret.split(' ')[1]
    else:
      if save_width != ret.split(' ')[0] or save_height != ret.split(' ')[1]:
        print(in_file + ' (' + str(ret.split(' ')[0]) + 'x' + ret.split(' ')[1] + ') ' + str(save_width) + 'x' + str(save_height))
        sys.exit()

  print(message_yellow('Image files\' size are no probrem'))


  #
  ##########################################################################################
  #
  if '6tiles' == args.tyling_type:

    #
    # 6 image files
    #
    #  +-----+--+
    #  |    6| 1|
    #  |     |  |
    #  |     +--+
    #  |     | 2|
    #  |     |  |
    #  +--+--+--+
    #  | 5| 4| 3|
    #  |  |  |  |
    #  +--+--+--+
    #

    #
    # No.1, 2, 3, 4, 5 are
    # 1/2, Strictly speaking, it's different.
    #

    resize_parts_width = (int(save_width) - int(args.gap_size)) / 2
    resize_parts_height = (int(save_height) - int(args.gap_size)) / 2
    resize_parts = '%sx%s!' % (int(resize_parts_width), int(resize_parts_height))

    for idx in [0, 1, 2, 3, 4]:
      ret = subprocess_run([ 'magick',
          args.input_files[idx],
          '-resize', resize_parts,
          'parts_' + str(idx + 1) + '.mpc',
        ])

    #
    # -append No. 1, 2 and 3 to 11
    #

    size_parts = '%sx%s' % (int(resize_parts_width), int(args.gap_size))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_1.mpc'
      ])
    ret = subprocess_run([ 'magick',
        'parts_1.mpc',
        'base_parts_1.mpc',
        'parts_2.mpc',
        'base_parts_1.mpc',
        'parts_3.mpc',
        '-append',
        'parts_11.mpc',
      ])

    #
    # +append No. 5 and 4 to 21
    #

    size_parts = '%sx%s' % (int(args.gap_size), int(resize_parts_height))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_2.mpc'
      ])
    ret = subprocess_run([ 'magick',
        'parts_5.mpc',
        'base_parts_2.mpc',
        'parts_4.mpc',
        '+append',
        'parts_21.mpc',
      ])

    #
    # -append No. 6 and 21 to 31
    #

    size_parts = '%sx%s' % (int(save_width), int(args.gap_size))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_3.mpc'
      ])
    ret = subprocess_run([ 'magick',
        args.input_files[5],
        'base_parts_3.mpc',
        'parts_21.mpc',
        '-append',
        'parts_31.mpc',
      ])

    #
    # +append No. 31 and 11 to 41
    #

    size_parts = '%sx%s' % (int(args.gap_size), (int(resize_parts_height) * 3) + (int(args.gap_size) * 2))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_4.mpc'
      ])

    ret = subprocess_run([ 'magick',
        'parts_31.mpc',
        'base_parts_4.mpc',
        'parts_11.mpc',
        '+append',
        args.output_file
      ])


  #
  ##########################################################################################
  #
  elif '5tiles' == args.tyling_type:

    #
    # 5 image files
    #
    #  +-----+---+
    #  |    5|  1|
    #  |     |   |
    #  |     |   |
    #  |     +---+
    #  +--+--+  2|
    #  | 4| 3|   |
    #  |  |  |   |
    #  +--+--+---+
    #
    #  Reduce image No.1 and NO.2 to 3/4
    #  Reduce image No.3 and NO.4 to 1/2
    #

    #
    # No.3 and No.4 are
    # 1/2, Strictly speaking, it's different.
    #

    resize_parts = '%sx%s' % ((int(save_width) - int(args.gap_size)) / 2, '')
    ret = subprocess_run([ 'magick',
        args.input_files[2],
        '-resize', resize_parts,
        'parts_3.mpc'
      ])
    ret = subprocess_run([ 'magick',
        args.input_files[3],
        '-resize', resize_parts,
        'parts_4.mpc'
      ])
    ret_parts_3_height = subprocess_check_output([
        'identify', '-format', '%h', 'parts_3.mpc'
      ])

    parts_31_height = int(save_height) + int(args.gap_size) + int(ret_parts_3_height)
    parts_11_height = ((int(save_height) / 4 * 3) * 2) + int(args.gap_size)
    parts_31_gap_height = int(args.gap_size) + (int(parts_11_height) - int(parts_31_height))


    #
    # +append 3 and 4 to 21
    #

    size_parts = '%sx%s' % (int(args.gap_size), ret_parts_3_height)
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_2.mpc'
      ])
    ret = subprocess_run([ 'magick',
        'parts_4.mpc',
        'base_parts_2.mpc',
        'parts_3.mpc',
        '+append',
        'parts_21.mpc',
      ])

    #
    # -append 5 and 21 to 31
    #

    size_parts = '%sx%s' % (int(save_width), int(parts_31_gap_height))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_3.mpc'
      ])
    ret = subprocess_run([ 'magick',
        args.input_files[4],
        'base_parts_3.mpc',
        'parts_21.mpc',
        '-append',
        'parts_31.mpc',
      ])

    #
    # No.1 and No.2 are
    # 3/4
    #

    resize_parts = '%sx%s' % (int(save_width) / 4 * 3, int(save_width) / 4 * 3)
    ret = subprocess_run([ 'magick',
        args.input_files[0],
        '-resize', resize_parts,
        'parts_1.mpc'
      ])
    ret = subprocess_run([ 'magick',
        args.input_files[1],
        '-resize', resize_parts,
        'parts_2.mpc'
      ])

    #
    # -append 1 and 2 to 11
    #

    size_parts = '%sx%s' % (int(save_width) / 4 * 3, int(args.gap_size))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_1.mpc'
      ])
    ret = subprocess_run([ 'magick',
        'parts_1.mpc',
        'base_parts_1.mpc',
        'parts_2.mpc',
        '-append',
       'parts_11.mpc',
      ])

    #
    # +append 31 and 11
    #

    size_parts = '%sx%s' % (int(args.gap_size), int(parts_11_height))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_4.mpc'
      ])

    ret = subprocess_run([ 'magick',
        'parts_31.mpc',
        'base_parts_4.mpc',
        'parts_11.mpc',
        '+append',
        args.output_file
      ])


  #
  ##########################################################################################
  #
  elif '4tiles' == args.tyling_type:

    #
    # 4 image files
    #
    #  +---+---+
    #  |  4|  1|
    #  +---+---+
    #  |  3|  2|
    #  +---+---+
    #

    size_parts = '%sx%s' % (int(save_width), int(args.gap_size))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_1.mpc'
      ])
    ret = subprocess_run([ 'magick',
        args.input_files[0],
        'base_parts_1.mpc',
        args.input_files[1],
        '-append',
        'parts_1.mpc',
      ])
    ret = subprocess_run([ 'magick',
        args.input_files[3],
        'base_parts_1.mpc',
        args.input_files[2],
        '-append',
        'parts_2.mpc',
      ])

    size_parts = '%sx%s' % (int(args.gap_size), int((int(save_height) * 2) + int(args.gap_size)))
    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts_2.mpc'
      ])

    ret = subprocess_run([ 'magick',
        'parts_2.mpc',
        'base_parts_2.mpc',
        'parts_1.mpc',
        '+append',
        args.output_file
      ])


  #
  ##########################################################################################
  #
  elif 'landscape' == args.tyling_type or 'portrait' == args.tyling_type:

    #
    # +/-append
    #
    #  +: Landscape
    #
    #    +---+---+...+---+
    #    |  1|  2|   |  n|
    #    +---+---+...+---+
    #
    #  -: Portrait
    #
    #    +---+
    #    |  1|
    #    +---+
    #    |  2|
    #    +---+
    #    .   .
    #    +---+
    #    |  n|
    #    +---+

    size_parts = ''
    if 'landscape' == args.tyling_type:
      size_parts = '%sx%s' % (int(args.gap_size), int(save_height))
    else:
      size_parts = '%sx%s' % (int(save_width), int(args.gap_size))

    ret = subprocess_run([
        'magick', '-size', size_parts, 'xc:' + args.gap_color, 'base_parts.mpc'
      ])
    exec_args = [
        'magick',
      ]
    for in_file in args.input_files:
      exec_args.append(in_file)
      exec_args.append('base_parts.mpc')
    exec_args.pop(-1)

    if 'landscape' == args.tyling_type:
      exec_args.append('+append')
    else:
      exec_args.append('-append')

    exec_args.append(args.output_file)
    ret = subprocess_run(exec_args)


  #
  ##########################################################################################
  #

  def _exec_delete(_files):
    for filename in glob.glob(_files):
      os.remove(filename)

  _exec_delete('*.mpc')
  _exec_delete('*.cache')




  sys.exit()
