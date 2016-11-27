#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import argparse
import struct
import binascii
import sys
import shutil
import os
import time

# d2s struct info:
# http://www.coreyh.org/diablo-2-files/documentation/d2s_save_file_format_1.13d.html

CHECKSUM_POS = 12
CHECKSUM_SIZE = np.dtype('int32').itemsize # 4 bytes

# TODO: add arg to change class
CHARACTER_POS = 40
CHARACTERS = {
  'amazon': bytearray.fromhex('00'),
  'sorceress': bytearray.fromhex('01'),
  'necromancer': bytearray.fromhex('02'),
  'paladin': bytearray.fromhex('03'),
  'barbarian': bytearray.fromhex('04'),
  'druid': bytearray.fromhex('05'),
  'assassin': bytearray.fromhex('06'),
}
NORMAL_QUEST_POS = 345
NM_QUEST_POS = 441
HELL_QUEST_POS = 537
COW_KING_BIT_POS = 2 + 6*2 + 10 # number of bits (not bytes) past the QUEST_POS
RESET_STATS_POS = 427

def calculate_checksum(byte_array):
  byte_array = np.copy(byte_array)
  byte_array[CHECKSUM_POS: CHECKSUM_POS + CHECKSUM_SIZE] = np.zeros(CHECKSUM_SIZE, dtype=np.uint8)
  checksum = np.int32(0)
  for b in byte_array:
    checksum = np.int32((checksum << 1) + b + (checksum < 0))
  return np.int32(checksum)

def int_to_hex(i, fmt='<l'):
  byte_string = struct.pack(fmt, i)
  return ' '.join('{:02x}'.format(c) for c in byte_string)

def print_bits(byte_array, start, end):
  print(np.unpackbits(byte_array[start:end]))

def int2bytes(i):
  hex_string = '%x' % i
  n = len(hex_string)
  return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def reset_stats(byte_array):
  byte_array = np.copy(byte_array)
  byte_array[427] = np.uint8(2)
  return byte_array

def write_d2s(byte_array, out_fname='sohax.d2s'):
  byte_array = np.copy(byte_array)
  checksum = calculate_checksum(byte_array)
  byte_array[CHECKSUM_POS:CHECKSUM_POS + CHECKSUM_SIZE] = list(struct.pack('<i', checksum))
  byte_array.tofile(out_fname)
  print('wrote new file to {}'.format(out_fname))

def backup(save_file):
  new_fname = '{}.{}'.format(os.path.basename(save_file), time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()))
  new_path = os.path.join(os.path.dirname(save_file), new_fname)
  shutil.copyfile(save_file, new_path)
  print('copied {} to {}'.format(save_file, new_path))

def main(save_file, should_reset_stats=False):
  backup(save_file)
  data = np.fromfile(save_file, dtype=np.uint8)
  if should_reset_stats:
    data = reset_stats(data)
  write_d2s(data, save_file)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Hack your diablo 2 save file')
  parser.add_argument(
    '--file', dest='save_file', type=str,
    help='Path to your d2s save file. eg "/Applications/Diablo\ II/Save/sohax.d2s"'
  )
  parser.add_argument(
    '--reset-stats', dest='should_reset_stats', action='store_true', default=False,
    help='Bribe Akara to reset your stats again'
  )
  args = parser.parse_args()
  if not args.save_file:
    print('Must specify path to save file')
    sys.exit(0)

  main(args.save_file, args.should_reset_stats)
