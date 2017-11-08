#!/usr/bin/env python

from __future__ import division
from Tkinter import *  
import pandas as pd


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