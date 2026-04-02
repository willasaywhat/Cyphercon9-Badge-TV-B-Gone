# Copyright (C) 2026 tymkrs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of tymkrs shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from tymkrs.

import machine
import rp2
import utime
import random
import gc

##
#	CHARACTER MAPS
##

menu_map = bytearray([
0b00000000, 0b00000000, 0b00001110, 0b00010001, 0b00001110, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00010010, 0b00011111, 0b00010000, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00011001, 0b00010101, 0b00010010, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00010001, 0b00010101, 0b00001010, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00000111, 0b00000100, 0b00011111, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00010111, 0b00010101, 0b00001001, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00001110, 0b00010101, 0b00001100, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00000001, 0b00011001, 0b00000111, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00001010, 0b00010101, 0b00001010, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00000110, 0b00010101, 0b00001110, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
0b00000000, 0b00000000, 0b00110000, 0b00001100, 0b00000011, 0b00000000, 0b00000000,
0b00001100, 0b00011110, 0b00000000, 0b00010010, 0b00001100, 0b00100001, 0b00011110,
0b00000000, 0b00110110, 0b00111001, 0b00111001, 0b00111001, 0b00110110, 0b00000000,
0b00000011, 0b00111011, 0b00111101, 0b00110101, 0b00111101, 0b00111011, 0b00000011,
0b00111111, 0b00100101, 0b00101001, 0b00110001, 0b00101001, 0b00100101, 0b00111111
])

