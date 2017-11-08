#!/usr/bin/env python

from Tkinter import *
import tkFont
import os 
from PIL import Image, ImageTk

from DataWindow import DataWindow

# window of character/stage options, stock count and virtual buttons
# the 1183x787 scale was originally used to create the dictionaries of positions
# at the end of the class (so it's now being used as a scaling reference)
# hovered/selected items are stored in StringVar's so that the MainWindow can 'trace'
# changes to these variables for taking action
class SelectionWindow(Frame):
  def __init__(self, master, *args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in master.keys()}
    Frame.__init__(self, master, di)
    
    #dimensions
    self.canH = int(598*master.scale)
    self.canW = int(900*master.scale)
    self.scaleX = self.canW/1183.
    self.scaleY = self.canH/787.
    self.sx = int(792*master.scale)  # local coords of where to put the stage images
    self.sy = int(497*master.scale)
    self.t1x = int(33*master.scale)
    self.t1y = int(448*master.scale)
    self.t2x = int(612*master.scale)
    self.t2y = int(448*master.scale)
    
    #vars for binding mouse movement/selection
    self.charTraceP1 = StringVar(self)    #stores character name under mouse; NA if no hover
    self.charTraceP2 = StringVar(self)    #stores character name under mouse; NA if no hover
    self.charTraceP3 = StringVar(self)    #stores character name under mouse; NA if no hover
    self.charTraceP4 = StringVar(self)    #stores character name under mouse; NA if no hover
    self.stagTrace = StringVar(self)    #stores stage name under mouse; NA if no hover
    self.stocTrace = StringVar(self)    #similar for stock count buttons 

    #vars for binding clicked options
    self.charLockP1 = StringVar(self)
    self.charLockP2 = StringVar(self)
    self.charLockP3 = StringVar(self)
    self.charLockP4 = StringVar(self)
    self.stagLock = StringVar(self)
    self.toggLock = StringVar(self) #unnecessary?
    self.stocLock = StringVar(self)
    self.statsLock = StringVar(self)
    self.zeroVars('lock')

    #current mode options
    self.toggleMode = StringVar(self)
    self.toggleMode.set('char')
    self.stockCount = StringVar(self)
    self.stockCount2 = StringVar(self)
    self.stockCount.set('')
    self.stockCount2.set('')
    self.readyForStock = False
    self.readyForStockFree = False
    self.readyForStockTeam = False
    self.readyForStats = False
    self.readyForStatsFree = False
    self.readyForStatsTeam = False
    self.lockInWin = BooleanVar(self)
    self.lockInWin.set(False)

    #handy variables
    self.master = master
    self.characters = master.characters
    self.stages = master.stages
    self.P1 = StringVar(self)
    self.P2 = StringVar(self)
    self.P3 = StringVar(self)
    self.P4 = StringVar(self)
    self.playMode = 0
    self.modeText = ['1v1','multi','multi']
    self.char1 = StringVar(self)
    self.char2 = StringVar(self)
    self.char3 = StringVar(self)
    self.char4 = StringVar(self)
    self.stage = StringVar(self)
    self.fn = tkFont.Font(family="Calibri", size=int(24*master.scale), weight=tkFont.BOLD)

    #canvas where all the action happens
    self.dictMake()
    self.charStageStock = Canvas(self,height=self.canH,width=self.canW,bg='#fff')
    self.iconImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Thumbs','%s.jpg')) % el).resize((int(64*master.scale),int(64*master.scale)),Image.ANTIALIAS)) for el in self.characters if el != 'QuestionMark'}
    self.stageImgs = {el:ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Stages','%s.gif')) % el).resize((int(160*master.scale),int(160*master.scale)),Image.ANTIALIAS)) for el in self.stages}

    #actual images
    for key in self.stockPixelDict.keys():
      posx,posy = self.stockPixelDict[key]
      posx = int(posx*self.scaleX)
      posy = int(posy*self.scaleY)
      if 'kP' in key:
        self.charStageStock.create_image(posx,posy,image=self.iconImgs['Logo'],tags='1v1')
      elif 'Butt' in key:
        self.charStageStock.create_image(posx,posy,image=self.iconImgs['Logo'],tags='butt')

    for key in self.stockPixelDict2.keys():
      if not('Butt' in key):
        posx,posy = self.stockPixelDict2[key]
        posx = int(posx*self.scaleX)
        posy = int(posy*self.scaleY)
        self.charStageStock.create_image(posx,posy,image=self.iconImgs['Logo'],tags='multi')

    self.charImg = ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Banners','charBanner.jpg'))).resize((int(900*master.scale),int(598*master.scale)),Image.ANTIALIAS))
    self.stagImg = ImageTk.PhotoImage(Image.open(os.path.abspath(os.path.join('.','Banners','stageBanner.jpg'))).resize((int(900*master.scale),int(598*master.scale)),Image.ANTIALIAS))
    self.charStageStock.create_image(self.canW/2,self.canH/2,image=self.charImg,tags='charButton')
    self.charStageStock.create_image(self.canW/2,self.canH/2,image=self.stagImg,tags='stageButton')
    self.charStageStock.tag_raise('charButton')

    #canvas binding for fancy effects
    self.charStageStock.bind('<Motion>',self.mouseTrace)          #track mouse movement over things of interest
    self.charStageStock.bind('<Control-Motion>',self.mouseTraceP2)
    self.charStageStock.bind('<Shift-Motion>',self.mouseTraceP3)        
    self.charStageStock.bind('<Shift-Control-Motion>',self.mouseTraceP4)
    self.charStageStock.bind('<ButtonRelease-1>',self.mouseSave)
    self.charStageStock.bind('<Control-ButtonRelease-1>',self.mouseSaveP2)
    self.charStageStock.bind('<Shift-ButtonRelease-1>',self.mouseSaveP3)
    self.charStageStock.bind('<Shift-Control-ButtonRelease-1>',self.mouseSaveP4)
    
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
      self.charStageStock.tag_raise('playMode')
      self.charStageStock.tag_raise(self.modeText[self.playMode])
      self.charStageStock.tag_raise('butt')

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

    if self.playMode == 1 and self.stockCount.get():
      if stockKey != self.stockCount2.get() and stockKey[-1] == self.stockCount.get()[-1] and not(stockKey[-2:] == self.stockCount.get()[-2:]):
        if mode=='hard' and stockKey != 'submitButton':
          self.stockCount2.set(stockKey)
        if mode=='hard' or not(self.stockCount2.get()):
          self.charStageStock.delete('head2')
          self.drawHeads(stockKey,'head2')
        return

    if stockKey and stockKey != self.stockCount.get():
      if mode=='hard' and stockKey != 'submitButton':
        if not(stockKey[-1:] == self.stockCount.get()[-1:]):
          self.stockCount2.set('')
          self.charStageStock.delete('head2')
        self.stockCount.set(stockKey)
      if mode=='hard' or not(self.stockCount.get()):
        self.charStageStock.delete('head')
        self.drawHeads(stockKey)

  def modeTextInsert(self,mode):
    if mode == 0:
      self.charStageStock.delete('playMode')
      self.charStageStock.create_text(self.t1x,self.t1y,anchor=W,text='P1 wins:',font=self.fn,tags='playMode')
      self.charStageStock.create_text(self.t2x,self.t2y,anchor=E,text='P2 wins:',font=self.fn,tags='playMode')
      self.charStageStock.tag_raise('playMode')
      self.charStageStock.tag_raise('1v1')
    elif mode == 1:
      self.charStageStock.delete('playMode')
      self.charStageStock.create_text(self.t1x,self.t1y,anchor=W,text='Team 1 wins:',font=self.fn,tags='playMode')
      self.charStageStock.create_text(self.t2x,self.t2y,anchor=E,text='Team 2 wins:',font=self.fn,tags='playMode')
      self.charStageStock.tag_raise('playMode')
      self.charStageStock.tag_raise('multi')
    else:
      self.charStageStock.delete('playMode')
      self.charStageStock.create_text(self.t1x,self.t1y,anchor=W,text='P1/P2 wins:',font=self.fn,tags='playMode')
      self.charStageStock.create_text(self.t2x,self.t2y,anchor=E,text='P3/P4 wins:',font=self.fn,tags='playMode')
      self.charStageStock.tag_raise('playMode')
      self.charStageStock.tag_raise('multi')

  def kickHeads(self,mode='hard'):
    if mode == 'hard' or not(self.stockCount.get()):
      self.charStageStock.delete('head')
      self.stockCount.set('')
    if mode == 'hard' or not(self.stockCount2.get()):
      self.charStageStock.delete('head2')
      self.stockCount2.set('')

  def drawHeads(self,stockKey,tag='head'):
    # search through the stockPixelDict for stock numbers <= stock count
    # draw little heads for each stock for the winner
    numSet = ['1','2','3','4']
    p = stockKey[-2:]
    # Mode == 0 and P => char1/char2 get okay    
    # Mode != 0 and A/B => all get okay
    if self.playMode and 'A' in p or 'B' in p:
      if 'A1' in p:
        charHead = self.iconImgs[self.char1.get()]
      elif 'B1' in p:
        charHead = self.iconImgs[self.char2.get()]
      elif 'A2' in p:
        if self.char3.get():
          charHead = self.iconImgs[self.char3.get()]
        else:
          return
      elif 'B2' in p:
        if self.char4.get():
          charHead = self.iconImgs[self.char4.get()]
        else:
          return
    elif 'P' in p:
      if 'P1' in p:
        charHead = self.iconImgs[self.char1.get()]
      elif 'P2' in p:
        charHead = self.iconImgs[self.char2.get()]
      else:
        return
    else:
      return

    if stockKey[0] in numSet:
      num = int(stockKey[0])
    else:
      num = 0

    if self.playMode:
      sPDict = self.stockPixelDict2
    else:
      sPDict = self.stockPixelDict

    candKeys = [key for key in sPDict.keys() if p in key and key[0] in numSet]
    for key in candKeys:
      if int(key[0]) <= num:
        posx,posy = sPDict[key]
        posx = int(posx*self.scaleX)
        posy = int(posy*self.scaleY)
        self.charStageStock.create_image(posx,posy,image=charHead,tags=tag)
        self.charStageStock.tag_raise(tag)

  def zeroVars(self,togg='trace'):
    if togg=='trace':
      self.kickStage('soft')
      #self.kickHeads('soft')
      self.charTraceP1.set('')
      self.charTraceP2.set('')
      self.charTraceP3.set('')
      self.charTraceP4.set('')
      self.stagTrace.set('')
      self.stocTrace.set('')
    elif togg=='lock':
      self.charLockP1.set('')
      self.charLockP2.set('')
      self.charLockP3.set('')
      self.charLockP4.set('')
      self.stagLock.set('')
      self.toggLock.set('')
      self.stocLock.set('')
      self.statsLock.set('')

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
    elif (x,y) in self.stockDict2 and self.playMode:
      selection = self.stockDict2[(x,y)]
    elif (x,y) in self.stockDict:
      selection = self.stockDict[(x,y)]

    return selection

  def updateVars(self,sel,mode,togg='trace'):

    if mode == 1:
      obCharTrace = self.charTraceP1
      obCharLock = self.charLockP1
    elif mode == 2:
      obCharTrace = self.charTraceP2
      obCharLock = self.charLockP2
    elif mode == 3:
      obCharTrace = self.charTraceP3
      obCharLock = self.charLockP3
    else:
      obCharTrace = self.charTraceP4
      obCharLock = self.charLockP4

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
          if self.stagTrace.get():
            self.stagTrace.set('')
            self.kickStage(mode='soft')

        # check if we've already hovered this and setStockCount softly if not
        if self.playMode:
          ob = self.stockPixelDict2
        else:
          ob = self.stockPixelDict

        if sel in ob.keys():
          if sel != self.stocTrace.get():
            self.stocTrace.set(sel)
            self.checkReady()
            if self.readyForStock:
              self.setStockCount(sel)
        else:
          if self.stocTrace.get():
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
      if self.playMode:
        ob = self.stockPixelDict2
      else:
        ob = self.stockPixelDict

      if sel in ob.keys() and sel != self.toggleMode.get():
        self.checkReady()
        if sel == 'submitButton':
          if self.readyForStock and self.stockCount.get():
            self.lockInWin.set(True)
        else:
          if self.readyForStock:
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

  def mouseTraceP3(self,event):
    # track the mouse position, and check it across the dictionaries
    if self.playMode:
      self.lastPos = (event.x,event.y)

      #check the position against the dictionaries of pixel locations of interest
      sel = self.checkDicts()
      self.updateVars(sel,mode=3)

  def mouseSaveP3(self,event=''):
    # same thing as above, but for the click mode instead of hovering mode
    if event and self.playMode:
      self.lastPos = (event.x,event.y)

      sel = self.checkDicts()
      self.updateVars(sel,mode=3,togg='lock')

  def mouseTraceP4(self,event):
    # track the mouse position, and check it across the dictionaries
    if self.playMode:
      self.lastPos = (event.x,event.y)

      #check the position against the dictionaries of pixel locations of interest
      sel = self.checkDicts()
      self.updateVars(sel,mode=4)

  def mouseSaveP4(self,event=''):
    # same thing as above, but for the click mode instead of hovering mode
    if event and self.playMode:
      self.lastPos = (event.x,event.y)

      sel = self.checkDicts()
      self.updateVars(sel,mode=4,togg='lock')

  def checkReady(self):
    # to allow a stock selection, we need players, characters and stage chosen
    # 1v1
    if self.playMode == 0:
      self.statVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2]]
      self.allVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2,self.stage]]
    elif self.playMode == 1:
      self.statVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2,self.P3,self.char3,self.P4,self.char4]]
      self.allVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2,self.P3,self.char3,self.P4,self.char4,self.stage]]
    else:
      # check that for each player, there's a character and vice versa; also make sure at least 2 players/characters
      l3 = [self.P3,self.char3]
      l4 = [self.P4,self.char4]
      l3check = [not(el.get()=='') for el in l3]
      l4check = [not(el.get()=='') for el in l4]

      if all([li[0] == li[1] for li in [l3check,l4check]]):
        PCs = [el for li in [l3,l4] for el in li if el.get()]
        self.statVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2]+PCs]
        self.allVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2]+PCs+[self.stage]]
      else:
        self.statVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2,self.P3,self.char3,self.P4,self.char4]]
        self.allVars = [el.get() for el in [self.P1,self.char1,self.P2,self.char2,self.P3,self.char3,self.P4,self.char4,self.stage]]

    if all(self.statVars):
      if not(self.readyForStats):
        self.readyForStats = True
    elif self.readyForStats:
      self.readyForStats = False

    if all(self.allVars):
      if not(self.readyForStock):
        self.readyForStock = True
    elif self.readyForStock:
      self.readyForStock = False


  def getMatchupData(self,vars):
    if self.playMode == 0:
      p1 = vars[0]
      c1 = vars[1]
      p2 = vars[2]
      c2 = vars[3]
      stage = vars[4]

      self.dataWin = DataWindow(self,file=self.master.dataFileName1v1,p1=p1,c1=c1,p2=p2,c2=c2,stage=stage,scale=self.master.scale)
      self.dataWin.focus_force()
      self.dataWin.lift()
      self.dataWin.mainloop()

    '''
    elif self.playMode == 1:
      p1 = vars[0]
      c1 = vars[1]
      p2 = vars[2]
      c2 = vars[3]
      p3 = vars[4]
      c3 = vars[5]
      p4 = vars[6]
      c4 = vars[7]
      stage = vars[8]
    else:
      p1 = vars[0]
      c1 = vars[1]
      p2 = vars[2]
      c2 = vars[3]

      if len(vars) == 9:
        p3 = vars[4]
        c3 = vars[5]
        p4 = vars[6]
        c4 = vars[7]
        stage = vars[8]
      elif len(vars) == 7:
        p3 = vars[4]
        c3 = vars[5]
        stage = vars[6]
      else:
        stage = vars[4]
    '''

  def dictMake(self):
    # set up dictionaries with pixels as keys and either a character or stage name, or a stock count or toggle button string
    self.charDict = {}
    self.stagDict = {}
    self.toggleDict = {}
    self.stockDict = {}
    self.stockDict2= {}
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
    self.stockPixelDict2= {'submitButton':(431,682),'4stockA1':(74,656),'3stockA1':(154,656),'2stockA1':(234,656),'1stockA1':(314,656),'1stockA2':(548,656),'2stockA2':(628,656),'3stockA2':(708,656),'4stockA2':(788,656),
                           '4stockB1':(74,735),'3stockB1':(154,735),'2stockB1':(234,735),'1stockB1':(314,735),'1stockB2':(548,735),'2stockB2':(628,735),'3stockB2':(708,735),'4stockB2':(788,735)}

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

    # 2v2 and freeforall mode stock count buttons
    for el in self.stockPixelDict2:
      pix = self.stockPixelDict2[el]
      x = pix[0]
      y = pix[1]
      #set of all x,y coords in the 72x72 swath of the smash logo:
      areaList = [(xa,ya) for xa in range(x-36,x+37) for ya in range(y-36,y+37)]   

      #each (x,y) pair will now be a key with a value of the character name
      for singCoord in areaList:
        scaleCoord = (int(singCoord[0]*self.scaleX),int(singCoord[1]*self.scaleY))
        self.stockDict2[scaleCoord] = el