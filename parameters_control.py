#----------------------------set global variables-----------------------#
rows = 80
cols = 80
time = 800               # Amount of time to run the simulation for
step = 1

aniInterval = 30        # milliseconds between each animation frame

#=== Wolf ===#
wolfProb = .05          # likelihood tile inits to wolf
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
sheepProb = .3          # likelihood tile inits to sheep
sheepMinInitAge = 0     # range of age for initial population
sheepMaxInitAge = 4
#= Sheep Birth Rate =#
sheepMatureAge = 2      # age necessary to have a child
sheepMinChildAge = 1    # range of age between which child leaves, initial is 0
sheepMaxChildAge = 3
sheepChildFood = 0      # the food ration necessary to have a child
#= Sheep Death Rate =#
sheepMaxFood = 5        # food gained when eating, dies at 0, initial is max
sheepEatFood = 2        # food at which sheep needs to eat again
grassMatureAge = 2      # age grass is edible, 0 after eaten, initial is rand between [0, max]