tymkrscii_map = bytearray([
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x66, 0x6, 0xcc, 0xc, 0x99, 0x19, 0x33, 0x13, 0x66, 0x6, 0xcc, 0xc, 0x99, 0x19, 0x33, 0x13,
0x33, 0x13, 0x99, 0x19, 0xcc, 0xc, 0x66, 0x6, 0x33, 0x13, 0x99, 0x19, 0xcc, 0xc, 0x66, 0x6,
0x40, 0x0, 0xe0, 0x0, 0xf0, 0x1, 0xf8, 0x3, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0,
0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xf8, 0x3, 0xf0, 0x1, 0xe0, 0x0, 0x40, 0x0,
0x8, 0x0, 0xc, 0x0, 0xe, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xe, 0x0, 0xc, 0x0, 0x8, 0x0,
0x0, 0x2, 0x0, 0x6, 0x0, 0xe, 0xff, 0x1f, 0xff, 0x1f, 0x0, 0xe, 0x0, 0x6, 0x0, 0x2,
0xff, 0x1f, 0x1, 0x10, 0x1, 0x10, 0x1, 0x10, 0x1, 0x10, 0x1, 0x10, 0x1, 0x10, 0xff, 0x1f,
0x0, 0x0, 0xfe, 0xf, 0x2, 0x8, 0x2, 0x8, 0x2, 0x8, 0x2, 0x8, 0xfe, 0xf, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xfc, 0x7, 0x4, 0x4, 0x4, 0x4, 0xfc, 0x7, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8, 0x3, 0xf8, 0x3, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0xf, 0x2, 0x8, 0xfa, 0xb, 0xfa, 0xb, 0x2, 0x8, 0xfe, 0xf, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0xff, 0x1f, 0x1, 0x10, 0xfd, 0x17, 0x5, 0x14, 0x5, 0x14, 0xfd, 0x17, 0x1, 0x10, 0xff, 0x1f,
0x1c, 0x0, 0x3e, 0x0, 0x7e, 0x0, 0xfc, 0x0, 0x7e, 0x0, 0x3e, 0x0, 0x1c, 0x0, 0x0, 0x0,
0x10, 0x0, 0x38, 0x0, 0xbc, 0x0, 0xfe, 0x0, 0xbc, 0x0, 0x38, 0x0, 0x10, 0x0, 0x0, 0x0,
0x38, 0x0, 0x38, 0x0, 0xbe, 0x0, 0xce, 0x0, 0xbe, 0x0, 0x38, 0x0, 0x38, 0x0, 0x0, 0x0,
0x10, 0x0, 0x38, 0x0, 0x7c, 0x0, 0xfe, 0x0, 0x7c, 0x0, 0x38, 0x0, 0x10, 0x0, 0x0, 0x0,
0x8, 0x0, 0x4, 0x0, 0xfc, 0x0, 0x4, 0x0, 0xfc, 0x0, 0x4, 0x0, 0x2, 0x0, 0x0, 0x0,
0xc0, 0x0, 0xb0, 0x0, 0x8c, 0x0, 0x82, 0x0, 0x8c, 0x0, 0xb0, 0x0, 0xc0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xc, 0x0, 0x12, 0x0, 0x12, 0x0, 0xc, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x92, 0x0, 0x7c, 0x0, 0x44, 0x0, 0xd6, 0x0, 0x44, 0x0, 0x7c, 0x0, 0x92, 0x0, 0x0, 0x0,
0x78, 0x0, 0x94, 0x0, 0x22, 0x1, 0xc9, 0x3, 0x22, 0x1, 0x94, 0x0, 0x78, 0x0, 0x0, 0x0,
0xcc, 0x0, 0xec, 0x0, 0xf4, 0x0, 0xf4, 0x0, 0xf4, 0x0, 0xec, 0x0, 0xcc, 0x0, 0x0, 0x0,
0xff, 0x1f, 0xaa, 0xa, 0x0, 0x0, 0x10, 0x10, 0xb1, 0x0, 0xa1, 0x0, 0x0, 0x0, 0xff, 0x1f,
0x80, 0x7, 0xc0, 0x3, 0xe6, 0x1f, 0xe2, 0x3, 0xe3, 0x1f, 0xc3, 0x3, 0xc4, 0x1, 0xf8, 0x0,
0x5c, 0x0, 0xe6, 0x0, 0x76, 0x0, 0xde, 0x0, 0x76, 0x0, 0xe6, 0x0, 0x5c, 0x0, 0x0, 0x0,
0x7c, 0x0, 0xf6, 0x0, 0xfe, 0x0, 0xde, 0x0, 0xfe, 0x0, 0xf6, 0x0, 0x7c, 0x0, 0x0, 0x0,
0x7c, 0x0, 0xd6, 0x0, 0xd6, 0x0, 0xde, 0x0, 0xd6, 0x0, 0xd6, 0x0, 0x7c, 0x0, 0x0, 0x0,
0x7c, 0x0, 0xfe, 0x0, 0xd6, 0x0, 0xde, 0x0, 0xd6, 0x0, 0xfe, 0x0, 0x7c, 0x0, 0x0, 0x0,
0x7c, 0x0, 0xde, 0x0, 0x96, 0x0, 0x9e, 0x0, 0x96, 0x0, 0xde, 0x0, 0x7c, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xbe, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x7, 0x0, 0x0, 0x0, 0x7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x28, 0x0, 0x28, 0x0, 0xfe, 0x0, 0x28, 0x0, 0xfe, 0x0, 0x28, 0x0, 0x28, 0x0, 0x0, 0x0,
0x0, 0x0, 0x48, 0x0, 0x54, 0x0, 0xfe, 0x0, 0x54, 0x0, 0x24, 0x0, 0x0, 0x0, 0x0, 0x0,
0x4, 0x0, 0x4a, 0x0, 0x24, 0x0, 0x10, 0x0, 0x48, 0x0, 0xa4, 0x0, 0x40, 0x0, 0x0, 0x0,
0x0, 0x0, 0x6c, 0x0, 0x92, 0x0, 0xa2, 0x0, 0x44, 0x0, 0xa0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xfe, 0x0, 0x1, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0xfe, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x12, 0x0, 0xc, 0x0, 0x3f, 0x0, 0xc, 0x0, 0x12, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x10, 0x0, 0x10, 0x0, 0x7c, 0x0, 0x10, 0x0, 0x10, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x2, 0x80, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x1, 0xc0, 0x0, 0x30, 0x0, 0xc, 0x0, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0xa2, 0x0, 0x92, 0x0, 0x8a, 0x0, 0x7c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x84, 0x0, 0xfe, 0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x84, 0x0, 0xc2, 0x0, 0xa2, 0x0, 0x92, 0x0, 0x8c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x44, 0x0, 0x82, 0x0, 0x92, 0x0, 0x92, 0x0, 0x6c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x30, 0x0, 0x28, 0x0, 0x24, 0x0, 0xfe, 0x0, 0x20, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x40, 0x0, 0x9e, 0x0, 0x92, 0x0, 0x92, 0x0, 0x60, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0x92, 0x0, 0x92, 0x0, 0x92, 0x0, 0x64, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x2, 0x0, 0x2, 0x0, 0xc2, 0x0, 0x32, 0x0, 0xe, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x6c, 0x0, 0x92, 0x0, 0x92, 0x0, 0x92, 0x0, 0x6c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x4c, 0x0, 0x92, 0x0, 0x92, 0x0, 0x92, 0x0, 0x7c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x6c, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x80, 0x0, 0x6c, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x10, 0x0, 0x28, 0x0, 0x44, 0x0, 0x82, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x28, 0x0, 0x28, 0x0, 0x28, 0x0, 0x28, 0x0, 0x28, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x82, 0x0, 0x44, 0x0, 0x28, 0x0, 0x10, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xc, 0x0, 0x2, 0x0, 0xa2, 0x0, 0x12, 0x0, 0xc, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0x82, 0x0, 0xba, 0x0, 0xaa, 0x0, 0x3c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xf8, 0x0, 0x14, 0x0, 0x12, 0x0, 0x14, 0x0, 0xf8, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x92, 0x0, 0x92, 0x0, 0x92, 0x0, 0x6c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0x82, 0x0, 0x82, 0x0, 0x82, 0x0, 0x44, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x82, 0x0, 0x82, 0x0, 0x82, 0x0, 0x7c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x92, 0x0, 0x92, 0x0, 0x92, 0x0, 0x82, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x12, 0x0, 0x12, 0x0, 0x2, 0x0, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0x82, 0x0, 0x92, 0x0, 0x92, 0x0, 0x72, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0xfe, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x82, 0x0, 0xfe, 0x0, 0x82, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x40, 0x0, 0x82, 0x0, 0x82, 0x0, 0x82, 0x0, 0x7e, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x10, 0x0, 0x28, 0x0, 0x44, 0x0, 0x82, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0,
0xfe, 0x0, 0x4, 0x0, 0x8, 0x0, 0x10, 0x0, 0x8, 0x0, 0x4, 0x0, 0xfe, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x4, 0x0, 0x8, 0x0, 0x10, 0x0, 0xfe, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0x82, 0x0, 0x82, 0x0, 0x82, 0x0, 0x7c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x12, 0x0, 0x12, 0x0, 0x12, 0x0, 0xc, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7c, 0x0, 0x82, 0x0, 0x82, 0x0, 0x42, 0x0, 0xbc, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x12, 0x0, 0x32, 0x0, 0x52, 0x0, 0x8c, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x4c, 0x0, 0x92, 0x0, 0x92, 0x0, 0x92, 0x0, 0x64, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x2, 0x0, 0x2, 0x0, 0xfe, 0x0, 0x2, 0x0, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x7e, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x7e, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x3e, 0x0, 0x40, 0x0, 0x80, 0x0, 0x40, 0x0, 0x3e, 0x0, 0x0, 0x0, 0x0, 0x0,
0xfe, 0x0, 0x40, 0x0, 0x20, 0x0, 0x10, 0x0, 0x20, 0x0, 0x40, 0x0, 0xfe, 0x0, 0x0, 0x0,
0x0, 0x0, 0xc6, 0x0, 0x28, 0x0, 0x10, 0x0, 0x28, 0x0, 0xc6, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x6, 0x0, 0x8, 0x0, 0xf0, 0x0, 0x8, 0x0, 0x6, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xc2, 0x0, 0xa2, 0x0, 0x92, 0x0, 0x8a, 0x0, 0x86, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1, 0x1, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x2, 0x0, 0xc, 0x0, 0x30, 0x0, 0xc0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0xff, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x4, 0x0, 0x2, 0x0, 0x1, 0x0, 0x2, 0x0, 0x4, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x2, 0x0, 0x4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x0, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0xf8, 0x0, 0x80, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0x70, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x0, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0x50, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x0, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0xfe, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x0, 0xa8, 0x0, 0xa8, 0x0, 0xa8, 0x0, 0xb0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x8, 0x0, 0xfc, 0x0, 0xa, 0x0, 0x2, 0x0, 0x4, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x4, 0x88, 0x8, 0x88, 0x8, 0x88, 0x8, 0xf0, 0x7, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0xf0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf4, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x4, 0x0, 0x8, 0x0, 0x8, 0xf4, 0x7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xfe, 0x0, 0x20, 0x0, 0x20, 0x0, 0x50, 0x0, 0x88, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x7e, 0x0, 0x80, 0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0xf0, 0x0, 0x8, 0x0, 0x8, 0x0, 0x30, 0x0, 0x8, 0x0, 0x8, 0x0, 0xf0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xf0, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0xf0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x0, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0x70, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xf0, 0xf, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0x70, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x70, 0x0, 0x88, 0x0, 0x88, 0x0, 0x88, 0x0, 0xf0, 0xf, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xf0, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x10, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x90, 0x0, 0xa8, 0x0, 0xa8, 0x0, 0xa8, 0x0, 0x48, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x8, 0x0, 0x7e, 0x0, 0x88, 0x0, 0x88, 0x0, 0x48, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x78, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x78, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x38, 0x0, 0x40, 0x0, 0x80, 0x0, 0x40, 0x0, 0x38, 0x0, 0x0, 0x0, 0x0, 0x0,
0x78, 0x0, 0x80, 0x0, 0x80, 0x0, 0x70, 0x0, 0x80, 0x0, 0x80, 0x0, 0x78, 0x0, 0x0, 0x0,
0x0, 0x0, 0x88, 0x0, 0x50, 0x0, 0x20, 0x0, 0x50, 0x0, 0x88, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x78, 0x4, 0x80, 0x8, 0x80, 0x8, 0x80, 0x8, 0xf8, 0x7, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x88, 0x0, 0xc8, 0x0, 0xa8, 0x0, 0x98, 0x0, 0x88, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x10, 0x0, 0xee, 0x0, 0x1, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xfe, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0xee, 0x0, 0x10, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x4, 0x0, 0x2, 0x0, 0x2, 0x0, 0x4, 0x0, 0x4, 0x0, 0x2, 0x0, 0x0, 0x0,
0x7c, 0x3, 0xc2, 0x4, 0xd1, 0x1, 0xc5, 0x0, 0xd1, 0x1, 0xc2, 0x4, 0x7c, 0x3, 0x0, 0x0,
0x40, 0x0, 0x0, 0x0, 0x40, 0x0, 0x0, 0x0, 0x40, 0x0, 0x0, 0x0, 0x40, 0x0, 0x0, 0x0,
0xe0, 0x0, 0x0, 0x0, 0xe0, 0x0, 0x0, 0x0, 0xe0, 0x0, 0x0, 0x0, 0xe0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb6, 0xd, 0xb6, 0xd, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xb6, 0xd, 0xb6, 0xd, 0xb6, 0xd, 0xb6, 0xd, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xbf, 0x1f, 0xbf, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xbf, 0x1f, 0xbf, 0x1f, 0xbf, 0x1f, 0xbf, 0x1f, 0x0, 0x0, 0x0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xe0, 0x1f, 0xe0, 0x1f, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0,
0x0, 0x0, 0x0, 0x0, 0xe0, 0x1f, 0x20, 0x0, 0x20, 0x0, 0xa0, 0x1f, 0xa0, 0x0, 0xa0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xe0, 0x1f, 0xe0, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0x0, 0x0, 0x0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x1f, 0x20, 0x0, 0x20, 0x0, 0xe0, 0x1f, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x0, 0xff, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0,
0x0, 0x0, 0x0, 0x0, 0xff, 0x0, 0x80, 0x0, 0x80, 0x0, 0xbf, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xff, 0x0, 0xff, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x0, 0x0, 0x0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xbf, 0x0, 0x80, 0x0, 0x80, 0x0, 0xff, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x40, 0x0, 0x40, 0x0,
0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xbf, 0x1f, 0xa0, 0x0, 0xa0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x40, 0x0, 0x40, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xbf, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x1f, 0xa0, 0x1f, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0, 0xc0, 0x1f, 0x40, 0x0, 0x40, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x1f, 0x20, 0x0, 0x20, 0x0, 0xa0, 0x1f, 0xa0, 0x0, 0xa0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xbf, 0x0, 0xbf, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0, 0x7f, 0x0, 0x40, 0x0, 0x40, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xbf, 0x0, 0x80, 0x0, 0x80, 0x0, 0xbf, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xa0, 0x0, 0xa0, 0x0, 0xa0, 0x0,
0x40, 0x0, 0x40, 0x0, 0xff, 0x1f, 0x40, 0x0, 0x40, 0x0, 0xff, 0x1f, 0x40, 0x0, 0x40, 0x0,
0xa0, 0x0, 0xa0, 0x0, 0xbf, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xbf, 0x1f, 0xa0, 0x0, 0xa0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1f, 0x80, 0x1f, 0xc0, 0x0, 0x40, 0x0, 0x40, 0x0,
0x40, 0x0, 0x40, 0x0, 0xc0, 0x0, 0x80, 0x1f, 0x0, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x40, 0x0, 0x40, 0x0, 0x60, 0x0, 0x3f, 0x0, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1f, 0x0, 0x3f, 0x0, 0x60, 0x0, 0x40, 0x0, 0x40, 0x0,
0x0, 0x1c, 0x0, 0xf, 0xc0, 0x3, 0xe0, 0x1, 0xf0, 0x0, 0x78, 0x0, 0x1e, 0x0, 0x7, 0x0,
0x7, 0x0, 0x1e, 0x0, 0x78, 0x0, 0xf0, 0x0, 0xe0, 0x1, 0xc0, 0x3, 0x0, 0xf, 0x0, 0x1c,
0x7, 0x1c, 0x1e, 0xf, 0xf8, 0x3, 0xf0, 0x1, 0xf0, 0x1, 0xf8, 0x3, 0x1e, 0xf, 0x7, 0x1c,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0x0, 0x0, 0x0, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xc0, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xc0, 0x1f, 0x0, 0x0, 0x0, 0x0,
0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0xe0, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x0, 0x0, 0x0, 0x0, 0x7f, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x7f, 0x0, 0x0, 0x0, 0x0, 0x0,
0x3f, 0x0, 0x3f, 0x0, 0x3f, 0x0, 0x3f, 0x0, 0x3f, 0x0, 0x3f, 0x0, 0x3f, 0x0, 0x3f, 0x0,
0x0, 0x18, 0x0, 0x18, 0x0, 0x18, 0x0, 0x18, 0x0, 0x18, 0x0, 0x18, 0x0, 0x18, 0x0, 0x18,
0x0, 0x1e, 0x0, 0x1e, 0x0, 0x1e, 0x0, 0x1e, 0x0, 0x1e, 0x0, 0x1e, 0x0, 0x1e, 0x0, 0x1e,
0x80, 0x1f, 0x80, 0x1f, 0x80, 0x1f, 0x80, 0x1f, 0x80, 0x1f, 0x80, 0x1f, 0x80, 0x1f, 0x80, 0x1f,
0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f,
0xf0, 0x1f, 0xf0, 0x1f, 0xf0, 0x1f, 0xf0, 0x1f, 0xf0, 0x1f, 0xf0, 0x1f, 0xf0, 0x1f, 0xf0, 0x1f,
0xfc, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f,
0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0xdd, 0x1d, 0xaa, 0xa, 0x77, 0x17, 0xaa, 0xa, 0xdd, 0x1d, 0xaa, 0xa, 0x77, 0x17, 0xaa, 0xa,
0x55, 0x15, 0xaa, 0xa, 0x55, 0x15, 0xaa, 0xa, 0x55, 0x15, 0xaa, 0xa, 0x55, 0x15, 0xaa, 0xa,
0x88, 0x8, 0x88, 0x8, 0x22, 0x2, 0x22, 0x2, 0x88, 0x8, 0x88, 0x8, 0x22, 0x2, 0x22, 0x2,
0x3, 0x0, 0x3, 0x0, 0x3, 0x0, 0x3, 0x0, 0x3, 0x0, 0x3, 0x0, 0x3, 0x0, 0x3, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f,
0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f,
0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0,
0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f,
0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0,
0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f,
0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0xc0, 0x1f, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0, 0x7f, 0x0,
0x0, 0x1c, 0x0, 0x1c, 0x0, 0x1f, 0xe0, 0x1f, 0xe0, 0x1f, 0xf8, 0x1f, 0xff, 0x1f, 0xff, 0x1f,
0xff, 0x1f, 0xff, 0x1f, 0xf8, 0x1f, 0xe0, 0x1f, 0xe0, 0x1f, 0x0, 0x1f, 0x0, 0x1c, 0x0, 0x1c,
0xff, 0x1f, 0xff, 0x1f, 0xff, 0x3, 0xff, 0x0, 0xff, 0x0, 0x1f, 0x0, 0x7, 0x0, 0x7, 0x0,
0x7, 0x0, 0x7, 0x0, 0x1f, 0x0, 0xff, 0x0, 0xff, 0x0, 0xff, 0x3, 0xff, 0x1f, 0xff, 0x1f,
0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0,
0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0,
0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0,
0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0,
0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0,
0x20, 0x0, 0x20, 0x0, 0x20, 0x0, 0x20, 0x0, 0x20, 0x0, 0x20, 0x0, 0x20, 0x0, 0x20, 0x0,
0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0, 0x40, 0x0,
0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0, 0x80, 0x0,
0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1, 0x0, 0x1,
0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2, 0x0, 0x2,
0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4, 0x0, 0x4,
0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8, 0x0, 0x8,
0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10, 0x0, 0x10,
0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0,
0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f,
0xff, 0x1f, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0,
0xff, 0x1f, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0,
0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0xff, 0x1f, 0x0, 0x0, 0xff, 0x1f,
0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f, 0x0, 0x0, 0x0, 0x0, 0xff, 0x1f, 0xff, 0x1f,
0x8, 0x2, 0x14, 0x5, 0xa2, 0x8, 0x0, 0x0, 0x0, 0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0,
0x8, 0x1, 0x94, 0x2, 0x0, 0x0, 0x67, 0xe, 0x90, 0x0, 0x97, 0xe, 0x60, 0x0, 0x0, 0x0
])

