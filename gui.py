#!/usr/bin/env python
import os
import gtk
import pygtk
import backend
import play
import signal
import sys
import record_sound
class Mixer:
	def __init__(self):
		self.window=gtk.Window(gtk.WINDOW_TOPLEVEL) 
		self.window.set_title("WAVE MIXER") 
		self.window.connect("destroy", self.destroy)
		self.window.set_size_request(1000,800) 
		self.fixed=gtk.Fixed()  
		self.window.add(self.fixed)
		self.fixed.show()
		self.timerevlist=[]
		self.modlist=[]
		self.mixlist=[]
		self.playing=[-1]*3
		self.pause=[-1]*3
		self.processpid=0;
		filelist=[-1]*3
		self.mixspause=-1;
		self.mixspid=-1;
		self.modspause=-1;
		self.modspid=-1;
		for i in range(3):
			checkbutton1 = gtk.CheckButton("Time Reversal")
			checkbutton2 = gtk.CheckButton("Select for Modulation")
			checkbutton3 = gtk.CheckButton("Select for Mix")
			self.fixed.put(checkbutton1,100+250*i,330)
			self.fixed.put(checkbutton2,100+250*i,360)
			self.fixed.put(checkbutton3,100+250*i,390)
			self.timerevlist.append(checkbutton1)
			self.modlist.append(checkbutton2)
			self.mixlist.append(checkbutton3)
	#scale for amplitude
		self.amplist=[]
		for i in range(3):	
			scale=gtk.HScale() 
			scale.set_range(0,10) 
			scale.set_value(1)
			scale.set_increments(0.5, 1) 
			scale.set_digits(1) 	
			scale.set_size_request(160, 45) 
			self.fixed.put(scale,100+i*250,130)
			self.amplist.append(scale)
	#scale for time Shift
		self.timeshiftlist=[]
		for i in range(3):	
			scale=gtk.HScale() 
			scale.set_range(-30,30) 
			scale.set_increments(1, 1) 
			scale.set_digits(0) 	
			scale.set_size_request(160, 45) 
			self.fixed.put(scale,100+i*250,200)
			self.timeshiftlist.append(scale)
	#scale for tCONTscaling
		self.timescalelist=[]
		for i in range(3):	
			scale=gtk.HScale() 
			scale.set_range(0.125,10) 
			scale.set_value(1)
			scale.set_increments(0.125, 0.125) 
			scale.set_digits(3) 
			scale.set_size_request(160, 45) 
			self.fixed.put(scale,100+i*250,270)
			self.timescalelist.append(scale)
		#filechooser
		self.filechooser=[]
		for i in range(3):
			filechooserbutton = gtk.FileChooserButton("Select A File", None)
			filechooserbutton.connect("file-set", self.file_selected,i)      
			filechooserbutton.set_width_chars(10)
			self.fixed.put(filechooserbutton,100+250*i,50)
			self.filechooser.append(filechooserbutton)
		
		for i in range(3):
			label = gtk.Label("Select File")
			self.fixed.put(label,120+i*250,30)
		for i in range(3):
			label = gtk.Label("Amplitude:")
			self.fixed.put(label,100+i*250,110)
		for i in range(3):
			label = gtk.Label("Time Shift:")
			self.fixed.put(label,100+i*250,180)
		for i in range(3):
			label = gtk.Label("Time Scaling:")
			self.fixed.put(label,100+i*250,250)
		self.button=[];
		for i in range(3):
			but=gtk.Button("Start")
			but1=gtk.Button("Play/Pause")
			but2=gtk.Button("Stop")
			self.button.append(but)
			self.fixed.put(but,100+i*250,500)
			self.fixed.put(but2,240+i*250,500)
			self.fixed.put(but1,150+i*250,500)
			but.connect("clicked",self.callback,i)
			but2.connect("clicked",self.stopback,i)
			but1.connect("clicked",self.pauseback,i)
		but=gtk.Button("Mix and Play")
		
		but3=gtk.Button("Stop Mix")
		but2=gtk.Button("Stop Modulation")
		but1=gtk.Button("Modulate and Play")
		but.connect("clicked",self.mixback)
		but1.connect("clicked",self.modback)
		but2.connect("clicked",self.modstop)
		but3.connect("clicked",self.mixstop)
		self.fixed.put(but,100,600-50)
		self.fixed.put(but3,100,600-20)
		self.fixed.put(but1,200,600-50)
		self.fixed.put(but2,200,600-20)
		recordbut=gtk.Button("Record")
		recordbut.connect("clicked",self.recordstart)
		self.fixed.put(recordbut,400,550)
		#recordbut=gtk.Button("Play")
		#recordbut.connect("clicked",self.recordplay)
		self.recordingplay=-1;
		self.recordpid=-1;
		#self.fixed.put(recordbut,480,550)
		self.window.show_all();
	def recordstart(self,button):
		print 'recording'
		record_sound.record_to_file("record.wav")
		print 'stoped'
		pass
	def recordplay(self,button):
		if self.recordpid==-1:
			pid=os.fork()
			if pid==0:
				play.play("record.wav")
				self.recordpid=-1;
				self.recordingplay=-1;
				sys.exit(0)
			else:
				self.recordpid=pid;
				self.recordingplay=1;

	def mixstop(self,button):
		if self.mixspid!=-1:
			os.kill(self.mixspid,signal.SIGSTOP);
			self.mixspid=-1;
			self.mixspause=-1
	def modstop(self,button):
		if self.modspid!=-1:
			os.kill(self.modspid,signal.SIGSTOP);
			self.modspid=-1;
			self.modspause=-1
	def mixback(self,button):
		if self.mixspause!=-1:
			if self.mixspause==0:
				os.kill(self.mixspid,signal.SIGTSTP);
				self.mixspause=1;
			else:
				os.kill(self.mixspid,signal.SIGCONT);
				self.mixspause=0;
			return 
		listfile=[]
		for i in range(3):
			if self.mixlist[i].get_active():
				filename=self.filechooser[i].get_filename()
				if not  filename:
					print "give the filename please"
					return 
				listfile.append(i)
		if len(listfile)==0:
			return;
		new=[]
		for i in listfile:
			newobj=backend.yogesh(self.filechooser[i].get_filename())
			print self.filechooser[i].get_filename()
			newobj.amp(self.amplist[i].get_value())
			newobj.shift(self.timeshiftlist[i].get_value())
			newobj.timescale(self.timescalelist[i].get_value())
			if self.timerevlist[i].get_active():
				newobj.timereverse()
			new.append(newobj)
		for i in range(len(new)-1):
			print 'mix with 0 and ',i+1
			new[0].mix(new[i+1])
		new[0].write("mix.wav")
		pid=os.fork()
		if pid==0:
			play.play("mix.wav")
			self.mixspid=-1
			self.mixspause=-1
			sys.exit(0)
		else:
			self.mixspause=0;
			self.mixspid=pid;
	def modback(self,button):
		if self.modspause!=-1:
			if self.modspause==0:
				os.kill(self.modspid,signal.SIGTSTP);
				self.modspause=1;
			else:
				os.kill(self.modspid,signal.SIGCONT);
				self.modspause=0;
			return 
		listfile=[]
		for i in range(3):
			if self.modlist[i].get_active():
				filename=self.filechooser[i].get_filename()
				if not  filename:
					print "give the filename please"
					return 
				listfile.append(i)
		if len(listfile)==0:
			return;
		new=[]
		for i in listfile:
			newobj=backend.yogesh(self.filechooser[i].get_filename())
			print self.filechooser[i].get_filename()
			newobj.amp(self.amplist[i].get_value())
			newobj.shift(self.timeshiftlist[i].get_value())
			newobj.timescale(self.timescalelist[i].get_value())
			if self.timerevlist[i].get_active():
				newobj.timereverse()
			new.append(newobj)
		for i in range(len(new)-1):
			print 'mod with 0 and ',i+1
			new[0].modulation(new[i+1])
		new[0].write("mod.wav")
		pid=os.fork()
		if pid==0:
			play.play("mod.wav")
			self.modspause=-1;
			self.modspid=-1;
			sys.exit(0)
			return 0;
		else:
			self.modspause=0;
			self.modspid=pid;

	def pauseback(self,button,i):
		if self.playing[i]!=-1:
			print "DEBUG=",self.pause[i]
			if self.pause[i]==0:
				os.kill(self.playing[i],signal.SIGTSTP);
				self.pause[i]=1;
			else:
				os.kill(self.playing[i],signal.SIGCONT);
				self.pause[i]=0;
	def stopback(self,button,i):
		if self.playing[i]!=-1:
			os.kill(self.playing[i],signal.SIGSTOP);
			self.playing[i]=-1
			self.pause[i]=-1
	def callback(self,button,i):
		print i,"was cliked\n"
		if self.playing[i]!=-1:
			return
		#print   self.filechooser[i].get_filename()		
		filename=self.filechooser[i].get_filename()		
		self.playing[i]=filename
		#print self.amplist[i].get_value()
		amplitudevalue = self.amplist[i].get_value()
		print self.timeshiftlist[i].get_value()
		
		timeshiftvalue=self.timeshiftlist[i].get_value()
#		print self.timescalelist[i].get_value()
		timescalevalue= self.timescalelist[i].get_value()
	#	print self.timerevlist[i].get_active()
		reverseornot=self.timerevlist[i].get_active()
		if filename:
			newob=backend.yogesh(filename);
			newob.amp(amplitudevalue)
			newob.shift(int(timeshiftvalue))
			newob.timescale(timescalevalue)
			if reverseornot :
				newob.timereverse()
			newob.write("final.wav")
			pid=os.fork()
			self.processpid=pid;
			if pid==0:
				print "over"
				play.play("final.wav")
				self.playing[i]=-1
				self.pause[i]=-1
				sys.exit(0)
			else:
				print "over"
				self.playing[i]=pid;
				self.pause[i]=0
	def file_selected(self, widget,i):
		print "Selected filepath: %s" % widget.get_filename()
	def destroy(self,widget,data=None):
		print 'aa';
		for i in range(3):
			if self.playing[i]!=-1:
				os.kill(self.playing[i],signal.SIGSTOP)
		if self.modspid!=-1:
			os.kill(self.modspid,signal.SIGSTOP)
		if self.mixspid!=-1:
			os.kill(self.mixspid,signal.SIGSTOP)

		gtk.main_quit()
Mixer()
gtk.main()
