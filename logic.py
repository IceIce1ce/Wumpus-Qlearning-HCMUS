import pygame
import time
import random
from resources.data import gamedata
from resources.images import Images
pygame.init()

BREEZE = 1 
STENCH = 2
PIT = 4
WUMPUS =8
AGENT = 16
GOLD = 32
BLANK = 64
RED=128

class KB:
    def __init__(self):
        self.unknown = []
        self.pit = []
        self.wumpus = []
        self.stench = []
        self.breeze = []
        self.visited = []
        self.safe = []
        
 
    def PossibleMove(self, str):
        temp = str.split(',')
        try:
            y = int(temp[0])
            x = int(temp[1])
        except ValueError: pass
        arrMove = []
        if(x - 1 >= 0):
            posX = x - 1
            posY = y
            s = chr(posY + 48) + ',' + chr(posX + 48)
            if(self.pit.count(s) == 0 or self.wumpus.count(s) == 0):
                arrMove.append(s)
        if(x + 1 <= 9):
            posX = x + 1
            posY = y 
            s = chr(posY + 48) + ',' + chr(posX + 48)
            if(self.pit.count(s) == 0 or self.wumpus.count(s) == 0):
                arrMove.append(s)
        if(y - 1 >= 0):
            posX = x
            posY = y - 1 
            s = chr(posY + 48) + ',' + chr(posX + 48)
            if(self.pit.count(s) == 0 or self.wumpus.count(s) == 0):
                arrMove.append(s)
        if(y + 1 <= 9):
            posX = x
            posY = y + 1
            s =  chr(posY + 48) + ',' + chr(posX + 48)
            if(self.pit.count(s) == 0 or self.wumpus.count(s) == 0):
                arrMove.append(s)
        
        return arrMove
    
    def addStench(self, str):
        self.stench.append(str)
        moves=[value for value in self.PossibleMove(str) if ((value not in self.safe) and (value not in self.visited))]
        for move in moves:
            self.infereWumpus(move) 
        
    def addBreeze(self, str):
        self.breeze.append(str)
        moves=[value for value in self.PossibleMove(str) if ((value not in self.safe) and (value not in self.visited))]
        for move in moves:
            self.inferePit(move)
            
    def inferePit(self, str):
        if(self.pit.count(str) > 0):
            return
        count = 0
        moves = self.PossibleMove(str)
        for move in moves:
            if(self.visited.count(move) > 0 and self.breeze.count(move) == 0):
                return
            else:
                if(self.breeze.count(move) > 0 and self.safe.count(move) == 0):
                    count = count + 1
                
        if(count >= 2 and self.pit.count(str) == 0):
            self.pit.append(str)
            if(self.unknown.count(str)):
                self.unknown=[value for value in self.unknown if value != str]
            self.unknown=[value for value in moves if value not in self.unknown]    
        else:
            self.unknown.append(str)
            
    def infereWumpus(self, str):
        if(self.wumpus.count(str) > 0):
            return
        count = 0
        moves = self.PossibleMove(str)
        for move in moves:
            if(self.visited.count(move) > 0 and self.stench.count(move) == 0):
                return
            else:
                if(self.stench.count(move) and self.safe.count(move) == 0):
                    count = count + 1
                
        if(count >= 2 and self.wumpus.count(str) == 0):
            self.wumpus.append(str)
            if(self.unknown.count(str)):
                self.unknown=[value for value in self.unknown if value != str]
            self.unknown=[value for value in moves if value not in self.unknown]
        else:
            self.unknown.append(str)
         