##
#   DISPLAY DRIVER
##
SX1262_CS   = machine.Pin(28, machine.Pin.OUT, value=1) # active low
LCDcs       = machine.Pin(7, machine.Pin.OUT, value=1) # active low
LCDreset    = machine.Pin(8, machine.Pin.OUT, value=0) # active low
LCDdataCMD  = machine.Pin(9, machine.Pin.OUT, value=0)
LCDsck      = machine.Pin(10, machine.Pin.ALT, value=0) # SPI1
LCDmosi     = machine.Pin(11, machine.Pin.ALT, value=0) # SPI1
LCDmiso     = machine.Pin(12, machine.Pin.OUT, value=0)
SPI1 = machine.SPI(
    1,   #engine
    baudrate=5000000, # screen max 5MHz
    polarity=1,  # CPOL clock idle state (0 = low)
    phase=1,   # CPHA 0 = read on rise and shift out on falling edge, 1 = read on falling and shift out on rising edge
    bits=8,
    firstbit=machine.SPI.MSB,
    sck=LCDsck,
    mosi=LCDmosi,
    miso=LCDmiso)

screen_buffer = bytearray(528)

def flip():
    for y in range(0, 4):
        setRowColLCD(y, 0)  # Valid row values 0-3, column values 0-131
        for x in range(0, 132):
            i = (y * 132) + x
            data = screen_buffer[i]
            spiByte(data, 1) # Write data to current ram location (writes one column of 8 bits. bit 0 on top, bit 7 on bottom)

def spiByte(data, DC):

    # format the data...
    xfer = bytearray()
    xfer.append(data & 0xFF)

    # set the data / #command pin
    LCDdataCMD.value(DC)

    # set CS low to indicate new xfer
    LCDcs.off()

    # send byte
    SPI1.write(xfer)

    # set CS high to indicate xfer done
    LCDcs.on()

    return

def spi2Byte(data, data1, DC):

    # format the data...
    xfer = bytearray()
    xfer.append(data & 0xFF)
    xfer.append(data1 & 0xFF)

    # set the data / #command pin
    LCDdataCMD.value(DC)

    # set CS low to indicate new xfer
    LCDcs.off()

    # send byte
    SPI1.write(xfer)

    # set CS high to indicate xfer done
    LCDcs.on()

    return

def initLCD():
    utime.sleep(0.1)  # Let display fully power update
    LCDreset.value(0)   # set pin high to release reset to display
    utime.sleep(0.1)  # hold reset low 100ms
    LCDreset.value(1)   # set pin high to release reset to display
    utime.sleep(0.1)  # Let display reset and come ready for 100ms

    # issue soft reset to screen
    spiByte(0xE2, 0)
    utime.sleep(0.1)  # Let display reset and come ready for 100ms

    # init screen per sample code
    spi2Byte(0xF8, 0x01, 0) # set booster level to 5x
    spiByte(0x23, 0) # set regulation ratio to 4.5
    spiByte(0x2C, 0) # Turn on voltage booster
    spiByte(0x2E, 0) # Turn on voltage booster and regulator
    spiByte(0x2F, 0) # Turn on voltage booster, regulator, and voltage follower
    spiByte(0xA2, 0) # Set LCD bias to 1/9
    spiByte(0xA1, 0) # Set SEG scan (MX) direction to normal (bit 0)
    spiByte(0xC8, 8) # Set COM scan (MY) direction to reverse (bit 3)
    spi2Byte(0x81, 0x12, 0) # set EV (contrast)
    spiByte(0x40, 0) # Set display start line (Ram to LCD)
    spiByte(0xA6, 0) # Set display mode normal / inverse (bit 0 = INV)
    spiByte(0xAF, 0) # Set display on (bit 0 = D, 1 = on)
    spiByte(0x00, 0) # Set column address (LSB) aka dram write pointer
    spiByte(0x10, 0) # Set column address (MSB)
    spiByte(0xB0, 0) # Set pate address of Ram
    spiByte(0xAF, 0) # Set display on (bit 0 = D, 1 = on)

    clearLCD()

    return

def clearLCD():

    # set dram pointer back to upper left
    setRowColLCD(0,0)

    # clear ram
    for j in range(4):
        spi2Byte(0x10, 0x00, 0) # set dram column address to 0 (valid range 0 to 131)
        spiByte(0xB0 + j, 0) # Set page (row) address in dram (valid range 0 to 3)
        for i in range(0x83 + 1):
            spiByte(0x00, 1) # Write data to current ram location (writes one column of 8 bits. bit 0 on top, bit 7 on bottom)

    # set dram pointer back to upper left
    setRowColLCD(0,0)

    return

def setRowColLCD(row, col):
    # set dram pointer back to lower left
    spi2Byte((((col >> 4) & 0x0F) | 0x10) , (col & 0x0F), 0) # set dram column address. byte one 0,0,0,1,C7,C6,C5,C4 byte two 0,0,0,0,C3,C2,C1,C0
    spiByte(((row & 0x0F) | 0xB0), 0) # Set page (row) address in dram. 1,0,1,1,R3,R2,R1,R0

    return

def invertLCD(onOff):

    if(onOff == 0):
        spiByte(0xA6, 0) # Set display mode normal / inverse (bit 0 = INV)
    else:
        spiByte(0xA7, 0) # Set display mode normal / inverse (bit 0 = INV)

    return

##
#	Graphics Driver
##

def pset(x, y, value):
    if x >= 0 and x <= 131 and y >= 0 and y <= 31:
        by = 0
        if y >= 0 and y <= 7:
            by = 0
            ry = y
        elif y >= 8 and y <= 15:
            by = 1
            ry = y - 8
        elif y >= 16 and y <= 23:
            by = 2
            ry = y - 16
        elif y >= 24 and y <= 31:
            by = 3
            ry = y - 24
        temp_byte = screen_buffer[(by * 132) + x]
        mask = 0b11111111 ^ (0b00000001 << ry)
        temp_byte = temp_byte & mask
        if value != 0:
            temp_byte = temp_byte | (0b00000001 << ry)
        screen_buffer[(by * 132) + x] = temp_byte

def top_blit(character_index, tile_index): # 0, 7 | c 0..255 | t 0..15
    if character_index < 0 or character_index > 255:
        return
    if tile_index < 0 or tile_index > 15:
        return
    character_origin = character_index * 16
    column_offset = tile_index * 8
    for column in range(0, 8):
        tymkrscii_l_byte = tymkrscii_map[character_origin + (column * 2)]
        tymkrscii_u_byte = tymkrscii_map[character_origin + (column * 2) + 1]
        for y in range(0, 8): # low byte
            temp_bit = tymkrscii_l_byte & 0b00000001
            tymkrscii_l_byte = tymkrscii_l_byte >> 1
            pset(column + column_offset, y + 7, temp_bit)
        for y in range(0, 5): # high byte
            temp_bit = tymkrscii_u_byte & 0b00000001
            tymkrscii_u_byte = tymkrscii_u_byte >> 1
            pset(column + column_offset, y + 7 + 8, temp_bit)

def bottom_blit(character_index, tile_index): # o 0, 20 | c 0..255 | t 0..15
    if character_index < 0 or character_index > 255:
        return
    if tile_index < 0 or tile_index > 15:
        return
    character_origin = character_index * 16
    column_offset = tile_index * 8
    for column in range(0, 8):
        tymkrscii_l_byte = tymkrscii_map[character_origin + (column * 2)]
        tymkrscii_u_byte = tymkrscii_map[character_origin + (column * 2) + 1]
        for y in range(0, 8): # low byte
            temp_bit = tymkrscii_l_byte & 0b00000001
            tymkrscii_l_byte = tymkrscii_l_byte >> 1
            pset(column + column_offset, y + 20, temp_bit)
        for y in range(0, 4): # high byte
            temp_bit = tymkrscii_u_byte & 0b00000001
            tymkrscii_u_byte = tymkrscii_u_byte >> 1
            pset(column + column_offset, y + 20 + 8, temp_bit)

def menu_blit(character_index, tile_index, inverted): # o 0, 0 | c 0..??? | t 0..15
    # icon is x 7 bytes by y 6 bits
    if inverted == 0 or inverted == 1:
        offset = tile_index * 8
        for x in range(0, 7):
            temp_byte = menu_map[(character_index * 7) + x]
            for y in range(0, 6):
                temp_bit = temp_byte & 0b00000001
                temp_byte = temp_byte >> 1
                pset(offset + x, y, temp_bit ^ inverted)
                
