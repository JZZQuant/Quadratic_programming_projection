# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 12:02:21 2017

@author: Swapnil
"""

from cvxopt import matrix, solvers

frameDetails <- fread("~/Desktop/frameDetails.csv")
requestStations <- matrix(c(1, 1, 0, 0, 1, 1, 1, 1, 1), nrow= 3, byrow = T)
rownames(requestStations) <- c("R1", "R2", "R3")
colnames(requestStations) <- c("A", "B", "C")
requestCounts <- c(40, 30, 30)
stationCounts <- c(25, 35, 40)






Q = 2*matrix([ [2, .5], [.5, 1] ])
p = matrix([1.0, 1.0])
G = matrix([[-1.0,0.0],[0.0,-1.0]])
h = matrix([0.0,0.0])
A = matrix([1.0, 1.0], (1,2))
b = matrix(1.0)
sol=solvers.qp(Q, p, G, h, A, b)