class Process:
    def __init__(self, map):
        self.history_move = []
        self.map = map
        self.KB = KB()
        y, x = self.map.find_agent()
        pos = chr(y + 48) + ',' + chr(x + 48)
        self.KB.visited.append(pos)

    def FindNearest(self, cur):
        temp = cur.split(',') #lấy vị trí hiện tại
        y = int(temp[0])
        x = int(temp[1])
        temp = self.KB.safe[0].split(',') #lấy vị trí safe đầu tiên
        dist_y = int(temp[0])
        dist_x = int(temp[1])
        res1=[]
        Max = abs(dist_x - x) + abs(dist_y - y)
        res = self.KB.safe[0]
        for s in self.KB.safe:
            if(s != self.KB.safe[0]):
                temp = s.split(',')
                temp_y = int(temp[0])
                temp_x = int(temp[1])
                value = abs(temp_x - x) + abs(temp_y - y)
                if(Max > value):
                    res = s
                    Max = value
        res1.append(res)
        return res1    
   
        
    def CalculateMove(self):
        y, x = self.map.find_agent()
        pos = chr(y + 48) + ',' + chr(x + 48)
        res = []
        # Check xem cur pos là ô trống k có dấu hiệu/vàng
        if(self.map.has_status(y, x, STENCH) == False and self.map.has_status(y, x, BREEZE) == False and self.map.has_status(y, x, GOLD) == False):
            next_move = self.KB.PossibleMove(pos)
            for s in next_move:
                if self.KB.visited.count(s)==0:          
                    if(self.KB.safe.count(s) == 0): 
                        self.KB.safe.append(s)
                    if(self.KB.unknown.count(s) > 0):
                        self.KB.unknown.remove(s)
                    if(self.KB.pit.count(s) > 0):
                        self.KB.pit.remove(s)
                    if(self.KB.wumpus.count(s)>0):
                        self.KB.wumpus.remove(s)    
            next_move=[i for i in next_move if i not in self.KB.visited]
            if(len(next_move) != 0):
                move_rand=random.randint(0, len(next_move) - 1)
                move=next_move[move_rand]
                self.KB.visited.append(move)
                res.append(move)
                while(self.KB.safe.count(move) > 0): 
                    self.KB.safe.remove(move)
                self.history_move.append(pos)
                return res 
            else: 
                if(len(self.KB.safe) != 0):
                    res=self.FindNearest(pos)
                    return res  
            return
        
        if(self.map.has_status(y, x, GOLD)):
            next_move = self.KB.PossibleMove(pos)
            for s in next_move:
                if self.KB.visited.count(s) ==0:          
                    if(self.KB.safe.count(s) == 0): 
                        self.KB.safe.append(s)
                    if(self.KB.unknown.count(s) > 0):
                        self.KB.unknown.remove(s)
                    if(self.KB.pit.count(s) > 0):
                        self.KB.pit.remove(s)
                    if(self.KB.wumpus.count(s)>0):
                        self.KB.wumpus.remove(s)  
            next_move=[i for i in next_move if i not in self.KB.visited]
            if(len(next_move) != 0):
                move_rand=random.randint(0, len(next_move) - 1)
                move=next_move[move_rand]
                res.append(move)
                self.KB.visited.append(move)
                while(self.KB.safe.count(move) > 0): #move in self.KB.safe
                    self.KB.safe.remove(move)
                self.history_move.append(pos)
                return res
            else: 
                if(len(self.KB.safe) != 0):
                    res=self.FindNearest(pos)     
                    return res      
            return 
        
        else:  # là trường hợp Stench or Breeze
            next_move = self.KB.PossibleMove(pos)
            if pos not in self.KB.visited:
                self.KB.visited.append(pos)
            if (self.map.has_status(y, x, STENCH)):
                local = chr(y + 48) + ',' + chr(x + 48)
                self.KB.addStench(local)
            if (self.map.has_status(y, x, BREEZE)):
                local = chr(y + 48) + ',' + chr(x + 48)
                self.KB.addBreeze(local)
            
            for s in next_move:
                if(self.KB.safe.count(s) > 0):
                    self.KB.visited.append(s)
                    while(self.KB.safe.count(s) > 0):
                        self.KB.safe.remove(s)
                    self.history_move.append(pos)
                    res.append(s)
                    return res
            nextmove=[]
            for s in next_move:
                if(self.KB.visited.count(s) > 0 and self.KB.stench.count(s) == 0 and self.KB.breeze.count(s) == 0):
                    nextmove.append(s)
            move_rand=random.randint(0, len(nextmove) - 1)
            move=nextmove[move_rand]
            res.append(move)    
            self.history_move.append(pos)
            return res            
 