def menu_clear():
    for i in range(0, 16):
        menu_blit(10, i, 0)

def set_top_text(text):
    working_text = text[0:16]
    while True:
        if len(working_text) < 16:
            working_text = working_text + " "
        else:
            break
    for x in range(0, 16):
        temp_byte = working_text[x:x+1]
        top_blit(ord(temp_byte), x)

def set_bottom_text(text):
    working_text = text[0:16]
    while True:
        if len(working_text) < 16:
            working_text = working_text + " "
        else:
            break
    for x in range(0, 16):
        temp_byte = working_text[x:x+1]
        bottom_blit(ord(temp_byte), x)

def set_bottom_array(text):
    for x in range(0, 16):
        temp_byte = text[x]
        bottom_blit(temp_byte, x)

def set_top_array(text):
    for x in range(0, 16):
        temp_byte = text[x]
        top_blit(temp_byte, x)

def text_to_array(text):
    working_text = text[0:16]
    temp_array = bytearray(16)
    while True:
        if len(working_text) < 16:
            working_text = working_text + " "
        else:
            break
    for x in range(0, 16):
        temp_byte = working_text[x:x+1]
        temp_array[x] = ord(temp_byte)
        #top_blit(ord(temp_byte), x)
    return temp_array

def glyph_next(value):
    global characterset_option, locks
    if locks[5] == 1:
        if characterset_option == 0: # simple
            if value == 32:
                value = 33
            elif value == 33:
                value = 48
            elif value >= 48 and value < 57:
                value = value + 1
            elif value == 57:
                value = 63
            elif value == 63:
                value = 97
            elif value >= 97 and value < 122:
                value = value + 1
            elif value == 122:
                value = 32
            else:
                value = 32
        elif characterset_option == 1: # advanced
            value = value + 1
            if value > 255:
                value = 0
    else:
        if value == 32:
            value = 33
        elif value == 33:
            value = 48
        elif value >= 48 and value < 57:
            value = value + 1
        elif value == 57:
            value = 63
        elif value == 63:
            value = 97
        elif value >= 97 and value < 122:
            value = value + 1
        elif value == 122:
            value = 32
        else:
            value = 32
    return value

def glyph_previous(value):
    global characterset_option, locks
    if locks[5] == 1:
        if characterset_option == 0: # simple
            if value == 32:
                value = 122
            elif value <= 122 and value > 97:
                value = value -1
            elif value == 97:
                value = 63
            elif value == 63:
                value = 57
            elif value <= 57 and value > 48:
                value = value - 1
            elif value == 48:
                value = 33
            elif value == 33:
                value = 32
            else:
                value = 32
        elif characterset_option == 1: # advanced
            value = value - 1
            if value < 0:
                value = 255
    else:
        if value == 32:
            value = 122
        elif value <= 122 and value > 97:
            value = value -1
        elif value == 97:
            value = 63
        elif value == 63:
            value = 57
        elif value <= 57 and value > 48:
            value = value - 1
        elif value == 48:
            value = 33
        elif value == 33:
            value = 32
        else:
            value = 32
    return value

##
#   IR DRIVER
##

TXout       = machine.Pin(16, machine.Pin.OUT, value=0) # uart0
IRin        = machine.Pin(17, machine.Pin.IN, value=0) # uart0
mod         = machine.Pin(18, machine.Pin.OUT, value=0)
uart0		= machine.UART(0, baudrate=3000, tx=TXout, rx=IRin)

def PIOirTxInit():
    sm0 = rp2.StateMachine(0, irPIO, freq=(38000*4), set_base=mod, in_base=TXout, jmp_pin=TXout)  # freq=2000
    sm0.active(1)
    return

@rp2.asm_pio(set_init=(rp2.PIO.OUT_LOW), in_shiftdir=rp2.PIO.SHIFT_LEFT)  # make sure to update this for every output pin you plan to use
def irPIO():
    wrap_target()
    label("loop_start")    # do not put a lable at the end of the loop it will not work as expected....
    set(pins, 0)            [0]
    jmp(pin, "loop_start")  [0]
    set(pins, 1)            [1]
    wrap()
    return

##
#	Network Driver
##

#[body][header: target_id_1 target_id_0 source_id_1 source_id_0 event_id body_len_1 body_len_0 | CS3 CS2 CS1 CS0 SYN SYN SYN SYN]
#type       event_id    format
#page       3           [body: text(16 bytes) alias(16 bytes)]
#broadcast  4           [body: text(16 bytes) alias(16 bytes)]
#command    5           [body: CMD]

# rx buffer len is 48, but bodylen can state a bodylen of 65536
# so we should only accept bodly lens that fit in the buffer 8192 would be a nice number to use (13 bits)
# if the bodylen is clamped to 8192 and we add 15 for the header it comes out to 8207, one less than the circular buffer length
# max checksum should end up at 2092785 (if we ignore that that bodylen would be invalid)

tx_buffer = bytearray(48)

# adaptive body len version (15 + body_len)
def tx(body_len):
    global idle_scroll
    idle_scroll[15] = 5 # 5 for outgoing
    range_top = 15 + body_len
    last_byte = range_top - 1
    for i in range(0, range_top):
        uart0.write(tx_buffer[last_byte - i:(last_byte - i) + 1])
        uart0.flush()
    pico_pulse()

rx_buffer = bytearray(48)
RPC = 0 # Rx Position Counter

def network_initialize():
    global RPC
    RPC = counter_start(48) # set up for size of ir.rx_buffer

def network_step():
    if rx(): # see if stuff was put in the rx_buffer
        if check_syncword(): # there is a sync word, so we may have a packet
            if check_checksum(): # checksum matches
                if DEBUG == True:
                    print("pre check packet rx:")
                    print(rx_buffer)                
                if tx_buffer_match() == False: # make sure we did not just send this
                    handle(get_event_id(), get_to_index(), get_from_index(), get_body_length(), get_body(get_body_length()))
                    if DEBUG == True:
                        print("tx buffer match check:")
                        print(False)
                else:
                    if DEBUG == True:
                        print("tx buffer match check:")
                        print(True)
                    
def tx_buffer_match(): # catch even outgoing relays with a remote index echos
    global tx_buffer
    match = True
    if DEBUG == True:
        print("tx buffer pre clear:")
        print(tx_buffer)
    for i in range(0, 47):
        tx_byte = tx_buffer[i]
        tx_buffer[i] = 0 # zero out so this only matches once
        rx_byte = peek(0 - i)
        #if DEBUG == True: print(tx_byte, rx_byte)
        if tx_byte != rx_byte:
            match = False
    if DEBUG == True:
        print("echo match?")
        print(match)
        print("tx buffer post clear:")
        print(tx_buffer)
    return match

def rx():
    global rx_buffer, RPC, counter
    new_data = False
    start = counter[RPC]
    while(uart0.any() > 0):
        counter_apply_delta(RPC, 1)
        rx_buffer[counter[RPC]] = int.from_bytes(uart0.read(1), 'big')
        new_data = True
    if new_data:
        #if DEBUG == True: print('network: new_data: ', end = '')
        start = start + 1
        if start >= 48:
            start = 0
        while True:
            #if DEBUG == True: print(str(rx_buffer[start]), end = ' ')
            if start == counter[RPC]:
                break
            else:
                start = start + 1
                if start >= 48:
                    start = 0
        #if DEBUG == True: print('')
    return new_data

def handle(event_id, to_index, from_index, body_length, body):
    global serial, idle_scroll
    idle_scroll[15] = 6 # 5 for outgoing
    if from_index == serial: # ignore packets from self
        if DEBUG == True: print('network: echo catcher: ')
        handle_echo(to_index, from_index, body)
        return
    if event_id == 3: # page or broadcast
        if to_index == 0: # a broadcast from origin
            handle_broadcast(True, to_index, from_index, body)
        else: # a page
            handle_page(to_index, from_index, body)
    elif event_id == 4: # relayed broadcast
        handle_broadcast(False, to_index, from_index, body)
    elif event_id == 5: # command
        handle_command()
    elif event_id == 7: # chat
        handle_chat()

def handle_echo(to_index, from_index, body): # detect if messages sent are out on the network now
    if DEBUG == True:
        print("network: handle_echo | from address: " + str(from_index) + " to address: " + str(to_index) + "body: ")
        print(body)
    text = body[16:32]
    queue_id = 0
    event_id = 3
    if DEBUG == True:
        print("text: ")
        print(text)
    match, entry_index = match_queue_entry(queue_id, event_id, from_index, to_index, text)
    if DEBUG == True:
        print("network: handle_echo | entry_index: " + str(entry_index) + " match: ")
        print(match)
    if match == True:
        increment_queue_count(queue_id, entry_index) # saw this packet out on network

def handle_command(command_index):
    pass

def handle_chat(body):
    pass

def handle_page(to_index, from_index, body):
    if DEBUG == True:
        print("network: handle | page from address: " + str(from_index) + " to address: " + str(to_index))
        print("alias: ")
    page_alias = body[0:16]
    if DEBUG == True:
        print(page_alias)
        print("text: ")
    page_text = body[16:32]
    if DEBUG == True: print(page_text)
    note_alias(from_index, page_alias)
    global serial
    if to_index == serial:
        event_id = 3
        if DEBUG == True: print("network: handle | adding inbox entry")
        inbox_add_entry(event_id, from_index, to_index, page_text)
    else:
        if DEBUG == True: print("network: handle | adding relay entry")
        event_id = 3
        relay_add_entry(event_id, from_index, to_index, page_text)

def handle_broadcast(origin, to_scope, from_index, body):
    if DEBUG == True:
        print("network: handle | broadcast from address: " + str(from_index) + " to scope: " + str(to_scope))
        print("alias: ")
    page_alias = body[0:16]
    if DEBUG == True:
        print(page_alias)
        print("text: ")
    page_text = body[16:32]
    if DEBUG == True: print(page_text)
    if origin == True:
        note_alias(from_index, page_alias)
    else: # only if alias is not known
        if read_social_memory(from_index) == 0:
            note_alias(from_index, page_alias)
    
    from_type = serial_to_type(from_index)
    if from_type == 1 or from_type == 2:
        event_id = 4
        if DEBUG == True: print("network: handle | adding inbox entry")
        inbox_add_entry(event_id, from_index, to_scope, page_text)
        if DEBUG == True: print("network: handle | adding relay entry")
        relay_add_entry(event_id, from_index, to_scope, page_text)
    else:
        event_id = 4
        if DEBUG == True: print("network: handle | adding relay entry")
        relay_add_entry(event_id, from_index, to_scope, page_text)
        
