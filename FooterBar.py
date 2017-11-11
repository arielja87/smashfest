#!/usr/bin/env python

from Tkinter import *  
import tkFont

class FooterBar(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master,**di)

    self.scale = master.scale
    self.fn = tkFont.Font(family="Times", size=int(14*self.scale))
    self.label = Label(self)
    self.statBar1 = StatusBar(self)
    self.statBar2 = StatusBar(self)
    self.statBar3 = StatusBar(self)

    self.label.grid(row=0,column=0,sticky=N+E+W+S)
    self.statBar1.grid(row=0,column=1,sticky=N+E+W+S)
    self.statBar2.grid(row=0,column=2,sticky=N+E+W+S)
    self.statBar3.grid(row=0,column=3,sticky=N+E+W+S)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=4)
    self.columnconfigure(2, weight=4)
    self.columnconfigure(3, weight=4)

    self.label.config(text='Recents:',font=self.fn)

  def get(self,toggle):
    if toggle == 2:
      t = self.statBar3.label.cget('text')
    elif toggle == 1:
      t = self.statBar2.label.cget('text')
    else:
      t = self.statBar1.label.cget('text')

    return t

  def set(self, format, args,toggle):
    if toggle == 2:
      self.statBar3.set(format, args)
    elif toggle == 1:
      self.statBar2.set(format, args)
    else:
      self.statBar1.set(format, args)

  def update(self,toggle):
    if toggle == 2:
      self.statBar3.update()
    elif toggle == 1:
      self.statBar2.update()
    else:
      self.statBar1.update()

class StatusBar(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master,di)

    self.wrap = master.scale*420
    self.fn = tkFont.Font(family="Times", size=int(12*master.scale))
    self.label = Label(self, bd=1, height=3, relief=SUNKEN, anchor=CENTER,font=self.fn,wraplength=self.wrap)
    self.label.pack(fill=X)

  def update(self):
    self.label.update_idletasks()

  def set(self, format, *args):
    self.clear()
    self.label.config(text=format % args, anchor=CENTER)
    self.label.update_idletasks()

  def clear(self):
    self.label.config(text="")
    self.label.update_idletasks()