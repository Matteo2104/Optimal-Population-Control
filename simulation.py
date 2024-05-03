import random
import matplotlib.pyplot as plt
import numpy as np
from occurrence import occurrence
from allzero import allzero
from checkstate import checkstate
from epsilongreedy import epsilongreedy

episodes = 200

food = 50
P = 100
behaviors = [0,1]

epsilon = 0.3
delta = 0.9
alpha = 0.5
gamma = 0.9
S = 10
A = 4
#N = [0 for i in range(A)]
#Q = [0 for i in range(A)]

Q = np.zeros([S,A])

# graphs
xpoints = []
good = []
bad = []
totals = []
historyN = []

'''
actions
- 0 : do nothing
- 1 : reward goods
- 2 : kill bads
- 3 : prevents
'''

for e in range(episodes):  
    # resetto la distribuzione di individui
    behaviors = [random.randint(0,1) for i in range(P)]

    s,_ = checkstate(behaviors)

    # avvio la simulazione
    while True:
        # decido l'azione in modo epsilon-greedy
        a = epsilongreedy(Q,A,epsilon)
        
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

                # se non ci sono scontri, non si apprende nulla quindi la nascita è casuale
                #behaviors.append(random.randint(0,1)) 
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
                    if a == 0: # do nothing
                        pass
                    elif a == 1: # rewards goods
                        behaviors.append(0)
                        behaviors.append(0)
                    elif a == 2: # kills bads
                        pass
                    elif a == 3: # prevents
                        pass

                # agent1 si riproduce con probabilità 50%, agent2 muore con probabilità 50%
                elif (agent1 == 1 and agent2 == 0):
                    # agent2
                    if random.uniform(0,1) > 0.5:
                        assoc[index2] = -2
                    
                    # agent1
                    if a == 0: # do nothing
                        if random.uniform(0,1) > 0.5:
                            behaviors.append(agent1)
                    elif a == 1: # rewards goods
                        if random.uniform(0,1) > 0.5:
                            behaviors.append(agent1)
                    elif a == 2: # kills bads
                        assoc[index1] = -2
                    elif a == 3: # prevents
                        assoc[index2] = -1
                            
                # agent1 muore con probabilità 50%, agent2 si riproduce con probabilità 50%
                elif (agent1 == 0 and agent2 == 1):
                    # agent1
                    if random.uniform(0,1) > 0.5:
                        assoc[index1] = -2

                    # agent2
                    if a == 0: # do nothing
                        if random.uniform(0,1) > 0.5:
                            behaviors.append(agent2)
                    elif a == 1: # rewards goods
                        if random.uniform(0,1) > 0.5:
                            behaviors.append(agent2)
                    elif a == 2: # kills bads
                        assoc[index2] = -2
                    elif a == 3: # prevents
                        assoc[index1] = -1

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

        # a questo punto effettuo la transizione
        sp,r = checkstate(behaviors)

        if sp == 0:
            Q[sp,a] = 0
            break
        else:
            ap = epsilongreedy(Q,A,epsilon)
            
            # SARSA update
            Q[s,a] = Q[s,a] + alpha*(r + gamma*Q[sp,ap] - Q[s,a])
            s = sp
            a = ap
    
    epsilon = delta*epsilon

    


    #historyN.append(N.copy())

    #xpoints.append(e)
    #good.append(goods)
    #bad.append(total-goods)
    #totals.append(total)

'''
# plots
plt.figure(1)
plt.plot(totals, label="total", color="black")
plt.plot(good, label="goods")
plt.plot(bad, label="bads")
plt.legend(loc="upper left")
'''

plt.figure(1)
plt.plot(np.transpose(historyN)[0], label="do nothing", color="grey")
plt.plot(np.transpose(historyN)[1], label="rewards goods", color="blue")
plt.plot(np.transpose(historyN)[2], label="kills bads", color="red")
plt.plot(np.transpose(historyN)[3], label="prevents", color="yellow")
plt.legend(loc="upper left")
plt.show()