def note_alias(from_index, alias):
    if from_index == 0: # never overwrite the alias for ghost
        print("ghosts are not real")
        return
    if DEBUG == True:
        print("network: note_alias | index: " + str(from_index) + " alias: ")
        print(alias)
    write_social_memory(from_index, 1)
    write_alias_memory(from_index, alias)

def inbox_add_entry(event_id, from_index, to_index, text):
    if inbox_match(event_id, from_index, to_index, text):
        if DEBUG == True: print("network: handle | page or broadcast is already in inbox_memory, drop packet")
        return # drop
    else:
        next_entry = inbox_next_entry()
        unread = 1
        if DEBUG == True: print("network: handle | wrote page or broadcast to inbox_memory slot " + str(next_entry))
        write_inbox_memory(next_entry, unread, event_id, from_index, to_index, text)
        ring()
        led_pulse()
        idle_mail_check()

def inbox_match(event_id, from_index, to_index, text):
    for i in range(0, 32):
        entry_unread, entry_event_id, entry_from_index, entry_to_index, entry_text = read_inbox_memory(i)
        if entry_event_id == event_id:
            if entry_from_index == from_index:
                if entry_to_index == to_index:
                    if entry_text == text:
                        return True
    return False

def inbox_next_entry():
    last_entry = read_inbox_last()
    next_entry = last_entry + 1
    if next_entry > 31:
        next_entry = 0
    write_inbox_last(next_entry)
    return next_entry

def relay_add_entry(event_id, from_index, to_index, text):
    global serial
    if from_index == serial:
        queue_id = 0
    else:
        queue_id = 1
    match, entry_index = match_queue_entry(queue_id, event_id, from_index, to_index, text)
    if match == True:
        increment_queue_count(queue_id, entry_index)
    else:
        add_queue_entry(queue_id, 0, event_id, to_index, from_index, text)
        led_pulse()
        led_pulse()

##
#   RX Packet Tools
##

#[header: target_id_1 target_id_0 source_id_1 source_id_0 event_id body_len_1 body_len_0 | CS3 CS2 CS1 CS0 SYN SYN SYN SYN]

SYNCWORD = -3           # -3 -2 -1 0
CHECKSUM = -7           # -7 -6 -5 -4
BODYLEN = -9            # -9 -8
EVENTID = -10           # -10
SID = -12               # -12 -11
TID = -14               # -14 -13

def peek(delta):
    global rx_buffer, RPC
    return rx_buffer[counter_calc_relative_position(RPC, delta)]

def check_syncword():
    global SYNCWORD
    passed = True
    for i in range(0, 4):
        if peek(SYNCWORD + i) != 22: passed = False
    #if DEBUG == True: print('network: check_syncword: ', end = '') # spammy
    #if DEBUG == True: print(passed) # spammy
    return passed

def check_checksum():
    passed = True
    body_length = get_body_length()
    if body_length > 32: # check that max body length is inbounds
        passed = False
        if DEBUG == True:
            print('network: check_checksum: ', end = '')
            print(passed)
    else:
        if get_checksum() != tally_checksum(body_length): passed = False
        if DEBUG == True:
            print('network: check_checksum: ', end = '')
            print(passed)
    return passed

def get_checksum():
    global CHECKSUM
    checksum = 0
    for i in range(0, 4):
        checksum = checksum + (peek(CHECKSUM + i) * (256 ** i))
    if DEBUG == True: print('network: get_checksum: ' + str(checksum))
    return checksum

#[header: target_id_1 target_id_0 source_id_1 source_id_0 event_id body_len_1 body_len_0 | CS3 CS2 CS1 CS0 SYN SYN SYN SYN]

def tally_checksum(body_length):
    tally = 0
    for i in range(-8, (-15 - body_length), -1):
        tally = tally + peek(i)
    if DEBUG == True: print('network: tally_checksum: ' + str(tally))
    return tally

def get_body(body_length):
    body = bytearray(body_length)
    for i in range(0, body_length):
        offset = -15 - i
        body[i] = peek(offset)
    return body

def get_to_index():
    to_index = 0
    for i in range(0, 2):
        to_index = to_index + (peek(TID + i) * (256 ** i))
    if DEBUG == True: print('network: get_to_index: ' + str(to_index))
    return to_index

def get_from_index():
    from_index = 0
    for i in range(0, 2):
        from_index = from_index + (peek(SID + i) * (256 ** i))
    if DEBUG == True: print('network: get_from_index: ' + str(from_index))
    return from_index

def get_body_length():
    body_length = 0
    for i in range(0, 2):
        body_length = body_length + (peek(BODYLEN + i) * (256 ** i))
    if DEBUG == True: print('network: get_body_length: ' + str(body_length))
    return body_length

def get_event_id():
    event_id = peek(EVENTID)
    if DEBUG == True: print('network: get_event_id event_id: ' + str(event_id))
    return event_id

##
#   TX Packet Tools
##

def tx_page(to_index, from_index, alias, body):
    full_body = bytearray(32)
    full_body[0:16] = alias
    full_body[16:32] = body
    if to_index == 0: # broadcast
        write_packet(4, to_index, from_index, full_body)
    else: # page
        write_packet(3, to_index, from_index, full_body)
    tx(32)

def tx_broadcast(to_index, from_index, alias, body):
    if DEBUG == True: print("len alias " + str(len(alias)) + " len body " + str(len(body)))
    full_body = bytearray(32)
    full_body[0:16] = alias
    full_body[16:32] = body
    write_packet(4, to_index, from_index, full_body)
    tx(32)

def write_packet(event_id, to_index, from_index, body):

    global tx_buffer
    body_length = len(body)

    if DEBUG == True:
        print('network: write_tx_header')
        print('network: write_tx_header body_length: ' + str(body_length))
        print('network: write_tx_header event_id: ' + str(event_id))
        print('network: write_tx_header to_index: ' + str(to_index))
        print('network: write_tx_header from_index: ' + str(from_index))
        print('network: write_tx body: ')
        print(body)

    #[header: target_id_1 target_id_0 source_id_1 source_id_0 event_id body_len_1 body_len_0 | CS3 CS2 CS1 CS0 SYN SYN SYN SYN]

    #if DEBUG == True: print("start write")

    # syncword
    tx_buffer[0:4] = bytearray([22, 22, 22, 22])
    #if DEBUG == True: print(tx_buffer[0:60])

    # body length
    tx_buffer[8:10] = body_length.to_bytes(2, 'big')
    #if DEBUG == True: print(tx_buffer[0:60])

    # event_id
    tx_buffer[10:11] = event_id.to_bytes(1, 'big')
    #if DEBUG == True: print(tx_buffer[0:60])

    # from index
    tx_buffer[11:13] = from_index.to_bytes(2, 'big')
    #if DEBUG == True: print(tx_buffer[0:60])

    # to index
    tx_buffer[13:15] = to_index.to_bytes(2, 'big')
    #if DEBUG == True: print(tx_buffer[0:60])

    # body
    tx_buffer[15:(15 + body_length)] = body
    #if DEBUG == True: print(tx_buffer[0:60])

    # checksum (have to do this one last so correct bytes are tallied)
    tx_buffer[4:8] = tally_tx_checksum(body_length).to_bytes(4, 'big')
    #if DEBUG == True: print(tx_buffer[0:60])
    #if DEBUG == True: print("end write")

def clear_tx_buffer():
    global tx_buffer
    for i in range(0, 48):
        tx_buffer[i] = 0
    if DEBUG == True: print('network: clear_tx_buffer')

def tally_tx_checksum(body_length):
    global tx_buffer
    # if DEBUG == True: print(tx_buffer[0:60])
    tally = 0
    for i in range(8, (15 + body_length)):
        # if DEBUG == True: print("i=" + str(i) + " tx_buffer[i]=" + str(tx_buffer[i]))
        tally = tally + tx_buffer[i]
    if DEBUG == True: print('network: tally_tx_checksum: ' + str(tally))
    return tally

##
#	Counter Driver
##

counter = []
threshold = []

def counter_start(new_threshold):
    global counter, threshold
    counter.append(0)
    threshold.append(new_threshold)
    if DEBUG == True: print('counters: started a new counter index: ' + str(len(threshold) - 1) + ' threhold: ' + str(new_threshold))
    return len(threshold) - 1

def counter_restart(index, new_threshold):
    global counter, threshold
    threshold[index] = new_threshold
    counter[index] = 0

def counter_reset(index):
    #if DEBUG == True: print('counters: reset counter index: ' + str(index)) #can get spammy so leaving it off
    counter[index] = 0

def counter_count(index): # increments counter, resets and returns True if threshold tripped
    global counter, threshold
    counter[index] = counter[index] + 1
    if counter[index] > threshold[index]:
        #if DEBUG == True: print('counters: counter #' + str(index) + ' tripped') #can get spammy so leaving it off
        counter_reset(index)
        return True
    return False

def counter_apply_delta(index, delta):
    global counter
    counter[index] = counter_calc_relative_position(index, delta)

def counter_calc_relative_position(index, delta):
    global counter
    relative_position = counter[index] + delta
    if relative_position < 0:
        relative_position = relative_position + threshold[index]
    elif relative_position >= threshold[index]:
        relative_position = relative_position - threshold[index]
    return relative_position

##
#	Serial Driver
##

#ghost       000..000	0
#founder     001..025	1
#extreme     026..100	2
#lifetime    101..110 	3
#speaker     111..220	4
#general     221..660	5
#vendor      661..675	6

serial = 221
badge_type = 5

def serial_load_file():
    f1 = open('serial', 'rb')
    serial_id = int.from_bytes(f1.read(2), 'big')
    f1.close()
    if DEBUG == True: print("init: serial #" + str(serial_id))
    return serial_id

def serial_to_type(encoded):
    if encoded >= 1 and encoded <= 25:
        return  1
    elif encoded >= 26 and encoded <= 100:
        return  2
    elif encoded >= 101 and encoded <= 110:
        return  3
    elif encoded >= 111 and encoded <= 220:
        return  4
    elif encoded >= 221 and encoded <= 660:
        return 5
    elif encoded >= 661 and encoded <= 675:
        return 6
    else:
        return 0

