# mokiview.py

## Accepted b/px formats:

* 00 (1-bit b/w)
  * 0 = #000000 
  * 1 = #FFFFFF
* 01 - (8-bit RGBA) byte = RRGGBBAA
* 03 - (24-bit color) RR GG BB
* FD (4-bit RGBA) byte = RGBARGBA
* FE (2-bit greyscale)
  * 00 = #000000 
  * 01 = #555555
  * 10 = #AAAAAA
  * 11 = #FFFFFF