states = {
    0 : [0,0.1],
    1 : [0.1,0.2],
    2 : [0.2,0.3],
    3 : [0.3,0.4],
    4 : [0.4,0.5],
    5 : [0.5,0.6],
    6 : [0.6,0.7],
    7 : [0.7,0.8],
    8 : [0.8,0.9],
    9 : [0.9,1]
}

def checkstate(behaviors):

    total = len(behaviors)
    goods = 0
    for n in range(len(behaviors)):
        if (behaviors[n] == 0):
            goods += 1 

    value = goods/total

    for key in states:
        rng = states[key]

        if rng[0] <= value < rng[1]:
            if key == 0:
                r = 1
            else:
                r = 0
            
            return (key,r)