def init_serial():
    global serial, badge_type
    serial = serial_load_file()
    badge_type = serial_to_type(serial)
    if badge_type == 0:
        if DEBUG == True: print("init: badge type: " + "ghost")
    elif badge_type == 1:
        if DEBUG == True: print("init: badge type: " + "founder")
    elif badge_type == 2:
        if DEBUG == True: print("init: badge type: " + "extreme")
    elif badge_type == 3:
        if DEBUG == True: print("init: badge type: " + "lifetime")
    elif badge_type == 4:
        if DEBUG == True: print("init: badge type: " + "speaker")
    elif badge_type == 5:
        if DEBUG == True: print("init: badge type: " + "general")
    elif badge_type == 6:
        if DEBUG == True: print("init: badge type: " + "vendor")

##
#	Memory Driver
##

def create_social_memory_if_missing():
    #check if social_memory file exists
    user_check = False
    try:
        f1 = open('social_memory', 'rb')
        f1.close()
        user_check = True
        if DEBUG == True: print('files: create_social_memory_if_missing: file found')
    except OSError:  # open failed
        pass
        if DEBUG == True: print('files: create_social_memory_if_missing: file not found')

    if user_check == False:
        if DEBUG == True: print('files: create_social_memory_if_missing: generating empty social_memory file')
        create_empty_social_memory()

def create_empty_social_memory():
    f = open('social_memory', 'wb+')
    for u in range(0, 676):
        unseen = 0
        f.write(unseen.to_bytes(1, 'big'))
    f.close()

def write_social_memory(remote_index, value):
    f = open('social_memory', 'rb+')
    f.seek( remote_index )
    f.write(value.to_bytes(1, 'big'))
    f.close()

def read_social_memory(remote_index):
    f = open('social_memory', 'rb')
    f.seek( remote_index )
    return int.from_bytes(f.read(1), 'big')

def create_alias_memory_if_missing():
    #check if alias_memory file exists
    user_check = False
    try:
        f1 = open('alias_memory', 'rb')
        f1.close()
        user_check = True
        if DEBUG == True: print('files: create_alias_memory_if_missing: file found')
    except OSError:  # open failed
        pass
        if DEBUG == True: print('files: create_alias_memory_if_missing: file not found')

    if user_check == False:
        if DEBUG == True: print('files: create_alias_memory_if_missing: generating empty alias_memory file')
        create_empty_alias_memory()

def create_empty_alias_memory():
    f = open('alias_memory', 'wb+')
    for u in range(0, 10816):
        unseen = 0
        f.write(unseen.to_bytes(1, 'big'))
    f.close()

def read_alias_memory(remote_index):
    f = open('alias_memory', 'rb')
    f.seek( remote_index * 16)
    temp = bytearray(16)
    for i in range(0, 16):
        value = int.from_bytes(f.read(1), 'big')
        temp[i] = value
    return temp # int.from_bytes(f.read(1), 'big')

def write_alias_memory(remote_index, alias_bytearray):
    f = open('alias_memory', 'rb+')
    f.seek( remote_index * 16 )
    for i in range(0, 16):
        value = alias_bytearray[i]
        f.write(value.to_bytes(1, 'big'))
    f.close()

def next_alias(remote_index):
    loop_count = 0
    memory_index = remote_index
    while True:
        memory_index = memory_index + 1
        if memory_index > 675:
            memory_index = 0
            loop_count = loop_count + 1
            if loop_count == 2: # catch if there are no populated entries
                return 0
        temp = read_social_memory(memory_index)
        #if DEBUG == True: print(memory_index, temp)
        if temp == 1:
            break
    # at this point remote_index should store the next populated entry index
    return memory_index

def previous_alias(remote_index):
    loop_count = 0
    memory_index = remote_index
    while True:
        memory_index = memory_index - 1
        if memory_index < 0:
            memory_index = 675
            loop_count = loop_count + 1
            if loop_count == 2: # catch if there are no populated entries
                return 0
        temp = read_social_memory(memory_index)
        if temp == 1:
            break
    # at this point remote_index should store the next populated entry index
    return memory_index

# inbox_memory
#	unread[1 byte], event_id[1 byte], from_index[2 bytes], to_index[2 bytes], text[16 bytes] | [22 bytes]
#	" x32
#	next_entry [1 byte] [705 bytes total]
#	unread: 0=empty 1=unread 2=read
#	unread[0:1] event_id[1:2] from_index[2:4] to_index[4:6] text[6:22]
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 [22 bytes]

def create_inbox_memory_if_missing():
    #check if inbox_memory file exists
    user_check = False
    try:
        f1 = open('inbox_memory', 'rb')
        f1.close()
        user_check = True
        if DEBUG == True: print('files: create_inbox_memory_if_missing: file found')
    except OSError:  # open failed
        pass
        if DEBUG == True: print('files: create_inbox_memory_if_missing: file not found')

    if user_check == False:
        if DEBUG == True: print('files: create_inbox_memory_if_missing: generating empty inbox_memory file')
        create_empty_inbox_memory()

def create_empty_inbox_memory():
    f = open('inbox_memory', 'wb+')
    for u in range(0, 705):
        unseen = 0
        f.write(unseen.to_bytes(1, 'big'))
    f.close()

def write_inbox_memory(next_entry, unread, event_id, from_index, to_index, text):
    f = open('inbox_memory', 'rb+')
    f.seek( next_entry * 22 )
    f.write(unread.to_bytes(1, 'big'))
    f.write(event_id.to_bytes(1, 'big'))
    f.write(from_index.to_bytes(2, 'big'))
    f.write(to_index.to_bytes(2, 'big'))
    for i in range(0, 16):
        value = text[i]
        f.write(value.to_bytes(1, 'big'))
    f.close()

def read_inbox_memory(memory_index):
    f = open('inbox_memory', 'rb')
    f.seek(memory_index * 22)
    temp_entry = bytearray(22)
    for i in range(0, 22):
        value = int.from_bytes(f.read(1), 'big')
        temp_entry[i] = value
    # unread[0:1] event_id[1:2] from_index[2:4] to_index[4:6] text[6:22]
    entry_unread = int.from_bytes(temp_entry[0:1], 'big')
    entry_event_id = int.from_bytes(temp_entry[1:2], 'big')
    entry_from_index = int.from_bytes(temp_entry[2:4], 'big')
    entry_to_index = int.from_bytes(temp_entry[4:6], 'big')
    entry_text = temp_entry[6:22]
    return entry_unread, entry_event_id, entry_from_index, entry_to_index, entry_text

def read_inbox_last():
    f = open('inbox_memory', 'rb')
    f.seek( 704 )
    return int.from_bytes(f.read(1), 'big')

def write_inbox_last(next_entry):
    f = open('inbox_memory', 'rb+')
    f.seek( 704 )
    f.write(next_entry.to_bytes(1, 'big'))
    f.close()

def read_inbox_unread(memory_index):
    f = open('inbox_memory', 'rb')
    f.seek(memory_index * 22)
    temp_entry = bytearray(22)
    for i in range(0, 22):
        value = int.from_bytes(f.read(1), 'big')
        temp_entry[i] = value
    # unread[0:1] event_id[1:2] from_index[2:4] to_index[4:6] text[6:22]
    entry_unread = int.from_bytes(temp_entry[0:1], 'big')
    return entry_unread

def write_inbox_unread(memory_index, unread):
    f = open('inbox_memory', 'rb+')
    f.seek( memory_index * 22 )
    f.write(unread.to_bytes(1, 'big'))
    f.close()

def next_page(base_index):
    loop_count = 0
    memory_index = base_index
    while True:
        memory_index = memory_index + 1
        if memory_index > 31:
            memory_index = 0
            loop_count = loop_count + 1
            if loop_count == 2: # catch if there are no populated entries
                return 0
        temp = read_inbox_unread(memory_index)
        if temp == 1 or temp == 2: # unread 1 or read 2, not empty 0
            break
    # at this point memory_index should store the next populated entry index
    return memory_index

def previous_page(base_index):
    loop_count = 0
    memory_index = base_index
    while True:
        memory_index = memory_index - 1
        if memory_index < 0:
            memory_index = 31
            loop_count = loop_count + 1
            if loop_count == 2: # catch if there are no populated entries
                return 0
        temp = read_inbox_unread(memory_index)
        if temp == 1 or temp == 2: # unread 1 or read 2, not empty 0
            break
    # at this point memory_index should store the next populated entry index
    return memory_index

##
#   VIBRATOR DRIVER
##

vib         = machine.Pin(2, machine.Pin.OUT, value=0)

def ring():
    vib.on()
    utime.sleep(0.1)
    vib.off()
    utime.sleep(0.1)

##
#   LED DRIVER
##

LED0		= machine.Pin(25, machine.Pin.OUT, value=0) # led on pico
LED1        = machine.Pin(0, machine.Pin.OUT, value=1)
LED2        = machine.Pin(6, machine.Pin.OUT, value=1)
LED3        = machine.Pin(27, machine.Pin.OUT, value=1)
LED4        = machine.Pin(13, machine.Pin.OUT, value=1)
LED5        = machine.Pin(20, machine.Pin.OUT, value=1)
LED6        = machine.Pin(19, machine.Pin.OUT, value=1)

def led_rotate():
    empty = True
    for i in range(1, 7):
        if led_get(i) == 1:
            empty = False
    if empty == True:
        led_set(6, 1)

    temp = led_get(6)
    for i in range(6, 1, -1):
        led_set(i, led_get(i - 1))
    led_set(1, temp)
        
def led_get(led_index): # red leds low=on | pico low=off
    global LED0, LED1, LED2, LED3, LED4, LED5, LED6
    if led_index == 0: # pico led
        if LED0.value() == 0:
            return 0
        else:
            return 1
    elif led_index == 1:
        if LED1.value() == 1:
            return 0
        else:
            return 1
    elif led_index == 2:
        if LED2.value() == 1:
            return 0
        else:
            return 1
    elif led_index == 3:
        if LED3.value() == 1:
            return 0
        else:
            return 1
    elif led_index == 4:
        if LED4.value() == 1:
            return 0
        else:
            return 1
    elif led_index == 5:
        if LED5.value() == 1:
            return 0
        else:
            return 1
    elif led_index == 6:
        if LED6.value() == 1:
            return 0
        else:
            return 1