def main(gamemap, gamecontrol, move, process):
    #if(len(move) != 0):
    move = process.CalculateMove()
    if(len(move) == 0 or len(move) != 0 and move[0] ==""):
        return -1
    
    print(move)
    s = move[0]
    move_next = s.split(',')
    y = int(move_next[0])
    x = int(move_next[1])
    row,col = gamecontrol.move(y,x)
    gamemap.open(row, col)

    time.sleep(0)

class GameControl:
    def __init__(self, gamemap):
        self.gamemap = gamemap

    def move(self, next_row, next_col):
        row, col = self.gamemap.find_agent()
        if (self.gamemap.is_legal(next_row, next_col) == False):
            return [row, col]

        self.gamemap.del_status(row, col, AGENT)
        self.gamemap.add_status(next_row, next_col, AGENT)
        return [next_row, next_col]

class Cell:
    def __init__(self):
        self.status = 0
        self.closed = True

class GameMap:
    def __init__(self, row_count, col_count):
        self.cell_table = [[]] * row_count
        for i in range(row_count):
            self.cell_table[i] = [None] * col_count
            for j in range(col_count):
                self.cell_table[i][j] = Cell()

    # Return (row, col)
    def find_agent(self):
        for i in range(self.get_row_count()):
            for j in range(self.get_col_count()):
                if (self.has_status(i, j, AGENT)):
                    return [i, j]
        return [-1, -1]

    #Đọc map
    def load_map(self, path):
        f=open(path,'r')
        size_maze=f.readline()
        size_maze=int(size_maze)
        matrix=f.readlines()
        for i in range(len(matrix)):
            x=matrix[i].strip()
            y=x.split('.')
            for j in range(len(y)):
                if y[j]=='W':
                    self.add_status(i,j, WUMPUS)
                if y[j]=='P':
                    self.add_status(i,j, PIT)
                if y[j]=='S':
                    self.add_status(i,j, STENCH)
                if y[j]=='B':
                    self.add_status(i,j, BREEZE)
                if y[j]=='G':
                    self.add_status(i,j, GOLD)
                if y[j]=="BS":
                    self.add_status(i,j,BREEZE)
                    self.add_status(i,j,STENCH)
        y_agent,x_agent=random.randint(0,10),random.randint(0,10)
        while self.has_status(x_agent,y_agent,WUMPUS)==True or self.has_status(x_agent,y_agent,PIT)==True or self.has_status(x_agent,y_agent,STENCH)==True or self.has_status(x_agent,y_agent,BREEZE)==True or self.has_status(x_agent,y_agent,GOLD)==True:
            x_agent,y_agent=random.randint(0,10),random.randint(0,10)

        self.add_status(y_agent,x_agent, AGENT)
        self.add_status(y_agent,x_agent,RED)
        self.open(y_agent, x_agent)
              
        f.close()
 
    def get_row_count(self):
        return len(self.cell_table)

    def get_col_count(self):
        return len(self.cell_table[0])

    def is_legal(self, row, col):
        zero = row >= 0 and col >= 0
        size = row < self.get_row_count() and col < self.get_col_count()
        return zero and size


    def open(self, row, col):
        if (self.is_legal(row, col) == False):
            return
        self.cell_table[row][col].closed = False
        s = chr(row + 48) + ',' + chr(col + 48)

    def add_status(self, row, col, status):
        if (self.is_legal(row, col) == False):
            return
        self.cell_table[row][col].status |= status

    def del_status(self, row, col, status):
        if (self.is_legal(row, col) == False):
            return
        self.cell_table[row][col].status &= ~status

    def has_status(self, row, col, status):
        if (self.is_legal(row, col) == False):
            return False
        return (self.cell_table[row][col].status & status) > 0
class ModelBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

