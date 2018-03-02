# hex.py
Simple file writer, accepts numbers in binary, octal, hex, decimal.

Format:

* bX - X_2
* oX - X_8
* dX - X_10
* xX - X_16

# koipond.py
Gravity Simulator. Editable infile are four options:
* party - Activate party mode (gravitational effects reversed)
* pond - Fish theme
* wall - Toggles wall preventing objects from leaving screen
* gay - Surprise

# mokitools.py
A helper for those manually writing 2-bit mokifiles.

* w - 11
* s - 10
* g - 01
* b - 00

Output is decimal.

# mokiview.py

.moki image viewer

| 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 0A | 0B | 0C | 0D | 0E | 0F |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 4D | 4F | 4F | 4F | 00 | 00 | 17 | 00 | 49 | 01 | F0 | 00 | 00 | 01 | 00 | 10 |
|  M |  O |  K |  I | b/px | Width | ... | Height | ... | Layers | Speed | Frames | ... | ... | (Image Start) | ... |

## Accepted b/px formats:

* 00 (1-bit b/w)
  * 0 = #000000 
  * 1 = #FFFFFF
* 01 - (8-bit RGBA) byte = RRGGBBAA
* 02 - (16-bit RGBA) byte = RRRRGGGG BBBBAAAA
* 03 - (24-bit RGB) RR GG BB
* 04 - (32-bit RGBA) RR GG BB AA
* E0 - Palette 1 "Earth"
  * 0 = #000000
  * 1 = #040613
  * 2 = #244058
  * 3 = #414b29
  * 4 = #4d4c48
  * 5 = #737b86
  * 6 = #78829b
  * 7 = #7c6d4c
  * 8 = #85796d
  * 9 = #908782
  * A = #9a8860
  * B = #ab8465
  * C = #c0c1b1
  * D = #c6d2c6
  * E = #eeeae7
  * F = #ffffff
* F0 (unimplemented) (24-bit vectorized RGB) 12-byte: ID RR GG BB X1__ Y1__ X2__ Y2__
* FB (6-bit RGB) byte = RRGGBBRR GGBBRRGG BBRRGGBB
* FC (4-bit RGBA) byte = RGBARGBA
* FD (3-bit RGB) byte = RGBRGBRG BRGBRGBR GBRGBRGB
* FE (2-bit greyscale)
  * 00 = #000000 
  * 01 = #555555
  * 10 = #AAAAAA
  * 11 = #FFFFFF
* FF - (unimplemented) Custom Palette, stored in header as RR GG BB RR GG BB ... etc, bitness automatically determined

## Width, Height

Big-endian. In pixels. Maximum 65,535.

## Layers

Number of layers, for image editing and 3-D imagery. Maximum 255.

## Speed

4 times the FPS. Minimum 0.25 hz, maximum 64 hz. 

## Frames

For video. Maximum 16,777,215 (18,641 hours of video at 1/4 hz, 78 hours of video at 60 hz.).

## Image Start

Byte where the image starts. Normally 0x10, but may be postponed to include metadata or palette information.

## Notes

* 0x0000 under Width, Height, Layers, and Frames is treated as 0x0001.
* Theoretical maximum filesize is 73496498551345642516 bytes (73.5 EB), of which 73496498551345642500 bytes is the image data. (65535x65535x255x16777215 px 32-bit color)
* Currently, Frames and Layers are unimplemented.
