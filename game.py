import numpy as np

S = 10
A = 4

P = np.zeros([S,S,A])

for a in range(A):
    for i in range(S):
        for j in range(S):
            P[i,j,a] = 1

earnings = np.zeros(S)
earnings[0] = 1

R = np.zeros([S,A])

for a in range(A):
    R[a] = np.dot(P[:,:,a],earnings)