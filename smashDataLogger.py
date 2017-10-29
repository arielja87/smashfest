#!/usr/bin/env python

from __future__ import division
from Tkinter import *
import tkFont
import tkMessageBox
import os 
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from datetime import datetime


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
    self.w = 1200
    self.h = 670
    
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
    self.colors = {'p1red':'#f55943','p2blue':'#7092be','pListGreen':'#77c18b'}
    self.dataFileName = 'smashStats.csv'
    self.dataFileName = os.path.abspath(os.path.join('.','smashStats.csv'))
    #self.dataFileName = os.path.abspath(os.path.join('.','junkStats.csv'))
    self.today = datetime.now()
    self.today = self.today.strftime('%Y%m%d')

    self.title("FREE FOR ALL")

    self.characters = ["Mario","Luigi","Peach","Bowser","Yoshi","DonkeyKong",
    "DiddyKong","Link","Zelda","Sheik","Ganondorf","ToonLink","Samus",
    "ZeroSuitSamus","Kirby","MetaKnight","KingDedede","Fox","Falco","Wolf",
    "Pikachu","Jigglypuff","Mewtwo","Squirtle","Ivysaur","Charizard","Lucario",
    "CaptainFalcon","Ness","Lucas","IceClimbers","Marth","Roy","Ike",
    "MrGameAndWatch","Pit","Wario","Olimar","RoboticOperatingBuddy","Snake",
    "Sonic",'QuestionMark','Logo']

    #add all the legal stages
    self.stages = ['battlefield','bowsersCastle','delfinosSecret','distantPlanet',
    'dreamland','finalDestination','fountainOfDreams','greenHillZone','hyruleCastle',
    'infiniteGlacier','lylatCruise','metalCavern','norfair','peachsCastle64','pokemonStadium2',
    'saffronCity','skyworld','smashville','warioLand','yoshisIsland','yoshisStory']

    #players!
    self.players = ['Allen','Brett','Joe','Josh','Ryan','Sean','Torben']
    self.nickNames = {'Allen':'CharLord','Brett':u'\u00c7o\u00e7k','Josh':u'\u00c7\u00f2\u00ecT','Torben':u'BUTTS'}
    self.avatars = {}

    #images of character faces and icons
    self.faceImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Faces','%s.gif')) % el).resize((int(80*self.scale),int(56*self.scale)),Image.ANTIALIAS)) for el in self.characters if el != 'Logo'}\


    self.P1 = PlayerHeadWindow(self,PNUM=1,FACES=self.faceImgs,BORDERCOLOR=self.colors['p1red'],bg='#fff')
    self.P2 = PlayerHeadWindow(self,PNUM=2,FACES=self.faceImgs,BORDERCOLOR=self.colors['p2blue'],bg='#fff')
    self.Ps = PlayerListWindow(self,BORDERCOLOR=self.colors['pListGreen'],bg='#fff')
    self.mainCanv = SelectionWindow(self,bg='#fff',highlightthickness=0)
    self.footBar = FooterBar(self)

    self.initUI()

    self.bind('<Tab>',self.modeSwitch)
    self.bind('<Escape>',self.reset)
    self.bind_all('<Up>',self.scrollUpP1)
    self.bind_all('<Down>',self.scrollDownP1)
    self.bind_all('<Control-Up>',self.scrollUpP2)
    self.bind_all('<Control-Down>',self.scrollDownP2)

    self.mainCanv.charTraceP1.trace('w',self.setCharacSoftP1)
    self.mainCanv.charLockP1.trace('w',self.setCharacHardP1)
    self.mainCanv.charTraceP2.trace('w',self.setCharacSoftP2)
    self.mainCanv.charLockP2.trace('w',self.setCharacHardP2)
    self.mainCanv.lockInWin.trace('w',self.publishMatch)

  def initUI(self):
    self.P1.grid(row=0,column=0,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.P2.grid(row=2,column=0,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.Ps.grid(row=4,column=0,rowspan=4,columnspan=1,sticky=N+S+E+W)
    self.mainCanv.grid(row=0,column=1,rowspan=8,columnspan=4,sticky=N+S+E+W)
    self.footBar.grid(row=9,column=0,columnspan=4,sticky=N+S+E+W)
    self.mainCanv.focus_force()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=4)

    first = np.random.permutation(self.players)
    p1 = first[0]
    p2 = first[1]
    self.P1.pickPlayer(p1)
    self.P2.pickPlayer(p2)
    self.Ps.player1.set(p1)
    self.Ps.player2.set(p2)
    self.Ps.labels[p1].config(highlightbackground=self.colors['p1red'])
    self.Ps.labels[p2].config(highlightbackground=self.colors['p2blue'])
    self.mainCanv.P1.set(p1)
    self.mainCanv.P2.set(p2)
    self.mainCanv.switchMode('stageButton')
    self.mainCanv.switchMode('charButton')
    self.setFooter(toggle=-1)

  # different sub-functions specific to hovering/clicking a character for P1/P2, that all pass control to setCharac
  def setCharacSoftP1(self,event,*args):
    charac = self.mainCanv.charTraceP1.get()
    self.setCharac(pNum=1,mode='soft',charac=charac)

  def setCharacSoftP2(self,event,*args):
    charac = self.mainCanv.charTraceP2.get()
    self.setCharac(pNum=2,mode='soft',charac=charac)

  def setCharacHardP1(self,event,*args):
    charac = self.mainCanv.charLockP1.get()
    self.setCharac(pNum=1,mode='hard',charac=charac)

  def setCharacHardP2(self,event,*args):
    charac = self.mainCanv.charLockP2.get()
    self.setCharac(pNum=2,mode='hard',charac=charac)

  def setCharac(self,pNum,mode,charac):
    if pNum == 1:
      obPnum = self.P1
      obOther= self.P2
      obCanvNum = self.mainCanv.char1
    else:
      obPnum = self.P2
      obOther= self.P1
      obCanvNum = self.mainCanv.char2

    if mode == 'soft':
      if charac:
        if not(obPnum.tempChar.get()):
          obPnum.pickCharacter(charac)
          obCanvNum.set(charac)
          obOther.kickCharacter(mode=mode)
      else:
        obPnum.kickCharacter(mode=mode)
    else:
      if charac:
        obPnum.pickCharacter(charac,mode=mode)
        obCanvNum.set(charac)
        obOther.kickCharacter(mode='soft')

  def modeSwitch(self,event=''):
    if self.mainCanv.toggleMode.get() == 'stageButton':
      self.mainCanv.switchMode('charButton')
    elif self.mainCanv.toggleMode.get() == 'charButton':
      self.mainCanv.switchMode('stageButton')

  def reset(self,event=''):
    # on Esc-press clear stockHeads, clear stage selection, clear character selection, reset toggleMode to character window
    self.mainCanv.kickHeads(mode='hard')
    self.mainCanv.kickStage(mode='hard')
    self.mainCanv.zeroVars()
    self.mainCanv.zeroVars(togg='lock')
    self.mainCanv.switchMode('charButton')
    self.mainCanv.char1.set('')
    self.mainCanv.char2.set('')
    self.P1.kickCharacter()
    self.P2.kickCharacter()

  def indCheck(self,obj,ind,incr):
    try:
      value = obj.get(ind+incr)
    except IndexError:
      value = ''

    return value

  def findIndex(self,box,element):
    #find index from element name
    try:
      index = box.get(0, "end").index(element)
      return index
    except ValueError:
      print'Item can not be found in the list!'
      index = -1 # Or whatever value you want to assign to it by default
      return index

  def scrollCheck(self,togg,direc):
    # check the scroll direction and toggle mode
    # for togg == 1, we're changing player 1
    if direc == 'up':
      incr = -1
    else:
      incr = 1

    if togg == 1:
      pCurr = self.P1.currName.get()
      pOther = self.P2.currName.get()
    else: 
      pCurr = self.P2.currName.get()
      pOther = self.P1.currName.get()

    indCurr = self.players.index(pCurr)
    indNext = (indCurr + incr) % len(self.players)
    pNext = self.players[indNext]

    if pNext != pOther:
      self.scrollPlayer(togg,pNext)
    else:
      indNext = (indNext+incr) % len(self.players)
      pNext = self.players[indNext]
      self.scrollPlayer(togg,pNext)

  def scrollPlayer(self,togg,name):
    # sets the appropriate variables for a P1/P2 change to another player
    if togg == 1:
      self.P1.pickPlayer(name)
      self.mainCanv.P1.set(name)
    else:
      self.P2.pickPlayer(name)
      self.mainCanv.P2.set(name)

    # this function just passes the toggle value along
    self.Ps.setPlayer(togg,name)

  # different sub-functions specific to scrolling up/down to a different P1/P2, that all pass control to scrollCheck/scrollPlayer
  def scrollUpP1(self,event):
    self.scrollCheck(1,'up')

  def scrollDownP1(self,event):
    self.scrollCheck(1,'down')

  def scrollUpP2(self,event):
    self.scrollCheck(2,'up')

  def scrollDownP2(self,event):
    self.scrollCheck(2,'down')

  def setFooter(self,toggle,text=''):
    if toggle in range(3):
      self.footBar.set('%s',text,toggle=toggle)
    else:
      f=open(self.dataFileName)
      lines=f.readlines()
      numMatches = len(lines)
      lastThree = lines[-3:]
      wasToday = [self.today in el for el in lastThree]
      numToday = sum(wasToday)
      f.close()

      for i in range(3):
        self.setFooter(i,'-----------')

      for (i,el) in enumerate(lastThree):
        if wasToday[i]:
          (dat,wp,wc,lp,lc,st,sg) = el.strip().split(',')
          text = '%s (%s) %s %s (%s)\n%s' % (wp,wc,'>'*int(st),lp,lc,sg)
          self.setFooter(toggle=numToday-i-1,text=text)
         
  def publishMatch(self,event,*args):
    # write winner to a file
    if self.mainCanv.lockInWin.get():
      self.mainCanv.lockInWin.set(False)

      stock = self.mainCanv.stockCount.get()
      stage = self.mainCanv.stage.get()
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

      num = stock[0]
      if num == '1':
        s = ''
      else:
        s = 's'

      # optionally add a bunch of text templates that are more exaggerated the higher num is and have a
      # random number decide which one gets picked 
      text = "Oh snap!? You mean %s's %s beat %s's %s by %s stock%s on %s???" % (pWin,cWin,pLose,cLose,num,s,stage)
      answer = tkMessageBox.askyesno("Continue?",text)

      if answer:
        n = int(num)
        self.logIt(pWin,cWin,pLose,cLose,n,stage)

        #get the previous two matches (to bump them down the recent list in the footer); update the footer
        text = "%s (%s) %s %s (%s)\n%s" % (pWin,cWin,'>'*n,pLose,cLose,stage)
        tNext1 = self.footBar.get(0)
        tNext2 = self.footBar.get(1)
        self.setFooter(toggle=0,text=text)
        self.setFooter(toggle=1,text=tNext1)
        self.setFooter(toggle=2,text=tNext2)

        #tkMessageBox.showinfo('Logged',text) 
        self.mainCanv.kickHeads(mode='hard')
        self.mainCanv.kickStage(mode='hard')
        self.mainCanv.switchMode('charButton')
      else:
        self.mainCanv.kickHeads()

  def logIt(self,winner,winnerChar,loser,loserChar,stockMargin,stage):
    # create a standard data frame, and append this match to a battleData file
    cols = ['WinningPlayer','WinningCharacter','LosingPlayer','LosingCharacter','StockCount','Stage']
    df = pd.DataFrame([[winner,winnerChar,loser,loserChar,stockMargin,stage]],columns=cols,index=[[timeNow()]])

    with open(self.dataFileName,'a') as f:
      df.to_csv(f, header=False)

    f.close()

  def centerWindow(self,w=300, h=200):
    # get screen width and height
    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    self.geometry('%dx%d+%d+%d' % (w, h, x, y))


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
    self.numW = 10
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

    self.initUI()
      
  def initUI(self):
    #actually place and arrange all the part
    self.grid_propagate(False)
    self.PnumText.pack(side=TOP)
    self.PnameText.pack(side=TOP)
    self.Pface.pack(side=TOP)

  def kickPlayer(self):
    self.PnameText.delete(1.0,END)
    self.currName.set('')

  def pickPlayer(self, name):
      #delete old name and put in new name
      self.kickPlayer()
      self.currName.set(name)
      self.PnameText.insert(END,name,self.cn)
      self.PnameText.tag_configure(self.cn, justify=self.cn)

      #delete old icon and put in new one

  def kickCharacter(self,mode='hard'):
    if mode == 'hard' or not(self.tempChar.get()):
      self.Pface.delete('temp')
      self.tempChar.set('')

  def pickCharacter(self, charac,mode='soft'):
      #delete old face picture and put in new one
      self.kickCharacter()
      if mode == 'hard':
        self.tempChar.set(charac)
      self.Pface.create_image(self.px,self.py,image=self.faces[charac],tags='temp')
      self.Pface.tag_raise('temp')


class PlayerListWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)

    self.borderColor = kwargs['BORDERCOLOR']
    self.cn = 'center'
    self.colors = master.colors
    self.players = master.players

    #text box sizing
    self.numH = 1
    self.numW = 15
    self.nameH = int(320*master.scale)
    self.nameW = int(130*master.scale)

    #fonts
    self.ft = tkFont.Font(family="Times", size=int(24*master.scale), weight=tkFont.BOLD, slant=tkFont.ITALIC)
    self.fn = tkFont.Font(family="Times", size=int(16*master.scale), weight=tkFont.BOLD)

    #label text
    self.PlistText = Text(self,height=self.numH,width=self.numW,font=self.ft)
    self.PlistText.tag_configure(self.cn, justify=self.cn)
    self.PlistText.insert(END,'Victim list',self.cn)
    self.PlistText.config(state='disabled',relief=FLAT)

    #player name vars/text
    self.player1 = StringVar()
    self.player2 = StringVar()
    self.PnamesBox = Frame(self,height=self.nameH,width=self.nameW,relief=FLAT)
    self.PnamesBox.config(highlightbackground=self.borderColor,highlightcolor=self.borderColor,highlightthickness=3)
    self.labels = {}
    for name in self.players:
      self.labels[name] = Text(self.PnamesBox,borderwidth=0,height=1,width=18,font=self.fn,highlightbackground='#fff',highlightcolor='#fff',highlightthickness=2)
      self.labels[name].insert(END,name)
      if name in master.nickNames.keys():
        text = ' (%s)' % master.nickNames[name]
        self.labels[name].insert(END,text)

      self.labels[name].config(state='disabled')

    self.initUI()

  def setPlayer(self,pNum,player):
    if pNum == 1:
      self.labels[self.player1.get()].config(highlightbackground='#fff')
      self.labels[player].config(highlightbackground=self.colors['p1red'])
      self.player1.set(player)
    else:
      self.labels[self.player2.get()].config(highlightbackground='#fff')
      self.labels[player].config(highlightbackground=self.colors['p2blue'])
      self.player2.set(player)

  def initUI(self):
    #actually place and arrange all the part
    self.grid_propagate(False)
    self.PlistText.pack(side=TOP)
    self.PnamesBox.pack(side=TOP)
    for name in sorted(self.players):
      self.labels[name].pack(side=TOP)

class SelectionWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)
    
    #dimensions
    self.canH = int(598*master.scale)
    self.canW = int(900*master.scale)
    self.scaleX = self.canW/1183.
    self.scaleY = self.canH/787.
    self.sx = int(792*master.scale)
    self.sy = int(497*master.scale)
    
    #vars for binding mouse movement/selection
    self.charTraceP1 = StringVar(self)    #stores character name under mouse; NA if no hover
    self.charTraceP2 = StringVar(self)    #stores character name under mouse; NA if no hover
    self.stagTrace = StringVar(self)    #stores stage name under mouse; NA if no hover
    self.stocTrace = StringVar(self)    #similar for stock count buttons 

    #vars for binding clicked options
    self.charLockP1 = StringVar(self)
    self.charLockP2 = StringVar(self)
    self.stagLock = StringVar(self)
    self.toggLock = StringVar(self) #unnecessary?
    self.stocLock = StringVar(self)
    self.statsLock = StringVar(self)
    self.zeroVars('lock')

    #current mode options
    self.toggleMode = StringVar(self)
    self.toggleMode.set('char')
    self.stockCount = StringVar(self)
    self.stockCount.set('')
    self.readyForStock = False
    self.readyForStats = True
    self.lockInWin = BooleanVar(self)
    self.lockInWin.set(False)

    self.master = master
    self.characters = master.characters
    self.stages = master.stages
    self.P1 = StringVar(self)
    self.P2 = StringVar(self)
    self.char1 = StringVar(self)
    self.char2 = StringVar(self)
    self.stage = StringVar(self)

    #canvas where all the action happens
    self.charStageStock = Canvas(self,height=self.canH,width=self.canW,bg='#fff')
    self.iconImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Thumbs','%s.jpg')) % el).resize((int(64*master.scale),int(64*master.scale)),Image.ANTIALIAS)) for el in self.characters if el != 'QuestionMark'}
    self.stageImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Stages','%s.gif')) % el).resize((int(160*master.scale),int(160*master.scale)),Image.ANTIALIAS)) for el in self.stages}

    #actual images
    self.charImg = ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Banners','charBanner.jpg'))).resize((int(900*master.scale),int(598*master.scale)),Image.ANTIALIAS))
    self.stagImg = ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Banners','stageBanner.jpg'))).resize((int(900*master.scale),int(598*master.scale)),Image.ANTIALIAS))
    self.charStageStock.create_image(self.canW/2,self.canH/2,image=self.charImg,tags='charButton')
    self.charStageStock.create_image(self.canW/2,self.canH/2,image=self.stagImg,tags='stageButton')
    self.charStageStock.tag_raise('charButton')


    #canvas binding for fancy effects
    self.charStageStock.bind('<Motion>',self.mouseTrace)          #track mouse movement over things of interest
    self.charStageStock.bind('<ButtonRelease-1>',self.mouseSave)
    self.charStageStock.bind('<Control-Motion>',self.mouseTraceP2)          #track mouse movement over things of interest
    self.charStageStock.bind('<Control-ButtonRelease-1>',self.mouseSaveP2)

    self.dictMake()
    
    self.initUI()

  def initUI(self):
    self.grid_propagate(False)
    self.charStageStock.pack()

  def switchMode(self,mode):
    #check that the goal would change anything
    #made the changes, raise the image, cleare the lock var
    if mode in self.toggleButtons and mode != self.toggleMode.get():
      self.toggleMode.set(mode)
      self.charStageStock.tag_raise(mode)
      self.charStageStock.tag_raise('head')
      self.charStageStock.tag_raise('temp')

  def kickStage(self,mode='hard'):
    # hard mode: delete stage selection
    # soft mode: if no stage selected, it'll soft delete the stage image
    if mode == 'hard' or not(self.stage.get()):
      self.charStageStock.delete('temp')
      self.stage.set('')
      self.stagLock.set('')

    self.checkReady()

  def pickStage(self,stage,mode='soft'):
    # hard mode: delete and replace stage
    # soft mode: allow an image to be placed, but don't confirm the stage
    self.kickStage(mode=mode)
    if mode == 'hard' or not(self.stage.get()) and stage in self.stages:
      if mode == 'hard':
        self.stage.set(stage)
      self.charStageStock.create_image(self.sx,self.sy,image=self.stageImgs[stage],tags='temp')
      
    self.checkReady()

  def setStockCount(self,stockKey,mode='soft'):
    # both modes: check if ready and if it's a new selection
    # hard mode: set stockCount and drawHeads
    # soft mode: check if stockCount is not set : don't set stockCount, but drawHeads 
    if stockKey and stockKey != self.stockCount.get() and self.readyForStock:
      if mode=='hard' and stockKey != 'submitButton':
        self.stockCount.set(stockKey)
      if mode=='hard' or not(self.stockCount.get()):
        self.charStageStock.delete('head')
        self.drawHeads(stockKey)

  def kickHeads(self,mode='hard'):
    if mode == 'hard' or not(self.stockCount.get()):
      self.charStageStock.delete('head')
      self.stockCount.set('')

  def drawHeads(self,stockKey):
    # search through the stockPixelDict for stock numbers <= stock count
    # draw little heads for each stock for the winner
    numSet = ['1','2','3','4']
    if 'P1' in stockKey:
      p = 'P1'
      charHead = self.iconImgs[self.char1.get()]
    elif 'P2' in stockKey: 
      p = 'P2'
      charHead = self.iconImgs[self.char2.get()]
    else:
      return

    if stockKey[0] in numSet:
      num = int(stockKey[0])
    else:
      num = 0

    candKeys = [key for key in self.stockPixelDict.keys() if p in key and key[0] in numSet]
    for key in candKeys:
      if int(key[0]) <= num:
        posx,posy = self.stockPixelDict[key]
        posx = int(posx*self.scaleX)
        posy = int(posy*self.scaleY)
        self.charStageStock.create_image(posx,posy,image=charHead,tags='head')
        self.charStageStock.tag_raise('head')

  def checkDicts(self):
    #search the dicts to see if the pixel is of interest
    x,y = self.lastPos[0],self.lastPos[1]
    selection = ''

    if (x,y) in self.charDict and self.toggleMode.get() == 'charButton':
      selection = self.charDict[(x,y)]
    elif (x,y) in self.stagDict and self.toggleMode.get() == 'stageButton':
      selection = self.stagDict[(x,y)]
    elif (x,y) in self.toggleDict:
      selection = self.toggleDict[(x,y)]
    elif (x,y) in self.stockDict:
      selection = self.stockDict[(x,y)]

    return selection

  def zeroVars(self,togg='trace'):
    if togg=='trace':
      self.kickStage('soft')
      self.kickHeads('soft')
      self.charTraceP1.set('')
      self.charTraceP2.set('')
      self.stagTrace.set('')
      self.stocTrace.set('')
    elif togg=='lock':
      self.charLockP1.set('')
      self.charLockP2.set('')
      self.stagLock.set('')
      self.toggLock.set('')
      self.stocLock.set('')
      self.statsLock.set('')

  def updateVars(self,sel,mode,togg='trace'):

    if mode == 1:
      obCharTrace = self.charTraceP1
      obCharLock = self.charLockP1
    else:
      obCharTrace = self.charTraceP2
      obCharLock = self.charLockP2

    if togg=='trace':
      #set all the trace variables according to whether the pixel matters
      if sel:

        # only need to update the trace variable; the MainWindow will act on changes
        # check if we've already hovered this char and set obCharTrace if not
        if sel in self.charCornerPixelDict.keys():
          if sel != obCharTrace.get():
            obCharTrace.set(sel)
        else:
          obCharTrace.set('')

        # check if we've already made the image hovered and pickStage softly if not
        if sel in self.stagCornerPixelDict.keys():
          if sel != self.stagTrace.get() and sel in self.stages:
            self.stagTrace.set(sel)
            self.pickStage(sel)   #default pick mode ='soft'
        else:
          self.stagTrace.set('')
          self.kickStage(mode='soft')

        # check if we've already hovered this and setStockCount softly if not
        if sel in self.stockPixelDict.keys():
          if sel != self.stocTrace.get():
            self.stocTrace.set(sel)
            self.checkReady()
            self.setStockCount(sel)
        else:
          self.kickHeads(mode='soft')
          self.stocTrace.set('')

      else:
        #not hovering anything : set all trace vars to empty
        self.zeroVars()

    elif togg=='lock':
      #check mouse click selections

      # if change in , set it; again MainWindow handles the actions
      if sel in self.charCornerPixelDict.keys() and sel != obCharLock.get():
        obCharLock.set(sel)

      # check if we've already chosen this stage, and pickStage hard if not
      if sel in self.stagCornerPixelDict.keys() and sel != self.stagLock.get() and sel in self.stages:
        self.stagLock.set(sel)
        self.pickStage(sel,mode='hard')

      # check if we've already set this stock count, and setStockCount hard if not
      if sel in self.stockPixelDict.keys() and sel != self.toggleMode.get():
        self.checkReady()
        if sel == 'submitButton':
          if self.readyForStock and self.stockCount.get():
            self.lockInWin.set(True)
        else:
          self.setStockCount(sel,mode='hard')

      # check our mode, set and switchMode if different
      if sel in self.toggleButtons and sel != self.toggLock.get():
        if sel == 'statsButton':
          if self.readyForStats:
            self.getMatchupData(self.allVars)
        else:
          self.toggLock.set(sel)
          self.switchMode(sel)

      #after any updates, recheck if stockCount can be updated
      self.checkReady()

    else:
      print('Something went wrong with the updateVars() function!')

  def mouseTrace(self,event):
    # track the mouse position, and check it across the dictionaries
    self.lastPos = (event.x,event.y)

    #check the position against the dictionaries of pixel locations of interest
    sel = self.checkDicts()
    self.updateVars(sel,mode=1)

  def mouseSave(self,event=''):
    # same thing as above, but for the click mode instead of hovering mode
    if event:
      self.lastPos = (event.x,event.y)

      sel = self.checkDicts()
      self.updateVars(sel,mode=1,togg='lock')

  def mouseTraceP2(self,event):
    # track the mouse position, and check it across the dictionaries
    self.lastPos = (event.x,event.y)

    #check the position against the dictionaries of pixel locations of interest
    sel = self.checkDicts()
    self.updateVars(sel,mode=2)

  def mouseSaveP2(self,event=''):
    # same thing as above, but for the click mode instead of hovering mode
    if event:
      self.lastPos = (event.x,event.y)

      sel = self.checkDicts()
      self.updateVars(sel,mode=2,togg='lock')

  def checkReady(self):
    # to allow a stock selection, we need players, characters and stage chosen
    self.statVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2]]
    self.allVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2,self.stage]]
    if all(self.statVars):
      self.readyForStats = True
    else:
      self.readyForStats = False

    if all(self.allVars):
      self.readyForStock = True
    else:
      self.readyForStock = False

  def getMatchupData(self,vars):
    p1 = vars[0]
    c1 = vars[1]
    p2 = vars[2]
    c2 = vars[3]
    stage = vars[4]

    self.dataWin = DataWindow(self,file=self.master.dataFileName,p1=p1,c1=c1,p2=p2,c2=c2,stage=stage,scale=self.master.scale)
    self.dataWin.focus_force()
    self.dataWin.lift()
    self.dataWin.mainloop()

  def dictMake(self):
    # set up dictionaries with pixels as keys and either a character or stage name, or a stock count or toggle button string
    self.charDict = {}
    self.stagDict = {}
    self.toggleDict = {}
    self.stockDict = {}
    self.toggleButtons = ['stageButton','charButton','statsButton']

    # these reference dictionaries will have a starting or center pixel for the sake of creating the reverse dictionary
    self.charCornerPixelDict = {'Wario':(111,84),'Mario':(218,84),'Luigi':(326,84),'Peach':(433,84),
                            'Bowser':(541,84),'Yoshi':(648,84),'DonkeyKong':(756,84),'DiddyKong':(863,84),
                            'CaptainFalcon':(971,84),'Wolf':(111,160),'Fox':(218,160),'Falco':(326,160),
                            'IceClimbers':(433,160),'Zelda':(541,160),'Sheik':(648,160),'Link':(756,160),
                            'ToonLink':(863,160),'Ganondorf':(971,160),'Mewtwo':(111,236),'Lucario':(218,236),
                            'Pikachu':(326,236),'Jigglypuff':(433,236),'Squirtle':(541,236),'Ivysaur':(648,236),
                            'Charizard':(756,236),'Samus':(863,236),'ZeroSuitSamus':(971,236),'Lucas':(111,312),
                            'Ness':(218,312),'Pit':(326,312),'Kirby':(433,312),'MetaKnight':(541,312),
                            'KingDedede':(648,312),'Ike':(756,312),'Marth':(863,312),'Roy':(971,312),'Olimar':(326,388),
                            'RoboticOperatingBuddy':(433,388),'MrGameAndWatch':(541,388),'Snake':(648,388),
                            'Sonic':(756,388)}

    self.stagCornerPixelDict = {'battlefield':(56,83),'bigBlue':(176,83),'bowsersCastle':(295,83),'brinstar':(414,83),'castleSiege':(534,83),
                                'corneria':(653,83),'delfinosSecret':(773,83),'distantPlanet':(892,83),'dreamland':(1011,83),'finalDestination':(56,160),'flatZone2':(176,160),
                                'fountainOfDreams':(295,160),'fourside':(414,160),'frigateOrpheon':(534,160),'greenHillZone':(653,160),'halberd':(773,160),'hanenbow':(892,160),
                                'hyruleCastle':(1011,160),'infiniteGlacier':(56,236),'jungleJapes':(176,236),'kongoJungle':(295,236),'luigisMansion':(414,236),'lylatCruise':(534,236),
                                'metalCavern':(653,236),'norfair':(773,236),'onett':(892,236),'peachsCastle64':(1011,236),'pictochat':(56,313),'pirateShip':(176,313),
                                'pokemonStadium2':(295,313),'portTownAeroDive':(414,313),'rumbleFalls':(534,313),'saffronCity':(653,313),'shadowMosesIsland':(773,313),'skyworld':(892,313),
                                'smashville':(1011,313),'spearPillar':(235,389),'hyruleTemple':(354,389),'trainingRoom':(474,389),'warioLand':(593,389),'yoshisIsland':(713,389),'yoshisStory':(833,389)}

    #start at 38,564, but they're 72x72 and I'll want these locations for placing icons later;
    # so the rough midpoint is actually (74,600) for the first one (and it's +\- 36 pixels)
    self.stockPixelDict = {'4stockP1':(74,682),'3stockP1':(154,682),'2stockP1':(234,682),'1stockP1':(314,682),'submitButton':(431,682),'1stockP2':(548,682),'2stockP2':(628,682),'3stockP2':(708,682),'4stockP2':(788,682)}

    #sort over all the characters' upper-left corner pixels
    for el in self.charCornerPixelDict.keys():
      pix = self.charCornerPixelDict[el]
      x = pix[0]
      y = pix[1]
      #set of all x,y coords in the 100x70 swath of the character's face:
      #also going +1 over on each range function because it doesn't include the upper bound
      areaList = [(xa,ya) for xa in range(x,x+101) for ya in range(y,y+71)]   

      #each (x,y) pair will now be a key with a value of the character name
      for singCoord in areaList:
        scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
        self.charDict[scaleCoord] = el

    #sort over all the stages' upper-left corner pixels
    for el in self.stagCornerPixelDict.keys():
      pix = self.stagCornerPixelDict[el]
      x = pix[0]
      y = pix[1]
      #set of all x,y coords in the 113x70 swath of the stage image:
      areaList = [(xa,ya) for xa in range(x,x+114) for ya in range(y,y+71)]   

      #each (x,y) pair will now be a key with a value of the character name
      for singCoord in areaList:
        scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
        self.stagDict[scaleCoord] = el

    #get the areas for the character and stage toggle buttons
    areaList = [(x,y) for x in range(350,566) for y in range(20,68)]
    for singCoord in areaList:
      scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
      self.toggleDict[scaleCoord] = 'charButton'

    areaList = [(x,y) for x in range(625,761) for y in range(20,68)]
    for singCoord in areaList:
      scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
      self.toggleDict[scaleCoord] = 'stageButton'

    areaList = [(x,y) for x in range(10,85) for y in range(505,545)]
    for singCoord in areaList:
      scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
      self.toggleDict[scaleCoord] = 'statsButton'

    #get the areas for the stock count buttons
    for el in self.stockPixelDict:
      pix = self.stockPixelDict[el]
      x = pix[0]
      y = pix[1]
      #set of all x,y coords in the 72x72 swath of the smash logo:
      areaList = [(xa,ya) for xa in range(x-36,x+37) for ya in range(y-36,y+37)]   

      #each (x,y) pair will now be a key with a value of the character name
      for singCoord in areaList:
        scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
        self.stockDict[scaleCoord] = el