class Model:
    def __init__(self, type, modelbox):
        self.type = gamedata.get_type(type)
        self.image = self.type["image"]
        self.modelbox = modelbox

    def set_point(self, point):
        self.modelbox.x = point[0]
        self.modelbox.y = point[1]

    def get_point(self):
        return [self.modelbox.x, self.modelbox.y]

    def get_size(self):
        return [self.modelbox.width, self.modelbox.height]

    def draw(self, window):
        window.draw(self.image, self.modelbox)

class Archer(Model):    
    def __init__(self):
        super().__init__("ARCHER", ModelBox(0, 0, 64, 64))
        self.current = ""
        self.score = 0 
    
class Blank(Model):
    def __init__(self):
        super().__init__("CLOSE", ModelBox(0, 0, 64, 64))

class Breeze(Model):
    def __init__(self):
        super().__init__("BREEZE", ModelBox(0, 0, 64, 64))

class Gold(Model):
    def __init__(self):
        super().__init__("GOLD", ModelBox(0, 0, 64, 64))

class Grid(Model):
    def __init__(self):
        super().__init__("GRID", ModelBox(0, 0, 640, 640))

class Pit(Model):
    def __init__(self):
        super().__init__("PIT", ModelBox(0, 0, 64, 64))

class Stench(Model):
    def __init__(self):
        super().__init__("STENCH", ModelBox(0, 0, 64, 64))
    
class Wumpus(Model):
    def __init__(self):
        super().__init__("WUMPUS", ModelBox(0, 0, 64, 64))

class Red(Model):
    def __init__(self):
        super().__init__("RED",ModelBox(0, 0, 64, 64))

class GameBoard:
    def __init__(self, map):
        self.map = map
        self.grid_model = Grid()
        self.blank_model = Blank()
        self.game_models = {
            AGENT: Archer(),
            PIT: Pit(),
            GOLD: Gold(),
            WUMPUS: Wumpus(),
            BREEZE: Breeze(),
            STENCH: Stench(),
            RED: Red()
        }

    def draw_model(self, window, model, r, c):
        size = model.get_size()
        point = model.get_point()
        point[0] = c * size[0]
        point[1] = r * size[1]
        model.set_point(point)
        model.draw(window)
    
    def draw_models(self, window, r, c):
        for key in self.game_models.keys():
            if (self.map.has_status(r, c, key)):
                self.draw_model(window, self.game_models[key], r, c)

    def draw(self, window):
        row_count = self.map.get_row_count()
        col_count = self.map.get_col_count()
        for r in range(row_count):
            for c in range(col_count):
                if (self.map.cell_table[r][c].closed):
                    self.draw_model(window, self.blank_model, r, c)
                else:
                    self.draw_models(window, r, c)

        self.grid_model.draw(window)

class Window:
    def __init__(self, title, width = 800, height = 600):
        self.display = pygame.display
        self.display.set_caption(title)
        self.surface = self.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.images = Images()
        self.background = ""
        self.running = True

    def draw(self, path, modelbox):
        if (path == None or path == ""):
            return

        temp = pygame.transform.scale(self.images.get(path), (modelbox.width, modelbox.height))
        self.surface.blit(temp, (modelbox.x, modelbox.y))
    
    def begin(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.surface.fill((255, 255, 255))
        self.draw(self.background, ModelBox(0, 0, 640, 640))

    def end(self):
        self.display.update()
        self.clock.tick(60)

def mainLogic():
    numberHero1 = input("Input type of map (1-5): ")  # 5 maps of game
    while numberHero1 <= '0' or numberHero1 >= '6':
        print("File of map isn't exist, try-again !!! ")
        numberHero1 = input("Input again type of wall (1-5): ")
    type_of_map1 = "map" + numberHero1 + ".txt"
    window = Window("Wumpus World", gamedata.get_rows() * 64, gamedata.get_cols() * 64)
    window.background = "background.png"
    gamemap = GameMap(10, 10)
    gamemap.load_map(type_of_map1)
    gamecontrol = GameControl(gamemap)
    board = GameBoard(gamemap)
    move = []
    process = Process(gamemap)
    while (window.running):
        window.begin()
        if main(gamemap, gamecontrol, move, process) ==-1:
            break
        board.draw(window)
        window.end()
    pygame.quit()