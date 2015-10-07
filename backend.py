import wave
import struct


class yogesh():
	def __init__(self,filename):
		self.paramater=0
		self.noofframe=0
		x=wave.open(filename,'r')
		self.paramater=x.getparams()
		print 'new object :',self.paramater
		self.noofframe=x.getnframes()
		wavedata=x.readframes(self.noofframe)
		newtuple= struct.unpack("%ih"%(self.paramater[0]*self.noofframe) ,wavedata)
		self.newlist=list(newtuple)
#	if 'a' in d.keys():
		
		#newlist=amplitudechange(newlist,action['a'])
		#print 'a=',action['a']
#	if 't' in d.keys():
#		newlist=timeshift(newlist,action['t'])
#		print 't=',action['t']
#	if 'r' in d.keys():
#		newlist=timereverse(newlist)
#		print 'reversing'
	def write(self,output):
		print "writing file"
		newwave=struct.pack("%ih"%(self.paramater[0]*self.noofframe),*self.newlist);
		y=wave.open(output,'w')
		y.setparams(self.paramater)
		y.writeframes(newwave)
		y.close()
	def mix(self,other):
		print "mixing file"
		xxx=max(len(self.newlist),len(other.newlist))
		l1=len(self.newlist)
		l2=len(other.newlist)
		newlist=[]
		mmax=[255,32767]
		mmin=[0,-32768]
		if self.paramater[1]==2:
			for i in range(xxx):
				temp=0
				if(i<l1):
					temp+=self.newlist[i]
				if(i<l2):
					temp+=other.newlist[i]
				if temp>mmax[1]:
					temp=mmax[1]
				elif temp<mmin[1]:
					temp=mmin[1]
				newlist.append(temp)
		else:
			for i in range(len(self.newlist)):
				self.newlist[i]-=128;
			for i in range(len(other.newlist)):
				other.newlist[i]-=128;
			for i in range(xxx):
				temp=0
				if(i<l1):
					temp+=self.newlist[i]
				if(i<l2):
					temp+=other.newlist[i]
				if temp>127:
					temp=127
				elif temp<-128:
					temp=-128
				newlist.append(temp+128) 	
		print self.paramater[0]
		self.newlist=newlist
		self.noofframe=xxx/self.paramater[0]
#		newwave=struct.pack("%ih"%(xxx),*newlist);
#		y=wave.open('mix.wav','w')
#		y.setparams(self.paramater)
#		y.writeframes(newwave)
#		y.close()
	def timescale(self,scale):
		print "time scalechange"
		new=[]
		if scale==1:
			return
		i=0.0;
		while(i*scale<len(self.newlist)):
			if int(i*scale)==i*scale:
				new.append(self.newlist[int(i*scale)])
			else:
				new.append(0)
			i=i+1;
		self.newlist=new
		self.noofframe=len(new)/self.paramater[0]			
	def modulation(self,other):
		print "modulating file"
		xxx=max(len(self.newlist),len(other.newlist))
		l1=len(self.newlist)
		l2=len(other.newlist)
		newlist=[]
		mmax=[255,32767]
		mmin=[0,-32768]
		if self.paramater[1]==2:
			for i in range(xxx):
				temp=0
				if(i<l1):
					if(i<l2):
						temp=self.newlist[i]*other.newlist[i]
				if temp>mmax[1]:
					temp=mmax[1]
				elif temp<mmin[1]:
					temp=mmin[1]
				newlist.append(temp)
		else:
			for i in range(len(self.newlist)):
				self.newlist[i]-=128;
			for i in range(len(other.newlist)):
				other.newlist[i]-=128;
			for i in range(xxx):
				temp=0
				if(i<l1):
					if(i<l2):
						temp=self.newlist[i]*other.newlist[i]
				if temp>127:
					temp=127
				elif temp<-128:
					temp=-128
				newlist.append(temp+128) 	
		print self.paramater[0]
		self.newlist=newlist
		self.noofframe=xxx/self.paramater[0]
#		newwave=struct.pack("%ih"%(xxx),*newlist);
#		y=wave.open('modulation.wav','w')
#		y.setparams(self.paramater)
#		y.writeframes(newwave)
#		y.close()

def amplitudechange(self,factor):
	#x=wave.open(filename,'r')
	#paramater=x.getparams()
	#noofframe=x.getnframes()
	#print paramater,'\n',noofframe
	#wavedata=x.readframes(noofframe)
	#newtuple= struct.unpack("%ih"%(paramater[0]*noofframe) ,wavedata)
	#newlist=list(newtuple)
	print "amplitude change"
	if factor==1:
		return 
	mmax=[255,32767]
	mmin=[0,-32768]
