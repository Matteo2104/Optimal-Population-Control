import random
import matplotlib.pyplot as plt
import numpy as np
from occurrence import occurrence
from allzero import allzero
from checkstate import checkstate
from epsilongreedy import epsilongreedy

episodes = 500

food = 50
P = 100

epsilon = 0.5
delta = 0.99

A = 4

# graphs
good = []
bad = []
total = []

'''
actions
- 0 : do nothing
- 1 : reward goods
- 2 : kill bads
- 3 : prevents
'''

# resetto la distribuzione di individui
rnd = random.randint(0,P)
goods = [0 for i in range(rnd)]
bads = [1 for i in range(rnd,P)]
behaviors = goods + bads
random.shuffle(behaviors)
print(len(behaviors))

a = 0

print(f"initial state {len(goods)/len(behaviors)}")

total.append(len(behaviors))
good.append(len(goods))
bad.append(len(behaviors) - len(goods))

totals = len(behaviors)
goods = len(goods)

for e in range(500):
#while len(behaviors) - goods > 0:
    # associo gli individui ai cibi in modo casuale
    # potrebbe essere fatto computazionalmente meglio, ma per ora va bene così
    assoc = [-1 for b in range(len(behaviors))]
    availability = [2 for f in range(food)]
    full = 0
    for i in range(0,len(assoc)):
        if full:
            # muore con probabilità 50%
            if random.uniform(0,1) > 0.5:
                assoc[i] = -2
            else:
                assoc[i] = -1
            continue

        assigned = 0
        while not assigned:
            f = random.randint(0,food-1)

            if availability[f] > 0:
                assoc[i] = f
                availability[f] -= 1
                assigned = 1
                if allzero(availability):
                    full = 1

    for f in range(food):
        # se non ci sono occorrenze, significa che nessun individuo è stato assegnato al cibo f 
        if (occurrence(assoc,f) == 0):
            continue
            
        # se c'è una sola occorrenza, significa che l'individuo i può mangiare tutto il cibo per sè e quindi riprodursi 
        elif (occurrence(assoc,f) == 1):
            index1 = assoc.index(f)
            assoc[index1] = -1
            agent1 = behaviors[index1]
            if a == 0:
                behaviors.append(agent1)
            if a == 2:
                if random.uniform(0,1) > 0.5:
                    behaviors.append(agent1)
                else:
                    assoc[index1] = -2
                
        # se ci sono due o più occorrenze, allora si gestiscono in base alle regole
        elif (occurrence(assoc,f) >= 2):
            index1 = assoc.index(f)
            assoc[index1] = -1
            agent1 = behaviors[index1] 
            
            index2 = assoc.index(f)
            assoc[index2] = -1
            agent2 = behaviors[index2]

            # entrambi sopravvivono ma non si riproducono
            if (agent1 == 0 and agent2 == 0):
                if a == 0: # do nothing
                    behaviors.append(0)
                    behaviors.append(0)
                elif a == 1: # rewards goods
                    behaviors.append(0)
                    #behaviors.append(0)
                elif a == 2: # kills bads
                    #assoc[index1] = -2
                    pass
                elif a == 3: # prevents
                    pass

            # agent1 si riproduce con probabilità 50%, agent2 muore con probabilità 50%
            elif (agent1 == 1 and agent2 == 0):
                # agent2
                assoc[index2] = -2
                
                # agent1
                if a == 0: # do nothing
                    behaviors.append(agent1)
                elif a == 1: # rewards goods
                    behaviors.append(agent1)
                elif a == 2: # kills bads
                    assoc[index1] = -2
                elif a == 3: # prevents
                    assoc[index2] = -1
                        
            # agent1 muore con probabilità 50%, agent2 si riproduce con probabilità 50%
            elif (agent1 == 0 and agent2 == 1):
                # agent1
                assoc[index1] = -2

                # agent2
                if a == 0: # do nothing
                    behaviors.append(agent2)
                elif a == 1: # rewards goods
                    behaviors.append(agent2)
                elif a == 2: # kills bads
                    assoc[index2] = -2
                elif a == 3: # prevents
                    assoc[index1] = -1

            # muoiono entrambi
            elif (agent1 == 1 and agent2 == 1):
                assoc[index1] = -2
                
                #behaviors.append(agent2)

    # rimuovo tutti gli individui morti
    dead = []
    for d in range(len(assoc)):
        if assoc[d] == -2:
            dead.append(d)

    for d in reversed(dead):
        del behaviors[d]

    totals = len(behaviors)
    goods = 0
    for i in range(totals):
        if behaviors[i] == 0:
            goods += 1
        
    total.append(totals)
    good.append(goods)
    bad.append(totals - goods)
        
plt.plot(total, color="black")
plt.plot(bad, color="red")
plt.plot(good, color="blue")
plt.show()

        

        