from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import numpy as np
from interface import Interface
from math import floor
from time import sleep


MARGIN = 20  # Pixels around the board

class Connect4GUI(Frame):
  def __init__(self, parent, interface, playingVersusBot):
    self.playingVersusBot = playingVersusBot
    self.interface = interface
    self.game = self.interface.game
    self.parent = parent
    Frame.__init__(self, parent)

    parent.update()
    self.height = parent.winfo_height()
    self.width = parent.winfo_width()

    self.setUp()
  
  def setUp(self):
    self.parent.title("Connect 4")
    self.pack(fill=BOTH, expand=1)
    self.canvas = Canvas(self, width=self.width, height=self.height)
    self.resetButton = Button(self, text="Reset game", state="normal", command=self.reset)
    self.resetButton.pack(fill=BOTH, side=BOTTOM)
    # self.replayButton = Button(self, text="Replay game", state="disabled", command=self.replay)
    # self.replayButton.pack(fill=BOTH, side=BOTTOM)
    
    self.canvas.pack(fill=BOTH, side=TOP)

    suitableHeight = floor(0.65 * self.height/self.game.getRows())
    suitableWidth = floor(0.65 * self.width/self.game.getColumns())

    self.squareWidth = min(suitableHeight, suitableWidth)


    self.drawBoard()
    self.canvas.bind("<Button-1>", self.clickCallback)

  def reset(self):
    self.interface.game.reset()
    self.eraseDiscs()
    self.eraseText()
    self.interface.resetStatusText()
    self.drawBoard()
  
  #def replay(self):
  #  self.interface.game.replayMode()
  #  i=0
  #  while True:
  #    sleep(0.2)
  #    self.interface.makeReplayMove()
  #    self.drawBoard()

  def drawBoard(self):
    state = self.interface.getGameState()
    print(state)
    rows = state.shape[0]
    columns = state.shape[1]

    # draw horizontal lines
    for row in range(rows + 1):
      color = "blue"
      # draw horizontal line to separate the rows of the board
      x0 = MARGIN
      x1 = MARGIN + columns * self.squareWidth

      y0 = MARGIN + row * self.squareWidth # const rowHeight
      y1 = y0 # line is straight

      self.canvas.create_line(x0, y0, x1, y1, fill=color)

    # draw vertical lines
    for column in range(columns + 1):
      color = "blue"
      # draw horizontal line to separate the rows of the board
      y0 = MARGIN
      y1 = MARGIN + rows * self.squareWidth

      x0 = MARGIN + column * self.squareWidth  # const colWidth
      x1 = x0  # line is straight

      self.canvas.create_line(x0, y0, x1, y1, fill=color)

    self.eraseDiscs()
    self.drawDiscs(state)
    self.eraseText()
    self.displayText(MARGIN + columns*self.squareWidth/2, MARGIN + (rows+1)*self.squareWidth)

  def displayText(self, x, y):
    color = "black"
    self.canvas.create_text(
          x, y, text=self.interface.getStatusText(), tags="info", fill=color
      )

  def eraseText(self):
    self.canvas.delete("info")
    
  def drawDiscs(self, state):
    color = "red"
    for row in range(state.shape[0]):
      for column in range(state.shape[1]):
        xLower = MARGIN + column*self.squareWidth
        xUpper = xLower + self.squareWidth
        xMiddle = xLower/2 + xUpper/2

        yLower = MARGIN + row*self.squareWidth
        yUpper = yLower + self.squareWidth
        yMiddle = yLower/2 + yUpper/2

        player = state[row, column]
        if player == 1:
          self.create_circle(xMiddle, yMiddle, 10, "black", "yellow", self.canvas)
        elif player == 2:
          self.create_circle(xMiddle, yMiddle, 10, "black", "red", self.canvas)
  
  def create_circle(self, x, y, r, outline, color, canvasName):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, outline=outline, fill=color, tags="discs")
  
  def eraseDiscs(self):
    self.canvas.delete("discs")

  def clickCallback(self, event):
    # event includes (x,y) where user clicked
    # determine which column the user clicks in
    x, y = event.x, event.y
    row, column = self.getBoardPos(x, y)
    # print((row,column))
    self.interface.makeMove(column)

    # if playing vs bot
    if self.playingVersusBot:
      botMadeMove = self.interface.makeBotMove()

    #if self.interface.game.hasEnded():
    #  self.replayButton["state"] = "normal"
    #else:
    #  self.replayButton["state"] = "disabled"

    self.drawBoard()

  def getBoardPos(self, x, y):
    column, offsetx = divmod(x-MARGIN, self.squareWidth)
    row, offsety = divmod(y-MARGIN, self.squareWidth)
    return (row, column)
