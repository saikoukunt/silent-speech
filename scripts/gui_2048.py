import random
import copy
import pygame
from sympy import false

class Board():
    def __init__(self, size = 4, score = 0, array = [], temp = False):
        self.width = 600
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('2048')

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.thickness = 50

        self.size = size
        self.array = array
        if array == []:
            for i in range(size):
                self.array.append([0] * size)
        self.score = score
        self.temp = temp
        self.rect = (self.width / self.thickness, self.height - self.width * ((self.thickness - 1) / self.thickness), self.width * ((self.thickness - 2) / self.thickness), self.width * ((self.thickness - 2) / self.thickness))

    def add_tile(self):
        # Adds a tile to the game board (2 with 90% chance and 4 with 10% chance)
        open_spots = []
        for x in range(self.size):
            for y in range(self.size):
                if self.array[x][y] == 0:
                    open_spots.append([x, y])
        if not open_spots:
            return
        new_spot = random.choice(open_spots)
        x, y = new_spot[0], new_spot[1]
        self.array[x][y] = random.choices([2, 4], weights = [0.9, 0.1])[0]
    
    def move(self):
        # Move the board based on the current key being pressed
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_left()
            if temp_board.array != self.array:
                self.move_left()
        
        elif keys[pygame.K_RIGHT]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_right()
            if temp_board.array != self.array:
                self.move_right()

        elif keys[pygame.K_UP]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_up()
            if temp_board.array != self.array:
                self.move_up()

        elif keys[pygame.K_DOWN]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_down()
            if temp_board.array != self.array:
                self.move_down()
        

    def move_left(self):
        # Move the board left, combining tiles as they move
        for row in self.array:
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if row[i] == 0:
                        if i == last_tile:
                            row[i] = int(row[x])
                            row[x] = 0
                            break
                    elif row[i] == row[x]:
                        row[i] *= 2
                        self.score += row[i]
                        row[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        row[i+1] = int(row[x])
                        if i + 1 != x:
                            row[x] = 0
                        break
        if not self.temp:
            self.add_tile()
        if self.check_loss():
            self.restart()

    def move_right(self):
        # Move the board right, combining tiles as they move
        for row in self.array:
            row.reverse()
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if row[i] == 0:
                        if i == last_tile:
                            row[i] = int(row[x])
                            row[x] = 0
                            break
                    elif row[i] == row[x]:
                        row[i] *= 2
                        self.score += row[i]
                        row[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        row[i+1] = int(row[x])
                        if i + 1 != x:
                            row[x] = 0
                        break
            row.reverse()
        if not self.temp:
            self.add_tile()
        if self.check_loss():
            self.restart()

    def move_up(self):
        # Move the board up, combining tiles as they move
        for y in range(self.size):
            col = []
            for x in range(self.size):
                col.append(int(self.array[x][y]))
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if col[i] == 0:
                        if i == last_tile:
                            col[i] = int(col[x])
                            col[x] = 0
                            break
                    elif col[i] == col[x]:
                        col[i] *= 2
                        self.score += col[i]
                        col[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        col[i+1] = int(col[x])
                        if i + 1 != x:
                            col[x] = 0
                        break
            for x in range(self.size):
                self.array[x][y] = col[x]
        if not self.temp:
            self.add_tile()
        if self.check_loss():
            self.restart()

    def move_down(self):
        # Move the board down, combining tiles as they move
        for y in range(self.size):
            col = []
            for x in range(self.size):
                col.append(int(self.array[x][y]))
            col.reverse()
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if col[i] == 0:
                        if i == last_tile:
                            col[i] = int(col[x])
                            col[x] = 0
                            break
                    elif col[i] == col[x]:
                        col[i] *= 2
                        self.score += col[i]
                        col[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        col[i+1] = int(col[x])
                        if i + 1 != x:
                            col[x] = 0
                        break
            col.reverse()
            for x in range(self.size):
                self.array[x][y] = col[x]
        if not self.temp:
            self.add_tile()
        if self.check_loss():
            self.restart()

    def draw(self):
        # Score
        text = self.font.render('Score : ' + str(self.score), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.width / 2, 50)
        self.win.blit(text, textRect)

        # Main Board Space
        pygame.draw.rect(self.win, (160, 160, 160), self.rect)

        # Tiles
        length = (self.thickness - 2 - self.size - 1) * self.width / (self.thickness * self.size)
        for x in range(self.size):
            for y in range(self.size):
                rect = (self.rect[0] + (self.width * (x + 1) / self.thickness) + length * x, self.rect[1] + (self.width * (y + 1) / self.thickness) + length * y, length, length)
                pygame.draw.rect(self.win, self.color(self.array[y][x]), rect)
                # Tile Value
                if self.array[y][x] != 0:
                    text = self.font.render(str(self.array[y][x]), True, (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (rect[0] + length / 2, rect[1] + length / 2)
                    self.win.blit(text, textRect)

    def board_full(self):
        # Check if there are any open spots on the board
        for row in self.array:
            if 0 in row:
                return false
        return True

    def check_loss(self):
        # We can only lose if every tile is filled so check that first
        if not self.board_full():
            return False

        # Check if it is possible to move in any of the four directions
        temp_board = Board(array = copy.deepcopy(self.array))
        temp_board.move_left()
        if temp_board.array != self.array:
            return False

        temp_board = Board(array = copy.deepcopy(self.array))
        temp_board.move_up()
        if temp_board.array != self.array:
            return False

        temp_board = Board(array = copy.deepcopy(self.array), temp = True)
        temp_board.move_right()
        if temp_board.array != self.array:
            return False

        temp_board = Board(array = copy.deepcopy(self.array), temp = True)
        temp_board.move_down()
        if temp_board.array != self.array:
            return False

        return True

    def restart(self):
        # Create a fresh board and place two starting tiles
        self.score = 0
        self.array = []
        for i in range(self.size):
            self.array.append([0] * self.size)
        self.add_tile()
        self.add_tile()

    def print_board(self):
        for row in self.array:
            print(row)

    def color(self, val):
        colors = {
            0: (180, 180, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 197, 63),
            1024: (237, 197, 63),
            2048: (237, 197, 30),
            4096: (100, 184, 145),
            8192: (56, 140, 100),
            16384: (56, 107, 126),
        }
        return colors[val]

    def redraw_window(self):
        self.win.fill((255, 255, 255))
        self.font.render('Score : ', False, (0, 0, 0))
        self.draw()
        pygame.display.update()

    def run(self, input):
        
        clock = pygame.time.Clock()
    
        # Changes grid size
        current_size = 4

        # Creates a board an populates it with 2 starting tiles
        self.restart()

        # Main loop
        while True:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            # This enables keyboard interaction with arrow keys
            # Comment it out if you want to test some other form of input
            # b.move()

            # ADD NEW INPUT CONDITIONS HERE

            if not input.empty():
                dir = input.get()
                if dir == 'left':
                    self.move_left()
                if dir == 'right':
                    self.move_right()
                if dir == 'up':
                    self.move_up()
                if dir == 'down':
                    self.move_down

            self.redraw_window()