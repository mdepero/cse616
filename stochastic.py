import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation



from parameters_trial import *



trials = 15


moves = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]

grass = np.random.randint(grassMatureAge, size=(rows, cols))
grid = np.empty([rows, cols], dtype=object)

assert wolfProb + sheepProb <= 1
assert sheepMaxFood >= sheepEatFood
assert wolfMaxFood >= wolfEatFood

sheepCount = [[] for x in range(trials)]
wolfCount  = [[] for x in range(trials)]
grassCount = []

#-------------------------define tile class and move function------------------#

def moveTo(i,j,k,l):
    grid[i+k,j+l].type = grid[i,j].type
    grid[i+k,j+l].sex = grid[i,j].sex
    grid[i+k,j+l].age = grid[i,j].age
    grid[i+k,j+l].hasChild = grid[i,j].hasChild
    grid[i+k,j+l].childAge = grid[i,j].childAge
    grid[i+k,j+l].foodRation = grid[i,j].foodRation
    grid[i,j].type = "empty"
    grid[i,j].hasChild = None
    grid[i,j].age = None
    grid[i,j].sex = None
    grid[i,j].foodRation = None
    grid[i,j].childAge = None



class Tile:
    def __init__(self, animalType, age, food):
        self.type = animalType
        self.sex = "male" if random.random() < .5 else "female"
        self.age = age
        self.hasChild = False
        self.childAge = 0
        self.foodRation = food;



