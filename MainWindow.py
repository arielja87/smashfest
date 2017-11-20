#!/usr/bin/env python

from __future__ import division
from Tkinter import *  
import tkMessageBox
import os 
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from datetime import datetime

from PlayerHeadWindow import PlayerHeadWindow
from PlayerListWindow import PlayerListWindow
from SelectionWindow import SelectionWindow
from FooterBar import FooterBar
#import PlayerPopup

# main controlling window; (most) everything has this as its parent
class MainWindow(Tk):
  def __init__(self, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in dir(Tk)}
    Tk.__init__(self, *args, **di)

    if 'scaleWindow' in kwargs:
      scaleWindow = kwargs['scaleWindow']
    else:
      scaleWindow = 'medium'

    # Window dimension (pixels)
    self.config(bg='#fff')
    self.w = 1485
    self.h = 690
    
    if scaleWindow == 'large':
      self.scale = 1.2
    elif scaleWindow == 'small':
      self.scale = .9
    elif scaleWindow == 'fit':
      self.scale = self.winfo_screenwidth()*.8/self.w
    else:
      self.scale = 1.
      #self.scale = 1.2
      #self.scale = .9
      #self.scale = self.winfo_screenwidth()*.8/self.w

    self.centerWindow(int(self.w*self.scale),int(self.h*self.scale))
    self.colors = {'p1red':'#f55943','p2purple':'#f5db43','p3yellow':'#5c3ba8','p4green':'#32b755','pListBlue':'#3568a0','pListOrange':'#f5af43'}
    self.dataFileName1v1 = os.path.abspath(os.path.join('.','smashStats.csv'))              # for 1v1 mode or only 2 players selected in Free-for-all mode
    self.dataFileNameFreeForAll = os.path.abspath(os.path.join('.','freeForAllStats.csv'))  # free-for-all mode with 3-4 players
    self.dataFileNameTeams = os.path.abspath(os.path.join('.','teamsStats.csv'))            # for 2v2 mode only
    #self.dataFileName1v1 = os.path.abspath(os.path.join('.','junkStats.csv'))
    #self.dataFileNameFreeForAll = os.path.abspath(os.path.join('.','junkFreeForAllStats.csv'))
    #self.dataFileNameTeams = os.path.abspath(os.path.join('.','junkTeamsStats.csv'))
    self.today = datetime.now()
    self.today = self.today.strftime('%Y%m%d')

    self.title("SMASH")

    self.characters = ["Mario","Luigi","Peach","Bowser","Yoshi","DonkeyKong",
    "DiddyKong","Link","Zelda","Sheik","Ganondorf","ToonLink","Samus",
    "ZeroSuitSamus","Kirby","MetaKnight","KingDedede","Fox","Falco","Wolf",
    "Pikachu","Jigglypuff","Mewtwo","Squirtle","Ivysaur","Charizard","Lucario",
    "CaptainFalcon","Ness","Lucas","IceClimbers","Marth","Roy","Ike",
    "MrGameAndWatch","Pit","Wario","Olimar","RoboticOperatingBuddy","Snake",
    "Sonic",'QuestionMark','Logo']

    #add all the legal stages
    self.stages = ['battlefield','delfinosSecret','hyruleCastle',
    'dreamland','finalDestination','fountainOfDreams','greenHillZone','norfair',
    'pokemonStadium2','smashville','warioLand','yoshisIsland','yoshisStory']

    #players!
    self.players = ['Allen','Atakan','Brett','Claire','Joe','Josh','Sean','Torben']
    self.nickNames = {'Allen':'CharLord','Brett':u'\u00c7o\u00e7k','Claire':'Jing','Joe':u'\u00c7g4y','Josh':u'\u00c7\u00f2\u00ecT','Sean':u'\u00c7uuck','Torben':u'BUTTS'}
    self.avatars = {}  # should add these at some point images to cover the question mark before choosing a character

    #images of character faces and icons
    self.faceImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Faces','%s.gif')) % el).resize((int(80*self.scale),int(56*self.scale)),Image.ANTIALIAS)) for el in self.characters if el != 'Logo'}\


    self.P1 = PlayerHeadWindow(self,PNUM=1,FACES=self.faceImgs,BORDERCOLOR=self.colors['p1red'],bg='#fff')
    self.P2 = PlayerHeadWindow(self,PNUM=2,FACES=self.faceImgs,BORDERCOLOR=self.colors['p3yellow'],bg='#fff')
    self.P3 = PlayerHeadWindow(self,PNUM=3,FACES=self.faceImgs,BORDERCOLOR=self.colors['p2purple'],bg='#fff')
    self.P4 = PlayerHeadWindow(self,PNUM=4,FACES=self.faceImgs,BORDERCOLOR=self.colors['p4green'],bg='#fff')
    self.Ps = PlayerListWindow(self,BORDERCOLOR=self.colors['pListBlue'],bg='#fff',team=1)
    self.Ps2 = PlayerListWindow(self,BORDERCOLOR=self.colors['pListOrange'],bg='#fff',team=2)
    self.mainCanv = SelectionWindow(self,bg='#fff',highlightthickness=0)
    self.footBar = FooterBar(self)

    self.initUI()

    self.bind_all('<Tab>',self.modeSwitch)
    self.bind_all('<Escape>',self.reset)
    self.bind_all('<Up>',self.scrollUpP1)
    self.bind_all('<Down>',self.scrollDownP1)
    self.bind_all('<Control-Up>',self.scrollUpP2)
    self.bind_all('<Control-Down>',self.scrollDownP2)
    self.bind_all('<Shift-Up>',self.scrollUpP3)
    self.bind_all('<Shift-Down>',self.scrollDownP3)
    self.bind_all('<Shift-Left>',self.kickP3)
    self.bind_all('<Shift-Right>',self.kickP3)
    self.bind_all('<Shift-Control-Up>',self.scrollUpP4)
    self.bind_all('<Shift-Control-Down>',self.scrollDownP4)
    self.bind_all('<Shift-Control-Left>',self.kickP4)
    self.bind_all('<Shift-Control-Right>',self.kickP4)
    self.bind_all('<F1>',self.setPlayMode1)
    self.bind_all('<F2>',self.setPlayMode2)
    self.bind_all('<F3>',self.setPlayMode3)

    self.mainCanv.charTraceP1.trace('w',self.setCharacSoftP1)
    self.mainCanv.charLockP1.trace('w',self.setCharacHardP1)
    self.mainCanv.charTraceP2.trace('w',self.setCharacSoftP2)
    self.mainCanv.charLockP2.trace('w',self.setCharacHardP2)
    self.mainCanv.charTraceP3.trace('w',self.setCharacSoftP3)
    self.mainCanv.charLockP3.trace('w',self.setCharacHardP3)
    self.mainCanv.charTraceP4.trace('w',self.setCharacSoftP4)
    self.mainCanv.charLockP4.trace('w',self.setCharacHardP4)
    self.mainCanv.lockInWin.trace('w',self.publishMatch)

  def initUI(self):
    self.P1.grid(row=0,column=0,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.P2.grid(row=2,column=0,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.Ps.grid(row=4,column=0,rowspan=4,columnspan=1,sticky=N+S+E+W)
    self.mainCanv.grid(row=0,column=1,rowspan=8,columnspan=4,sticky=N+S+E+W)
    self.P3.grid(row=0,column=5,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.P4.grid(row=2,column=5,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.Ps2.grid(row=4,column=5,rowspan=4,columnspan=1,sticky=N+S+E+W)
    self.footBar.grid(row=9,column=0,columnspan=6,sticky=N+S+E+W)
    self.mainCanv.focus_force()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=4)
    self.columnconfigure(5, weight=1)

    first = np.random.permutation(self.players)
    p1 = first[0]
    p2 = first[1]
    self.P1.pickPlayer(p1)
    self.P2.pickPlayer(p2)
    self.Ps.player1.set(p1)
    self.Ps.player2.set(p2)
    self.Ps2.playMode.set(self.Ps2.modes[0])
    self.Ps.labels[p1].config(highlightbackground=self.colors['p1red'])
    self.Ps.labels[p2].config(highlightbackground=self.colors['p3yellow'])
    self.Ps2.labels[self.Ps2.modes[0]].config(highlightbackground='#000')
    self.mainCanv.P1.set(p1)
    self.mainCanv.P2.set(p2)
    self.mainCanv.switchMode('stageButton')
    self.mainCanv.switchMode('charButton')
    self.mainCanv.modeTextInsert(0)
    self.setFooter(toggle=-1)

  # different sub-functions specific to hovering/clicking a character for P1/P2, that all pass control to setCharac
  def setCharac(self,pNum,mode,charac):
    obOthers = [self.P1,self.P2,self.P3,self.P4]
    obPnum = obOthers[pNum-1]
    del obOthers[pNum-1]

    if pNum == 1:
      obCanvNum = self.mainCanv.char1
    elif pNum == 2:
      obCanvNum = self.mainCanv.char2
    elif pNum == 3:
      obCanvNum = self.mainCanv.char3
    else:
      obCanvNum = self.mainCanv.char4

    if mode == 'soft':
      if charac:
        if not(obPnum.tempChar.get()):
          obPnum.pickCharacter(charac)
          #obCanvNum.set(charac)
          for obOther in obOthers:
            obOther.kickCharacter(mode=mode)
      else:
        obPnum.kickCharacter(mode=mode)
    else:
      if charac:
        obPnum.pickCharacter(charac,mode=mode)
        obCanvNum.set(charac)
        for obOther in obOthers:
          obOther.kickCharacter(mode='soft')

  def setCharacSoftP1(self,event,*args):
    charac = self.mainCanv.charTraceP1.get()
    self.setCharac(pNum=1,mode='soft',charac=charac)

  def setCharacSoftP2(self,event,*args):
    charac = self.mainCanv.charTraceP2.get()
    self.setCharac(pNum=2,mode='soft',charac=charac)

  def setCharacSoftP3(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
      charac = self.mainCanv.charTraceP3.get()
      self.setCharac(pNum=3,mode='soft',charac=charac)

  def setCharacSoftP4(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
      charac = self.mainCanv.charTraceP4.get()
      self.setCharac(pNum=4,mode='soft',charac=charac)

  def setCharacHardP1(self,event,*args):
    charac = self.mainCanv.charLockP1.get()
    self.setCharac(pNum=1,mode='hard',charac=charac)

  def setCharacHardP2(self,event,*args):
    charac = self.mainCanv.charLockP2.get()
    self.setCharac(pNum=2,mode='hard',charac=charac)

  def setCharacHardP3(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
      charac = self.mainCanv.charLockP3.get()
      self.setCharac(pNum=3,mode='hard',charac=charac)

  def setCharacHardP4(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
      charac = self.mainCanv.charLockP4.get()
      self.setCharac(pNum=4,mode='hard',charac=charac)

  # switching between stage and character modes
  def modeSwitch(self,event=''):
    if self.mainCanv.toggleMode.get() == 'stageButton':
      self.mainCanv.switchMode('charButton')
    elif self.mainCanv.toggleMode.get() == 'charButton':
      self.mainCanv.switchMode('stageButton')

  # switching between play modes (i.e. 1-v-1, free-for-all, etc.)
  def setPlayMode1(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
      self.Ps2.setMode(self.Ps2.modes[0])
      self.mainCanv.playMode = 0
      self.mainCanv.modeTextInsert(0)
      self.mainCanv.kickHeads('soft')
      for el in self.mainCanv.modeText:
        if el == self.mainCanv.modeText[self.mainCanv.playMode]:
          self.mainCanv.charStageStock.tag_raise(el)
        else:
          self.mainCanv.charStageStock.tag_lower(el)

      self.kickP3()
      self.kickP4()
      ra = self.P1.PnumText.tag_ranges('team')
      if ra:
        for ob in [self.P1.PnumText,self.P2.PnumText,self.P3.PnumText,self.P4.PnumText]:
          ob.config(state='normal')
          ob.delete(ra[0],ra[1])
          ob.config(state='disabled')

  # players 3 and 4 not allowed in 1v1 mode
  def kickP3(self,event=''):
    if self.mainCanv.P3.get():
      self.P3.kickPlayer()
      self.mainCanv.P3.set('')
      self.Ps.unSetPlayer(3)
    if self.mainCanv.char3.get():
      self.P3.kickCharacter()
      self.mainCanv.char3.set('')
      self.mainCanv.charLockP3.set('')

  def kickP4(self,event=''):
    if self.mainCanv.P4.get():
      self.P4.kickPlayer()
      self.mainCanv.P4.set('')
      self.Ps.unSetPlayer(4)
    if self.mainCanv.char4.get():
      self.P4.kickCharacter()
      self.mainCanv.char4.set('')
      self.mainCanv.charLockP4.set('')

  def setPlayMode2(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[1]):
      self.Ps2.setMode(self.Ps2.modes[1])
      self.mainCanv.playMode = 1
      self.mainCanv.modeTextInsert(1)
      self.mainCanv.kickHeads('soft')
      for el in self.mainCanv.modeText:
        if el == self.mainCanv.modeText[self.mainCanv.playMode]:
          self.mainCanv.charStageStock.tag_raise(el)
        else:
          self.mainCanv.charStageStock.tag_lower(el)
      for ob in [self.P1.PnumText,self.P2.PnumText]:
        ob.config(state='normal')
        ob.insert(END,', Team 1','team')
        ob.config(state='disabled')
      for ob in [self.P3.PnumText,self.P4.PnumText]:
        ob.config(state='normal')
        ob.insert(END,', Team 2','team')
        ob.config(state='disabled')

  def setPlayMode3(self,event,*args):
    if not(self.Ps2.playMode.get() == self.Ps2.modes[2]):
      self.Ps2.setMode(self.Ps2.modes[2])
      self.mainCanv.playMode = 2
      self.mainCanv.modeTextInsert(2)
      self.mainCanv.kickHeads('soft')
      for el in self.mainCanv.modeText:
        if el == self.mainCanv.modeText[self.mainCanv.playMode]:
          self.mainCanv.charStageStock.tag_raise(el)
        else:
          self.mainCanv.charStageStock.tag_lower(el)

      ra = self.P1.PnumText.tag_ranges('team')
      if ra:
        for ob in [self.P1.PnumText,self.P2.PnumText,self.P3.PnumText,self.P4.PnumText]:
          ob.config(state='normal')
          ob.delete(ra[0],ra[1])
          ob.config(state='disabled')

  # on Esc-press clear stockHeads, clear stage selection, clear character selection, reset toggleMode to character window
  def reset(self,event=''):
    self.mainCanv.kickHeads(mode='hard')
    self.mainCanv.kickStage(mode='hard')
    self.mainCanv.zeroVars()
    self.mainCanv.zeroVars(togg='lock')
    self.mainCanv.switchMode('charButton')
    self.mainCanv.char1.set('')
    self.mainCanv.char2.set('')
    self.mainCanv.char3.set('')
    self.mainCanv.char4.set('')
    self.P1.kickCharacter()
    self.P2.kickCharacter()
    self.P3.kickCharacter()
    self.P4.kickCharacter()

  # main 'scrolling' function; up/down keys cycle players through the player list
  def scrollCheck(self,togg,direc):
    # check the scroll direction and toggle mode
    # for togg == 1, we're changing player 1
    if direc == 'up':
      incr = -1
    else:
      incr = 1

    pList = [self.P1,self.P2,self.P3,self.P4]
    pOthers = []
    # when switching player, erase the highlight box around the switched-from player
    # if there was not an entry, there's nothing to erase (i.e. P3/P4 show no one)
    eraseMode = True

    if togg == 1:
      pCurr = self.P1.currName.get()
      del pList[0]
    elif togg == 2: 
      pCurr = self.P2.currName.get()
      del pList[1]
    elif togg == 3: 
      if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
        pCurr = self.P3.currName.get()
        del pList[2]
      else:
        return
    else: 
      if not(self.Ps2.playMode.get() == self.Ps2.modes[0]):
        pCurr = self.P4.currName.get()
        del pList[3]
      else:
        return
   
    for p in pList:
      if p.currName.get():
        pOthers.append(p.currName.get())

    if pCurr:
      indCurr = self.players.index(pCurr)
    else:
      eraseMode = False
      indCurr = 0

    indNext = (indCurr + incr) % len(self.players)
    pNext = self.players[indNext]

    if not(pNext in pOthers):
      self.scrollPlayer(togg,pNext,eraseMode)
    else:
      indNext = (indNext+incr) % len(self.players)
      pNext = self.players[indNext]
      if not(pNext in pOthers):
        self.scrollPlayer(togg,pNext,eraseMode)
      else:
        indNext = (indNext+incr) % len(self.players)
        pNext = self.players[indNext]
        if not(pNext in pOthers):
          self.scrollPlayer(togg,pNext,eraseMode)
        else:
          indNext = (indNext+incr) % len(self.players)
          pNext = self.players[indNext]
          if not(pNext in pOthers):
            self.scrollPlayer(togg,pNext,eraseMode)
          else:
            self.unscrollPlayer(togg)

  def unscrollPlayer(self,togg):
    # if there are more desired players than players in the list, 
    # pull that player name out of selection when attempting to scroll
    if togg == 3:
      self.P3.kickCharacter()
      self.P3.kickPlayer()
      self.mainCanv.P3.set('')
      self.Ps.unSetPlayer(togg)
    elif togg == 4:
      self.P4.kickCharacter()
      self.P4.kickPlayer()
      self.mainCanv.P4.set('')
      self.Ps.unSetPlayer(togg)

  def scrollPlayer(self,togg,name,eraseMode):
    # sets the appropriate variables for a P1/P2/P3/P4 change to another player
    if togg == 1:
      self.P1.pickPlayer(name)
      self.mainCanv.P1.set(name)
    elif togg == 2:
      self.P2.pickPlayer(name)
      self.mainCanv.P2.set(name)
    elif togg == 3:
      self.P3.pickPlayer(name)
      self.mainCanv.P3.set(name)
    else:
      self.P4.pickPlayer(name)
      self.mainCanv.P4.set(name)

    # this function just passes the toggle value along
    self.Ps.setPlayer(togg,name,eraseMode)

  # different sub-functions specific to scrolling up/down to a different P1/P2, that all pass control to scrollCheck/scrollPlayer
  def scrollUpP1(self,event):
    self.scrollCheck(1,'up')

  def scrollDownP1(self,event):
    self.scrollCheck(1,'down')

  def scrollUpP2(self,event):
    self.scrollCheck(2,'up')

  def scrollDownP2(self,event):
    self.scrollCheck(2,'down')

  def scrollUpP3(self,event):
    self.scrollCheck(3,'up')

  def scrollDownP3(self,event):
    self.scrollCheck(3,'down')

  def scrollUpP4(self,event):
    self.scrollCheck(4,'up')

  def scrollDownP4(self,event):
    self.scrollCheck(4,'down')

  # adding a match to the footer bar, or adding (up to) 3 matches from today to it
  def setFooter(self,toggle,text=''):
    if toggle in range(3):
      self.footBar.set('%s',text,toggle=toggle)
    else:
      f=open(self.dataFileName1v1)
      lines=f.readlines()
      f.close()
      numMatches = len(lines)
      lastThree = lines[-3:]
      lastThree.reverse()
      wasToday = [self.today in el for el in lastThree]

      '''
      f=open(self.dataFileNameTeams)
      lines=f.readlines()
      f.close()
      numMatches = len(lines)
      if numMatches >= 3:
        lastThree2 = lines[-3:]
        lastThree2.reverse()
        wasToday2 = [self.today in el for el in lastThree2]
      else:
        lastThree2 = []
        wasToday2 = []

      f=open(self.dataFileNameFreeForAll)
      lines=f.readlines()
      f.close()
      numMatches = len(lines)
      if numMatches >= 3:
        lastThree3 = lines[-3:]
        lastThree3.reverse()
        wasToday3 = [self.today in el for el in lastThree3]
      else:
        lastThree3 = []
        wasToday3 = []

      lastThree = sorted(lastThree+lastThree2+lastThree3,key=lambda el:el.strip().split(',')[0])[0:3]
      '''

      for i in range(3):
        self.setFooter(toggle=i,text='-----------')

      for (i,el) in enumerate(lastThree):
        if wasToday[i]:
          (dat,wp,wc,lp,lc,st,sg) = el.strip().split(',')
          text = '%s (%s) %s %s (%s)\n%s' % (wp,wc,'>'*int(st),lp,lc,sg)
          self.setFooter(toggle=i,text=text)
    
  # write winner(s)/loser(s) to a file
  def publishMatch(self,event,*args):
    if self.mainCanv.lockInWin.get():
      stock = self.mainCanv.stockCount.get()
      stage = self.mainCanv.stage.get()
      num = stock[0]
      n = [int(num)]
      if num == '1':
        s = ''
      else:
        s = 's'

      if self.mainCanv.playMode == 0:
        self.mainCanv.lockInWin.set(False)

        if 'P1' in stock:
          pWin = self.mainCanv.P1.get()
          cWin = self.mainCanv.char1.get()
          pLose = self.mainCanv.P2.get()
          cLose = self.mainCanv.char2.get()
        else: 
          pWin = self.mainCanv.P2.get()
          cWin = self.mainCanv.char2.get()
          pLose = self.mainCanv.P1.get()
          cLose = self.mainCanv.char1.get()

        # optionally add a bunch of text templates that are more exaggerated the higher num is and have a
        # random number decide which one gets picked 
        text = "Oh snap!? You mean %s's %s beat %s's %s by %s stock%s on %s???" % (pWin,cWin,pLose,cLose,num,s,stage)
        footText = "%s (%s) %s %s (%s)\n%s" % (pWin,cWin,'>'*n[0],pLose,cLose,stage)
        winners = [pWin,cWin]
        losers = [pLose,cLose]

      elif self.mainCanv.playMode == 1:
        if self.mainCanv.stockCount2.get():
          stock2= self.mainCanv.stockCount2.get()
          num2= stock2[0]
        else:
          num2 = 0

        if '1' in stock[-2:]:
          pWin1= self.mainCanv.P1.get()
          cWin1= self.mainCanv.char1.get()
          pWin2= self.mainCanv.P2.get()
          cWin2= self.mainCanv.char2.get()
          pLose1= self.mainCanv.P3.get()
          cLose1= self.mainCanv.char3.get()
          pLose2= self.mainCanv.P4.get()
          cLose2= self.mainCanv.char4.get()
        else:
          pWin1 = self.mainCanv.P3.get()
          cWin1 = self.mainCanv.char3.get()
          pWin2= self.mainCanv.P4.get()
          cWin2= self.mainCanv.char4.get()
          pLose1 = self.mainCanv.P1.get()
          cLose1 = self.mainCanv.char1.get()
          pLose2= self.mainCanv.P2.get()
          cLose2= self.mainCanv.char2.get()

        if 'B' in stock:
          num,num2 = num2,num
        n = [int(el) for el in [num,num2]]

        text = "Oh snap!? You mean %s (%s) + %s (%s) beat %s (%s) + %s (%s) by %s/%s stocks on %s???" % (pWin1,cWin1,pWin2,cWin2,pLose1,cLose1,pLose2,cLose2,num,num2,stage)
        footText = "%s (%s) + %s (%s) %s %s (%s) + %s (%s)\n%s" % (pWin1,cWin1,pWin2,cWin2,'>'*sum(n),pLose1,cLose1,pLose2,cLose2,stage)
        winners = [pWin1,cWin1,pWin2,cWin2]
        losers = [pLose1,cLose1,pLose2,cLose2]

      else:
        n = [int(num)]
        loseList = [self.mainCanv.P1,self.mainCanv.char1,self.mainCanv.P2,self.mainCanv.char2,self.mainCanv.P3,self.mainCanv.char3,self.mainCanv.P4,self.mainCanv.char4]

        if 'A' in stock[-2:]:
          if '1' in stock[-2:]:
            pWin= self.mainCanv.P1.get()
            cWin= self.mainCanv.char1.get()
            del(loseList[0:2])
          else:
            pWin= self.mainCanv.P3.get()
            cWin= self.mainCanv.char3.get()
            del(loseList[4:6])
        else:
          if '1' in stock[-2:]:
            pWin= self.mainCanv.P2.get()
            cWin= self.mainCanv.char2.get()
            del(loseList[2:4])
          else:
            pWin= self.mainCanv.P4.get()
            cWin= self.mainCanv.char4.get()
            del(loseList[6:8])

        pLose = [ob.get() for ob in loseList if ob.get()]

        loseText = ''
        for (i,t) in enumerate(pLose):
          if i%2:
            loseText = loseText+'(%s) ' % t
          else:
            if i>1:
              loseText = loseText+'/ '
            loseText = loseText+'%s ' % t
        text = "Oh snap!? You mean %s (%s) beat %s by %s stock%s on %s???" % (pWin,cWin,loseText,num,s,stage)
        footText = "%s (%s) %s %s \n%s" % (pWin,cWin,'>'*n[0],loseText,stage)
        winners = [pWin,cWin]
        losers = pLose

      answer = tkMessageBox.askyesno("Continue?",text)
      if answer:
        self.logIt([winners,losers,n,stage])

        #get the previous two matches (to bump them down the recent list in the footer); update the footer
        tNext1 = self.footBar.get(0)
        tNext2 = self.footBar.get(1)
        self.setFooter(toggle=0,text=footText)
        self.setFooter(toggle=1,text=tNext1)
        self.setFooter(toggle=2,text=tNext2)

        #tkMessageBox.showinfo('Logged',text) 
        self.mainCanv.kickHeads(mode='hard')
        self.mainCanv.kickStage(mode='hard')
        self.mainCanv.switchMode('charButton')
      else:
        self.mainCanv.kickHeads()

  # create a data frame of the match info, and append this match to the appropriate battleData file
  def logIt(self,matchData):
    winGroup,loseGroup,stockGroup,stage = matchData[0],matchData[1],matchData[2],[matchData[3]]
    if len(winGroup)==4:
      # 11 args => teams
      cols = ['WinningP1','WinningChar1','WinningP2','WinningChar2','LosingP1','LosingChar1','LosingP2','LosingChar2','StockCountP1','StockCountP2','Stage']
      fname = self.dataFileNameTeams
    else:
      # 1v1 or freeforall; length of loseGroup depends on number of losers
      loserHeaders = ['LosingPlayer','LosingCharacter','LosingP2','LosingChar2','LosingP3','LosingChar3']
      if len(loseGroup) == 2:
        cols = ['WinningPlayer','WinningCharacter']+loserHeaders[0:2]+['StockCount','Stage']
        fname = self.dataFileName1v1
      else:
        cols = ['WinningPlayer','WinningCharacter']+loserHeaders+['StockCount','Stage']
        fname = self.dataFileNameFreeForAll
        for i in range(6-len(loseGroup)):
          loseGroup.append('')

    df = pd.DataFrame([winGroup+loseGroup+stockGroup+stage],columns=cols,index=[[self.timeNow()]])

    with open(fname,'a') as f:
      df.to_csv(f, header=False)
    f.close()

  def timeNow(self):
    t = datetime.now()
    return t.strftime('%Y%m%d%H%M')

  def centerWindow(self,w=300, h=200):
    # get screen width and height
    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    self.geometry('%dx%d+%d+%d' % (w, h, x, y))
    self.resizable(0,0)