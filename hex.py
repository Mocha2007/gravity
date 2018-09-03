filename = input('Filename\n> ')
ha = ''
while 1:
	try:
		print(ha)
	except:
		pass
	current = input('Hex\n> ').lower()
	if current == 'end':
		break
	if current == 'moki':
		ha += ''.join(list(map(chr, [77, 79, 75, 73, 3, 0, 5, 0, 5, 1, 240, 0, 0, 1, 0, 16])))
	else:
		try:
			ha += chr(int('0' + (current[0] if current[0] in 'box' else '') + current[1:], {'b': 2, 'd': 10, 'o': 8, 'x': 16}[current[0]]))
		except:
			print('Invalid Number')
open(filename, "w").write(ha)