#----------------------------initialize simulation----------------------#
for t in range(trials):
    # for stats
    wolves = 0
    sheep = 0
    grasses = 0
    for j in range(0, rows):
        for k in range(0, cols):
            r = random.random()
            if (r < wolfProb):
                grid[j,k] = Tile("wolf", random.randint(wolfMinInitAge, wolfMaxInitAge), wolfMaxFood)
                wolves += 1
            elif(r < wolfProb + sheepProb):
                grid[j,k] = Tile("sheep", random.randint(sheepMinInitAge, sheepMaxInitAge), sheepMaxFood)
                sheep += 1
            else:
                grid[j,k] = Tile("empty", 0, 0)
            if (grass[j,k] >= grassMatureAge):
                grasses += 1
    #---------------------------run simulation-----------------------------#
    # outputAnimals = np.empty([int(time/step),rows,cols], dtype=int)
    # outputAnimals.fill(0)
    outputGrass   = []
    #####- for each time step -#####
    for i in range(0, time, step):
        wolves = 0
        sheep = 0
        grasses = 0
        ####- for each tile -####
        for j in range(0, rows):
            for k in range(0, cols):
                ### shuffle possible moves so we don't prefer any one direction ###
                random.shuffle(moves)
                tile = grid[j,k]
                eaten = False
                moved = False

                ###- get list of various types of tiles around us -###
                empty = []
                malesheep = []
                maleWolves = []
                for move in moves:
                    if(j+move[0] < rows and j+move[0] >= 0 and k+move[1] < cols and k+move[1] >= 0):
                        if (grid[j+move[0],k+move[1]].type == "empty"):
                            empty.append(move)
                        elif(grid[j+move[0],k+move[1]].sex == "male"):
                            if(grid[j+move[0],k+move[1]].type == "sheep" and grid[j+move[0],k+move[1]].age > sheepMatureAge and grid[j+move[0],k+move[1]].foodRation >= sheepChildFood):
                                malesheep.append(move)
                            if(grid[j+move[0],k+move[1]].type == "wolf" and grid[j+move[0],k+move[1]].age > wolfMatureAge and grid[j+move[0],k+move[1]].foodRation >= wolfChildFood):
                                maleWolves.append(move)

                ###- sheep -###
                if(tile.type == "sheep"):
                    sheep += 1
                    # outputAnimals[i,j,k] = 1
                    ##- handle female specific stuff -##
                    if(tile.sex == "female"):
                        #- female with child specific stuff -#
                        if(tile.hasChild == True):
                            if(tile.childAge > random.randint(sheepMinChildAge, sheepMaxChildAge) and len(empty)>0):
                                #- add child -#
                                grid[j+empty[0][0],k+empty[0][1]] = Tile("sheep", tile.childAge, tile.foodRation)
                                #- child leaves mother -#
                                tile.childAge = 0
                                tile.hasChild = False
                                del empty[0] # this move is no longer empty b/c child moved there
                            else:
                                tile.childAge += 1

                        #- handle sheep gaining sheep from male -#
                        if(tile.age > sheepMatureAge and tile.foodRation >= sheepChildFood and len(malesheep) > 0 and tile.hasChild == False):
                            tile.hasChild = True
                            tile.childAge = 0

                    ##- look for any empty tile with grass -##
                    for location in empty:
                        if(grass[j+location[0],k+location[1]] >= grassMatureAge):
                            ###- grass found, move to that location -###
                            moveTo(j,k,location[0],location[1])
                            tile = grid[j+location[0], k +location[1]]
                            moved = True
                            if(grid[j+location[0],k+location[1]].foodRation < sheepEatFood):
                                grid[j+location[0],k+location[1]].foodRation = sheepMaxFood
                                eaten = True
                            grass[j+location[0],k+location[1]] = 0
                            break
                    ##- if no grass found, just move randomly -##
                    if(not moved and len(empty)>0):
                         moveTo(j,k,empty[0][0],empty[0][1])
                         tile = grid[j+empty[0][0], k +empty[0][1]]
                ###- wolf -###
                elif(grid[j,k].type == "wolf"):
                    wolves += 1
                    # outputAnimals[i,j,k] = 2
                    ##- handle female specific stuff -##
                    if(tile.sex == "female"):
                        #- female with child specific stuff -#
                        if(tile.hasChild == True):
                            if(tile.childAge > random.randint(wolfMinChildAge, wolfMaxChildAge) and len(empty)>0):
                                #- add child -#
                                grid[j+empty[0][0],k+empty[0][1]] = Tile("wolf", tile.childAge, tile.foodRation)
                                #- child leaves mother -#
                                tile.childAge = 0
                                tile.hasChild = False
                                del empty[0] # this move is no longer empty b/c child moved there
                            else:
                                tile.childAge += 1

                        ##- handle sheep gaining sheep from male -##
                        if(tile.age > wolfMatureAge and tile.foodRation >= wolfChildFood and len(maleWolves) > 0 and tile.hasChild == False):
                            tile.hasChild = True
                            tile.childAge = 0

                    #- look for any empty tile with grass -#
                    if(tile.foodRation < wolfEatFood):
                        for location in moves:
                            if(j+location[0] < rows and j+location[0] >= 0 and k+location[1] < cols and k+location[1] >= 0):
                                if(grid[j+location[0],k+location[1]].type == "sheep"):
                                    ###- grass found, move to that location -###
                                    moveTo(j,k,location[0],location[1])
                                    tile = grid[j+location[0], k +location[1]]
                                    moved = True
                                    eaten = True
                                    tile.foodRation = wolfMaxFood
                                    # grass[j+location[0],k+location[1]] = 0
                                    break

                    #- if no grass found, just move randomly -#
                    if(not moved and len(empty)>0):
                         moveTo(j,k,empty[0][0],empty[0][1])
                         tile = grid[j+empty[0][0], k +empty[0][1]]

                ###-handle grass-###
                if (grass[j,k] >= grassMatureAge):
                    grasses += 1
                grass[j,k] = grass[j,k]+1
                if(tile.type != "empty"):
                    tile.age += 1
                    if(not eaten):
                        tile.foodRation = tile.foodRation-1
                        if(tile.foodRation <= 0):
                            tile.type = "empty"
                            tile.hasChild = None
                            tile.age = None
                            tile.sex = None
                            tile.foodRation = None
                            tile.childAge = None

        outputGrass.append(grass)
        grassCount.append(grasses)
        wolfCount[t].append(wolves)
        sheepCount[t].append(sheep)




# index = 0

# def update(i):
#     mat.set_array(outputAnimals[i])
#     return [mat]



# fig, ax = plt.subplots()
# mat = ax.matshow(outputAnimals[0])
# plt.colorbar(mat)
# ani = animation.FuncAnimation(fig, update, frames=time, interval=aniInterval, blit=True) 

# Use the below line to view the animation rather than save it
# plt.show()

# Use the below lines to save the animation rather than view it
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=(int)(1000/aniInterval), metadata=dict(artist='Me'), bitrate=1800)
# ani.save('try_animation.mp4', writer=writer)

# plt.close()
# plt.clf()
for t in range(trials):
    plt.plot(range(0, time, step), wolfCount[t], color='red')
    plt.plot(range(0, time, step), sheepCount[t], color='green')
# plt.plot(range(0, time, step), grassCount)
wolvesAvg = [sum([wolfCount[t][i] for t in range(trials)])/trials for i in range((int)(time/step))]
sheepAvg = [sum([sheepCount[t][i] for t in range(trials)])/trials for i in range((int)(time/step))]

plt.plot(range(0, time, step), wolvesAvg, color='#ffaaaa',linewidth=3.0)
plt.plot(range(0, time, step), sheepAvg, color='#aaffaa',linewidth=3.0)


plt.show()
