from tkinter.ttk import Frame
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from tkinter import ALL
import random
import numpy as np
import time
import json

# handle image using json
with open('dataQlearning.json') as f: dataImg = json.load(f) # load data from json
raw_data_img1 = dataImg["imgWumpusGame"][0] # take dictionary of element 0
wallHero = raw_data_img1.get('img1') # get data img1
raw_data_img2 = dataImg["imgWumpusGame"][1] # take dictionary of element 1
breezeHero = raw_data_img2.get('img2') # get data img2
raw_data_img3 = dataImg["imgWumpusGame"][2] # take dictionary of element 2
agentHero = raw_data_img3.get('img3') # get data img3
raw_data_img4 = dataImg["imgWumpusGame"][3] # take dictionary of element 3
wumpusHero = raw_data_img4.get('img4') # get data img4
raw_data_img5 = dataImg["imgWumpusGame"][4] # take dictionary of element 4
floorHero = raw_data_img5.get('img5') # get data img5
raw_data_img6 = dataImg["imgWumpusGame"][5] # take dictionary of element 5
pitHero = raw_data_img6.get('img6') # get data img6
raw_data_img7 = dataImg["imgWumpusGame"][6] # take dictionary of element 6
goldHero = raw_data_img7.get('img7') # get data img7
raw_data_img8 = dataImg["imgWumpusGame"][7] # take dictionary of element 7
stenchHero = raw_data_img8.get('img8') # get data img8

