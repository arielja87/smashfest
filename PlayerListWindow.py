#!/usr/bin/env python

from Tkinter import *
import tkFont

# left column contains the list of players (navigable with up/down/left/right)
# right column contains playing modes (1v1, free-for-all) 
class PlayerListWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)

    self.borderColor = kwargs['BORDERCOLOR']
    self.team = kwargs['team']
    self.cn = 'center'
    self.colors = master.colors
    self.players = master.players

    #text box sizing
    self.numH = 1
    self.numW = 15
    self.nameH = int(320*master.scale)
    self.nameW = int(130*master.scale)
    self.modeH = int(100*master.scale)
    self.modeW = int(100*master.scale)

    #fonts
    self.ft = tkFont.Font(family="Times", size=int(24*master.scale), weight=tkFont.BOLD, slant=tkFont.ITALIC)
    self.fn = tkFont.Font(family="Times", size=int(16*master.scale), weight=tkFont.BOLD)
    self.fn2 = tkFont.Font(family="Times", size=int(24*master.scale), weight=tkFont.BOLD)

    if self.team == 1:
      #label text
      self.PlistText = Text(self,height=self.numH,width=self.numW,font=self.ft)
      self.PlistText.tag_configure(self.cn, justify=self.cn)
      self.PlistText.insert(END,'Victim list',self.cn)
      self.PlistText.config(state='disabled',relief=FLAT)

      #player name vars/text
      self.player1 = StringVar()
      self.player2 = StringVar()
      self.player3 = StringVar()
      self.player4 = StringVar()

      self.PnamesBox = Frame(self,height=self.nameH,width=self.nameW,relief=FLAT)
      self.PnamesBox.config(highlightbackground=self.borderColor,highlightcolor=self.borderColor,highlightthickness=3)
      
      self.labels = {}
      for name in self.players:
        self.labels[name] = Text(self.PnamesBox,borderwidth=0,height=1,width=self.numW,font=self.fn,highlightbackground='#fff',highlightcolor='#fff',highlightthickness=2)
        self.labels[name].insert(END,'{:<10}'.format(name))
        if name in master.nickNames.keys():
          text = ' (%s)' % master.nickNames[name]
          self.labels[name].insert(END,text)

        self.labels[name].config(state='disabled')
    else:
      self.modes = ['1 v 1','Teams','Free-for-all']
      self.modeText = Text(self,height=self.numH,width=self.numW,font=self.ft)
      self.modeText.tag_configure(self.cn, justify=self.cn)
      self.modeText.insert(END,'Play mode',self.cn)
      self.modeText.config(state='disabled',relief=FLAT)

      self.playMode = StringVar()

      self.PmodeBox = Frame(self,height=self.nameH,width=self.nameW,relief=FLAT)
      self.PmodeBox.config(highlightbackground=self.borderColor,highlightcolor=self.borderColor,highlightthickness=3)

      self.labels = {}
      for mode in self.modes:
        self.labels[mode] = Text(self.PmodeBox,borderwidth=0,height=1,width=self.numW,font=self.fn,highlightbackground='#fff',highlightcolor='#fff',highlightthickness=2)
        self.labels[mode].insert(END,'{0:^{1}}'.format(mode,self.numW))
        self.labels[mode].config(state='disabled')

    self.initUI()

  # un-highlight the players name in the textbox
  def unSetPlayer(self,pNum):
    if pNum == 1:
      obPlayer = self.player1
    elif pNum == 2:
      obPlayer = self.player2
    elif pNum == 3:
      obPlayer = self.player3
    else:
      obPlayer = self.player4
      
    self.labels[obPlayer.get()].config(highlightbackground='#fff')

  # assign player names to P1/P2/P3/P4
  # if changing P1 from 'Brett' to 'Josh', remove highlight first (i.e. erase)
  # if P3 didn't exist, and now is assigned to 'Allen' no 'erase'  
  def setPlayer(self,pNum,player,erase=True):
    if pNum == 1:
      obPlayer = self.player1
      color = self.colors['p1red']
    elif pNum == 2:
      obPlayer = self.player2
      color = self.colors['p3yellow']
    elif pNum == 3:
      obPlayer = self.player3
      color = self.colors['p2purple']
    else:
      obPlayer = self.player4
      color = self.colors['p4green']

    if erase:
      self.labels[obPlayer.get()].config(highlightbackground='#fff')
    self.labels[player].config(highlightbackground=color)
    obPlayer.set(player)

    # ra = self.labels[player].tag_ranges('pnum')
    # if ra:
    #   self.labels[player].delete(ra[0],ra[1])

    # te = 'P%s' % str(pNum)
    # self.labels[player].insert(self.numW-2,te)

  def setMode(self,mode):
    self.labels[self.playMode.get()].config(highlightbackground='#fff')
    self.labels[mode].config(highlightbackground='#000')
    self.playMode.set(mode)

  def initUI(self):
    #actually place and arrange all the part
    self.grid_propagate(False)
    if self.team == 1:
      self.PlistText.pack(side=TOP)
      self.PnamesBox.pack(side=TOP)
      for name in sorted(self.players):
        self.labels[name].pack(side=TOP)
    else:
      self.modeText.pack(side=TOP)
      self.PmodeBox.pack(side=TOP)
      for mode in self.modes:
        self.labels[mode].pack(side=TOP)