#	for i in range(100):
#		print newtuple[300000+i],
#	print
	if self.paramater[1]==2:
		for i in range(len(self.newlist)):
			self.newlist[i]=factor*self.newlist[i]
			if self.newlist[i]>mmax[1]:
				self.newlist[i]=mmax[1]
			elif self.newlist[i]<mmin[1]:
				self.newlist[i]=mmin[1]
	else:
		for i in range(len(self.newlist)):
			self.newlist[i]-=128;
		for i in range(self.newlist):
			self.newlist[i]=factor*self.newlist[i]
			if self.newlist[i]>127:
				self.newlist[i]=127
			elif self.newlist[i]<-128:
				self.newlist[i]=-128
		for i in range(self.newlist):
			self.newlist[i]+=128;
#	for i in range(100):
#		print newlist[300000+i],
	return self.newlist;
	#newwave=struct.pack("%ih"%(paramater[0]*noofframe),*newlist);
	#y=wave.open(output,'w')
	#y.setparams(paramater)
	#y.writeframes(newwave)


def timeshift(self,shift):
	#x=wave.open(filename,'r')
	#paramater=x.getparams()
	#noofframe=x.getnframes()
	#print paramater,'\n',noofframe
	#wavedata=x.readframes(noofframe)
	#newtuple= struct.unpack("%ih"%(paramater[0]*noofframe) ,wavedata)
	framewidth=self.paramater[2]*shift*self.paramater[0]
	print "timeshift",framewidth
	if shift==0:
		return
	if framewidth>0:
		new=[]
		print 'shift=',framewidth;
		for i in range(int(framewidth)):
			new.append(0)
		new.extend(self.newlist)
		#for i in newtuple:
		#	newlist.append(i)
	else:
		new=[]
		for i in range(len(self.newlist)):
			if i >= -framewidth:
				new.append(self.newlist[i])
	self.newlist=new;
	
	self.noofframe+=(framewidth/self.paramater[0])
	return self.newlist
	#newwave=struct.pack("%ih"%(paramater[0]*noofframe+framewidth),*newlist);
	#y=wave.open(output,'w')
	#y.setparams(paramater)
	#y.writeframes(newwave)

def timereverse(self):
	#x=wave.open(filename,'r')
	#paramater=x.getparams()
	#noofframe=x.getnframes()
	#print paramater,'\n',noofframe
	#wavedata=x.readframes(noofframe)
	#newtuple= struct.unpack("%ih"%(paramater[0]*noofframe) ,wavedata)
	print "reversing"
	if self.paramater[0]==2:
		even=[]
		odd=[]
		newlist=[]
		for i in range(len(self.newlist)):
			if i%2==0:
				even.append(self.newlist[i])
			else:
				odd.append(self.newlist[i])
		even.reverse()
		odd.reverse()
		for i in range(len(self.newlist)):
			if i%2==0:
				newlist.append(even[i/2])
			else:
				newlist.append(odd[i/2])
		self.newlist=newlist;

	else:
		self.newlist.reverse()
	return newlist
	#newwave=struct.pack("%ih"%(paramater[0]*noofframe),*newlist);
	#y=wave.open(output,'w')
	#y.setparams(paramater)
	#y.writeframes(newwave)

yogesh.amp=amplitudechange
yogesh.shift=timeshift
yogesh.timereverse=timereverse
def debug():
	a=yogesh('./Pirates_of_the_Caribbean_Soundtrack_1080p_ISG_.wav')
	a.timescale(1.5)
	a.write("time.wav")
	#b=yogesh('./pirates_of_the_caribbean_theme_song_on_violin_LIVE.wav')
	#a.mix(b)
	#a.write("aabhas.wav")
#b=yogesh('./pirates_of_the_caribbean_theme_song_on_violin_LIVE.wav')
#a.amp(1)
#a.shift(0)
#a.timereverse()
#a.write('output.wav')
#a.mix(b)
#a.modulation(b)
#amplitudechange('./Pirates_of_the_Caribbean_Soundtrack_1080p_ISG_.wav','output.wav',2)
#timeshift('./Pirates_of_the_Caribbean_Soundtrack_1080p_ISG_.wav','output.wav',-5)
#timereverse('./Pirates_of_the_Caribbean_Soundtrack_1080p_ISG_.wav','output1.wav')
#timereverse('./output1.wav','output.wav')