# main process for game: set GUI, button, map, image, handle movement, check collision...
class MainProcess(tk.Canvas):
    def __init__(self, master, mapGame, agent_qlearning, *args, **kwargs):
        # master: Frame, map: map of game, agent_qlearning: type of agent is used in game is q_learning
        tk.Canvas.__init__(self, *args, **kwargs, bg='#26201c')
        self.master = master
        self.map = mapGame
        self.agent_qlearning = agent_qlearning
        text = Label(self, text="Please wait about 5s to finish train the agent", bg="#26201c", fg="#fff")
        text.place(x=90, y=490)
        # set button type of game
        self.button = Button(text="Start wumpus Qlearning", fg="black", command=self.StartButtonQlearning, bg="pink")
        self.button.place(x=135, y=440)
        self.Score = 0 # default score of agent is 0
        # init for map
        self.Init_Map()
        self.pack() # self.canvas.pack()
    # button use for logic agent
    def StartButtonQlearning(self):
        self.delete(ALL) # clear all items from the canvas to start on a clean slate
        self.StartWumpusQlearning() # start logic agent game from button
    # init image for game
    def InitImageGame(self, wallMap, breezeImg, agentImg, wumpusImg, floorImg, pitImg, goldImg, stenchImg):
        self.wallMap = Image.open(wallMap) # set image for map
        MAX_SIZE_THUMBNAIL_WALL = (42, 42) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.wallMap.thumbnail(MAX_SIZE_THUMBNAIL_WALL, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.map_locs = ImageTk.PhotoImage(self.wallMap) # get position of map for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.wind = Image.open(breezeImg) # set image for breeze
        MAX_SIZE_THUMBNAIL_WIND = (30, 30) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.wind.thumbnail(MAX_SIZE_THUMBNAIL_WIND, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.breeze_locs = ImageTk.PhotoImage(self.wind) # get position of breeze for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.player = Image.open(agentImg) # set image for agent
        MAX_SIZE_THUMBNAIL_PLAYER = (40, 40) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.player.thumbnail(MAX_SIZE_THUMBNAIL_PLAYER, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.player_location = ImageTk.PhotoImage(self.player) # get position of agent for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.wumpus = Image.open(wumpusImg) # set image for wumpus
        MAX_SIZE_THUMBNAIL_MONSTER = (30, 30) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.wumpus.thumbnail((MAX_SIZE_THUMBNAIL_MONSTER), Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.wumpus_locs = ImageTk.PhotoImage(self.wumpus) # get position of wumpus for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.lane = Image.open(floorImg) # set image path agent had moved
        MAX_SIZE_THUMBNAIL_FLOOR = (40, 40) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.lane.thumbnail(MAX_SIZE_THUMBNAIL_FLOOR, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.floor_locs = ImageTk.PhotoImage(self.lane) # get position of floor for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.pit = Image.open(pitImg) # set image for pit
        MAX_SIZE_THUMBNAIL_PIT = (30, 30) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.pit.thumbnail(MAX_SIZE_THUMBNAIL_PIT, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.pit_locs = ImageTk.PhotoImage(self.pit) # get position of pit for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.gold = Image.open(goldImg) # set image for goal
        MAX_SIZE_THUMBNAIL_GOLD = (30, 30) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.gold.thumbnail(MAX_SIZE_THUMBNAIL_GOLD, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.gold_locs = ImageTk.PhotoImage(self.gold) # get position of gold for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.smell = Image.open(stenchImg) # set image for stench
        MAX_SIZE_THUMBNAIL_STENCH = (30, 30) # modifiy the image to contain a thumbnail version of itself, no larger than the given size
        self.smell.thumbnail(MAX_SIZE_THUMBNAIL_STENCH, Image.ANTIALIAS) # use antialias to get a high-quality downsampling filter
        self.stench_locs = ImageTk.PhotoImage(self.smell) # get position of stench for drawing, PhotoImage class is used to display images in labels, buttons, canvases, and text widgets
        self.isWin = False # set default win = False
        self.GameOver = False # set default game over = False
        # default map: x_start = 0, y_end = 9, these value use for random position of agent
        self.row = 0
        self.column = 9
    def Create_tiles(self, x, y): self.create_image(x, y, image=self.map_locs, anchor=NW, tag="tiles") # create image cells for map game
    def DrawTiles(self):
        self.Create_tiles(10, 10) # draw tile at first position
        # min row/column: 10, max row/column: 370
        # j = 0, 40, 80, 120, 160, 200, 240, 280, 320, 360
        for j in range(0, 361, 40):
            # i = 0, 40, 80, 120, 160, 200, 240, 280, 320
            for i in range(0, 321, 40): self.Create_tiles(50 + i, 10 + j) # tile's interval (10, 50, 90, 130, 170, 210, 250, 290, 330, 370)
        for i in range(0, 321, 40): self.Create_tiles(10, 50 + i) # draw all cells in first column except first cell had drawn before
        self.pack(fill=BOTH, expand=1)
    def Init_Map(self):
        self.InitImageGame(wallHero, breezeHero, agentHero, wumpusHero, floorHero, pitHero, goldHero, stenchHero) # init for game
        self.DrawTiles() # draw image for map
        self.create_map() # create map
    def StartWumpusQlearning(self):
        self.Init_Map() # init map for logic game
        x_agent, y_agent = self.agent_qlearning.get_position() # get current position of agent
        error_square_grid = 10 # change this value to balance distance wall stains when agent moving
        # thumbnail = (40,40), so we have to take current coordinate of agent multiply 40
        self.x, self.y = self.Player_Location(error_square_grid + y_agent * 40, error_square_grid + x_agent * 40)
        self.agent_qlearning.training(self.map) # start training agent
        # if agent didn't finish process (finish limit move or episode)
        while not self.agent_qlearning.finishProcess():
            row, column = self.agent_qlearning.get_action() # get action agent could be do at that position
            self.agent_qlearning.move(row, column, self.map[row][column]) # get best move
            self.Move(column, row) # start move agent
            self.Score = self.agent_qlearning.get_total_rewards() # get total score of agent
            time.sleep(0.1)
            self.update() # update each state moving
            self.IsGameOver() # check if agent lose the game
            self.IsAgentWin() # check if agent win the game
    def IsGameOver(self):
        if self.GameOver: self.Animation_GameOver() # animation if agent lose the game
    def IsAgentWin(self):
        if self.isWin: self.Animation_Winner() # animation if agent win the game
    def AnimateGifWin(self, counter1):
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("image/wingame.gif"))]
        self.image = self.create_image(200, 200, image=self.sequence[0])
        self.itemconfig(self.image, image=self.sequence[counter1])
        self.after(100, lambda: self.AnimateGifWin((counter1+1) % len(self.sequence)))
    def Animation_Winner(self):
        self.delete(ALL) # delete all state of game after finishing, then animate gif image
        while True:
            self.AnimateGifWin(1)
            self.update()
    def AnimateGifLose(self, counter):
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("image/gameover.gif"))]
        self.image = self.create_image(200, 200, image=self.sequence[0])
        self.itemconfig(self.image, image=self.sequence[counter])
        self.after(100, lambda: self.AnimateGifLose((counter+1) % len(self.sequence)))
    def Animation_GameOver(self):
        self.delete(ALL) # delete all state of game after finishing, then animate gif image
        while True:
            self.AnimateGifLose(1)
            self.update()
    def ConvertLocationToCoordinate(self, column, row):
        # make row/col from 0-9 become: 10, 50, 90, 130, 170, 210, 250, 290, 330, 370 for handling movement of image
        column, row = 10 + 40 * column, 10 + 40 * row # thumbnail agent set (40, 40)
        return column, row
    def Move(self, x, y):
        # convert current position to coordinate, example agent's current position is (4,8) -> coordinate image (170, 330)
        x, y = self.ConvertLocationToCoordinate(x, y) # min coordinate: 10 + 40 * 0 = 10, max coordinate: 10 + 40 * 9 = 370
        location = self.find_withtag("player") # get agent
        if len(location) != 0: self.delete(location[0]) # if current location of agent after randoming is not an empty cell
        ################### need fix something here for better movement ##################
        if self.x == x:
            if self.y > y and (self.y - y) == 40: self.Top(x, y)
            elif self.y > y and (self.y - y) > 40:
                y = self.y - 40
                self.Top(x, y)
            elif self.y < y and (y - self.y) == 40: self.Down(x, y)
            elif self.y < y and (y - self.y) > 40:
                self.y = y - 40
                self.Down(x, y)
        elif self.y == y:
            if self.x > x and (self.x - x) == 40: self.Left(x, y)
            elif self.x > x and (self.x - x) > 40:
                x = self.x - 40
                self.Left(x, y)
            elif self.x < x and (x - self.x) == 40: self.Right(x, y)
            elif self.x < x and (x - self.x) > 40:
                self.x = x - 40
                self.Right(x, y)
        elif self.x != x and self.y != y:
            if self.y > self.x and y > x:
                if (self.x - x) == 40 or (x - self.x) == 40:
                    x = self.x
                    if self.y > y: self.Top(x, y)
                    else: self.Down(x, y)
                elif (x - self.x) > 40:
                    y = self.y
                    self.Right(x, y)
                elif (self.x - x) > 40:
                    y = self.y
                    self.Left(x, y)
            '''
            elif self.x > self.y and x > y:
                if (self.y - y) == 40 or (y - self.y) == 40:
                    y = self.y
                    if self.x > x: self.Left(x, y)
                    else: self.Right(x, y)
                elif (y - self.y) > 40:
                    x = self.x
                    self.Down(x, y)
                elif (self.y - y) > 40:
                    x = self.x
                    self.Top(x, y)
            '''
        ################### need fix something here for better movement ##################
    def Left(self, x, y):
        thumbnailDistanceBetweenCell = 40
        x = x + thumbnailDistanceBetweenCell # default error distance when moving between cells
        self.create_image((x, y), image=self.floor_locs, anchor=NW, tag="lane") # print footprint in map when agent moving
        self.row -= 1 # decrease value row when moving left
        self.x, self.y = self.Player_Location(x - thumbnailDistanceBetweenCell, y) # update new position of agent
        self.checkCollision() # check left direction is collision or not
    def Right(self, x, y):
        thumbnailDistanceBetweenCell = 40
        x = x - thumbnailDistanceBetweenCell # default error distance when moving between cells
        self.create_image((x, y), image=self.floor_locs, anchor=NW, tag="lane")  # print footprint in map when agent moving
        self.row += 1 # increase value row when moving right
        self.x, self.y = self.Player_Location(x + thumbnailDistanceBetweenCell, y) # update new position of agent
        self.checkCollision() # check left direction is collision or not
    def Top(self, x, y):
        thumbnailDistanceBetweenCell = 40
        y = y + thumbnailDistanceBetweenCell # default error distance when moving between cells
        self.create_image((x, y), image=self.floor_locs, anchor=NW, tag="lane")  # print footprint in map when agent moving
        self.column -= 1 # decrease value column when moving up
        self.x, self.y = self.Player_Location(x, y - thumbnailDistanceBetweenCell) # update new position of agent
        self.checkCollision() # check left direction is collision or not
    def Down(self, x, y):
        thumbnailDistanceBetweenCell = 40
        y = y - thumbnailDistanceBetweenCell # default error distance when moving between cells
        self.create_image((x, y), image=self.floor_locs, anchor=NW, tag="lane")  # print footprint in map when agent moving
        self.column += 1 # increase value column when moving down
        self.x, self.y = self.Player_Location(x, y + thumbnailDistanceBetweenCell) # update new position of agent
        self.checkCollision() # check left direction is collision or not
    def Player_Location(self, x, y):
        self.create_image(x, y, image=self.player_location, anchor=NW, tag="player") # draw image agent each step moving
        print("current row and column of path's agent:", [x, y])
        return x, y
    def addWumpus(self, x, y): self.create_image(x, y, image=self.wumpus_locs, anchor=NW, tag="wumpus") # draw image for wumpus
    def addPit(self, x, y): self.create_image(x, y, image=self.pit_locs, anchor=NW, tag="pit") # draw image for pit
    def addGold(self, x, y): self.create_image(x, y, image=self.gold_locs, anchor=NW, tag="gold") # draw image for gold
    def addBreeze(self, x, y): self.create_image(x, y, image=self.breeze_locs, anchor=NW, tag="breeze") # draw image for breeze
    def addStench(self, x, y): self.create_image(x, y, image=self.stench_locs, anchor=NW, tag="stench") # draw image for stench
    # add wumpus, pit, gold, breeze, stench to map
    def create_map(self):
        size_map = 10 # default size of map is 10x10
        distance_between_object = 14 # change this value for distance position of objects in map game
        for row in range(size_map):
            for column in range(size_map):
                # if at that cell is pit(character 1), thumbnail floor(40,40), so multiply row/column by 40
                if self.map[row][column] == 1: self.addPit(distance_between_object + column * 40, distance_between_object + row * 40)
                # if at that cell is breeze(character 2), thumbnail floor(40,40), so multiply row/column by 40
                if self.map[row][column] == 2: self.addBreeze(distance_between_object + column * 40, distance_between_object + row * 40)
                # if at that cell is wumpus(character 3), thumbnail floor(40,40), so multiply row/column by 40
                if self.map[row][column] == 3: self.addWumpus(distance_between_object + column * 40, distance_between_object + row * 40)
                # if at that cell is stench(character 4), thumbnail floor(40,40), so multiply row/column by 40
                if self.map[row][column] == 4: self.addStench(distance_between_object + column * 40, distance_between_object + row * 40)
                # if at that cell is gold(character 5), thumbnail floor(40,40), so multiply row/column by 40
                if self.map[row][column] == 5: self.addGold(distance_between_object + column * 40, distance_between_object + row * 40)
    def checkCollision(self):
        # find tags of objects to check collision
        wumpus = self.find_withtag("wumpus")
        pit = self.find_withtag("pit")
        gold = self.find_withtag("gold")
        player = self.find_withtag("player")
        breeze = self.find_withtag("breeze")
        smell = self.find_withtag("stench")
        x1, y1, x2, y2 = self.bbox(player) # get 4 points coordinate move and next move of agent
        overlap = self.find_overlapping(x1, y1, x2, y2) # add tag to all items which overlap the rectangle defined by x1,y1,x2,y2
        for over in overlap:
            for w in wumpus:
                if w == over:
                    self.GameOver = True # set state game to lose for being eaten by wumpus
                    print("Game Over!!! Your agent are eaten by wumpus")
            for p in pit:
                if p == over:
                    self.GameOver = True # set state game to lose for falling into the pit
                    print("Game Over, Your agent are fallen into the pit")
            for g in gold:
                if g == over:
                    self.delete(g) # if agent find gold, delete gold from map
                    self.Score += 100 # then add 100 points for each gold agent eat
                    print("Current score of agent:", self.Score)
                    if len(gold) == 1:
                        print("Agent win the game")
                        self.isWin = True # set state game to win if agent find and eat all gold
            for b in breeze:
                if b == over: print("Cell has breeze") # print notify for moving into breeze cells
            for s in smell:
                if s == over: print("Cell has stench") # print notify for moving into stench cells

performanceMeasure = dict() # create a dictionary for calculating point of reward table
performanceMeasure[0] = -10 # move to empty cell -10 points in reward system
performanceMeasure[1] = -10000 # falling in pit -10000 points in reward system
performanceMeasure[2] = -10 # move to breeze cells -10 points in reward system
performanceMeasure[3] = -10000 # being eaten by wumpus -10000 points in reward system
performanceMeasure[4] = -10 # move to stench cells -10000 points in reward system
performanceMeasure[5] = -10 # pick up gold -10 points in reward system

def DictMapScore(scoreMap):
    initMapScore = dict() # create a dictionary store score of map
    initMapScore[0] = -1 # move to empty cells -1 point
    initMapScore[1] = -10000 # falling into pit -10000 points
    initMapScore[2] = -1 # move to breeze cells -1 point
    initMapScore[3] = -10000 # being eaten by wumpus -10000 points
    initMapScore[4] = -1 # move to stench cells -1 point
    initMapScore[5] = 100 # pick up gold +100 points
    return initMapScore[scoreMap]

# https://www.freecodecamp.org/news/an-introduction-to-q-learning-reinforcement-learning-14ac0b4493cc/
def initRewardTable():
    q_table = np.zeros((100, 100), dtype=int) # create a maxtrix 100x100 with all values are 0
    size_map = 10 # size default of map
    for row in range(size_map):
        for column in range(size_map):
            # get 4 neighbor cells at that cell
            for cell in GetNeighborCells(row, column):
                # example current position agent is (9,8) -> x_pos = 9*10+8=98, 4 points neighbor of that cell is (9,9), (9,7), (8,8), (10,8)
                # (10,8) is out of bound, so ignore that position, (9,9)->y_pos=99, (9,7)->y_pos=97, (8,8)->y_pos=88
                # each cell move decrease -1 point, so update -1
                # set (98,99), (98,97), (98, 88) value -1, similarly all cells in matrix 100x100 of q_table are -1 (just update -1 when this cell is directly reachable from previous cell)
                # else if a location is not directly reachable from a particular location, give a reward of 0
                q_table[row * 10 + column][cell.row * 10 + cell.column] = -1
    return q_table

# update new state at that cell in q_table
def updateRewardTable(q_table, row, column, new_state_qtable):
    for cell in GetNeighborCells(row, column):
        # if cells have breeze, pit, wumpus, stench, update cells at q_table from -1 to correspond states
        q_table[cell.row * 10 + cell.column][row * 10 + column] = new_state_qtable

def RewardtableToMap(mapGame, q_table):
    size_map = 10 # default size of map
    for row in range(size_map):
        for column in range(size_map):
            for cell in GetNeighborCells(row, column):
                # update correspond reward from map to q_table
                q_table[cell.row * 10 + cell.column][row * 10 + column] = DictMapScore(map[row][column])

# https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56
class QAgent:
    def __init__(self, row, column, max_move, discount_factor=0.8, learning_rate=0.5, epsilon=0.1, episode=100):
        self.map = np.zeros((10, 10), dtype=int) # create default size map is a matrix 10x10
        self.row = row
        self.column = column
        self.state = row * 10 + column # current state of agent in matrix 100x100 of reward table
        self.reward_table = initRewardTable()
        # create a q_table size 100x100, default all values from q_table are 0, these values will change after training
        self.q_table = np.array(np.zeros([100, 100])) # initializing q-values
        ''' need fix for double q-learning
        self.q_a_table = np.array(np.zeros([100, 100])) # initializing q-a-values
        self.q_b_table = np.array(np.zeros([100, 100])) # initializing q-b-values
        self.q_table = self.q_a_table + self.q_b_table # initializing q-values
        '''
        self.max_move = max_move # limit move of agent for training purpose
        self.total_reward = 0 # default reward of agent is 0
        self.episode = episode # number of game play, update and store Q-value after an episode, when the episode initially starts, every Q-value is 0
        self.discount_factor = discount_factor # gamma: balance immediate and future reward, usually in range[0.8, 0.99]
        self.learning_rate = learning_rate # alpha: defined how much you accept the new value with the old value
        self.epsilon = epsilon # epsilon: balance exploration by using epsilon, greed 10%
    def adjust_discount_factor(self, discount_factor):
        self.discount_factor = discount_factor
    def adjust_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate
    def adjust_epsilon(self, epsilon):
        self.epsilon = epsilon
    def adjust_episode(self, episode):
        self.episode = episode
    def move(self, row, column, new_state_qtable):
        # update new state of reward table after each step moving of agent
        updateRewardTable(self.reward_table, row, column, performanceMeasure[new_state_qtable])
        self.row = row
        self.column = column
        self.state = self.row * 10 + self.column
        old_reward = self.total_reward # old reward of agent
        self.total_reward += DictMapScore(new_state_qtable) # update point of agent after each new state from q_table
        # if total reward is a negative number, decrease an episode and continue training agent with a new episode
        if self.total_reward - old_reward < -1: self.episode -= 1
        self.update_qtable(row, column)
        self.max_move -= 1 # decrease max limit move of agent (limit move of agent just for training purpose)
    def get_position(self):
        return self.row, self.column # get current position of agent
    def eval_actions(self):
        epsilon = 0.5
        available_actions = []
        for matrix in range(100):
            # assume current position of agent is (0, 1)
            # if coordinate [1][0...99] from reward_table after training still = -1, apply action at that position
            if self.reward_table[self.state][matrix] != 0: available_actions.append(matrix)
        ''' need optimize for evaluating action better
        eps = 0.01
        max_action = np.random.choice(available_actions)
        for best_action in available_actions:
            if self.q_table[self.state][best_action] > self.q_table[self.state][max_action]: max_action = best_action
            elif self.q_table[self.state][best_action] == self.q_table[self.state][max_action]:
                if np.random.uniform(0, 1) < eps: max_action = best_action
        self.state = max_action
        return max_action
        '''
        # break ties among max values randomly if ties exist
        # if no ties exist, the max will be selected with probability = 1
        # on each step, the agent selects maximum value over all the actions for state s' (maxQ(s',a'))
        max_action = available_actions[0] # take first value for max_action, then compare to get max value action
        # max_Q = np.where(np.max(available_actions) == available_actions)[0]
        # max_action = np.random.choice(max_Q)
        for action in available_actions:
            # if q_table[1][0...99 != 0] > self.q_table[1][max(0...99) != 0] -> update max_action
            if self.q_table[self.state][action] > self.q_table[self.state][max_action]: max_action = action
            # elif 2 value are the same, random a number between 0 and 1, then compare with a value epsilon
            elif self.q_table[self.state][action] == self.q_table[self.state][max_action]:
                if random.random() < epsilon: max_action = action
        self.state = max_action # update current state with max_action
        return max_action
    def get_action(self):
        state_action = self.eval_actions() # get max action
        # if state_action is an odd number such as 15, row = 1, column = 5 -> current state = 1 * 10 + 5 = 15
        row, column = int(state_action / 10), int(state_action % 10)
        return row, column
    # https://medium.com/@curiousily/solving-an-mdp-with-q-learning-from-scratch-deep-reinforcement-learning-for-hackers-part-1-45d1d360c120
    # https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/
    # https://blog.floydhub.com/an-introduction-to-q-learning-reinforcement-learning/
    def update_qtable(self, row, column):
        new_epsilon = 0.8 # compare these value with a random number to choose action
        next_state = self.state # assume current position of agent is (1, 1) -> next_state = 1 * 10 + 1 = 11
        # get 4 neighbors at that cell
        for cell in GetNeighborCells(row, column):
            state = cell.row * 10 + cell.column # four coordinates will be (1,0), (1,2), (0,1), (2,1) correspond to state 10, 12, 1, 21
            r = self.reward_table
            available_action = []
            for i in range(100):
                if r[next_state][i] != 0: available_action.append(i) # if reward_table[11][0...99] != 0 after training, add action at that position
            action = np.argmax(self.q_table[next_state,])
            next_max = action
            Temporal_Difference = self.reward_table[state, next_state] + self.discount_factor * self.q_table[next_state, next_max] - self.q_table[state, next_state]
            self.q_table[state, next_state] += self.learning_rate * Temporal_Difference
            ''' need fix for double q-learning
            if np.random.rand() < 0.5:
                self.q_a_table += self.learning_rate * (self.reward_table[state, next_state] + self.discount_factor * self.q_b_table[next_state, np.argmax(self.q_a_table[next_state,])] - self.q_a_table[state, next_state])
            else:
                self.q_b_table += self.learning_rate * (self.reward_table[state, next_state] + self.discount_factor * self.q_a_table[next_state, np.argmax(self.q_b_table[next_state,])] - self.q_b_table[state, next_state])
            '''
        rewards = self.reward_table
        Q = self.q_table
        r = np.copy(rewards) # copy the rewards matrix to new matrix
        for i in range(10):
            state = np.random.randint(0, 100) # pick up a state randomly
            total_reward = 0 # default total reward is 0
            MIN_INF, MAX_INF = -999, 100 # starting location and ending location of total_reward
            while MIN_INF < total_reward < MAX_INF:
                avai_actions = []
                for j in range(100):
                    if r[state, j] != 0: avai_actions.append(j) # iterate through the new rewards matrix and get the actions != 0
                # if value random < epsilon, pick an action randomly from the list of avai action which lead us to next state
                if np.random.uniform(0, 1) < self.epsilon: next_state = np.random.choice(avai_actions) # explore action space
                # else exploit learned values
                else:
                    '''
                    max_next_state = np.max(Q[state, avai_actions])
                    action = avai_actions[0]
                    for i in avai_actions:
                        if Q[state][i] == max_next_state:
                            if random.random() < new_epsilon: action = i
                            else: action = np.argmax(Q[state,])
                    '''
                    max_next_state = Q[state, avai_actions[0]] # take first q_value
                    action = avai_actions[0] # take first action from list
                    for i in avai_actions:
                        if Q[state, i] > max_next_state:
                            max_next_state = Q[state, i] # update again max_next_state if find q_value bigger
                            action = i # update again action
                        elif Q[state][i] == max_next_state:
                            if random.random() < new_epsilon: action = i # if equal, take a value random, then compare to value epsilon to choose action
                    next_state = action
                available_action = []
                for i in range(100):
                    # after moving to next state, add action at next position that new reward table != 0
                    if r[next_state][i] != 0: available_action.append(i)
                action = np.argmax(Q[next_state,])
                next_max = action
                Temporal_Difference = rewards[state, next_state] + self.discount_factor * Q[next_state, next_max] - Q[state, next_state]
                Q[state, next_state] += self.learning_rate * Temporal_Difference
                ''' need fix for double q-learning
                if np.random.rand() < 0.5:
                    self.q_a_table += self.learning_rate * (self.reward_table[state, next_state] + self.discount_factor * self.q_b_table[next_state, np.argmax(self.q_a_table[next_state,])] - self.q_a_table[state, next_state])
                else:
                    self.q_b_table += self.learning_rate * (self.reward_table[state, next_state] + self.discount_factor * self.q_a_table[next_state, np.argmax(self.q_b_table[next_state,])] - self.q_b_table[state, next_state])
                '''
                total_reward += rewards[state, next_state] # update total reward of agent
                state = next_state # change to next state
        self.q_table = Q
    def training(self, map):
        print("Start training process")
        epochs, penalties = 0, 0
        new_epsilon = 0.8
        RewardtableToMap(map, self.reward_table) # convert reward of map correspond to q_table
        rewards = self.reward_table
        gamma_training = 0.75
        Q = self.q_table
        rewards_new = np.copy(rewards) # copy the rewards matrix to new matrix
        # q-learning process
        for i in range(10000):
            state = np.random.randint(0, 100) # pick up a state randomly
            total_reward = 0 # default total reward is 0
            playable_actions = []  # for traversing through the neighbor locations in the maze
            for j in range(100):
                if rewards_new[state, j] != 0: playable_actions.append(j)  # iterate through the new rewards matrix and get the actions != 0
            # if value random < epsilon, pick an action randomly from the list of playable action which lead us to next state
            if np.random.uniform(0, 1) < self.epsilon: next_state = np.random.choice(playable_actions)
            else:
                '''
                max_next_state = np.max(Q[state, playable_actions])
                action = playable_actions[0]
                for i in playable_actions:
                if Q[state][i] == max_next_state:
                if random.random() < new_epsilon: action = i
                else: action = np.argmax(Q[state,])
                '''
                max_next_state = Q[state, playable_actions[0]]
                action = playable_actions[0]
                for i in playable_actions:
                    if Q[state, i] > max_next_state:
                        max_next_state = Q[state, i]
                        action = i
                    elif Q[state][i] == max_next_state:
                        if random.random() < new_epsilon: action = i
                next_state = action
            play_actions = []
            for i in range(100):
                # after moving to next state, add action at next position that new reward table != 0
                if rewards_new[next_state][i] != 0: play_actions.append(i)
            action = np.argmax(Q[next_state,])
            next_max = action
            Temporal_Difference = rewards[state, next_state] + gamma_training * Q[next_state, next_max] - Q[state, next_state]
            Q[state, next_state] += self.learning_rate * Temporal_Difference
            ''' need fix for double q-learning
            if np.random.rand() < 0.5:
                self.q_a_table += self.learning_rate * (self.reward_table[state, next_state] + self.discount_factor * self.q_b_table[next_state, np.argmax(self.q_a_table[next_state,])] - self.q_a_table[state, next_state])
            else:
                self.q_b_table += self.learning_rate * (self.reward_table[state, next_state] + self.discount_factor * self.q_a_table[next_state, np.argmax(self.q_b_table[next_state,])] - self.q_b_table[state, next_state])
            '''
            total_reward += rewards[state, next_state]  # update total reward of agent
            if self.total_reward == -10: penalties += 1
            epochs += 1
        self.q_table = Q
        print("Training finished")
        print(f"Results after {self.episode} episodes:")
        print(f"Average timesteps per episode: {epochs / self.episode}")
        print(f"Average penalties per episode: {penalties / self.episode}")
    def finishProcess(self):
        # if agent has no more limit move or finish episode
        if self.max_move <= 0 or self.episode <= 0: return True
        return False
    def get_total_rewards(self):
        return self.total_reward # return current total reward

def GenerateMap(mapFile):
    size_map = 10
    map = np.zeros((size_map, size_map), dtype=int) # create a matrix 10x10 for map
    map_data = open(mapFile, 'r')
    default_size_map = map_data.readline() # read size of map
    for i in range(size_map):
        line = map_data.readline() # read matrix of map
        for j in range(len(line)):
            if line[j] == 'P':
                # count number of dot line from index 0 to character P at that line
                # number of dot line = column position of pit in that line
                map[i][line.count('.', 0, j)] = 1 # map[0][4], map[1][4], map[2][4], map[3][1]... is positions that have pit, set these positions value 1
                SetNeighborCells(map, i, line.count('.', 0, j), 2) # set up 4 neighbor cells near pit cell character 2 (breeze)
            if line[j] == 'W':
                # count number of dot line from index 0 to character W at that line
                # number of dot line = column position of wumpus in that line
                map[i][line.count('.', 0, j)] = 3 # set up cells that have wumpus value 3
                SetNeighborCells(map, i, line.count('.', 0, j), 4) # set up 4 neighbor cells near wumpus cell character 4 (stench)
            if line[j] == 'G':
                # count number of dot line from index 0 to character G at that line
                # number of dot line = column position of gold in that line
                map[i][line.count('.', 0, j)] = 5 # set cells that have gold value 5 and this value's also use for processing q_learning
    # default random position of agent in any position of map
    random_position_row, random_position_column = np.random.randint(0, 10), np.random.randint(0, 10)
    # if position random for agent is collision pit, wumpus or gold, random position again
    while map[random_position_row][random_position_column] == 1 or map[random_position_row][random_position_column] == 3 or map[random_position_row][random_position_column] == 5:
        random_position_row, random_position_column = np.random.randint(0, 10), np.random.randint(0, 10)
    return default_size_map, map, random_position_row, random_position_column # return size map, map data and position random for agent

class InitCellMap:
    def __init__(self, row, column):
        self.row = row
        self.column = column

def SetNeighborCells(map, row, column, value):
    # add 4 neighbors area around a cell
    leftNeighbor, rightNeighbor, downNeighbor, upNeighbor = InitCellMap(row, column - 1), InitCellMap(row, column + 1), InitCellMap(row - 1, column), InitCellMap(row + 1, column)
    cells = [] # empty cell store 4 neighbors of each cell
    cells.append(leftNeighbor)
    cells.append(rightNeighbor)
    cells.append(downNeighbor)
    cells.append(upNeighbor)
    for cell in cells:
        # if row and column in range(0,9), add value to that cell
        if 0 <= cell.row <= 9 and 0 <= cell.column <= 9: map[cell.row][cell.column] = value

def GetNeighborCells(row, column):
    # add 4 neighbors area around a cell
    leftNeighbor, rightNeighbor, downNeighbor, upNeighbor = InitCellMap(row, column - 1), InitCellMap(row, column + 1), InitCellMap(row - 1, column), InitCellMap(row + 1, column)
    cells = []  # empty cell store 4 neighbors of each cell
    cells.append(leftNeighbor)
    cells.append(rightNeighbor)
    cells.append(downNeighbor)
    cells.append(upNeighbor)
    valid_neighbor_cells = [] # list store 4 neighbor cells that is not out of bound
    for cell in cells:
        # if row and column in range(0,9), add these cells to list valid_cell
        if 0 <= cell.row <= 9 and 0 < cell.column <= 9: valid_neighbor_cells.append(cell)
    return valid_neighbor_cells

class Wumpus(Frame):
    def __init__(self, master, map, row, column, limit_move, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.master = master
        master.title("Wumpus AI")
        agent_qlearning = QAgent(row, column, limit_move)
        self.game = MainProcess(self.master, map, agent_qlearning, width=600, height=600)
        self.pack()

if __name__ == '__main__':
    while True:
        print("Welcome to the wumpus world")
        print("1. Wumpus logic")
        print("2. Wumpus Qlearning")
        print("3. Exit")
        option = int(input("Input your choice (1->2): "))
        if option == 1:
            import logic as logicHero # import here to avoid pygame auto start window
            logicHero.mainLogic()
        elif option == 2:
            numberHero = input("Input type of map (1-5): ")  # 5 maps of game
            while numberHero <= '0' or numberHero >= '6':
                print("File of map isn't exist, try-again !!! ")
                numberHero = input("Input again type of wall (1-5): ")
            type_of_map = "map" + numberHero + ".txt"
            default_size_map, map, random_position_row, random_position_column = GenerateMap(type_of_map)
            limit_move = 100 # increase limit move of agent if size of map is larger
            App = Tk()
            App.geometry("420x540")
            Wumpus(App, map, random_position_row, random_position_column, limit_move)
            App.mainloop()
        elif option == 3:
            exit(0)
        else: print("Invalid input, try-again !!!")