class Stats2P:
  def __init__(self, file, p1,c1,p2,c2,stage=''):
    self.dataFileName = file
    self.p1 = p1
    self.c1 = c1
    self.p2 = p2
    self.c2 = c2
    self.stage = stage

    # load the battle data file and search over a set of conditions
    # match win ratio player-to-player
    # match win ratio character-to-character
    # % of matches p1/p2 wins with that char, across all data
    # % of matches p1/p2 wins on that stage, across all data
    # total stock margin vs win percentage: i.e. do they win many close and lose few by a lot?

    self.wp = 'WinningPlayer'
    self.wc = 'WinningCharacter'
    self.lp = 'LosingPlayer'
    self.lc = 'LosingCharacter'
    self.sc = 'StockCount'
    self.st = 'Stage'

    self.data = pd.read_csv(self.dataFileName)
    
    if self.stage:
      self.stageTrue = self.data.apply(self.DFfunc,axis=1,args=(self.st,self.stage)) 
    self.stockCount= self.data[self.sc]

    # data frames for individual config matching
    # e.g. p1W will give a bool-valued dataFrame with True where each row has the
    # winning player (wp) == player 1 (p1)

    '''
    # "intersection" means for intersection of p1 vs p2 or p1+c1 vs p2 or p1+c1 vs p2+c2, etc. 
    # match intersections; for each intersection the format is:
    bool win/loss arrays          : true for lines that match, false otherwise
    counters                      : how many matches were played 
    stage specific counters       : how many matches were played (and on this stage)
    win ratio                     : win to loss ratio as a %
    *stock margin                  : average number of stocks left per match for wins/losses/total 
    stage-specific win ratio      : % win-loss ratio on this stage
    stage-specific stock margin   : same as above, on this stage

    *stock margin note e.g.: 
    3x 1-stock wins => (avg. +1.0) 
    6x 3-stock losses =>(avg. -3.0)
    9x total, [(3*+1) + (6*-3)] / 9 => (avg. -1.67)  
    => margins = +1.0/-3.0/-1.67
    '''

    self.allCount = len(self.stockCount)
    if stage:
      self.stageCount = sum(self.stageTrue)

    # p1 v all
    p1W = self.data.apply(self.DFfunc,axis=1,args=(self.wp,self.p1)) 
    p1L = self.data.apply(self.DFfunc,axis=1,args=(self.lp,self.p1)) 
    (self.p1WinRatioAll,self.p1AllCount,self.p1StockMarginAll) = self.calcRatiosAndMargins(p1W,p1L)

    # p2 v all
    p2W = self.data.apply(self.DFfunc,axis=1,args=(self.wp,self.p2)) 
    p2L = self.data.apply(self.DFfunc,axis=1,args=(self.lp,self.p2)) 
    (self.p2WinRatioAll,self.p2AllCount,self.p2StockMarginAll) = self.calcRatiosAndMargins(p2W,p2L)
    
    # c1 v all
    c1W = self.data.apply(self.DFfunc,axis=1,args=(self.wc,self.c1)) 
    c1L = self.data.apply(self.DFfunc,axis=1,args=(self.lc,self.c1)) 
    c1Notc2 = c1W&c1L     # need to not count character dittos: if captain falcon wins and captain falcon loses, what does that say?
    c1Notc2 = ~c1Notc2
    c1WnoDitto = c1W&c1Notc2
    c1LnoDitto = c1L&c1Notc2
    (self.c1WinRatioAll,self.c1AllCount,self.c1StockMarginAll) = self.calcRatiosAndMargins(c1WnoDitto,c1LnoDitto)
    
    # c2 v all
    c2W = self.data.apply(self.DFfunc,axis=1,args=(self.wc,self.c2)) 
    c2L = self.data.apply(self.DFfunc,axis=1,args=(self.lc,self.c2))
    c2WnoDitto = c2W&c1Notc2
    c2LnoDitto = c2L&c1Notc2 
    (self.c2WinRatioAll,self.c2AllCount,self.c2StockMarginAll) = self.calcRatiosAndMargins(c2WnoDitto,c2LnoDitto)

    # p1+c1 v all
    p1c1W = p1W&c1W
    p1c1L = p1L&c1L
    (self.p1c1WinRatioAll,self.p1c1AllCount,self.p1c1StockMarginAll) = self.calcRatiosAndMargins(p1c1W,p1c1L)

    # p2+c2 v all
    p2c2W = p2W&c2W
    p2c2L = p2L&c2L
    (self.p2c2WinRatioAll,self.p2c2AllCount,self.p2c2StockMarginAll) = self.calcRatiosAndMargins(p2c2W,p2c2L)

    # p1 v p2 (all characters)
    p1Wp2L = p1W&p2L
    p2Wp1L = p2W&p1L
    (self.p1p2WinRatio,self.p1p2Count,self.p1p2StockMargin) = self.calcRatiosAndMargins(p1Wp2L,p2Wp1L)
    
    # p1 (all characters) v c2 (all players)
    p1Wc2L = p1W&c2L
    c2Wp1L = c2W&p1L
    (self.p1c2WinRatio,self.p1c2Count,self.p1c2StockMargin) = self.calcRatiosAndMargins(p1Wc2L,c2Wp1L)
    
    # p2 (all characters) v c1 (all players)
    p2Wc1L = p2W&c1L
    c1Wp2L = c1W&p2L
    (self.p2c1WinRatio,self.p2c1Count,self.p2c1StockMargin) = self.calcRatiosAndMargins(p2Wc1L,c1Wp2L)
    
    # p1+c1 v p2 (all characters)
    p1c1Wp2L = p1c1W&p2L
    p2Wp1c1L = p2W&p1c1L
    (self.p1c1p2WinRatio,self.p1c1p2Count,self.p1c1p2StockMargin) = self.calcRatiosAndMargins(p1c1Wp2L,p2Wp1c1L)
    
    # p1+c1 v c2 (all players)
    p1c1Wc2L = p1c1W&c2L
    c2Wp1c1L = c2W&p1c1L
    (self.p1c1c2WinRatio,self.p1c1c2Count,self.p1c1c2StockMargin) = self.calcRatiosAndMargins(p1c1Wc2L,c2Wp1c1L)

    # p2+c2 v p1 (all characters)  
    p2c2Wp1L = p2c2W&p1L
    p1Wp2c2L = p1W&p2c2L
    (self.p2c2p1WinRatio,self.p2c2p1Count,self.p2c2p1StockMargin) = self.calcRatiosAndMargins(p2c2Wp1L,p1Wp2c2L)
    
    # p2+c2 v c1 (all players)
    p2c2Wc1L = p2c2W&c1L
    c1Wp2c2L = c1W&p2c2L
    (self.p2c2c1WinRatio,self.p2c2c1Count,self.p2c2c1StockMargin) = self.calcRatiosAndMargins(p2c2Wc1L,c1Wp2c2L)
    
    # p1+c1 v p2+c2
    p1c1Wp2c2L = p1c1W&p2c2L
    p2c2Wp1c1L = p2c2W&p1c1L
    (self.p1c1p2c2WinRatio,self.p1c1p2c2Count,self.p1c1p2c2StockMargin) = self.calcRatiosAndMargins(p1c1Wp2c2L,p2c2Wp1c1L)
    
    # c1 v c2 (all players)
    c1Wc2L = c1W&c2L&c1Notc2
    c2Wc1L = c2W&c1L&c1Notc2
    (self.c1c2WinRatio,self.c1c2Count,self.c1c2StockMargin) = self.calcRatiosAndMargins(c1Wc2L,c2Wc1L)

    # all the above but for stage matching
    if self.stage:
      (self.p1WinStageAll,self.p1AllStCount,self.p1StageMarginAll) = self.calcRatiosAndMargins(p1W,p1L,stage=True)
      (self.p2WinStageAll,self.p2AllStCount,self.p2StageMarginAll) = self.calcRatiosAndMargins(p2W,p2L,stage=True)
      (self.c1WinStageAll,self.c1AllStCount,self.c1StageMarginAll) = self.calcRatiosAndMargins(c1W&c1Notc2,c1L&c1Notc2,stage=True)
      (self.c2WinStageAll,self.c2AllStCount,self.c2StageMarginAll) = self.calcRatiosAndMargins(c2W&c1Notc2,c2L&c1Notc2,stage=True)
      (self.p1c1WinStageAll,self.p1c1AllStCount,self.p1c1StageMarginAll) = self.calcRatiosAndMargins(p1c1W,p1c1L,stage=True)
      (self.p2c2WinStageAll,self.p2c2AllStCount,self.p2c2StageMarginAll) = self.calcRatiosAndMargins(p2c2W,p2c2L,stage=True)
      (self.p1p2WinStage,self.p1p2StCount,self.p1p2StageMargin) = self.calcRatiosAndMargins(p1Wp2L,p2Wp1L,stage=True)
      (self.p1c2WinStage,self.p1c2StCount,self.p1c2StageMargin) = self.calcRatiosAndMargins(p1Wc2L,c2Wp1L,stage=True)
      (self.p2c1WinStage,self.p2c1StCount,self.p2c1StageMargin) = self.calcRatiosAndMargins(p2Wc1L,c1Wp2L,stage=True)
      (self.p1c1p2WinStage,self.p1c1p2StCount,self.p1c1p2StageMargin) = self.calcRatiosAndMargins(p1c1Wp2L,p2Wp1c1L,stage=True)
      (self.p1c1c2WinStage,self.p1c1c2StCount,self.p1c1c2StageMargin) = self.calcRatiosAndMargins(p1c1Wc2L,c2Wp1c1L,stage=True)
      (self.p2c2p1WinStage,self.p2c2p1StCount,self.p2c2p1StageMargin) = self.calcRatiosAndMargins(p2c2Wp1L,p1Wp2c2L,stage=True)
      (self.p2c2c1WinStage,self.p2c2c1StCount,self.p2c2c1StageMargin) = self.calcRatiosAndMargins(p2c2Wc1L,c1Wp2c2L,stage=True)
      (self.p1c1p2c2WinStage,self.p1c1p2c2StCount,self.p1c1p2c2StageMargin) = self.calcRatiosAndMargins(p1c1Wp2c2L,p2c2Wp1c1L,stage=True)
      (self.c1c2WinStage,self.c1c2StCount,self.c1c2StageMargin) = self.calcRatiosAndMargins(c1Wc2L,c2Wc1L,stage=True)

    '''
    Stats stuff to add:

    # a slider (or just buttons) to match to only today/this week/this month/this quarter/this year/all time

    '''

  def statString(self,ratio,margins,reverse=False):
    altRat, altMars = self.getAltStat(ratio,margins)
    rats = [ratio,altRat]
    mars = [margins[0],margins[1],margins[2],altMars[0],altMars[1],altMars[2]]

    stRats = []
    stMars = []
    for el in rats:
      if el == '----':
        stRats.append(el)
      else:
        stRats.append('%3.f%%' % el)

    for el in mars:
      if el == '----':
        stMars.append('%4s' % el)
      else:
        stMars.append('%+.2f' % el)
    if reverse:
      return '%4s:%4s  %5s/%5s/%5s' % (stRats[1],stRats[0],stMars[3],stMars[4],stMars[5])
    else:
      return '%4s:%4s  %5s/%5s/%5s' % (stRats[0],stRats[1],stMars[0],stMars[1],stMars[2])

  def getAltStat(self,ratio,margins):
    if ratio == '----':
      altRatio = '----'
    else:
      altRatio = 100-ratio

    altMargins = []
    for marg in margins:
      if marg == '----':
        altMargins.append('----')
      else:
        altMargins.append(-1*marg)

    altMargins = tuple([altMargins[1],altMargins[0],altMargins[2]])

    return altRatio,altMargins

  def attemptDiv(self,num,den):
    if den == 0:
      return '----'
    else:
      try:
        calc = num/den
        return calc
      except ZeroDivisionError:
        return '----'

  def DFfunc(self,row,attr,val):
    return row[attr] == val

  def calcRatiosAndMargins(self,wins,losses,stage=False):
    if stage == True:
      wins = wins&self.stageTrue
      losses = losses&self.stageTrue

    winCount = sum(wins)
    lossCount= sum(losses)
    totCount = winCount+lossCount
    winRatio = self.attemptDiv(winCount*100.,totCount)
    winMargin = self.attemptDiv(sum(wins*self.stockCount)*1.,winCount)
    lossMargin = self.attemptDiv(sum(losses*self.stockCount)*-1.,lossCount)
    allMargin = self.attemptDiv(sum(wins*self.stockCount)*1. - sum(losses*self.stockCount)*1.,totCount)

    return (winRatio,totCount,(winMargin,lossMargin,allMargin))

