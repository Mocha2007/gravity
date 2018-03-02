import binascii,pygame
from math import ceil
from sys import exit
pygame.init()

loc = 'test3.bmp'#'test1.bmp'

# https://stackoverflow.com/a/34687617/2579798
# Open in binary mode (so you don't read two byte line endings on Windows as one byte)
# and use with statement (always do this to avoid leaked file descriptors, unflushed files)
with open(loc, 'rb') as f:
    # Slurp the whole file and efficiently convert it to hex all at once
    image = binascii.hexlify(f.read())

# create the image array
image = str(image)[2:-1]
ia = []
for i in range(0,len(image),2):#convert to a decimal array OwO
	ia+=[int('0x'+image[i:i+2],16)]

def findsize(bmp):#w,h
	w = bmp[18]+256*bmp[19]+256**2*bmp[20]+256**3*bmp[21]
	h = bmp[22]+256*bmp[23]+256**2*bmp[24]+256**3*bmp[25]
	return w,h

mul = 2
size = findsize(ia)[0]*mul,findsize(ia)[1]*mul
screen = pygame.display.set_mode(size)

def zeromatrix(x,y):
	a = []
	for i in range(x):
		a+=[[0]*y]
	return a

def getpixeldata(bmp):#w,h
	start = bmp[10]+256*bmp[11]+256**2*bmp[12]+256**3*bmp[13]
	imgsize = findsize(bmp)
	ceilingedsize = int(ceil(findsize(bmp)[0]/4)*4),int(ceil(findsize(bmp)[1]/4)*4)
	data = zeromatrix(imgsize[0],imgsize[1])#zeromatrix(ceilingedsize[0],imgsize[1])
	bs = bmp[start:]
	for i in range(0,len(bs),3):
		try:
			tribyte = (bs[i],bs[i+1],bs[i+2])[::-1]
			coord = round(i/3%imgsize[1]),round(i/3//imgsize[1])
			data[coord[0]][coord[1]] = tribyte
		except:print('ERROR loading',coord)
		#print('Reading',coord[::-1])
	return list(map(lambda x:x[::-1],data))#[::-1]

print('Loading image...')
final = getpixeldata(ia)#[::-1]
fsize = findsize(ia)
#disp
print('Rendering image...')
for col in range(fsize[0]):
	for row in range(fsize[1]):
		pixel = final[col][row]
		pygame.draw.rect(screen,pixel,pygame.Rect(col*mul,row*mul,mul,mul))
		pygame.display.flip()
		if pixel==0:input((col,row))
		print('Rendering',pixel,'@',(col,row))

while 1:
	ev = pygame.event.get()
	for event in ev:
		if event.type == pygame.MOUSEBUTTONUP:pass
		elif event.type == pygame.QUIT:
			pygame.quit()
			exit()