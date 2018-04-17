#----------------------------set global variables-----------------------#
rows = 80
cols = 80
time = 800               # Amount of time to run the simulation for
step = 1

aniInterval = 30        # milliseconds between each animation frame

#=== Wolf ===#
wolfProb = .02          # likelihood tile inits to wolf
wolfMinInitAge = 4      # range of age for initial population
wolfMaxInitAge = 6
#= Wolf Birth Rate =#
wolfMatureAge = 2       # age necessary to have a child
wolfMinChildAge = 1     # range of age between which child leaves, initial is 0
wolfMaxChildAge = 3
wolfChildFood = 0       # the food ration necessary to have a child
#= Wolf Death Rate =#
wolfMaxFood = 5         # food gained when eating, dies at 0, initial is max
wolfEatFood = 2         # food at which wolf needs to eat again (eat if foodRation <= wolfEatFood)

#=== Sheep ===#
sheepProb = .10          # likelihood tile inits to sheep
sheepMinInitAge = 0     # range of age for initial population
sheepMaxInitAge = 4
#= Sheep Birth Rate =#
sheepMatureAge = 4      # age necessary to have a child
sheepMinChildAge = 2    # range of age between which child leaves, initial is 0
sheepMaxChildAge = 4
sheepChildFood = 2      # the food ration necessary to have a child
#= Sheep Death Rate =#
sheepMaxFood = 4        # food gained when eating, dies at 0, initial is max
sheepEatFood = 2        # food at which sheep needs to eat again
grassMatureAge = 2      # age grass is edible, 0 after eaten, initial is rand between [0, max]


# while total num of wolves is about same as normal sim, ensure at least a min amount of wovles start in the pen
minWolvesInPen = 30
releasedPerStep = 3