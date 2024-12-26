print("Bienvenue sur le jeu du Puissance 4 (Ctrl+C pour stopper l'execution du programme)\n--- Chargement... ---")

from term_ctrl import *

terminal = TerminalControler()
terminal.show("Fait par Miala avec ", force_activ=True)

import pygame

terminal.progress()

pygame.init()
terminal.progress()

import threading
terminal.progress()

from display_ctrl import *
terminal.progress()

from grid_ctrl import *
terminal.progress()

from puissance_bot import *
terminal.progress()

grid = Grid()
terminal.progress()
 
bot = Puissance_Bot(grid, terminal, 4)
#bot2 = Puissance_Bot(grid, terminal, 6, 0)
terminal.progress()

displayer = Displayer(grid, bot)#, bot2)
terminal.progress()

terminal.progress()

terminal.progress(end = True)

terminal.show("Fin du chargement.\nR:Restart\nS:Settings\nZ:As ctrl+z normally", force_activ=True, end = True)

# play = threading.Thread(target = displayer.play())
# play.start()
# play.join()
displayer.play()

print("Player Left")