#!/usr/bin/env python

from Tkinter import *
import tkFont

# this frame consists of a label ('Player 1'), a canvas w/ a question mark (where character images go),
# and a text box with the player name
class PlayerHeadWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)

    self.pnum = kwargs['PNUM']
    self.faces = kwargs['FACES']
    self.borderColor = kwargs['BORDERCOLOR']

    self.cn = 'center'
    
    #text box sizing
    self.numH = 1
    self.numW = 16
    self.nameH = 1
    self.nameW = 10

    #canvas sizing, placement
    self.px = int(50*master.scale)
    self.py = int(40*master.scale)
    self.pW = self.px*2
    self.pH = self.py*2

    self.ft = tkFont.Font(family="Times", size=int(24*master.scale), weight=tkFont.BOLD, slant=tkFont.ITALIC)
    self.fn = tkFont.Font(family="Times", size=int(28*master.scale), weight=tkFont.BOLD)

    #player 1/2 text
    self.PnumText = Text(self,height=self.numH,width=self.numW,font=self.ft)
    self.PnumText.tag_configure(self.cn, justify=self.cn)
    self.PnumText.insert(END,'Player %d' % self.pnum,self.cn)
    self.PnumText.config(state='disabled',relief=FLAT)

    #player name text
    self.currName = StringVar()
    self.currName.set('')
    self.PnameText = Text(self,height=self.nameH,width=self.nameW,font=self.fn)
    self.PnameText.config(highlightbackground=self.borderColor,highlightcolor=self.borderColor,highlightthickness=3)

    #character face/? image
    self.tempChar = StringVar()
    self.tempChar.set('')
    self.Pface = Canvas(self,height=self.pH,width=self.pW,bg='#fff')
    self.Pface.create_image(self.px,self.py,image=self.faces['QuestionMark'],tags='perm')
    self.Pface.config(highlightthickness=0)

    #if pnum in [3,4]:

    self.initUI()
      
  def initUI(self):
    #actually place and arrange all the part
    self.grid_propagate(False)
    self.PnumText.pack(side=TOP)
    self.PnameText.pack(side=TOP)
    self.Pface.pack(side=TOP)

  # remove that player from the text box
  def kickPlayer(self):
    self.PnameText.delete(1.0,END)
    self.currName.set('')

  # add a player to the text box
  def pickPlayer(self, name):
      #delete old name and put in new name
      self.kickPlayer()
      self.currName.set(name)
      self.PnameText.insert(END,name,self.cn)
      self.PnameText.tag_configure(self.cn, justify=self.cn)

  # remove the character image from over the question mark
  def kickCharacter(self,mode='hard'):
    if mode == 'hard' or not(self.tempChar.get()):
      self.Pface.delete('temp')
      self.tempChar.set('')

  # add the character image
  def pickCharacter(self, charac,mode='soft'):
      #delete old face picture and put in new one
      self.kickCharacter()
      if mode == 'hard':
        self.tempChar.set(charac)
      self.Pface.create_image(self.px,self.py,image=self.faces[charac],tags='temp')
      self.Pface.tag_raise('temp')