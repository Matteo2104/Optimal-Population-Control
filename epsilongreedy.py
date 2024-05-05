import random
import numpy as np

def epsilongreedy(Qs,A,epsilon):
    if random.uniform(0,1) > epsilon:
        a = np.argmax(Qs)
    else:
        a = random.randint(0,A-1)
    
    return a