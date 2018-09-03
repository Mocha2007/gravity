def twobit(colorstring):
	'''w = white, s = silver, g = grey, b = black'''
	return int('0b'+colorstring.replace('w', '11').replace('s', '10').replace('g', '01').replace('b', '00'), 2)

while 1:
	try:
		print(twobit(input('s?\n> ')))
	except:
		pass