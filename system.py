import random
import matplotlib.pyplot as plt
from occurrence import occurrence

episodes = 1000
food = 50
k = 0.01
sigma = 0.1
#behaviors = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
behaviors = [0,0,0,0]

xpoints = []
good = []
bad = []

for i in range(episodes):
    '''
    L'idea è quella di creare un array di associazioni, in cui l'elemento i corrisponde al cibo a cui viene associato l'individuo i nell'iterazione corrente  
    '''
    assoc = [random.randint(0,food-1) for b in range(len(behaviors))]    

    for f in range(food):
        # se non ci sono occorrenze, significa che nessun individuo è stato assegnato al cibo f 
        if (occurrence(assoc,f) == 0):
            continue
            
        # se c'è una sola occorrenza, significa che l'individuo i può mangiare tutto il cibo per sè e quindi riprodursi con probabilità 100%
        elif (occurrence(assoc,f) == 1):
            index1 = assoc.index(f)
            assoc[index1] = -1
            agent1 = behaviors[index1]
            #agent1 = 0 if random.uniform(0,1) < behavior1 else 1
            #agent1 = max(0,agent1 + random.gauss(0,sigma))

            # se non ci sono scontri, non si apprende nulla quindi la nascita è casuale
            behaviors.append(random.uniform(0,1)) 
                
        # se ci sono due o più occorrenze, allora si gestiscono i primi due in base alle regole e tutti gli altri muoiono con probabilità 50% perchè non si nutrono
        elif (occurrence(assoc,f) >= 2):
            index1 = assoc.index(f)
            assoc[index1] = -1
            behavior1 = behaviors[index1] 
            agent1 = 0 if random.uniform(0,1) < behavior1 else 1
            
            index2 = assoc.index(f)
            assoc[index2] = -1
            behavior2 = behaviors[index2]
            agent2 = 0 if random.uniform(0,1) < behavior2 else 1

            # ripulisco le associazioni triple
            while (f in assoc):
                indexi = assoc.index(f)
                assoc[indexi] = -1
                if (random.uniform(0,1) < 0.5):
                    assoc[indexi] = -2 # muore
            
            # entrambi sopravvivono ma non si riproducono
            if (agent1 == 0 and agent2 == 0):
                pass

            # agent1 si riproduce con probabilità 50%, agent2 muore con probabilità 50%
            elif (agent1 == 1 and agent2 == 0):
                # agent1
                if (random.uniform(0,1) > 0.5):
                    #behaviors.append(behavior1 + k*(1-behavior1)) 
                    behaviors.append(behavior1)

                # agent2
                if (random.uniform(0,1) > 0.5):
                    assoc[index2] = -2

            # agent1 muore con probabilità 50%, agent2 si riproduce con probabilità 50%
            elif (agent1 == 0 and agent2 == 1):
                # agent1
                if (random.uniform(0,1) > 0.5):
                    assoc[index1] = -2

                # agent2
                if (random.uniform(0,1) > 0.5):
                    #behaviors.append(behavior2 + k*(1-behavior2)) 
                    behaviors.append(behavior2)

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

    # conteggio del numero dei buoni
    total = len(behaviors)
    counter = 0
    for n in range(len(behaviors)):
        if (behaviors[n] == 0):
            counter += 1 

    # Reinforcement Learning
    

    xpoints.append(i)
    good.append(counter)
    bad.append(total-counter)
          
#plt.plot(xpoints,total)
plt.plot(xpoints,good)
plt.plot(xpoints,bad)
plt.show()
