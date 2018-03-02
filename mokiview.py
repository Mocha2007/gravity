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

def zeromatrix(size):
	a = []
	for i in range(size[1]):
		a+=[[0]*size[0]]
	return a

def getpixeldata(bmp):#w,h
	mode = findmode(bmp)
	start = findstart(bmp)
	imgsize = findsize(bmp)
	data = zeromatrix(imgsize)
	bs = bmp[start:]
	if mode==0:
		for i in range(len(bs)):
			byte = bs[i]
			try:
				for j in range(8):#for each bit
					bit = int('{0:08b}'.format(byte)[j])
					tribyte = (255,255,255) if bit else (0,0,0)
					coord = (8*i+j)%imgsize[0],round((8*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
					#print(coord,'=',tribyte)
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==1:
		for i in range(len(bs)):
			byte = '{0:08b}'.format(bs[i])
			try:
				tribyte = int(byte[0])*170+int(byte[1])*85,int(byte[2])*170+int(byte[3])*85,int(byte[4])*170+int(byte[5])*85
				coord = i%imgsize[0],round(i//imgsize[0])
				data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==2:
		for i in range(0,len(bs),2):
			byte = '{0:08b}'.format(bs[i:i+2])
			try:
				tribyte = int('0b'+byte[0:4],2)*17,int('0b'+byte[4:8],2)*17,int('0b'+byte[8:12],2)*17
				coord = round(i/2%imgsize[0]),round(i/2//imgsize[0])
				data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==3:
		for i in range(0,len(bs),3):
			try:
				tribyte = (bs[i],bs[i+1],bs[i+2])
				coord = round(i/3%imgsize[0]),round(i/3//imgsize[0])
				data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==4:
		for i in range(0,len(bs),4):
			try:
				tribyte = (bs[i],bs[i+1],bs[i+2])
				coord = round(i/4%imgsize[0]),round(i/4//imgsize[0])
				data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==224:
		for i in range(len(bs)):
			byte = '{0:08b}'.format(bs[i])
			try:
				for j in range(2):#for every 4 bits
					bits = int('0b'+byte[4*j:4*j+4],2)
					tribyte = [(0,0,0),(4,6,19),(36,64,88),(65,75,41),(77,76,72),(115,123,134),(120,130,155),(124,109,76),(133,121,109),(144,135,130),(154,136,96),(171,132,101),(192,193,177),(198,210,198),(238,234,231),(255,255,255)][bits]
					coord = (2*i+j)%imgsize[0],round((2*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==225:
		for i in range(len(bs)):
			byte = bs[i]
			try:
				for j in range(4):#for every 2 bits
					bit = int('0b'+'{0:08b}'.format(byte)[2*j:2*j+2],2)
					tribyte = [(84,79,75),(167,104,86),(196,176,169),(247,129,91)][bit]
					coord = (4*i+j)%imgsize[0],round((4*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
	elif mode==226:
		for i in range(len(bs)):
			byte = bs[i]
			try:
				for j in range(4):#for every 2 bits
					bit = int('0b'+'{0:08b}'.format(byte)[2*j:2*j+2],2)
					tribyte = [(24,40,144),(56,96,192),(128,96,192),(144,16,176)][bit]
					coord = (4*i+j)%imgsize[0],round((4*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==251:
		for i in range(0,len(bs),3):
			byte = '{0:08b}'.format(bs[i:i+3])
			try:
				for j in range(4):#for every 6 bits in 24
					bits = byte[6*j:6*j+6]
					tribyte = (int('0b'+bits[0],2)*85,int('0b'+bits[1],2)*85,int('0b'+bits[2],2)*85)
					coord = (2*i+j)%imgsize[0],round((2*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==252:
		for i in range(len(bs)):
			byte = '{0:08b}'.format(bs[i])
			try:
				for j in range(2):#for every 4 bits
					bits = byte[4*j:4*j+4]
					tribyte = (int('0b'+bits[0],2)*255,int('0b'+bits[1],2)*255,int('0b'+bits[2],2)*255)
					coord = (2*i+j)%imgsize[0],round((2*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==253:
		for i in range(0,len(bs),3):
			byte = '{0:08b}'.format(bs[i:i+3])
			try:
				for j in range(8):#for every 3 bits in 24
					bits = byte[3*j:3*j+3]
					tribyte = (int('0b'+bits[0],2)*255,int('0b'+bits[1],2)*255,int('0b'+bits[2],2)*255)
					coord = (2*i+j)%imgsize[0],round((2*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	elif mode==254:
		for i in range(len(bs)):
			byte = bs[i]
			try:
				for j in range(4):#for every 2 bits
					bit = int('0b'+'{0:08b}'.format(byte)[2*j:2*j+2],2)
					tribyte = (255,255,255) if bit==3 else ((170,170,170) if bit==2 else ((85,85,85) if bit==1 else (0,0,0)))
					coord = (4*i+j)%imgsize[0],round((4*i+j)//imgsize[0])
					data[coord[1]][coord[0]] = tribyte
			except Exception as e:print('ERROR loading',coord,e)
	else:print('Unrecognized mode')
	return data

while 1:#safety net
	loc = input('Location\n> ')# self-referential.moki
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
final = getpixeldata(ia)
fsize = findsize(ia)

#disp
print('Rendering image...')
for row in range(fsize[1]):
	for col in range(fsize[0]):
		pixel = final[row][col]
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
