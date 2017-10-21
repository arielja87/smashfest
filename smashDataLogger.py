#!/usr/bin/env python

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

    # Window dimension (pixels)
    self.config(bg='#fff')
    self.w = 1200
    self.h = 650
    self.centerWindow(self.w,self.h)
    self.colors = {'p1red':'#f55943','p2blue':'#7092be','pListGreen':'#77c18b'}
    self.playerToggle = 1
    self.dataFileName = 'smashStats.csv'
    #self.dataFileName = 'junkStats.csv'
    self.dataLoaded = 0     # haven't loaded yet

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

    #images of character faces and icons
    self.faceImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Faces','%s.gif')) % el)) for el in self.characters if el != 'Logo'}\

    self.P1 = PlayerHeadWindow(self,PNUM=1,FACES=self.faceImgs,BORDERCOLOR=self.colors['p1red'],bg='#fff')
    self.P2 = PlayerHeadWindow(self,PNUM=2,FACES=self.faceImgs,BORDERCOLOR=self.colors['p2blue'],bg='#fff')
    self.Ps = PlayerListWindow(self,BORDERCOLOR=self.colors['pListGreen'],bg='#fff')
    self.mainCanv = SelectionWindow(self,bg='#fff',highlightthickness=0)

    self.initUI()

    self.bind_all('<Tab>',self.modeSwitch)
    self.bind_all('<Escape>',self.reset)
    self.bind_all('<Up>',self.scrollUpP1)
    self.bind_all('<Down>',self.scrollDownP1)
    self.bind_all('<Control-Up>',self.scrollUpP2)
    self.bind_all('<Control-Down>',self.scrollDownP2)

    self.mainCanv.charTraceP1.trace('w',self.setCharacSoftP1)
    self.mainCanv.charLockP1.trace('w',self.setCharacHardP1)
    self.mainCanv.charTraceP2.trace('w',self.setCharacSoftP2)
    self.mainCanv.charLockP2.trace('w',self.setCharacHardP2)
    self.mainCanv.lockInWin.trace('w',self.publishMatch)

    #self.getMatchupData('Sean','CaptainFalcon','Torben','CaptainFalcon','pokemonStadium2')

  def initUI(self):
    self.P1.grid(row=0,column=0,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.P2.grid(row=2,column=0,rowspan=2,columnspan=1,sticky=N+S+E+W)
    self.Ps.grid(row=4,column=0,rowspan=4,columnspan=1,sticky=N+S+E+W)
    self.mainCanv.grid(row=0,column=1,rowspan=8,columnspan=4,sticky=N+S+E+W)
    self.mainCanv.focus_force()

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

  def pSwitch(self,event=''):
      if self.playerToggle == 1:
        self.playerToggle = 2
        self.P1.kickCharacter(mode='soft') #so switching mode mid-hover doesn't leave a char-head lingering
      elif self.playerToggle == 2:
        self.playerToggle = 1
        self.P2.kickCharacter(mode='soft') #so switching mode mid-hover doesn't leave a char-head lingering

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
        text = "%s's %s %s %s's %s on %s" % (pWin,cWin,'>'*n,pLose,cLose,stage)
        tkMessageBox.showinfo('Logged',text) 
        self.reset()
      else:
        self.mainCanv.kickHeads()

  def logIt(self,winner,winnerChar,loser,loserChar,stockMargin,stage):
    # create a standard data frame, and append this match to a battleData file
    cols = ['WinningPlayer','WinningCharacter','LosingPlayer','LosingCharacter','StockCount','Stage']
    df = pd.DataFrame([[winner,winnerChar,loser,loserChar,stockMargin,stage]],columns=cols,index=[[timeNow()]])

    with open(self.dataFileName,'a') as f:
      df.to_csv(f, header=False)

    f.close()

  def attemptDiv(self,num,den):
    try:
      calc = num/den
      return calc
    except ZeroDivisionError:
      return 'No data'

  def DFfunc(self,row,attr,val):
    return row[attr] == val

  def getMatchupData(self,p1,c1,p2,c2,stage,refresh=True):
    # load the battle data file and search over a set of conditions
    # match win ratio player-to-player
    # match win ratio character-to-character
    # % of matches p1/p2 wins with that char, across all data
    # % of matches p1/p2 wins on that stage, across all data
    # total stock margin vs win percentage: i.e. do they win many close and lose few by a lot?
    wp = 'WinningPlayer'
    wc = 'WinningCharacter'
    lp = 'LosingPlayer'
    lc = 'LosingCharacter'
    sc = 'StockCount'
    st = 'Stage'
    if refresh or not(self.dataLoaded):
      self.data = pd.read_csv(self.dataFileName)
      self.dataLoaded = 1

    # data frames for individual config matching
    # e.g. p1W will give a bool-valued dataFrame with True where each row has the
    # winning player (wp) == player 1 (p1)

    p1W = self.data.apply(self.DFfunc,axis=1,args=(wp,p1)) 
    p2W = self.data.apply(self.DFfunc,axis=1,args=(wp,p2)) 
    p1L = self.data.apply(self.DFfunc,axis=1,args=(lp,p1)) 
    p2L = self.data.apply(self.DFfunc,axis=1,args=(lp,p2)) 
    c1W = self.data.apply(self.DFfunc,axis=1,args=(wc,c1)) 
    c2W = self.data.apply(self.DFfunc,axis=1,args=(wc,c2)) 
    c1L = self.data.apply(self.DFfunc,axis=1,args=(lc,c1)) 
    c2L = self.data.apply(self.DFfunc,axis=1,args=(lc,c2)) 
    stageTrue = self.data.apply(self.DFfunc,axis=1,args=(st,stage)) 
    stockCount= self.data[sc]

    # intersections
    p1c1W = p1W&c1W
    p1c1L = p1L&c1L
    p2c2W = p2W&c2W
    p2c2L = p2L&c2L
    p1Wp2L = p1W&p2L
    p2Wp1L = p2W&p1L
    p1c1Wp2c2L = p1W&c1W&p2L&c2L
    p2c2Wp1c1L = p2W&c2W&p1L&c1L

    c1Wc2L = c1W&c2L
    c2Wc1L = c2W&c1L

    # match counts
    p1Count = sum([sum(p1W),sum(p1L)])
    p2Count = sum([sum(p2W),sum(p2L)])
    p1c1Count = sum([sum(p1c1W),sum(p1c1L)])
    p2c2Count = sum([sum(p2c2W),sum(p2c2L)])
    p1p2Count = sum([sum(p1Wp2L),sum(p2Wp1L)])
    p1c1p2c2Count = sum([sum(p1c1Wp2c2L),sum(p2c2Wp1c1L)])

    c1Count = sum([sum(c1W),sum(c1L)])
    c2Count = sum([sum(c2W),sum(c2L)])
    c1c2Count = sum([sum(c1Wc2L),sum(c2Wc1L)])

    p1StCount = sum([sum(p1W&stageTrue),sum(p1L&stageTrue)])
    p2StCount = sum([sum(p2W&stageTrue),sum(p2L&stageTrue)])
    p1c1StCount = sum([sum(p1c1W&stageTrue),sum(p1c1L&stageTrue)])
    p2c2StCount = sum([sum(p2c2W&stageTrue),sum(p2c2L&stageTrue)])
    p1p2StCount = sum([sum(p1Wp2L&stageTrue),sum(p2Wp1L&stageTrue)])
    p1c1p2c2StCount = sum([sum(p1c1Wp2c2L&stageTrue),sum(p2c2Wp1c1L&stageTrue)])

    c1StCount = sum([sum(c1W&stageTrue),sum(c1L&stageTrue)])
    c2StCount = sum([sum(c2W&stageTrue),sum(c2L&stageTrue)])
    c1c2StCount = sum([sum(c1Wc2L&stageTrue),sum(c2Wc1L&stageTrue)])

    #win ratios
    #player specific
    self.p1WinRatioAll = self.attemptDiv(sum(p1W)*100.,p1Count)
    self.p2WinRatioAll = self.attemptDiv(sum(p2W)*100.,p2Count)
    self.p1StockMarginAll = self.attemptDiv(sum(p1W*stockCount)*1. - sum(p1L*stockCount)*1.,p1Count)
    self.p2StockMarginAll = self.attemptDiv(sum(p2W*stockCount)*1. - sum(p2L*stockCount)*1.,p2Count)

    self.p1c1WinRatio = self.attemptDiv(sum(p1c1W)*100.,p1c1Count)
    self.p2c2WinRatio = self.attemptDiv(sum(p2c2W)*100.,p2c2Count)
    self.p1c1StockMargin = self.attemptDiv(sum(p1c1W*stockCount)*1. - sum(p1c1L*stockCount)*1.,p1c1Count)
    self.p2c2StockMargin = self.attemptDiv(sum(p2c2W*stockCount)*1. - sum(p2c2L*stockCount)*1.,p2c2Count)

    self.p1p2WinRatio = self.attemptDiv(sum(p1Wp2L)*100.,p1p2Count)
    self.p1c1p2c2WinRatio = self.attemptDiv(sum(p1c1Wp2c2L)*100.,p1c1p2c2Count)
    self.p1p2StockMargin = self.attemptDiv(sum(p1Wp2L*stockCount)*1. - sum(p2Wp1L*stockCount)*1.,p1p2Count)
    self.p1c1p2c2StockMargin = self.attemptDiv(sum(p1c1Wp2c2L*stockCount)*1. - sum(p2c2Wp1c1L*stockCount)*1.,p1c1p2c2Count)
    # if the data exists for each of the above, the opposite ratio is just 100 - this one

    #character specific
    self.c1WinRatioAll = self.attemptDiv(sum(c1W)*100.,c1Count)
    self.c2WinRatioAll = self.attemptDiv(sum(c2W)*100.,c2Count)
    self.c1StockMarginAll = self.attemptDiv(sum(c1W*stockCount)*1. - sum(c1L*stockCount)*1.,c1Count)
    self.c2StockMarginAll = self.attemptDiv(sum(c2W*stockCount)*1. - sum(c2L*stockCount)*1.,c2Count)

    self.c1c2WinRatio = self.attemptDiv(sum(c1Wc2L)*100.,c1c2Count)
    self.c1c2StockMargin = self.attemptDiv(sum(c1Wc2L*stockCount)*1. - sum(c2Wc1L*stockCount)*1.,c1c2Count)

    '''
    Stats stuff to add:

    # add player# + character# v. all stats for each p+c
    # a slider (or just buttons) to match to only today/this week/this month/this quarter/this year/all time

    '''

    #stage specific 
    # basically just cross stage into the data for extra measure
    self.p1WinStageAll = self.attemptDiv(sum(p1W&stageTrue)*100.,p1StCount)
    self.p2WinStageAll = self.attemptDiv(sum(p2W&stageTrue)*100.,p2StCount)
    self.p1StageMarginAll = self.attemptDiv(sum((p1W&stageTrue)*stockCount)*1. - sum((p1L&stageTrue)*stockCount)*1.,p1StCount)
    self.p2StageMarginAll = self.attemptDiv(sum((p2W&stageTrue)*stockCount)*1. - sum((p2L&stageTrue)*stockCount)*1.,p2StCount)

    self.p1c1WinStage = self.attemptDiv(sum(p1c1W&stageTrue)*100.,p1c1StCount)
    self.p2c2WinStage = self.attemptDiv(sum(p2c2W&stageTrue)*100.,p2c2StCount)
    self.p1c1StageMargin = self.attemptDiv(sum((p1c1W&stageTrue)*stockCount)*1. - sum((p1c1L&stageTrue)*stockCount)*1.,p1c1StCount)
    self.p2c2StageMargin = self.attemptDiv(sum((p2c2W&stageTrue)*stockCount)*1. - sum((p2c2L&stageTrue)*stockCount)*1.,p2c2StCount)

    self.p1p2WinStage = self.attemptDiv(sum(p1Wp2L&stageTrue)*100.,p1p2StCount)
    self.p1c1p2c2WinStage = self.attemptDiv(sum(p1c1Wp2c2L&stageTrue)*100.,p1c1p2c2StCount)
    self.p1p2StageMargin = self.attemptDiv(sum((p1Wp2L&stageTrue)*stockCount)*1. - sum((p2Wp1L&stageTrue)*stockCount)*1.,p1p2StCount)
    self.p1c1p2c2StageMargin = self.attemptDiv(sum((p1c1Wp2c2L&stageTrue)*stockCount)*1. - sum((p2c2Wp1c1L&stageTrue)*stockCount)*1.,p1c1p2c2StCount)
    # if the data exists for each of the above, the opposite Stage is just 100 - this one

    #character specific
    self.c1WinStageAll = self.attemptDiv(sum(c1W&stageTrue)*100.,c1StCount)
    self.c2WinStageAll = self.attemptDiv(sum(c2W&stageTrue)*100.,c2StCount)
    self.c1StageMarginAll = self.attemptDiv(sum((c1W&stageTrue)*stockCount)*1. - sum((c1L&stageTrue)*stockCount)*1.,c1StCount)
    self.c2StageMarginAll = self.attemptDiv(sum((c2W&stageTrue)*stockCount)*1. - sum((c2L&stageTrue)*stockCount)*1.,c2StCount)

    self.c1c2WinStage = self.attemptDiv(sum(c1Wc2L&stageTrue)*100.,c1c2StCount)
    self.c1c2StageMargin = self.attemptDiv(sum((c1Wc2L&stageTrue)*stockCount)*1. - sum((c2Wc1L&stageTrue)*stockCount)*1.,c1c2StCount)

    self.dataWin = DataWindow(self,p1=p1,p2=p2,c1=c1,c2=c2,stage=stage)
    self.dataWin.place(relx=0.5, rely=0.5, anchor=CENTER)
    self.dataWin.focus_force()


    '''
    print('p1 win ratio %2f, %.2f margin' % (p1WinRatioAll,p1StockMarginAll))
    print('p2 win ratio %2f, %.2f margin' % (p2WinRatioAll,p2StockMarginAll))
    print('p1 v p2 ratio %2f, %.2f margin' % (p1p2WinRatio,p1p2StockMargin))
    print('p1c1 win ratio %2f, %.2f margin' % (p1c1WinRatio,p1c1StockMargin))
    print('p2c2 win ratio %2f, %.2f margin' % (p2c2WinRatio,p2c2StockMargin))
    print('p1c1 v p2c2 ratio %2f, %.2f margin' % (p1c1p2c2WinRatio,p1c1p2c2StockMargin))

    print('c1 wins %2f, %.2f margin' % (c1WinRatioAll,c1StockMarginAll))
    print('c2 wins %2f, %.2f margin' % (c2WinRatioAll,c2StockMarginAll))
    print('c1 v c2 ratio %2f, %.2f margin' % (c1c2WinRatio,c1c2StockMargin))

    print '\n\n'

    print('p1 win ratio %2f, %.2f margin, stage true' % (p1WinStageAll,p1StageMarginAll))
    print('p2 win ratio %2f, %.2f margin, stage true' % (p2WinStageAll,p2StageMarginAll))
    print('p1 v p2 ratio %2f, %.2f margin, stage true' % (p1p2WinStage,p1p2StageMargin))
    print('p1c1 win ratio %2f, %.2f margin, stage true' % (p1c1WinStage,p1c1StageMargin))
    print('p2c2 win ratio %2f, %.2f margin, stage true' % (p2c2WinStage,p2c2StageMargin))
    print('p1c1 v p2c2 ratio %2f, %.2f margin, stage true' % (p1c1p2c2WinStage,p1c1p2c2StageMargin))

    print('c1 wins %2f, %.2f margin, stage true' % (c1WinStageAll,c1StageMarginAll))
    print('c2 wins %2f, %.2f margin, stage true' % (c2WinStageAll,c2StageMarginAll))
    print('c1 v c2 ratio %2f, %.2f margin, stage true' % (c1c2WinStage,c1c2StageMargin))
    '''

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
    self.px = 50
    self.py = 40
    self.pW = self.px*2
    self.pH = self.py*2

    self.ft = tkFont.Font(family="Times", size=24, weight=tkFont.BOLD, slant=tkFont.ITALIC)
    self.fn = tkFont.Font(family="Times", size=28, weight=tkFont.BOLD)

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
    self.nameH = 320
    self.nameW = 130

    #fonts
    self.ft = tkFont.Font(family="Times", size=24, weight=tkFont.BOLD, slant=tkFont.ITALIC)
    self.fn = tkFont.Font(family="Times", size=16, weight=tkFont.BOLD)

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

    #self.PnamesBoxFrame.pack(side=TOP)
    #self.PnamesCanv.place()

class SelectionWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)
    
    #dimensions
    self.canH = 598
    self.canW = 900
    self.scaleX = self.canW/1183.
    self.scaleY = self.canH/787.
    self.sx = 792
    self.sy = 497
    
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

    #current mode options
    self.toggleMode = StringVar(self)
    self.toggleMode.set('char')
    self.stockCount = StringVar(self)
    self.stockCount.set('')
    self.readyForStock = False
    self.lockInWin = BooleanVar(self)
    self.lockInWin.set(False)

    self.characters = master.characters
    self.stages = master.stages
    self.P1 = StringVar(self)
    self.P2 = StringVar(self)
    self.char1 = StringVar(self)
    self.char2 = StringVar(self)
    self.stage = StringVar(self)

    #canvas where all the action happens
    self.charStageStock = Canvas(self,height=self.canH,width=self.canW,bg='#fff')
    self.iconImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Thumbs','%s.jpg')) % el)) for el in self.characters if el != 'QuestionMark'}
    self.stageImgs = {el:PhotoImage(file = os.path.join('.','Stages','%s.gif') % el) for el in self.stages}

    #actual images
    self.charImg = ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Banners','charBanner.jpg'))))
    self.charStageStock.create_image(self.canW/2,self.canH/2,image=self.charImg,tags='charButton')
    self.stagImg = ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Banners','stageBanner.jpg'))))
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
    if all([el.get() for el in [self.P1,self.P2,self.char1,self.char2,self.stage]]):
      self.readyForStock = True
    else:
      self.readyForStock = False

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


class DataWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)

    self.p1 = kwargs['p1']
    self.p2 = kwargs['p2']
    self.c1 = kwargs['c1']
    self.c2 = kwargs['c2']
    self.stage = kwargs['stage']

    self.bind_all('<Escape>',self.closeIt)
    self.config(height=70,width=500)

    self.fr = Frame(self)
    self.fr.config(highlightbackground='#000',highlightthickness=4)
    self.labels = Frame(self.fr)
    self.stageLab = Frame(self.fr)
    self.allData= Frame(self.fr)
    self.pData = Frame(self.fr)
    self.pcData = Frame(self.fr)
    self.cData = Frame(self.fr)

    self.labText = {}
    self.stgText = {}
    self.allText = {}
    self.pText = {}
    self.pcText = {}
    self.cText = {}

    for i in range(5):
      if i == 0:
        wid = 15
        col = '#fff'
      else:
        wid = 32
        col = master.colors['p1red']

      self.labText[i] = Text(self.labels,height=1,width=wid)
      self.stgText[i] = Text(self.stageLab,height=1,width=wid)
      self.allText[i] = Text(self.allData,height=1,width=wid)
      self.pText[i] = Text(self.pData,height=1,width=wid)
      self.pcText[i] = Text(self.pcData,height=1,width=wid)
      self.cText[i] = Text(self.cData,height=1,width=wid)

      self.labText[i].config(highlightbackground='#fff',highlightthickness=2)
      self.stgText[i].config(highlightbackground='#fff',highlightthickness=2)
      self.allText[i].config(highlightbackground=col,highlightthickness=2)

      if i in [0,1,3]:
        self.pText[i].config(highlightbackground=col,highlightthickness=2)
        self.pcText[i].config(highlightbackground=col,highlightthickness=2)
      else:
        self.pText[i].config(highlightbackground='#fff',highlightthickness=2)
        self.pcText[i].config(highlightbackground="#fff",highlightthickness=2)

      if i in [0,2,4]:
        self.cText[i].config(highlightbackground=col,highlightthickness=2)
      else:
        self.cText[i].config(highlightbackground='#fff',highlightthickness=2)

    self.labText[0].insert(END,'Categ. \ Fight')
    self.labText[1].insert(END,'P1 :      %.15s' % (self.p1))
    self.labText[2].insert(END,'C1 :      %.15s' % (self.c1))
    self.labText[3].insert(END,'P2 :      %.15s' % (self.p2))
    self.labText[4].insert(END,'C2 :      %.15s' % (self.c2))

    self.stgText[1].insert(END,'all data       /      this stage')
    self.stgText[2].insert(END,'all data       /      this stage')
    self.stgText[3].insert(END,'all data       /      this stage')
    self.stgText[4].insert(END,'all data       /      this stage')

    self.allText[0].insert(END,'?? vs. all')
    self.allText[1].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.p1WinRatioAll,master.p1StockMarginAll,master.p1WinStageAll,master.p1StageMarginAll))
    self.allText[2].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.c1WinRatioAll,master.c1StockMarginAll,master.c1WinStageAll,master.c1StageMarginAll))
    self.allText[3].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.p2WinRatioAll,master.p2StockMarginAll,master.p2WinStageAll,master.p2StageMarginAll))
    self.allText[4].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.c2WinRatioAll,master.c2StockMarginAll,master.c2WinStageAll,master.c2StageMarginAll))

    self.pText[0].insert(END,'p v p')
    self.pText[1].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.p1p2WinRatio,master.p1p2StockMargin,master.p1p2WinStage,master.p1p2StageMargin))
    vals = self.textAssign([master.p1p2WinRatio,master.p1p2StockMargin,master.p1p2WinStage,master.p1p2StageMargin])
    self.pText[3].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (vals[0],vals[1],vals[2],vals[3]))

    self.pcText[0].insert(END,'p+c v p+c')
    self.pcText[1].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.p1c1p2c2WinRatio,master.p1c1p2c2StockMargin,master.p1c1p2c2WinStage,master.p1c1p2c2StageMargin))
    vals = self.textAssign([master.p1c1p2c2WinRatio,master.p1c1p2c2StockMargin,master.p1c1p2c2WinStage,master.p1c1p2c2StageMargin])
    self.pcText[3].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (vals[0],vals[1],vals[2],vals[3]))

    self.cText[0].insert(END,'c v c')
    self.cText[2].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (master.c1c2WinRatio,master.c1c2StockMargin,master.c1c2WinStage,master.c1c2StageMargin))
    vals = self.textAssign([master.c1c2WinRatio,master.c1c2StockMargin,master.c1c2WinStage,master.c1c2StageMargin])
    self.cText[4].insert(END,'%3d%%  %+.2f    /     %3d%%  %+.2f' % (vals[0],vals[1],vals[2],vals[3]))

    self.initUI()

  def closeIt(self,event):
    self.destroy()

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

  def initUI(self):
    self.fr.pack(fill=BOTH)
    self.labels.pack(side=TOP,fill=BOTH)
    self.stageLab.pack(side=TOP)
    self.allData.pack(side=TOP)
    self.pData.pack(side=TOP)
    self.pcData.pack(side=TOP)
    self.cData.pack(side=TOP)
    for i in range(5):
      self.labText[i].grid(row=0,column=i,columnspan=1,sticky=N+S+E+W)
      self.stgText[i].grid(row=1,column=i,columnspan=1,sticky=N+S+E+W)
      self.allText[i].grid(row=2,column=i,columnspan=1,sticky=N+S+E+W)
      self.pText[i].grid(row=3,column=i,columnspan=1,sticky=N+S+E+W)
      self.pcText[i].grid(row=4,column=i,columnspan=1,sticky=N+S+E+W)
      self.cText[i].grid(row=5,column=i,columnspan=1,sticky=N+S+E+W)

    self.focus_force()

def onClosing():
  for widget in top.winfo_children():
    widget.destroy()

  top.destroy()

def timeNow():
  t = datetime.now()
  return t.strftime('%Y%m%d%H%M')

def main():
  global top
  top = MainWindow()
  top.protocol("WM_DELETE_WINDOW", onClosing)
  top.focus_force()
  top.lift()
  top.mainloop()

if __name__ == '__main__':
  main()