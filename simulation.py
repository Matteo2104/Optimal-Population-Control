import random
import matplotlib.pyplot as plt
import numpy as np
from occurrence import occurrence
from allzero import allzero
from checkstate import checkstate
from epsilongreedy import epsilongreedy

episodes = 5e3

food = 50
P = 100

epsilon = 0.2
delta = 0.995
alpha = 1
gamma = 0.9

S = 20
A = 3

Q = np.zeros([S,A])

'''
actions
- 0 : do nothing
- 1 : reward goods
- 2 : kill bads (but sometimes also goods)
'''

# resetto la distribuzione di individui
rnd = random.randint(0,P)
goods = [0 for i in range(rnd)]
bads = [1 for i in range(rnd,P)]
behaviors = goods + bads
random.shuffle(behaviors)

history = []
policy = []
goodss = []
badss = []
foods = []

for e in range(int(episodes)):  
    print(f"episode {e}")

    s,_,_,_ = checkstate(behaviors)

    # decido l'azione in modo epsilon-greedy
    a = epsilongreedy(Q[s],A,epsilon)

    if a == 0:
        food -= 1
    elif a == 1:
        pass
    elif a==2: 
        food += 1

    food = max(1,food)

    #while True:
    # associo gli individui ai cibi in modo casuale
    # potrebbe essere fatto computazionalmente meglio, ma per ora va bene così
    assoc = [-1 for b in range(len(behaviors))]
    availability = [2 for f in range(food)]

    if len(availability) == 0:
        full = 1
    else: 
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
            behaviors.append(agent1) 
            
        # se ci sono due o più occorrenze, allora si gestiscono i primi due in base alle regole e tutti gli altri muoiono con probabilità 50% perchè non si nutrono
        elif (occurrence(assoc,f) >= 2):
            index1 = assoc.index(f)
            assoc[index1] = -1
            agent1 = behaviors[index1] 
            
            index2 = assoc.index(f)
            assoc[index2] = -1
            agent2 = behaviors[index2]

            # entrambi sopravvivono ma non si riproducono
            if (agent1 == 0 and agent2 == 0):
                pass

            # agent1 si riproduce, agent2 muore con probabilità 50%
            elif (agent1 == 1 and agent2 == 0):
                # agent2
                if random.uniform(0,1) > 0.5:
                    assoc[index2] = -2
                
                # agent1
                if random.uniform(0,1) > 0.5:
                    behaviors.append(agent1)
                        
            # agent1 muore con probabilità 50%, agent2 si riproduce
            elif (agent1 == 0 and agent2 == 1):
                # agent1
                if random.uniform(0,1) > 0.5:
                    assoc[index1] = -2

                # agent2
                if random.uniform(0,1) > 0.5:
                    behaviors.append(agent2)

            # muoiono entrambi
            elif (agent1 == 1 and agent2 == 1):
                assoc[index1] = -2
                assoc[index2] = -2

    # rimuovo tutti gli individui morti
    dead = []
    for d in range(len(assoc)):
        if assoc[d] == -2:
            dead.append(d)

    for d in reversed(dead):
        del behaviors[d]

    # a questo punto effettuo la transizione di stato
    sp,r,goods,bads = checkstate(behaviors)
    ap = epsilongreedy(Q[s],A,epsilon)
    
    # SARSA update
    Q[s,a] = Q[s,a] + alpha*(r + gamma*Q[sp,ap] - Q[s,a])
    s = sp
    a = ap  

    goodss.append(goods)
    badss.append(bads)
    history.append(s)
    policy.append(a)
    foods.append(food)
    
    #epsilon = delta*epsilon

    optimal = [np.argmax(Q[i,:]) for i in range(S)]
    print(f"policy ottima {optimal}")

print(len(history))

figure, axis = plt.subplots(2, 2)

axis[0,0].plot(history, color="black")
axis[0,0].set_title("Visited states")

axis[0,1].plot(goodss, color="blue")
axis[0,1].plot(badss, color="red")
axis[0,1].set_title("Individuals")

axis[1,0].plot(policy, label="actions took", color="grey")
axis[1,0].set_title("Policy")

axis[1,1].plot(foods, label="food", color="green")
axis[1,1].set_title("Food")

plt.legend(loc="upper left")

plt.show()

        