def led_set(led_index, value): # red leds low=on | pico low=off
    global LED0, LED1, LED2, LED3, LED4, LED5, LED6
    if led_index == 0: # pico led
        if value == 0:
            LED0.off()
        else:
            LED0.on()
    elif led_index == 1:
        if value == 0:
            LED1.on()
        else:
            LED1.off()
    elif led_index == 2:
        if value == 0:
            LED2.on()
        else:
            LED2.off()
    elif led_index == 3:
        if value == 0:
            LED3.on()
        else:
            LED3.off()
    elif led_index == 4:
        if value == 0:
            LED4.on()
        else:
            LED4.off()
    elif led_index == 5:
        if value == 0:
            LED5.on()
        else:
            LED5.off()
    elif led_index == 6:
        if value == 0:
            LED6.on()
        else:
            LED6.off()

def led_pulse():
    for i in range(0, 7):
        led_set(i, 1)
    utime.sleep(0.01)
    for i in range(0, 7):
        led_set(i, 0)
    utime.sleep(0.01)
    
def pico_pulse():
    led_set(0, 1)
    utime.sleep(0.01)
    led_set(0, 0)
    utime.sleep(0.01)

##
#   BUTTON DRIVER
##
social      = machine.Pin(1, machine.Pin.IN, value=0)
sw1dwn      = machine.Pin(3, machine.Pin.IN, value=0)
sw1push     = machine.Pin(14, machine.Pin.IN, value=0)
sw1up       = machine.Pin(15, machine.Pin.IN, value=0)
sw2dwn      = machine.Pin(21, machine.Pin.IN, value=0)
sw2push     = machine.Pin(22, machine.Pin.IN, value=0)
sw2up       = machine.Pin(26, machine.Pin.IN, value=0)

sw_0_i	= False
sw_1_u	= False
sw_1_d	= False
sw_1_i	= False
sw_2_u	= False
sw_2_d	= False
sw_2_i	= False

def ui_handler():
    global sw_0_i, sw_1_u, sw_1_d, sw_1_i, sw_2_u, sw_2_d, sw_2_i
    if social.value() == 0 and sw_0_i == False:
        sw_0_i = True
        if DEBUG == True: print("sw_0_i pressed")
        led_pulse()
    elif social.value() == 1 and sw_0_i == True:
        sw_0_i = False
        if DEBUG == True: print("sw_0_i unpressed")
        handle_sw_0_i()
    if sw1up.value() == 0 and sw_1_u == False:
        sw_1_u = True
        if DEBUG == True: print("sw_1_u pressed")
        led_pulse()
    elif sw1up.value() == 1 and sw_1_u == True:
        sw_1_u = False
        if DEBUG == True: print("sw_1_u unpressed")
        handle_sw_1_u()
    if sw1dwn.value() == 0 and sw_1_d == False:
        sw_1_d = True
        if DEBUG == True: print("sw_1_d pressed")
        led_pulse()
    elif sw1dwn.value() == 1 and sw_1_d == True:
        sw_1_d = False
        if DEBUG == True: print("sw_1_d unpressed")
        handle_sw_1_d()
    if sw1push.value() == 0 and sw_1_i == False:
        sw_1_i = True
        if DEBUG == True: print("sw_1_i pressed")
        led_pulse()
    elif sw1push.value() == 1 and sw_1_i == True:
        sw_1_i = False
        if DEBUG == True: print("sw_1_i unpressed")
        handle_sw_1_i()
    if sw2up.value() == 0 and sw_2_u == False:
        sw_2_u = True
        if DEBUG == True: print("sw_2_u pressed")
        led_pulse()
    elif sw2up.value() == 1 and sw_2_u == True:
        sw_2_u = False
        if DEBUG == True: print("sw_2_u unpressed")
        handle_sw_2_u()
    if sw2dwn.value() == 0 and sw_2_d == False:
        sw_2_d = True
        if DEBUG == True: print("sw_2_d pressed")
        led_pulse()
    elif sw2dwn.value() == 1 and sw_2_d == True:
        sw_2_d = False
        if DEBUG == True: print("sw_2_d unpressed")
        handle_sw_2_d()
    if sw2push.value() == 0 and sw_2_i == False:
        sw_2_i = True
        if DEBUG == True: print("sw_2_i pressed")
        led_pulse()
    elif sw2push.value() == 1 and sw_2_i == True:
        sw_2_i = False
        if DEBUG == True: print("sw_2_i unpressed")
        handle_sw_2_i()

def handle_sw_0_i():
    if mode == 0: # idle
        global serial
        tx_page(serial, serial, read_alias_memory(serial), bytearray(16))
    elif mode == 1: # alias
        alias_save()
        mode_init(0) # >> idle
    elif mode == 4: # compose_2
        global compose_contact, serial, alias, compose_text
        #add_queue_entry(queue_id, entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text)
        #tx_page(compose_contact, serial, alias, compose_text)
        add_queue_entry(0, 0, 3, compose_contact, serial, compose_text)
        mode_init(0) # >> idle
def handle_sw_1_i():
    if mode == 0:
        mode_init(1) # >> alias
    else:
        mode_init(0) # cancel and return to idle
def handle_sw_1_u():
    if mode == 0: # idle
        mode_init(2) # >> inbox
    elif mode == 1: # alias
        alias_cursor_left()
    elif mode == 4: # compose_2
        compose_2_cursor_left()
def handle_sw_1_d():
    shift_key()
def handle_sw_2_i():
    if mode == 0: # idle
        mode_init(3) # >> compose_1
    elif mode == 1: # alias
        alias_cursor_right()
    elif mode == 2: # inbox
        inbox_mark_read()
    elif mode == 3: # compose_1
        mode_init(4) # >> compose_2
    elif mode == 4: # compose_2
        compose_2_cursor_right()
def handle_sw_2_u():
    if mode == 0: # idle
        mode_init(3) # >> compose_1
    elif mode == 3: # compose_1
        compose_1_previous_contact()
def handle_sw_2_d():
    if mode == 0: # idle
        mode_init(3) # >> compose_1
    elif mode == 3: # compose_1
        compose_1_next_contact()

def shift_key():
    global mode, characterset_option
    if mode == 1 or mode == 4: # alias or compose_2
        if characterset_option == 0:
            characterset_option = 1
            if DEBUG == True: print("ui: shift_key | shift is on")
        else:
            characterset_option = 0
            if DEBUG == True: print("ui: shift_key | shift is off")

##
#	Menu Graphics Driver
##

mode = 0

def mode_handler():
    global mode
    if mode == 0: # idle
        idle_animate()
    elif mode == 1: # alias
        alias_animate()
    elif mode == 2: # inbox
        inbox_animate()
    elif mode == 3: # compose page 1
        compose_1_animate()
    elif mode == 4: # compose page 2
        compose_2_animate()
    flip()

def mode_init(mode_index):
    global mode
    if mode_index == 0:
        global alias
        if alias == bytearray(16):
            if DEBUG == True: print("menu: init | alias not set, starting alias")
            mode_init(1)
            return
        else:
            mode = 0
            idle_init()
    elif mode_index == 1:
        mode = 1
        alias_init()
    elif mode_index == 2:
        mode = 2
        inbox_init()
    elif mode_index == 3:
        mode = 3
        compose_1_init()
    elif mode_index == 4:
        mode = 4
        compose_2_init()

##
#	idle app
##

idle_scroll = bytearray(16)
you_have_got_mail = 0

def idle_init():
    global idle_scroll
    idle_mail_check()
    set_top_text("")
    set_bottom_text("    willasaywhat")
    # willa edit
    # bottom_blit(22, 0)
    # bottom_blit(23, 1)
    # bottom_blit(24, 2)
    # bottom_blit(25, 3)
    # bottom_blit(26, 4)
    
def idle_animate():
    global idle_scroll, you_have_got_mail
    for i in range(0, 15):
        idle_scroll[i] = idle_scroll[i + 1]
        top_blit(idle_scroll[i], i)
    idle_scroll[15] = 0
    top_blit(idle_scroll[15], 15)
    menu_blit(random.getrandbits(4), random.getrandbits(4), random.getrandbits(1))
    if you_have_got_mail > 0:
        led_rotate()

def idle_mail_check():
    global you_have_got_mail
    you_have_got_mail = 0
    for memory_index in range(0, 32):
        if read_inbox_unread(memory_index) == 1:
            you_have_got_mail = you_have_got_mail + 1  

##
#	alias app
##

temp_alias = bytearray(16)
alias_cpos = 0

def alias_init():
    global alias, temp_alias
    temp_alias = alias
    set_top_text("edit your name:")
    menu_clear()
    menu_blit(13, 15, 0)

def alias_save():
    global alias, temp_alias
    alias = temp_alias
    write_alias_memory(serial, alias)
    if DEBUG == True: print("alias | alias saved")

def alias_animate():
    global alias, temp_alias, alias_cpos, sw_2_u, sw_2_d
    if sw_2_u == True: # cycle glyph up
        global alias_cpos, temp_alias
        temp = temp_alias[alias_cpos]
        temp = glyph_next(temp)
        temp_alias[alias_cpos] = temp
    if sw_2_d == True: # cycle glyph down
        global alias_cpos, temp_alias
        temp = temp_alias[alias_cpos]
        temp = glyph_previous(temp)
        temp_alias[alias_cpos] = temp
    for x in range(0, 132):
        pset(x, 31, 0)
    set_bottom_array(alias)
    for x in range(0, 8):
        pset((alias_cpos * 8) + x, 31, 1)

def alias_cursor_left():
    global alias_cpos
    if DEBUG == True: print("alias | cursor left")
    temp = alias_cpos
    temp = temp - 1
    if temp < 0:
        temp = 0
    if temp > 15:
        temp = 15
    alias_cpos = temp

def alias_cursor_right():
    global alias_cpos
    if DEBUG == True: print("alias | cursor right")
    temp = alias_cpos
    temp = temp + 1
    if temp < 0:
        temp = 0
    if temp > 15:
        temp = 15
    alias_cpos = temp

##
#	compose 1 app
##

compose_contact = 0

def compose_1_init():
    global compose_contact
    compose_contact = 0
    menu_clear()
    menu_blit(14, 15, 0)
    set_top_text("send to:")
    set_bottom_array(read_alias_memory(compose_contact))

def compose_1_animate():
    global compose_contact
    set_bottom_array(read_alias_memory(compose_contact))

