states = {
    0: [0.0, 0.05],
    1: [0.05, 0.1],
    2: [0.1, 0.15],
    3: [0.15, 0.2],
    4: [0.2, 0.25],
    5: [0.25, 0.3],
    6: [0.3, 0.35],
    7: [0.35, 0.4],
    8: [0.4, 0.45],
    9: [0.45, 0.5],
    10: [0.5, 0.55],
    11: [0.55, 0.6],
    12: [0.6, 0.65],
    13: [0.65, 0.7],
    14: [0.7, 0.75],
    15: [0.75, 0.8],
    16: [0.8, 0.85],
    17: [0.85, 0.9],
    18: [0.9, 0.95],
    19: [0.95, 1.0]
}

def checkstate(behaviors):
    total = len(behaviors)
    goods = 0
    bads = 0
    for n in range(len(behaviors)):
        if (behaviors[n] == 0):
            goods += 1 
        else:
            bads += 1

    if total == 0:
        return (0,-1,0,0)
    else:
        value = goods/total

    r = 2*(goods/total - 0.5)
    for key in states:
        rng = states[key]
        if value == 0:
            s = 0
            break
        if rng[0] < value <= rng[1]:
            s = key  
            break
    
    return (s,r,goods,bads)