#!/usr/bin/env python

from __future__ import division
from Tkinter import *
import tkFont
import tkMessageBox
import os 
import sys
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from datetime import datetime

from MainWindow import MainWindow

'''
Using the GUI:

cmd line scale windows, e.g.: 
> python smashDataLogger.py small
  - scale options 'large','small','fit' or none given (1x scaling)

Up/Down     : Player 1
+Ctrl       : Player 2
+Shft       : Player 3
+Shft+Ctrl  : Player 4

Mouse       : Character 1
+Ctrl       : Character 2
+Shft       : Character 3
+Shft+Ctrl  : Character 4

Tab         : Switch between characters and stages
Escape      : Clear the characters, stages

F1          : 1 v 1 mode
F2          : Free-for-all
F3          : Teams (i.e. 2 v 2)

'''

def onClosing():
  for widget in top.winfo_children():
    widget.destroy()

  top.destroy()

def main(*args,**kwargs):
  global top
  if args:
    scaleWindow = args[0]
    top = MainWindow(scaleWindow=scaleWindow)
  else:
    top = MainWindow()
  top.protocol("WM_DELETE_WINDOW", onClosing)
  top.focus_force()
  top.lift()
  top.mainloop()

if __name__ == '__main__':
  args = sys.argv
  if len(args) == 2:
    mode = args[1]
    if mode in ['large','small','fit']:
      main(mode)
    else:
      main()
  else:
    main()