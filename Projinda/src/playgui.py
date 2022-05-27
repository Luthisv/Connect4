from interface import Interface
from connect4gui import Connect4GUI
from tkinter import Tk
import sys

if __name__ == '__main__':
  arguments = sys.argv  # argv[0] is always filename

  playingVersusBot = True
  if len(arguments) > 1 and arguments[1] == "nobot":
    playingVersusBot = False

  interface = Interface(2)

  root = Tk()
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  root.geometry("%dx%d" % (screen_width/2, screen_height/2))
  Connect4GUI(root, interface, playingVersusBot)
  root.mainloop()
