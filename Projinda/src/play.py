from interface import Interface
import sys

if __name__ == '__main__':
  arguments = sys.argv # argv[0] is always filename

  playingVersusBot = True
  if len(arguments) > 1 and arguments[1] == "nobot":
    playingVersusBot = False
    
  interface = Interface(2)
  print(interface.getGameState())
  while True:
    try:
      userInput = input(interface.getInputMsg())
      reset = interface.handleInput(int(userInput))
      
      if reset:
        print(interface.getGameState())
        continue

      print(interface.getUserInterface())
      if playingVersusBot:
        botMove = interface.makeBotMove()
        if botMove:
          print(interface.getUserInterface())
    except Exception as e:
      print(e)