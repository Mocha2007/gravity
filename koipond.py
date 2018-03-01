import pygame,random
from time import sleep,time
from math import atan2
from sys import exit

# introverts versus extroverts
party = False
# makes it fish-themed
pond = True
# should objects bounce off wall or go oob
wall = True

#from winsound import PlaySound as play
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)
pygame.mixer.Channel(1).set_volume(.2)
#music
if pond:pygame.mixer.Sound('aquarium.wav').play(-1).set_volume(1)

def play(filename):
	if pygame.mixer.Channel(1).get_queue()==None:pygame.mixer.Channel(1).stop()
	pygame.mixer.Channel(1).queue(pygame.mixer.Sound(filename))
def ding():
	if pond:play('blub.wav')
def splash():
	if pond:play('splash.wav')

rows = 24 if pond else 48
columns = 48 if pond else 96
spritesize = 32 if pond else 16
bspritesize = 16

width = columns*spritesize
height = rows*spritesize
size = width,height
screen = pygame.display.set_mode(size)

black = (0,0,0)
white = (255,255,255)
skyblue = (0,96,192)

dot_red = pygame.image.load("dot_red.png")
dot_blue = pygame.image.load("dot_blue.png")
dot_green = pygame.image.load("dot_green.png")
dot_white = pygame.image.load("dot_white.png")
fish = pygame.image.load("fish_32.png")
afish = pygame.image.load("afish_32.png")

g = 20#gravitational constant
gdisabledist = 16#disable gravity under this distance to prevent shooting, default = 16
animals = 40#objects to simulate
bounceefficiency = .5#velocity fraction retained after bounce
maxv = 5#maximum speed

def bounce(info):
	if not wall:return info
	currentpos = info[1]
	currentvel = info[2]
	for i in range(len(currentpos)):
		currentpos[i]+=currentvel[i]
		if currentpos[i]<=0:
			currentpos[i]=0
			currentvel[i]=-currentvel[i]*bounceefficiency
			ding()
		elif currentpos[i]>=size[i]-spritesize:
			currentpos[i]=size[i]-spritesize
			currentvel[i]=-currentvel[i]*bounceefficiency
			ding()
	return [info[0],currentpos,currentvel]+info[3:]

def robj():
	pos = [fish if pond else dot_red,[random.randint(0,width),random.randint(0,height)],[0,0],1]
	neg = [afish if pond else dot_blue,[random.randint(0,width),random.randint(0,height)],[0,0],-1]#set to -1 for craziness
	neu = [dot_green,[random.randint(0,width),random.randint(0,height)],[0,0],0]
	base = [dot_red,[random.randint(0,width),random.randint(0,height)],[0,0]]
	return random.choice([pos,pos,neg]) if party else pos#random.choice([pos,neg,neu])#base + [rabsunit()]

def rabsunit():
	return random.random()*2-1

def grav(objlist):
	o = objlist
	for i in range(len(o)):#for each object
		#change pos
		for j in range(len(o[i][1])):#for each spatial dimension
			objlist[i][1][j]+=o[i][2][j]#increase by velocity
		#change vel
		for j in range(len(o)):#for each other obj
			absdistance = ((o[j][1][0]-o[i][1][0])**2+(o[j][1][1]-o[i][1][1])**2)**.5
			if party:
				absacceleration = 0 if absdistance==0 else g*o[i][3]/(absdistance)**2
			else:
				absacceleration = 0 if absdistance==0 else g*o[j][3]/(absdistance)**2
			for k in range(len(o[i][2])):#for each velocity dimension, a = M/r^2
				dimdistance = o[j][1][k]-o[i][1][k]
				dimacceleration = 0 if absdistance<gdisabledist else dimdistance*absacceleration/absdistance
				objlist[i][2][k]+=dimacceleration#increase by acceleration
				if objlist[i][2][k]>maxv:objlist[i][2][k]=maxv#limit to maxv
				elif objlist[i][2][k]<-maxv:objlist[i][2][k]=-maxv#limit to -maxv
	return objlist

def mass(o):
	return sum(map(lambda x:x[3],o))

def barycenter(objlist):
	t = mass(objlist)
	x = sum(map(lambda x:x[3]/t*x[1][0],objlist))
	y = sum(map(lambda x:x[3]/t*x[1][1],objlist))
	return x,y

#setup
objects = []
for i in range(animals):
	objects+=[robj()]
#main
b=0,0
fps=120
while 1:
	oldb=b
	start = time()
	#objects = minimize(objects)
	screen.fill(skyblue if pond else black)#disable for trails
	bm=mass(objects)
	for i in objects:
		i = bounce(i)
		currentobj = pygame.transform.rotate(i[0],atan2(-i[2][1],i[2][0])*57.29577951308232) if pond else i[0]
		screen.blit(currentobj,(i[1][0],i[1][1]))
	#barycenter display
	b = barycenter(objects)
	screen.blit(dot_white,b)
	bv = b[0]-oldb[0],b[1]-oldb[1]
	bv2 = (bv[0]**2+bv[1]**2)**.5,round(atan2(-bv[1],bv[0])*57.29577951308232)%360
	#barycenter info
	binfo = ['Barycenter M='+str(bm),
			'('+str(int(b[0]-width/2))+','+str(int(height/2-b[1]))+')',
			'('+str(round(fps*bv[0]))+' px/s,'+str(round(-fps*bv[1]))+' px/s)',
			'('+str(bv2[1])+'\xb0 @ '+str(round(fps*bv2[0]))+' px/s)'
			]
	for i in range(len(binfo)):
		label = myfont.render(binfo[i],1,white)
		screen.blit(label,(b[0]+16,b[1]+16*(i+1)))
	#barycenter velocity vector
	pygame.draw.aaline(screen,white,(b[0]+bspritesize/2,b[1]+bspritesize/2),(b[0]+bv[0]*500+bspritesize/2,b[1]+bv[1]*500+bspritesize/2),1)
	#display
	pygame.display.flip()
	objects = grav(objects)
	fps=int(1/(time()-start))
	print(fps,'FPS')
	br=0
	# get all events
	ev = pygame.event.get()
	# proceed events
	for event in ev:
		# handle MOUSEBUTTONUP
		if event.type == pygame.MOUSEBUTTONUP:
			print('NO TOUCHIE','DA FISHIES' if pond else '')
			splash()
		elif event.type == pygame.QUIT:
			pygame.quit()
			exit()