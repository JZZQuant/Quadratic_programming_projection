import numpy as np
from cvxopt import matrix, solvers, glpk
from solver_main import solver_main

def _system2_old(sparse, down, right):
    solvers.options['show_progress'] = False

    A_ = sparse
    b_ = np.apply_along_axis(lambda x: np.sum(x * down), 1, sparse) - right
    b_[-1] = right[-1]
    var_ = A_.shape[1]
    A = A_[-1, :]
    b = b_[-1]
    A_ = np.concatenate([A_, -1 * np.identity(var_), np.identity(var_)])
    b_ = np.concatenate([b_, np.zeros(var_), down])
    c_ = np.ones(var_)
    sol_ = solvers.lp(matrix(-1 * c_), G=matrix(A_.astype(np.double)), h=matrix(b_.astype(np.double)),
                      A=matrix(A.astype(np.double)).T, b=matrix(b.astype(np.double)), solver='glpk',
                      options = {'glpk':{'msg_lev':'GLP_MSG_OFF'}})
    return sol_


def _system2(sparse, down, right):
    solvers.options['show_progress'] = False

    combinatorial_constraints, constraints_availability = solver_main(np.matrix(sparse), down, right)
    constraint_matrix = np.zeros((len(constraints_availability), sparse.shape[1]))
    for i in range(len(combinatorial_constraints)):
        constraint_matrix[i, list(combinatorial_constraints[i])] = 1
    constraint_RHS = np.array(constraints_availability)

    var_ = sparse.shape[1]
    G = np.concatenate([constraint_matrix, -1 * np.identity(var_), np.identity(var_)])
    h = np.concatenate([constraint_RHS, np.zeros(var_), down])
    c = np.ones(var_)
    A = sparse[-1,:]
    b = right[-1]

    sol_ = solvers.lp(matrix(-1 * c), G=matrix(G.astype(np.double)), h=matrix(h.astype(np.double)),
                      A=matrix(A.astype(np.double)).T, b=matrix(b.astype(np.double)), solver=glpk,
                      options = {'glpk':{'msg_lev':'GLP_MSG_OFF'}})
    return sol_