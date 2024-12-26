import pygame
import threading

class NoPlaceError(ValueError):
    def __init__(self, arg):
        self.error = arg
        self.args = {arg}

class Displayer():

    window_resolution = (690,640)
    blank_color = (255, 255, 255)
    black_color = (0,0,0)
    player_colors = [(255, 38, 0), (0, 255, 200)]
    player_light_colors = [(255, 141, 121), (180, 255, 213)]
    font = pygame.font.Font("font/robotomono.ttf", 25)  # Nom, taille.
    icon = pygame.image.load("img/icon_png.png")
    title = "Puissance 4 - by Miala"
    
    def __init__(self, grid, bot, sec_bot = None):
        self.grid = grid
        self.bot = bot
        self.sec_bot = sec_bot
        # self.bot_play = "NOT"
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)
        self.window_surface = pygame.display.set_mode(self.window_resolution)
        self.show_text("Chargement...", 18, 45)
        self.draw_grid()

        self.pls_players = False
        self.start_player = 0

    def set_settings(self):
        def ask_player(msg, nb=0):
            try:
                return int(input(msg))-nb
            except KeyboardInterrupt:
                raise KeyboardInterrupt("Jeu interrompu... A la prochaine !")
            except:
                print("\tOops ! Il y a eu une erreur... Veuillez réessayer.")
                return ask_player(msg)
            

        self.pls_players = bool(ask_player("1 (+ bot) ou 2 joueurs ?\n", 1))
        if self.pls_players:
            self.start_player = bool(ask_player("Joueur qui commence: [0] pour le orange, [1] pour le bleu ?\n"))
        else:
            self.start_player = bool(ask_player("Joueur qui commence: [0] pour vous, [1] pour le bot ?\n"))
            self.bot.max = ask_player("Nombre de coups à l'avance du bot:\n")    

    def play(self):
        self.grid.list_init()
        self.round = self.start_player
        self.last = []

        self.restart = False
        self.mouse = 0

        pygame.mouse.set_pos([300,300])
        self.show_text("Jouez !")

        self.game_loop()

        if self.restart: self.play()

    def show_text(self, txt, x=0, y=600, color=None, flip = True):
        if color == None:
            color = self.blank_color
        rect = pygame.Rect(x,y,600,35)
        pygame.draw.rect(self.window_surface,self.black_color,rect)
        text = self.font.render(txt, True, color)
        self.window_surface.blit(text, [x + 10, y])
        if flip:pygame.display.flip()

    def draw_grid(self):
        self.window_surface.fill(self.black_color)

        #col
        for x in range(89, 600, 100):
            pygame.draw.line(self.window_surface, self.blank_color, [x,0],[x,600], 22)#ligne: surface,color,depart,fin, épaisseur:Pixels

        #lin
        for y in range(89, 600, 100):
            pygame.draw.line(self.window_surface, self.blank_color, [0,y],[700,y], 22)

    def game_loop(self):
        self.launchef = True
        while self.launchef:

            self.bot_ctrl()
            
            self.get_mouse_pos()

            self.check_mouse_rect()

            if self.have_played:
                self.check_winner()

            pygame.display.flip()

            self.check_events()

    def bot_ctrl(self):
        if self.pls_players == False and self.round == self.bot.player:
            self.show_text("En attente du bot...")
            # if self.bot_play == "END" or self.bot_play == "NOT":
            #     if self.bot_play == "NOT":play_bot = self.bot.play()
            #     else:play_bot = self.to_play[self.last[-1]]
            play_bot = self.bot.play()
            if play_bot != None:
                self.grid.list[play_bot][1] = self.bot.player
                self.grid.columns[play_bot % 7] -= 1
                pygame.draw.rect(self.window_surface,self.player_colors[self.bot.player],self.grid.list[play_bot][0])
                self.last.append(play_bot)
            self.round = self.round * (-1) + 1
            self.check_winner()
            self.show_text("Jouez !")
            # self.bot_play = "NOT"
        elif self.sec_bot != None:
            if self.pls_players == False and self.round == self.sec_bot.player:
                self.show_text("En attente du bot... (2) ")
                last_len = len(self.last)
                play_bot = self.sec_bot.play()
                if play_bot != None:
                    self.grid.list[play_bot][1] = self.sec_bot.player
                    self.grid.columns[play_bot % 7] -= 1
                    pygame.draw.rect(self.window_surface,self.player_colors[self.sec_bot.player],self.grid.list[play_bot][0])
                    self.last.append(play_bot)
                self.round = self.round * (-1) + 1
                self.check_winner()
        # else:
        #     if self.bot_play == "NOT":
        #         self.bot_play = "PLAY"
        #         self.bot_pross = threading.Thread(target = self.preplay(4))#en arrière plan
        #         self.bot_pross.start()

    # def preplay(self, nb_coups):
    #     self.to_play = self.bot.preplay(nb_coups)
    #     self.bot_play = "END"

    def get_mouse_pos(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def check_mouse_rect(self, dont_draw_act = True):
        self.have_played = False
        key = 0
        dont_draw = []
        for place in self.grid.list:
            rect = place[0]
            user = place[1]
            if user != (-1):
                # print(f"i: {key}//grid: {place}")
                pygame.draw.rect(self.window_surface,self.player_colors[user],rect)
                if dont_draw_act: dont_draw.append(key)
            if rect.collidepoint(self.mouse_x,self.mouse_y):
                try:
                    column = key % 7
                    column_items = self.grid.columns[column]
                    if column_items == 0: raise NoPlaceError("Plus de place !")
                    list_id = (column_items - 1) * 7 + column
                    rect = self.grid.list[list_id][0]
                    if dont_draw_act: dont_draw.append(list_id)
                    if self.mouse == 0:
                        pygame.draw.rect(self.window_surface, self.player_light_colors[self.round], rect)
                    else: 
                        self.grid.list[list_id][1] = self.round
                        pygame.draw.rect(self.window_surface, self.player_colors[self.round], rect)
                        self.round = self.round * (-1) + 1
                        self.last.append(list_id)
                        self.grid.columns[column] -= 1
                        self.have_played = True
                except NoPlaceError:
                    pass
            else:
                if not key in dont_draw:
                    pygame.draw.rect(self.window_surface,self.black_color,rect)

            key += 1

    def check_winner(self):
        winner = self.grid.check_win()
        if winner != (-1):
            if winner == 1:
                winner = "bleu"
            else:
                winner = "orange"
            self.show_text(f"Le gagnant est le {winner}! [ESPACE]")
            self.end_game_loop()

        elif (len(self.last) == 42):
            self.show_text("Egalité ! [ESPACE]")
            self.end_game_loop()

    def end_game_loop(self):
        while self.launchef:
            for place in self.grid.list:
                rect = place[0]
                user = place[1]
                if user != (-1):
                    # print(f"i: {key}//grid: {place}")
                    pygame.draw.rect(self.window_surface,self.player_colors[user],rect)
                else:
                    pygame.draw.rect(self.window_surface,self.black_color,rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.launchef = False
                    print("Au revoir !")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Rejouez !")
                        self.restart = True
                        self.launchef = False




    def check_events(self):
        self.mouse = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Au revoir !")
                self.launchef = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart = True
                    self.launchef = False
                    print("Redémarrage...")
                if event.key == pygame.K_s:
                    self.restart = True
                    self.launchef = False
                    print("Paramètres:")
                    self.set_settings()
                if event.key == pygame.K_z:
                    self.rmv_last_move()
                    if not self.pls_players: self.rmv_last_move()
                    self.draw_grid()

    def rmv_last_move(self):
        try:
            #print(f"last: {self.last}")
            key = self.last[-1]
            column = key % 7
            column_items = self.grid.columns[column]
            list_id = (column_items - 1) * 7 + column   
            self.round = self.round * (-1) + 1
            self.grid.list[list_id][1] = -1
            self.grid.columns[column] += 1
            del self.last[-1]
            self.mouse = 0
            self.check_mouse_rect(False)
            #print(f"last: {self.last}; key: {key}; col: {self.grid.columns};grid: {self.grid.list}")
           
        except IndexError:
            pass
            
        