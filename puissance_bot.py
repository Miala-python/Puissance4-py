import copy
import time
import threading

class Puissance_Bot():
    def __init__(self, grid, term, max, player = 1):
        self.grid = grid
        self.player = player
        self.terminal = term
        self.max=max

    def wait_process(self, wait_s = 4.5):
        if self.terminal.prgrs:
            time.sleep(wait_s)
            if self.playing:
                rest = int((time.time() - self.timer) / (self.i + 1) * (7 - self.i))
                if self.i == 0 and rest > 60:
                    self.terminal.show(f"| Calcul du temps... (+ de {rest}s) ", force_activ=True)
                elif self.i > 0:
                    self.terminal.show(f"| Il reste ≈{rest}s ", force_activ=True)
                self.terminal.flush()
                if rest > 20:
                    self.wait_process(rest / 2)


    def play(self, nb_coups=None):
        try:
            if nb_coups == None:
                nb_coups = self.max
            if self.terminal.prgrs: self.terminal.show("Chargement du bot: ", force_activ=True)
            self.max = nb_coups
            self.playing = True
            self.i = 0
            self.timer = time.time()
            wait_pross = threading.Thread(target = self.wait_process)#en arrière plan , self = self
            wait_pross.start()
            move_to_play = self.start_calc(self.grid.list, self.grid.columns)
            self.playing = False
            self.terminal.progress(end = True)
            return move_to_play
        except KeyboardInterrupt:
            self.playing = False
            raise KeyboardInterrupt("Veuillez patienter pendant la fermeture du programme ou fermer cette fenetre")

    def start_calc(self, grid, col):
        points = {}
        for self.i in range(7):
            self.terminal.progress()

            column_item = col[self.i]
            if column_item != 0:
                list_id = (column_item - 1) * 7 + self.i
                new_grid = copy.deepcopy(grid)
                new_col = copy.deepcopy(col)
                new_col[self.i] -= 1
                new_grid[list_id][1] = self.player
                point = self.calc_move(new_grid, new_col, 1, 0)
                points[list_id] = point

        if points == {}:
            return None

        pts_sorted = sorted(points.items(), key=lambda x: x[1])
        # print(f"Pts: {points} //Class: {pts_sorted}")
        key = pts_sorted[-1][0]
        # try:
        #     # print(key, "//", points[(col[3] - 1) * 7 + 3])
        #     if key == points[(col[3] - 1) * 7 + 3]:
        #         return (col[3] - 1) * 7 + 3
        # except IndexError:
        #     pass
        return key

    def calc_move(self, grid, col, lvl, player):
        verif_player = (player == self.player)
        if lvl == self.max or (-1) != self.grid.check_win(grid):
            return self.grid.point_counter(grid, self.player) / (1 + (lvl * 0.00001))

        points = {}
        next_lvl = lvl + 1
        next_player = player * (-1) + 1
        for i in range(7):
            column_item = col[i]
            if column_item != 0:
                list_id = (column_item - 1) * 7 + i
                new_grid = copy.deepcopy(grid)
                new_col = copy.deepcopy(col)
                new_col[i] -= 1
                new_grid[list_id][1] = player
                point = self.calc_move(new_grid, new_col, next_lvl, next_player)
                points[list_id] = point

        # if col[3] < 6:
        #     print(f"lvl:{lvl} //pts:{points}")

        if points == {}:
            return self.grid.point_counter(grid, self.player) / (1 + (lvl * 0.00001))

        pts_sorted = sorted(points.items(), key=lambda x: x[1])
        return pts_sorted[(not verif_player) - 1][1]
    
    # def preplay(self, nb_coups):
    #     if self.terminal.prgrs: self.terminal.show("Chargement du bot: ", force_activ=True)
    #     self.max = nb_coups
    #     self.playing = True
    #     to_play = {}
    #     for i in range(7):
    #         self.terminal.progress()
    #         column_item = self.grid.columns[i]
    #         if column_item != 0:
    #             list_id = (column_item - 1) * 7 + i
    #             new_grid = copy.deepcopy(self.grid.list)
    #             new_col = copy.deepcopy(self.grid.columns)
    #             new_col[i] -= 1
    #             new_grid[list_id][1] = self.player
    #             to_play[list_id] = self.start_calc(new_grid, new_col)

    #     self.terminal.progress(end = True)
    #     return to_play

    # def old_calc_move(self, grid, col, lvl, player):
    #     verif_player = player == self.player
    #     if (-1) != self.grid.check_win(grid):
    #         return self.grid.point_counter(grid, self.player) - (2*verif_player-1) * lvl
    #     elif lvl == self.max:
    #         return self.grid.point_counter(grid, self.player)
        

    #     points = {}
    #     next_lvl = lvl + 1
    #     for i in range(7):
    #         column_item = col[i]
    #         if column_item != 0:
    #             list_id = (column_item - 1) * 7 + i
    #             new_grid = copy.deepcopy(grid)
    #             new_col = copy.deepcopy(col)
    #             new_col[i] -= 1
    #             new_grid[list_id][1] = player
    #             point = self.calc_move(new_grid, new_col, next_lvl, player * (-1) + 1)
    #             if verif_player:
    #                 point *= (point < 999999999) * (-1.1)
    #             # if verif_player and point < -999999999:
    #             #     point *= -1.1
    #             # elif (not verif_player) and point > 999999999:
    #             #     point *= -1.1
    #             points[list_id] = point
                
    

    #     if points == {}:
    #         return self.grid.point_counter(grid, self.player)
        
    #     pts_sorted = sorted(points.items(), key=lambda x: x[1])
    #     return pts_sorted[(not verif_player) - 1][1] + sum(points.values()) * .0001