class DataWindow(Toplevel):
  def __init__(self, master,*args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in dir(Toplevel)}
    Toplevel.__init__(self, master, **di)

    self.file = kwargs['file']
    self.p1 = kwargs['p1']
    self.c1 = kwargs['c1']
    self.p2 = kwargs['p2']
    self.c2 = kwargs['c2']
    if 'stage' in kwargs.keys():
      self.stage = kwargs['stage']
    else:
      self.stage = ''

    if 'scale' in kwargs.keys():
      self.scale = kwargs['scale']
    else:
      self.scale = 1.
    
    self.bind_all('<Escape>',self.closeIt)
    self.bind_all('<Tab>',self.switchFrame)

    self.h = int(200*self.scale)
    self.w = int(1350*self.scale)
    
    self.colors = {'p1red':'#f55943','p2blue':'#7092be','p12blend':'#ac7886'}
    self.frMode = 1

    self.centerWindow(h=self.h,w=self.w)

    self.stats = Stats2P(file=self.file,p1=self.p1,c1=self.c1,p2=self.p2,c2=self.c2,stage=self.stage)

    self.hf = tkFont.Font(family="Times", size=int(14*self.scale), weight=tkFont.BOLD)
    self.bf = tkFont.Font(family="Times", size=int(12*self.scale))

    self.fr = Frame(self)
    self.fr.config(highlightbackground='#000',highlightthickness=4)
    self.topLabels = Frame(self.fr)
    self.subLabels = Frame(self.fr)
    self.allV = Frame(self.fr)
    self.p1V = Frame(self.fr)
    self.p1c1V = Frame(self.fr)
    self.c1V = Frame(self.fr)

    self.labelText = {}
    self.subLabelText = {}
    self.allVText = {}
    self.p1VText = {}
    self.p1c1VText = {}
    self.c1VText = {}

    if self.stage:
      self.fr2 = Frame(self)
      self.fr2.config(highlightbackground='#000',highlightthickness=4)
      self.topLabels2 = Frame(self.fr2)
      self.subLabels2 = Frame(self.fr2)
      self.allV2 = Frame(self.fr2)
      self.p1V2 = Frame(self.fr2)
      self.p1c1V2 = Frame(self.fr2)
      self.c1V2 = Frame(self.fr2)
      self.labelText2 = {}
      self.subLabelText2 = {}
      self.allVText2 = {}
      self.p1VText2 = {}
      self.p1c1VText2 = {}
      self.c1VText2 = {}

    for i in range(5):
      if i == 0:
        wid = 15
      else:
        wid = 28

      self.labelText[i] = Text(self.topLabels,height=1,width=wid,highlightthickness=2,relief=FLAT,font=self.hf)
      self.subLabelText[i] = Text(self.subLabels,height=1,width=wid,highlightthickness=2,relief=FLAT,font=self.hf)
      self.allVText[i] = Text(self.allV,height=1,width=wid,highlightthickness=2,font=self.bf)
      self.p1VText[i] = Text(self.p1V,height=1,width=wid,highlightthickness=2,font=self.bf)
      self.p1c1VText[i] = Text(self.p1c1V,height=1,width=wid,highlightthickness=2,font=self.bf)
      self.c1VText[i] = Text(self.c1V,height=1,width=wid,highlightthickness=2,font=self.bf)

      if self.stage:
        self.labelText2[i] = Text(self.topLabels2,height=1,width=wid,highlightthickness=2,relief=FLAT,font=self.hf)
        self.subLabelText2[i] = Text(self.subLabels2,height=1,width=wid,highlightthickness=2,relief=FLAT,font=self.hf)
        self.allVText2[i] = Text(self.allV2,height=1,width=wid,highlightthickness=2,font=self.bf)
        self.p1VText2[i] = Text(self.p1V2,height=1,width=wid,highlightthickness=2,font=self.bf)
        self.p1c1VText2[i] = Text(self.p1c1V2,height=1,width=wid,highlightthickness=2,font=self.bf)
        self.c1VText2[i] = Text(self.c1V2,height=1,width=wid,highlightthickness=2,font=self.bf)
    
    self.labelText[2].config(highlightbackground=self.colors['p2blue'])
    self.labelText[3].config(highlightbackground=self.colors['p2blue'])
    if self.stage:
      self.labelText2[2].config(highlightbackground=self.colors['p2blue'])
      self.labelText2[3].config(highlightbackground=self.colors['p2blue'])

    self.p1VText[0].config(highlightbackground=self.colors['p1red'],font=self.hf)
    self.p1c1VText[0].config(highlightbackground=self.colors['p1red'],font=self.hf)
    self.allVText[2].config(highlightbackground=self.colors['p2blue'])
    self.allVText[3].config(highlightbackground=self.colors['p2blue'])
    self.p1VText[1].config(highlightbackground=self.colors['p1red'])
    self.p1VText[2].config(highlightbackground=self.colors['p12blend'])
    self.p1VText[3].config(highlightbackground=self.colors['p2blue'])
    self.p1c1VText[1].config(highlightbackground=self.colors['p1red'])
    self.p1c1VText[2].config(highlightbackground=self.colors['p1red'])
    self.p1c1VText[3].config(highlightbackground=self.colors['p12blend'])
    self.allVText[0].config(font=self.hf)
    self.p1VText[0].config(font=self.hf)
    self.p1c1VText[0].config(font=self.hf)
    self.c1VText[0].config(font=self.hf)

    if self.stage:
      self.p1VText2[0].config(highlightbackground=self.colors['p1red'],font=self.hf)
      self.p1c1VText2[0].config(highlightbackground=self.colors['p1red'],font=self.hf)
      self.allVText2[2].config(highlightbackground=self.colors['p2blue'])
      self.allVText2[3].config(highlightbackground=self.colors['p2blue'])
      self.p1VText2[1].config(highlightbackground=self.colors['p1red'])
      self.p1VText2[2].config(highlightbackground=self.colors['p12blend'])
      self.p1VText2[3].config(highlightbackground=self.colors['p2blue'])
      self.p1c1VText2[1].config(highlightbackground=self.colors['p1red'])
      self.p1c1VText2[2].config(highlightbackground=self.colors['p1red'])
      self.p1c1VText2[3].config(highlightbackground=self.colors['p12blend'])
      self.allVText2[0].config(font=self.hf)
      self.p1VText2[0].config(font=self.hf)
      self.p1c1VText2[0].config(font=self.hf)
      self.c1VText2[0].config(font=self.hf)

    self.labelText[0].insert(END,'{:<14}'.format('P1, C1\ P2, C2'))
    self.labelText[1].insert(END,'vs. all : ')
    self.labelText[2].insert(END,'vs. %s : ' % (self.p2))
    self.labelText[3].insert(END,'vs. %s + %s: ' % (self.p2,self.c2))
    self.labelText[4].insert(END,'vs. %s :' % (self.c2))

    self.subLabelText[0].insert(END,'{:<14}'.format('------------------'))
    self.subLabelText[1].insert(END,'all data')
    self.subLabelText[2].insert(END,'all data')
    self.subLabelText[3].insert(END,'all data')
    self.subLabelText[4].insert(END,'all data')

    self.allVText[0].insert(END,'{:<14}'.format('all:'))
    self.allVText[1].insert(END,'-----------------  /%dx logged games' % self.stats.allCount)
    self.allVText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2WinRatioAll,self.stats.p2StockMarginAll,reverse=True),self.stats.p2AllCount))
    self.allVText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2WinRatioAll,self.stats.p2c2StockMarginAll,reverse=True),self.stats.p2c2AllCount))
    self.allVText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c2WinRatioAll,self.stats.c2StockMarginAll,reverse=True),self.stats.c2AllCount))

    self.p1VText[0].insert(END,'{:<14}'.format(self.p1))
    self.p1VText[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1WinRatioAll,self.stats.p1StockMarginAll),self.stats.p1AllCount))
    self.p1VText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1p2WinRatio,self.stats.p1p2StockMargin),self.stats.p1p2Count))
    self.p1VText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2p1WinRatio,self.stats.p2c2p1StockMargin,reverse=True),self.stats.p2c2p1Count))
    self.p1VText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c2WinRatio,self.stats.p1c2StockMargin),self.stats.p1c2Count))

    self.p1c1VText[0].insert(END,'{0:<6}{1:<1}{2:<8}'.format(self.p1,'+',self.c1))
    self.p1c1VText[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1WinRatioAll,self.stats.p1c1StockMarginAll),self.stats.p1c1AllCount))
    self.p1c1VText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2WinRatio,self.stats.p1c1p2StockMargin),self.stats.p1c1p2Count))
    self.p1c1VText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2c2WinRatio,self.stats.p1c1p2c2StockMargin),self.stats.p1c1p2c2Count))
    self.p1c1VText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1c2WinRatio,self.stats.p1c1c2StockMargin),self.stats.p1c1c2Count))

    self.c1VText[0].insert(END,'{:<14}'.format(self.c1))
    self.c1VText[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1WinRatioAll,self.stats.c1StockMarginAll),self.stats.c1AllCount))
    self.c1VText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c1WinRatio,self.stats.p2c1StockMargin,reverse=True),self.stats.p2c1Count))
    self.c1VText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2c1WinRatio,self.stats.p2c2c1StockMargin,reverse=True),self.stats.p2c2c1Count))
    self.c1VText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1c2WinRatio,self.stats.c1c2StockMargin),self.stats.c1c2Count))

    if self.stage:
      self.labelText2[0].insert(END,'{:<14}'.format('P1, C1\ P2, C2'))
      self.labelText2[1].insert(END,'vs. all : ')
      self.labelText2[2].insert(END,'vs. %s : ' % (self.p2))
      self.labelText2[3].insert(END,'vs. %s + %s: ' % (self.p2,self.c2))
      self.labelText2[4].insert(END,'vs. %s :' % (self.c2))

      self.subLabelText2[0].insert(END,'{:<14}'.format('------------------'))
      self.subLabelText2[1].insert(END,'this stage')
      self.subLabelText2[2].insert(END,'this stage')
      self.subLabelText2[3].insert(END,'this stage')
      self.subLabelText2[4].insert(END,'this stage')

      self.allVText2[0].insert(END,'{:<14}'.format('all:'))
      self.allVText2[1].insert(END,'-----------------  /%dx logged games' % self.stats.stageCount)
      self.allVText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2WinStageAll,self.stats.p2StageMarginAll,reverse=True),self.stats.p2AllStCount))
      self.allVText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2WinStageAll,self.stats.p2c2StageMarginAll,reverse=True),self.stats.p2c2AllStCount))
      self.allVText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c2WinStageAll,self.stats.c2StageMarginAll,reverse=True),self.stats.c2AllStCount))

      self.p1VText2[0].insert(END,'{:<14}'.format(self.p1))
      self.p1VText2[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1WinStageAll,self.stats.p1StageMarginAll),self.stats.p1AllStCount))
      self.p1VText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1p2WinStage,self.stats.p1p2StageMargin),self.stats.p1p2StCount))
      self.p1VText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2p1WinStage,self.stats.p2c2p1StageMargin,reverse=True),self.stats.p2c2p1StCount))
      self.p1VText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c2WinStage,self.stats.p1c2StageMargin),self.stats.p1c2StCount))

      self.p1c1VText2[0].insert(END,'{0:<6}{1:<1}{2:<8}'.format(self.p1,'+',self.c1))
      self.p1c1VText2[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1WinStageAll,self.stats.p1c1StageMarginAll),self.stats.p1c1AllStCount))
      self.p1c1VText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2WinStage,self.stats.p1c1p2StageMargin),self.stats.p1c1p2StCount))
      self.p1c1VText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2c2WinStage,self.stats.p1c1p2c2StageMargin),self.stats.p1c1p2c2StCount))
      self.p1c1VText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1c2WinStage,self.stats.p1c1c2StageMargin),self.stats.p1c1c2StCount))

      self.c1VText2[0].insert(END,'{:<14}'.format(self.c1))
      self.c1VText2[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1WinStageAll,self.stats.c1StageMarginAll),self.stats.c1AllStCount))
      self.c1VText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c1WinStage,self.stats.p2c1StageMargin,reverse=True),self.stats.p2c1StCount))
      self.c1VText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2c1WinStage,self.stats.p2c2c1StageMargin,reverse=True),self.stats.p2c2c1StCount))
      self.c1VText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1c2WinStage,self.stats.c1c2StageMargin),self.stats.c1c2StCount))

    self.initUI()

  def initUI(self):
    self.fr.place(relx=0.5,rely=0.5, anchor=CENTER)
    self.subLabels.pack(side=TOP,fill=BOTH)
    self.topLabels.pack(side=TOP,fill=BOTH)
    self.allV.pack(side=TOP,fill=BOTH)
    self.p1V.pack(side=TOP,fill=BOTH)
    self.p1c1V.pack(side=TOP,fill=BOTH)
    self.c1V.pack(side=TOP,fill=BOTH)

    for i in range(5):
      self.labelText[i].grid(row=0,column=i,columnspan=1,sticky=N+S+E+W)
      self.subLabelText[i].grid(row=1,column=i,columnspan=1,sticky=N+S+E+W)
      self.allVText[i].grid(row=2,column=i,columnspan=1,sticky=N+S+E+W)
      self.p1VText[i].grid(row=3,column=i,columnspan=1,sticky=N+S+E+W)
      self.p1c1VText[i].grid(row=4,column=i,columnspan=1,sticky=N+S+E+W)
      self.c1VText[i].grid(row=5,column=i,columnspan=1,sticky=N+S+E+W)

    for el in [self.subLabels,self.topLabels,self.allV,self.p1V,self.p1c1V,self.c1V]:
      el.columnconfigure(0, weight=1)
      el.columnconfigure(1, weight=4)
      el.columnconfigure(2, weight=4)
      el.columnconfigure(3, weight=4)
      el.columnconfigure(4, weight=4)

    # if stage chosen
    if self.stage:
      self.fr2.place(relx=0.5,rely=0.5, anchor=CENTER)
      self.subLabels2.pack(side=TOP,fill=BOTH)
      self.topLabels2.pack(side=TOP,fill=BOTH)
      self.allV2.pack(side=TOP,fill=BOTH)
      self.p1V2.pack(side=TOP,fill=BOTH)
      self.p1c1V2.pack(side=TOP,fill=BOTH)
      self.c1V2.pack(side=TOP,fill=BOTH)

      for i in range(5):
        self.labelText2[i].grid(row=0,column=i,columnspan=1,sticky=N+S+E+W)
        self.subLabelText2[i].grid(row=1,column=i,columnspan=1,sticky=N+S+E+W)
        self.allVText2[i].grid(row=2,column=i,columnspan=1,sticky=N+S+E+W)
        self.p1VText2[i].grid(row=3,column=i,columnspan=1,sticky=N+S+E+W)
        self.p1c1VText2[i].grid(row=4,column=i,columnspan=1,sticky=N+S+E+W)
        self.c1VText2[i].grid(row=5,column=i,columnspan=1,sticky=N+S+E+W)

      for el in [self.subLabels2,self.topLabels2,self.allV2,self.p1V2,self.p1c1V2,self.c1V2]:
        el.columnconfigure(0, weight=1)
        el.columnconfigure(1, weight=4)
        el.columnconfigure(2, weight=4)
        el.columnconfigure(3, weight=4)
        el.columnconfigure(4, weight=4)

    self.fr.lift()
    self.focus_force()

  def centerWindow(self,w=500, h=200):
    # get screen width and height
    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    self.geometry('%dx%d+%d+%d' % (w, h, x, y))

  def closeIt(self,event):
    for widget in self.winfo_children():
      widget.destroy()

    self.unbind_all('<Escape>')
    self.unbind_all('<Tab>')

    self.destroy()

  def switchFrame(self,event):
    if self.stage:
      if self.frMode:
        self.frMode = 0
        self.fr2.lift()
        self.focus_force()
      else:
        self.frMode = 1
        self.fr.lift()
        self.focus_force()

  def textAssign(self,values):
    co = 0
    ret = []
    for val in values:
      if str(val) == 'nan':
        ret.append('nan')
      else:
        if co%2 == 0:
          ret.append(100-int(val))
        else:
          ret.append(-int(val))
      co=co+1

    return ret

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
    #self.statBar1.grid(row=1,column=0,sticky=N+E+W+S)
    #self.statBar2.grid(row=2,column=0,sticky=N+E+W+S)
    #self.statBar3.grid(row=3,column=0,sticky=N+E+W+S)
    self.statBar1.grid(row=0,column=1,sticky=N+E+W+S)
    self.statBar2.grid(row=0,column=2,sticky=N+E+W+S)
    self.statBar3.grid(row=0,column=3,sticky=N+E+W+S)
    self.grid_columnconfigure(0,minsize=int(150*self.scale))
    self.grid_columnconfigure(1,minsize=int(325*self.scale))
    self.grid_columnconfigure(2,minsize=int(325*self.scale))
    self.grid_columnconfigure(3,minsize=int(325*self.scale))

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

    self.fn = tkFont.Font(family="Times", size=int(12*master.scale))
    self.label = Label(self, bd=1, height=2, relief=SUNKEN, anchor=CENTER,font=self.fn)
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

def onClosing():
  for widget in top.winfo_children():
    widget.destroy()

  top.destroy()

def timeNow():
  t = datetime.now()
  return t.strftime('%Y%m%d%H%M')

def main(**kwargs):
  if 'scaleWindow' in kwargs:
    scaleWindow = kwargs['scaleWindow']
    if not(scaleWindow in ['large','medium','small']):
      scaleWindow = 'medium'
  else: 
    scaleWindow = 'medium'
  global top
  top = MainWindow(scaleWindow=scaleWindow)
  top.protocol("WM_DELETE_WINDOW", onClosing)
  top.focus_force()
  top.lift()
  top.mainloop()

if __name__ == '__main__':
  main()