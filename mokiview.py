import binascii,pygame
from sys import exit
from os import stat
pygame.init()

def findsize(bmp):#w,h
	w = bmp[6]+256*bmp[5]
	h = bmp[8]+256*bmp[7]
	return w,h

def findstart(bmp):
	return bmp[15]+256*bmp[14]

def findmode(bmp):
	return bmp[4]

def zeromatrix(x,y):
	a = []
	for i in range(x):
		a+=[[0]*y]
	return a

def getpixeldata(bmp):#w,h
	mode = findmode(bmp)
	start = findstart(bmp)
	imgsize = findsize(bmp)
	data = zeromatrix(imgsize[0],imgsize[1])
	bs = bmp[start:]
	if mode==0:
		for i in range(len(bs)):
			byte = bs[i]
			try:
				for j in range(8):#for each bit
					bit = int('{0:08b}'.format(byte)[j])
					tribyte = (255,255,255) if bit else (0,0,0)
					coord = (8*i+j)%imgsize[1],round((8*i+j)//imgsize[1])
					data[coord[0]][coord[1]] = tribyte
					#print(coord,'=',tribyte)
			except:print('ERROR loading',coord)
	elif mode==1:
		for i in range(len(bs)):
			byte = '{0:08b}'.format(bs[i])
			try:
				tribyte = int(byte[0])*128+int(byte[1])*64,int(byte[2])*128+int(byte[3])*64,int(byte[4])*128+int(byte[5])*64
				coord = i%imgsize[1],round(i//imgsize[1])
				data[coord[1]][coord[0]] = tribyte
				#print(coord,'=',tribyte)
			except:print('ERROR loading',coord)
	elif mode==3:
		for i in range(0,len(bs),3):
			try:
				tribyte = (bs[i],bs[i+1],bs[i+2])
				coord = round(i/3%imgsize[1]),round(i/3//imgsize[1])
				data[coord[0]][coord[1]] = tribyte
			except:print('ERROR loading',coord)
	else:print('Unrecognized mode')
	return data

while 1:#safety net
	loc = input('Location\n> ')# mokiview.py or test.moki
	try:
		if stat(loc).st_size<2**20:
			# https://stackoverflow.com/a/34687617/2579798
			with open(loc,'rb') as f:image=binascii.hexlify(f.read())

			# create the image array
			image = str(image)[2:-1]
			ia = []
			for i in range(0,len(image),2):#convert to a decimal array OwO
				ia+=[int('0x'+image[i:i+2],16)]

			mul = max(int(512/max(findsize(ia))),1)
			size = int(findsize(ia)[0]*mul),int(findsize(ia)[1]*mul)
			if size[0]<2048>size[1]:
				screen = pygame.display.set_mode(size)
				break
			else:print('Image too Large!')
		else:print('File too Large!')
	except FileNotFoundError:print('File does not exist!')

print('Loading image...')
final = getpixeldata(ia)#[::-1]
fsize = findsize(ia)

#disp
print('Rendering image...')
for col in range(fsize[0]):
	for row in range(fsize[1]):
		pixel = final[col][row]
		pygame.draw.rect(screen,pixel,pygame.Rect(col*mul,row*mul,mul,mul))
		if pixel==0:print('ERROR rendering',(col,row))
pygame.display.flip()

#events
while 1:
	ev = pygame.event.get()
	for event in ev:
		if event.type == pygame.MOUSEBUTTONUP:pass
		elif event.type == pygame.QUIT:
			pygame.quit()
			exit()