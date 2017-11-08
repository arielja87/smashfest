#!/usr/bin/env python

from Tkinter import *  
import tkFont

class PlayerPopup(Tk):
  def __init__(self, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in dir(Tk)}
    Tk.__init__(self, *args, **di)

    self.fn = tkFont.Font(family='Times',size=20)
    self.label1 = Label(self,font=self.fn)
    self.label2 = Label(self,font=self.fn)
    self.regulars = Listbox(self,font=self.fn)
    self.playing = Listbox(self,font=self.fn)
    self.entry = Entry(self,font=self.fn)

    self.label1.config(text='Regulars:',font=self.fn)
    self.label2.config(text='Confirmed:',font=self.fn)
    for name in ['Allen','Brett','Joe','Josh','Ryan','Sean','Torben']:
      self.regulars.insert(END,name)

    self.initUI()

  def initUI(self):
    self.label1.grid(row=0,column=0,sticky=N+S+E+W)
    self.label2.grid(row=0,column=1,sticky=N+S+E+W)
    self.regulars.grid(row=1,column=0,sticky=N+S+E+W)
    self.playing.grid(row=1,column=1,sticky=N+S+E+W)
    self.entry.grid(row=2,column=0,columnspan=2,sticky=N+S+E+W)

  def addName(self,event=''):
    nameToAdd = self.entry.get()
    self.entry.delete(0,END)
    self.regulars.insert(END,name)