import pygame

class Grid():
    
    list = []

    def __init__(self):
        self.list_init()

    def list_init(*args):
        Grid.list = []
        Grid.columns = []
        
        for y in range(6):
            for x in range(7):
                if y == 0:Grid.columns.append(6)
                Grid.list.append([pygame.Rect(x * 100,y * 100,90,90),-1])

    def check_win(self, grid = None):
        if grid == None:
            grid = self.list
        for y in range(6):
            for x in range(7):
                i = 7 * y + x
                #Ligne
                if x < 4:
                    if (-1) != grid[i][1] and grid[i][1] == grid[i+1][1] and grid[i+1][1] == grid[i+2][1] and grid[i+2][1] == grid[i+3][1]:
                        return grid[i][1]
                #collonne
                if y < 3:
                    if (-1) != grid[i][1] and grid[i][1] == grid[i+7][1] and grid[i+7][1] == grid[i+14][1] and grid[i+14][1] == grid[i+21][1]:
                        return grid[i][1]
                #diag TOP />
                if y > 2 and x < 4:
                    if (-1) != grid[i][1] and grid[i][1] == grid[i-6][1] and grid[i-6][1] == grid[i-12][1] and grid[i-12][1] == grid[i-18][1]:
                        return grid[i][1]
                #diag BOT \>
                if y < 3 and x < 4:
                    if (-1) != grid[i][1] and grid[i][1] == grid[i+8][1] and grid[i+8][1] == grid[i+16][1] and grid[i+16][1] == grid[i+24][1]:
                        return grid[i][1]
        return (-1)

    def point_counter(self, grid, player):
        def p_chg(val):
            if val == (-1):
                return 1
            return Grid.player_change(val, player)
         
        points = 0
        for y in range(6):
            for x in range(7):
                i = 7 * y + x
                #Ligne
                if x < 4:
                    points += p_chg(grid[i][1]) * p_chg(grid[i+1][1]) * p_chg(grid[i+2][1]) * p_chg(grid[i+3][1])
                #collonne
                if y < 3:
                    points += p_chg(grid[i][1]) * p_chg(grid[i+7][1]) * p_chg(grid[i+14][1]) * p_chg(grid[i+21][1])

                #diag TOP />
                if y > 2 and x < 4:
                    points += p_chg(grid[i][1]) * p_chg(grid[i-6][1]) * p_chg(grid[i-12][1]) * p_chg(grid[i-18][1])

                #diag BOT \>
                if y < 3 and x < 4:
                    points += p_chg(grid[i][1]) * p_chg(grid[i+8][1]) * p_chg(grid[i+16][1]) * p_chg(grid[i+24][1])

        #gagnant
        winner = self.check_win(grid)
        if winner == player:
            points += 9999999999
            points **= 2
        elif winner != (-1):
            points -= points
            points -= 9999999999

        return int(points)

    def player_change(value, player):
        if player == 0:
            return value * (-3) + 3
        else:
            return value * 3