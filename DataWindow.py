#!/usr/bin/env python

from __future__ import division
from Tkinter import *  

from Stats2P import Stats2P

class DataWindow(Toplevel):
  def __init__(self, master,*args, **kwargs):
    di= {elem: kwargs[elem] for elem in kwargs.keys() if elem in dir(Toplevel)}
    Toplevel.__init__(self, master, **di)

    self.master = master
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
    
    self.bind_all('<BackSpace>',self.closeIt)
    self.bind_all('<Left>',self.switchFrame)
    self.bind_all('<Right>',self.switchFrame)

    self.h = int(200*self.scale)
    self.w = int(1350*self.scale)
    
    self.colors = {'p1red':'#f55943','p2purple':'#f5db43','p3yellow':'#5c3ba8','p4green':'#32b755','p12blend':'#ac7886'}
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

      self.labelText[i] = Text(self.topLabels,height=1,width=wid,highlightthickness=2,font=self.hf)
      self.subLabelText[i] = Text(self.subLabels,height=1,width=wid,highlightthickness=2,font=self.hf)
      self.allVText[i] = Text(self.allV,height=1,width=wid,highlightthickness=2,font=self.bf)
      self.p1VText[i] = Text(self.p1V,height=1,width=wid,highlightthickness=2,font=self.bf)
      self.p1c1VText[i] = Text(self.p1c1V,height=1,width=wid,highlightthickness=2,font=self.bf)
      self.c1VText[i] = Text(self.c1V,height=1,width=wid,highlightthickness=2,font=self.bf)

      if self.stage:
        self.labelText2[i] = Text(self.topLabels2,height=1,width=wid,highlightthickness=2,font=self.hf)
        self.subLabelText2[i] = Text(self.subLabels2,height=1,width=wid,highlightthickness=2,font=self.hf)
        self.allVText2[i] = Text(self.allV2,height=1,width=wid,highlightthickness=2,font=self.bf)
        self.p1VText2[i] = Text(self.p1V2,height=1,width=wid,highlightthickness=2,font=self.bf)
        self.p1c1VText2[i] = Text(self.p1c1V2,height=1,width=wid,highlightthickness=2,font=self.bf)
        self.c1VText2[i] = Text(self.c1V2,height=1,width=wid,highlightthickness=2,font=self.bf)
    
    self.labelText[2].config(highlightbackground=self.colors['p3yellow'])
    self.labelText[3].config(highlightbackground=self.colors['p3yellow'])
    if self.stage:
      self.labelText2[2].config(highlightbackground=self.colors['p3yellow'])
      self.labelText2[3].config(highlightbackground=self.colors['p3yellow'])

    self.p1VText[0].config(highlightbackground=self.colors['p1red'],font=self.hf)
    self.p1c1VText[0].config(highlightbackground=self.colors['p1red'],font=self.hf)
    self.allVText[2].config(highlightbackground=self.colors['p3yellow'])
    self.allVText[3].config(highlightbackground=self.colors['p3yellow'])
    self.p1VText[1].config(highlightbackground=self.colors['p1red'])
    self.p1VText[2].config(highlightbackground=self.colors['p12blend'])
    self.p1VText[3].config(highlightbackground=self.colors['p3yellow'])
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
      self.allVText2[2].config(highlightbackground=self.colors['p3yellow'])
      self.allVText2[3].config(highlightbackground=self.colors['p3yellow'])
      self.p1VText2[1].config(highlightbackground=self.colors['p1red'])
      self.p1VText2[2].config(highlightbackground=self.colors['p12blend'])
      self.p1VText2[3].config(highlightbackground=self.colors['p3yellow'])
      self.p1c1VText2[1].config(highlightbackground=self.colors['p1red'])
      self.p1c1VText2[2].config(highlightbackground=self.colors['p1red'])
      self.p1c1VText2[3].config(highlightbackground=self.colors['p12blend'])
      self.allVText2[0].config(font=self.hf)
      self.p1VText2[0].config(font=self.hf)
      self.p1c1VText2[0].config(font=self.hf)
      self.c1VText2[0].config(font=self.hf)

    self.labelText[0].insert(END,'{:<17}'.format('P1, C1   \   P2, C2'))
    self.labelText[1].insert(END,'vs. all : ')
    self.labelText[2].insert(END,'vs. {:<14}'.format(self.p2))
    self.labelText[3].insert(END,'vs. {0:<6}{1:<1}{2:<8}'.format(self.p2,'+',self.c2))
    self.labelText[4].insert(END,'vs. {:<14}'.format(self.c2))

    self.subLabelText[0].insert(END,'{:<17}'.format('------------------'))
    self.subLabelText[1].insert(END,'all data')
    self.subLabelText[2].insert(END,'all data')
    self.subLabelText[3].insert(END,'all data')
    self.subLabelText[4].insert(END,'all data')

    self.allVText[0].insert(END,'{:<17} ... :'.format('all'))
    self.allVText[1].insert(END,'-----------------  /%dx logged games' % self.stats.allCount)
    self.allVText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2WinRatioAll,self.stats.p2StockMarginAll,reverse=True),self.stats.p2AllCount))
    self.allVText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2WinRatioAll,self.stats.p2c2StockMarginAll,reverse=True),self.stats.p2c2AllCount))
    self.allVText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c2WinRatioAll,self.stats.c2StockMarginAll,reverse=True),self.stats.c2AllCount))

    self.p1VText[0].insert(END,'{:<17} ... :'.format(self.p1))
    self.p1VText[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1WinRatioAll,self.stats.p1StockMarginAll),self.stats.p1AllCount))
    self.p1VText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1p2WinRatio,self.stats.p1p2StockMargin),self.stats.p1p2Count))
    self.p1VText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2p1WinRatio,self.stats.p2c2p1StockMargin,reverse=True),self.stats.p2c2p1Count))
    self.p1VText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c2WinRatio,self.stats.p1c2StockMargin),self.stats.p1c2Count))

    self.p1c1VText[0].insert(END,'{0:<6}{1:<1}{2:<8} ... :'.format(self.p1,'+',self.c1))
    self.p1c1VText[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1WinRatioAll,self.stats.p1c1StockMarginAll),self.stats.p1c1AllCount))
    self.p1c1VText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2WinRatio,self.stats.p1c1p2StockMargin),self.stats.p1c1p2Count))
    self.p1c1VText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2c2WinRatio,self.stats.p1c1p2c2StockMargin),self.stats.p1c1p2c2Count))
    self.p1c1VText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1c2WinRatio,self.stats.p1c1c2StockMargin),self.stats.p1c1c2Count))

    self.c1VText[0].insert(END,'{:<17} ... :'.format(self.c1))
    self.c1VText[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1WinRatioAll,self.stats.c1StockMarginAll),self.stats.c1AllCount))
    self.c1VText[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c1WinRatio,self.stats.p2c1StockMargin,reverse=True),self.stats.p2c1Count))
    self.c1VText[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2c1WinRatio,self.stats.p2c2c1StockMargin,reverse=True),self.stats.p2c2c1Count))
    self.c1VText[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1c2WinRatio,self.stats.c1c2StockMargin),self.stats.c1c2Count))

    if self.stage:
      self.labelText2[0].insert(END,'{:<17}'.format('P1, C1   \   P2, C2'))
      self.labelText2[1].insert(END,'vs. all : ')
      self.labelText2[2].insert(END,'vs. {:<14}'.format(self.p2))
      self.labelText2[3].insert(END,'vs. {0:<6}{1:1}{2:<8}'.format(self.p2,'+',self.c2))
      self.labelText2[4].insert(END,'vs. {:<14}'.format(self.c2))

      self.subLabelText2[0].insert(END,'{:<17}'.format('------------------'))
      self.subLabelText2[1].insert(END,'this stage')
      self.subLabelText2[2].insert(END,'this stage')
      self.subLabelText2[3].insert(END,'this stage')
      self.subLabelText2[4].insert(END,'this stage')

      self.allVText2[0].insert(END,'{:<17} ... :'.format('all:'))
      self.allVText2[1].insert(END,'-----------------  /%dx logged games' % self.stats.stageCount)
      self.allVText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2WinStageAll,self.stats.p2StageMarginAll,reverse=True),self.stats.p2AllStCount))
      self.allVText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2WinStageAll,self.stats.p2c2StageMarginAll,reverse=True),self.stats.p2c2AllStCount))
      self.allVText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c2WinStageAll,self.stats.c2StageMarginAll,reverse=True),self.stats.c2AllStCount))

      self.p1VText2[0].insert(END,'{:<17} ... :'.format(self.p1))
      self.p1VText2[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1WinStageAll,self.stats.p1StageMarginAll),self.stats.p1AllStCount))
      self.p1VText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1p2WinStage,self.stats.p1p2StageMargin),self.stats.p1p2StCount))
      self.p1VText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2p1WinStage,self.stats.p2c2p1StageMargin,reverse=True),self.stats.p2c2p1StCount))
      self.p1VText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c2WinStage,self.stats.p1c2StageMargin),self.stats.p1c2StCount))

      self.p1c1VText2[0].insert(END,'{0:<6}{1:<1}{2:<8} ... :'.format(self.p1,'+',self.c1))
      self.p1c1VText2[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1WinStageAll,self.stats.p1c1StageMarginAll),self.stats.p1c1AllStCount))
      self.p1c1VText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2WinStage,self.stats.p1c1p2StageMargin),self.stats.p1c1p2StCount))
      self.p1c1VText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1p2c2WinStage,self.stats.p1c1p2c2StageMargin),self.stats.p1c1p2c2StCount))
      self.p1c1VText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p1c1c2WinStage,self.stats.p1c1c2StageMargin),self.stats.p1c1c2StCount))

      self.c1VText2[0].insert(END,'{:<17} ... :'.format(self.c1))
      self.c1VText2[1].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1WinStageAll,self.stats.c1StageMarginAll),self.stats.c1AllStCount))
      self.c1VText2[2].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c1WinStage,self.stats.p2c1StageMargin,reverse=True),self.stats.p2c1StCount))
      self.c1VText2[3].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.p2c2c1WinStage,self.stats.p2c2c1StageMargin,reverse=True),self.stats.p2c2c1StCount))
      self.c1VText2[4].insert(END,'%s  /%dx games' % (self.stats.statString(self.stats.c1c2WinStage,self.stats.c1c2StageMargin),self.stats.c1c2StCount))

    self.initUI()

  def initUI(self):
    self.fr.place(relx=0.5,rely=0.5, anchor=CENTER,relwidth=1,relheight=1)
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
      self.fr2.place(relx=0.5,rely=0.5, anchor=CENTER,relwidth=1,relheight=1)
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
    self.resizable(0,0)

  def closeIt(self,event):
    for widget in self.winfo_children():
      widget.destroy()

    self.unbind_all('<BackSpace>')
    self.unbind_all('<Left>')
    self.unbind_all('<Right>')

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