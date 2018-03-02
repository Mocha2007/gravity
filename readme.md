# mokiview.py

## Accepted b/px formats:

* 00 (1-bit b/w)
  * 0 = #000000 
  * 1 = #FFFFFF
* 01 - (8-bit RGBA) byte = RRGGBBAA
* 03 - (24-bit color) RR GG BB
* 04 - (32-bit color) RR GG BB AA
* F0 (unimplemented) (24-bit vectorized RGB) 12-byte: ID RR GG BB X1__ Y1__ X2__ Y2__
* FD (4-bit RGBA) byte = RGBARGBA
* FE (2-bit greyscale)
  * 00 = #000000 
  * 01 = #555555
  * 10 = #AAAAAA
  * 11 = #FFFFFF
* FF - (unimplemented) Custom Palette, stored in header as RR GG BB RR GG BB ... etc, bitness automatically determined