def compose_1_previous_contact():
    global compose_contact
    compose_contact = previous_alias(compose_contact)

def compose_1_next_contact():
    global compose_contact
    compose_contact = next_alias(compose_contact)

##
#	compose 2 app
##

compose_text = bytearray(16)
compose_cpos = 0

def compose_2_init():
    global compose_text, compose_cpos
    compose_text = bytearray(16)
    compose_cpos = 0
    set_top_array(read_alias_memory(compose_contact))
    set_bottom_text("")

def compose_2_animate():
    global compose_contact, compose_text, compose_cpos, sw_2_u, sw_2_d
    if sw_2_u == True: # cycle glyph up
        temp = compose_text[compose_cpos]
        temp = glyph_next(temp)
        compose_text[compose_cpos] = temp
    if sw_2_d == True: # cycle glyph down
        temp = compose_text[compose_cpos]
        temp = glyph_previous(temp)
        compose_text[compose_cpos] = temp
    for x in range(0, 132):
        pset(x, 31, 0)
    set_top_array(read_alias_memory(compose_contact))
    set_bottom_array(compose_text)
    for x in range(0, 8):
        pset((compose_cpos * 8) + x, 31, 1)

def compose_2_cursor_left():
    global compose_cpos
    if DEBUG == True: print("compose 2 | cursor left")
    temp = compose_cpos
    temp = temp - 1
    if temp < 0:
        temp = 0
    if temp > 15:
        temp = 15
    compose_cpos = temp

def compose_2_cursor_right():
    global compose_cpos
    if DEBUG == True: print("compose 2 | cursor right")
    temp = compose_cpos
    temp = temp + 1
    if temp < 0:
        temp = 0
    if temp > 15:
        temp = 15
    compose_cpos = temp

##
#	inbox app
##

inbox_memory_index = 0

def inbox_init():
    global inbox_memory_index
    inbox_memory_index = read_inbox_last()
    entry_unread, entry_event_id, entry_from_index, entry_to_index, entry_text = read_inbox_memory(inbox_memory_index)
    menu_clear()
    menu_blit(15, 15, 0)
    set_top_array(read_alias_memory(entry_from_index))
    set_bottom_array(entry_text)
    
def inbox_animate():
    global inbox_memory_index, sw_2_u, sw_2_d
    if sw_2_u == True: # next entry
        inbox_memory_index = next_page(inbox_memory_index)
    if sw_2_d == True: # previous entry
        inbox_memory_index = previous_page(inbox_memory_index)    
    entry_unread, entry_event_id, entry_from_index, entry_to_index, entry_text = read_inbox_memory(inbox_memory_index)
    if entry_unread == 1: # unread
        menu_blit(10, 0, 1)
    elif entry_unread == 2: # read
        menu_blit(11, 0, 1)
    if entry_event_id == 3: # page
        menu_blit(13, 2, 0)
    elif entry_event_id == 4: # broadcast
        menu_blit(12, 2, 0)
    set_top_array(read_alias_memory(entry_from_index))
    set_bottom_array(entry_text)
    
def inbox_mark_read():
    global inbox_memory_index
    write_inbox_unread(inbox_memory_index, 2)

##
#	queue driver
##

queue = bytearray(176) # entry_count 1, entry_event_id 1, entry_to_index 2, entry_from_index 2, entry_text 16 = 22
queue_pointer = 0

def queue_step():
    global queue_pointer, serial
    
    # queue 0
    entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text = read_queue_entry(0, queue_pointer)
    if entry_count < 4 and entry_from_index == serial: # not stale and from me
        if entry_event_id == 3:
            tx_page(entry_to_index, entry_from_index, read_alias_memory(entry_from_index), entry_text)
        elif entry_event_id == 4:
            tx_broadcast(entry_to_index, entry_from_index, read_alias_memory(entry_from_index), entry_text)
    
    # queue 1
    entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text = read_queue_entry(1, queue_pointer)
    if entry_count < 4: # not stale
        if entry_event_id == 3:
            tx_page(entry_to_index, entry_from_index, read_alias_memory(entry_from_index), entry_text)
        elif entry_event_id == 4:
            tx_broadcast(entry_to_index, entry_from_index, read_alias_memory(entry_from_index), entry_text)
    
    increment_queue_pointer()

def increment_queue_pointer():
    global queue_pointer
    temp = queue_pointer
    temp = temp + 1
    if temp > 3:
        temp = 0
    queue_pointer = temp

def remove_queue_entry(queue_id, entry_index):
    ubound = 3 - entry_index
    for o in range(0, ubound):
        entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text = read_queue_entry(queue_id, (entry_index + o + 1))
        write_queue_entry(queue_id, (entry_index + o), entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text)
    set_queue_count(queue_id, 3, 4) # count of 4 = stale, will not tx

def add_queue_entry(queue_id, entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text):
    fifo_queue(queue_id)
    write_queue_entry(queue_id, 0, entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text)
    
def fifo_queue(queue_id): # move enties down (entry 3 falls off)
    for i in range(3, 0, -1):
        entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text = read_queue_entry(queue_id, i - 1)
        write_queue_entry(queue_id, i, entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text)
    set_queue_count(queue_id, 0, 4) # count of 4 = stale, will not tx

def read_queue_entry(queue_id, entry_index):
    global queue
    entry_offset = ((queue_id * 88) + (entry_index * 22))
    entry_count = int.from_bytes(queue[(entry_offset + 0):(entry_offset + 1)], 'big')
    entry_event_id = int.from_bytes(queue[(entry_offset + 1):(entry_offset + 2)], 'big')
    entry_to_index = int.from_bytes(queue[(entry_offset + 2):(entry_offset + 4)], 'big')
    entry_from_index = int.from_bytes(queue[(entry_offset + 4):(entry_offset + 6)], 'big')
    entry_text = queue[(entry_offset + 6):(entry_offset + 22)]
    if DEBUG == True: print("read_queue_entry: queue_id " + str(queue_id) + " entry_index " + str(entry_index))
    return entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text

def write_queue_entry(queue_id, entry_index, entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text):
    global queue
    entry_offset = ((queue_id * 88) + (entry_index * 22))
    queue[(entry_offset + 0):(entry_offset + 1)] = entry_count.to_bytes(1, 'big')
    queue[(entry_offset + 1):(entry_offset + 2)] = entry_event_id.to_bytes(1, 'big')
    queue[(entry_offset + 2):(entry_offset + 4)] = entry_to_index.to_bytes(2, 'big')
    queue[(entry_offset + 4):(entry_offset + 6)] = entry_from_index.to_bytes(2, 'big')
    queue[(entry_offset + 6):(entry_offset + 22)] = entry_text
    if DEBUG == True: print("write_queue_entry: queue_id " + str(queue_id) + " entry_index " + str(entry_index))
    
def get_queue_count(queue_id, entry_index):
    global queue
    entry_offset = ((queue_id * 88) + (entry_index * 22))
    entry_count = int.from_bytes(queue[(entry_offset + 0):(entry_offset + 1)], 'big')
    if DEBUG == True: print("get_queue_count: queue_id " + str(queue_id) + " entry_index " + str(entry_index) + " entry_count " + str(entry_count))
    return entry_count

def set_queue_count(queue_id, entry_index, entry_count):
    global queue
    entry_offset = ((queue_id * 88) + (entry_index * 22))
    queue[(entry_offset + 0):(entry_offset + 1)] = entry_count.to_bytes(1, 'big')
    if DEBUG == True: print("set_queue_count: queue_id " + str(queue_id) + " entry_index " + str(entry_index) + " entry_count " + str(entry_count))
    pass

def match_queue_entry(queue_id, event_id, from_index, to_index, text):
    for i in range(0, 4):
        entry_count, entry_event_id, entry_to_index, entry_from_index, entry_text = read_queue_entry(queue_id, i)
        if DEBUG == True:
            print("match_queue_entry breakout index: " + str(i))
            print("event_id: " + str(event_id) + " from_index: " + str(from_index) + " to_index: " + str(to_index) + " text: ")
            print(text)
            print("entry_event_id: " + str(entry_event_id) + " entry_from_index: " + str(entry_from_index) + " entry_to_index: " + str(entry_to_index) + " entry_text: ")
            print(entry_text)
        if event_id == entry_event_id and from_index == entry_from_index and to_index == entry_to_index and text == entry_text:
            if DEBUG == True: print("match_queue_entry | match found in queue " + str(queue_id) + " at index " + str(i))
            return True, i
        else:
            if DEBUG == True: print("match_queue_entry | match not found in queue " + str(queue_id) + " at index " + str(i))
    return False, 0

def increment_queue_count(queue_id, entry_index):
    entry_count = get_queue_count(queue_id, entry_index)
    entry_count = entry_count + 1
    if entry_count > 255:
        entry_count = 255
    set_queue_count(queue_id, entry_index, entry_count)
    if DEBUG == True: print("*** increment_queue_count: queue_id " + str(queue_id) + " entry_index " + str(entry_index) + " entry_count now " + str(entry_count))

##
#	Init
##

def init():
    global alias, locks, characterset_option
    if DEBUG == True:
        print("Cyphercon 9 Pager")
        print("init: booting up")
        print("init: checking files")
    create_alias_memory_if_missing()
    create_social_memory_if_missing()
    create_inbox_memory_if_missing()
    if DEBUG == True: print("init: loading serial number")
    init_serial()
    if DEBUG == True: print("init: loading local alias from alias_memory file")
    alias = read_alias_memory(serial)
    if DEBUG == True:
        print(alias)
        print("init: summoning spirits")
    if badge_type == 1 or badge_type == 2:
        write_alias_memory(0, text_to_array("BROADCAST"))
        locks = bytearray([0, 0, 0, 0, 0, 1])
    else:
        write_alias_memory(0, text_to_array("/dev/null"))
        locks = bytearray([0, 0, 0, 0, 0, 0])
    characterset_option = 0
    if DEBUG == True: print("init: starting IR")
    PIOirTxInit()
    if DEBUG == True: print("init: starting network stack")
    network_initialize()
    if DEBUG == True: print("init: starting display")
    initLCD()
    if DEBUG == True: print("menu system: starting menu")
    mode_init(0)

##
#	Main Entry
##

DEBUG = True

init()

while True:
    gc.collect()
    ui_handler()
    mode_handler()
    network_step()
    if random.getrandbits(2) == 0: queue_step()