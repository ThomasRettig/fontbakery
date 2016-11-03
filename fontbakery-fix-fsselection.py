#!/usr/bin/env python
# Copyright 2016 The Fontbakery Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import argparse
import csv
import os
import sys

from fontTools import ttLib
import tabulate

parser = argparse.ArgumentParser(description='Print out fsSelection'
                                             ' bitmask of the fonts')
parser.add_argument('font', nargs="+")
parser.add_argument('--csv', default=False, action='store_true')
parser.add_argument('--autofix', default=False, action='store_true')


def getByte2(ttfont):
  return ttfont['OS/2'].fsSelection >> 8


def getByte1(ttfont):
  return ttfont['OS/2'].fsSelection & 255


def printInfo(fonts, print_csv=False):
  rows = []
  headers = ['filename', 'fsSelection']
  for font in fonts:
    ttfont = ttLib.TTFont(font)
    row = [os.path.basename(font)]
    row.append(('{:#010b} '
                '{:#010b}'
                '').format(getByte2(ttfont),
                           getByte1(ttfont)).replace('0b', ''))
    rows.append(row)

  def as_csv(rows):
    writer = csv.writer(sys.stdout)
    writer.writerows([headers])
    writer.writerows(rows)
    sys.exit(0)

  if print_csv:
    as_csv(rows)
  else:
    print(tabulate.tabulate(rows, headers, tablefmt="pipe"))


def main():
  args = parser.parse_args()
  if args.autofix:
    for font in args.font:
      ttfont = ttLib.TTFont(font)
      if '-Regular' in font:
        ttfont['OS/2'].fsSelection |= 0b1000000
      if '-Bold' in font:
        ttfont['OS/2'].fsSelection |= 0b100000
      if 'Italic' in font:
        ttfont['OS/2'].fsSelection |= 0b1
      ttfont.save(font + '.fix')
    printInfo([f + '.fix' for f in args.font], print_csv=args.csv)
    sys.exit(0)
  printInfo(args.font, print_csv=args.csv)


if __name__ == '__main__':
    main()
