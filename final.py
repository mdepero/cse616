import random

#----------------------------set global variables-----------------------#
rows = 100
cols = 100
time = 100
step = 1

wolfMatureAge = 8
wolfMinChildAge = 0
wolfMaxChildAge = 4
wolfChildFood = 2
wolfMaxFood = 4
wolfMinInitAge = 0
wolfMaxInitAge = wolfMatureAge

sheepMatureAge = 8
sheepMinChildAge = 0
sheepMaxChildAge = 4
sheepChildFood = 2
sheepMaxFood = 4
sheepMinInitAge = 0
sheepMaxInitAge = wolfMatureAge

grassMatureAge = 4

wolfProb = .2
sheepProb = .4

moves = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]

grass = [[0] * rows] * cols
grid = [[0] * rows] * cols

assert wolfMaxChildAge < wolfMatureAge
assert sheepMaxChildAge < sheepMatureAge
assert wolfProb + sheepProb <= 1

#-------------------------define tile class and move function------------------#

def moveTo(i,j,k,l):
    grid[i+k][j+l] = grid[i][j]
    grid[i][j].type = "empty"


class Tile:
    def __init__(self, animalType, age, food):
        self.type = animalType
        self.sex = "male" if random.random() < .5 else "female"
        self.age = age
        self.hasChild = False
        self.childAge = 0
        self.foodRation = food;



#----------------------------initialize simulation----------------------#

for j in range(0, rows):
    for k in range(0, cols):
        r = random.random()
        if (r < wolfProb):
            grid[j][k] = Tile("wolf", random.randint(wolfMinInitAge, wolfMaxInitAge), wolfMaxFood)
        else:
            if(r < wolfProb + sheepProb):
                grid[j][k] = Tile("sheep", random.randint(sheepMinInitAge, sheepMaxInitAge), sheepMaxFood)
        grass[j][k] = random.randint(0, grassMatureAge)


#---------------------------run simulation-----------------------------#

#####- for each time step -#####
for i in range(0, time, step):
    ####- for each tile -####
    for j in range(0, rows):
        for k in range(0, cols):
            ### shuffle possible moves so we don't prefer any one direction ###
            random.shuffle(moves)
            tile = grid[j][k]
            eaten = False
            moved = False

            ###- get list of various types of tiles around us -###
            empty = []
            malesheep = []
            maleWolves = []
            for move in moves:
                if(j+move[0] < rows and j+move[0] >= 0 and k+move[1] < cols and k+move[1] >= 0):
                    if (grid[j+move[0]][k+move[1]].type == "empty"):
                        empty.append(move)
                    elif(grid[j+move[0]][k+move[1]].sex == "male"):
                        if(grid[j+move[0]][k+move[1]].type == "sheep" and grid[j+move[0]][k+move[1]].age > sheepMatureAge and grid[j+move[0]][k+move[1]].foodRation > sheepChildFood):
                            malesheeps.append(move)
                        if(grid[j+move[0]][k+move[1]].type == "wolf" and grid[j+move[0]][k+move[1]].age > wolfMatureAge and grid[j+move[0]][k+move[1]].foodRation > wolfChildFood):
                            maleWolves.append(move)

            ###- sheep -###
            if(tile.type == "sheep"):
                ##- handle female specific stuff -##
                if(tile.sex == "female"):
                    #- female with child specific stuff -#
                    if(tile.hasChild == True):
                        if(tile.childAge > random.randint(sheepMinChildAge, sheepMaxChildAge) and len(empty)>0):
                            #- add child -#
                            grid[j+empty[0][0]][k+empty[0][1]] = Tile("sheep", tile.childAge, tile.foodRation)
                            #- child leaves mother -#
                            tile.childAge = 0
                            tile.hasChild = False
                            del empty[0] # this mbb6dcb91-5978-4525-ab33-cc36abe532f1ove is no longer empty b/c child moved there
                        tile.childAge += 1

                    #- handle sheep gaining sheep from male -#
                    if(tile.age > sheepMatureAge and tile.foodRation > sheepMinFood and len(malesheep) > 0 and tile.hasChild == False):
                        tile.hasChild = True
                        tile.childAge = 0

                ##- look for any empty tile with grass -##
                for location in empty:
                    if(grass[j+location[0]][k+location[1]] >= grassMatureAge):
                        ###- grass found, move to that location -###
                        moveTo(j,k,location[0],location[1])
                        moved = True
                        if(tile.foodRation < sheepMaxFood):
                            tile.foodRation = sheepMaxFood
                            eaten = True
                        grass[j+location[0]][k+location[1]] = 0
                        break
                ##- if no grass found, just move randomly -##
                if(not moved and len(empty)>0):
                    moveTo(j,k,empty[0][0],empty[0][1])

            ###- wolf -###
            elif(grid[j][k].type == "wolf"):
                ##- handle female specific stuff -##
                if(tile.sex == "female"):
                    #- female with child specific stuff -#
                    if(tile.hasChild == True):
                        if(tile.childAge > random.randint(wolfMinChildAge, wolfMaxChildAge) and len(empty)>0):
                            #- add child -#
                            grid[j+empty[0][0]][k+empty[0][1]] = Tile("wolf", tile.childAge, tile.foodRation)
                            #- child leaves mother -#
                            tile.childAge = 0
                            tile.hasChild = False
                            del empty[0] # this move is no longer empty b/c child moved there
                        tile.childAge += 1

                    ##- handle sheep gaining sheep from male -##
                    if(tile.age > wolfMatureAge and tile.foodRation > wolfMinFood and len(malesWolves) > 0 and tile.hasChild == False):
                        tile.hasChild = True
                        tile.childAge = 0

                #- look for any empty tile with grass -#
                if(tile.foodRation < wolfMaxFood):
                    for location in moves:
                        if(j+location[0] < rows and j+location[0] >= 0 and k+location[1] < cols and k+location[1] >= 0):
                            if(grid[j+location[0]][k+location[1]].type == "sheep"):
                                ###- grass found, move to that location -###
                                moveTo(j,k,location[0],location[1])
                                moved = True
                                eaten = True
                                tile.foodRation = wolfMaxFood
                                grass[j+location[0]][k+location[1]] = 0
                                break

                #- if no grass found, just move randomly -#
                if(not moved and len(empty)>0):
                    moveTo(j,k,empty[0][0],empty[0][1])

            ###-handle grass-###
            grass[j][k] = grass[j][k]+1
            if(not eaten):
                tile.foodRation = tile.foodRation-1
                if(tile.foodRation == 0):
                    tile.type = "empty"
