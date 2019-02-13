import numpy as np
from scipy.linalg import block_diag
from cvxopt import matrix, solvers, glpk


def _system1(sparse_,down_,right_):
    solvers.options['show_progress'] = False
    row_constraints=block_diag(*sparse_)
    column_constraints=np.concatenate(np.apply_along_axis(lambda x: block_diag(*x),1,sparse_)).T
    # print(row_constraints, column_constraints)
    A=np.append(row_constraints,column_constraints,axis=0)
    A=A.astype("d")
    rows=np.where(np.sum(A,axis=1)!=0)[0]
    cols=np.where(np.sum(A,axis=0)!=0)[0]
    A=A[:,cols][rows,:]
    variables=A.shape[1]
    b=np.concatenate([right_, down_], axis=0)
    b=b.astype("d")
    c=np.ones(variables)
    rank=np.linalg.matrix_rank(A)
    A=A[:rank,:]
    b=b[:rank]
    g=matrix(-1*np.identity(variables,dtype='d'))
    H=matrix(np.zeros(variables,dtype='d'))
    sol = solvers.lp(matrix(-1*c),G=g,h=H,A=matrix(A),b=matrix(b), solver='glpk',
                     options = {'glpk':{'msg_lev':'GLP_MSG_OFF'}})
    return sol


def make_infeasible(sparse,_right,_down):
    init=_right[0]
    _right[0]= sum(sparse[0,:]*_down)+1
    i=1
    while sum(_right)!=sum(_down):
        new=int(_right[i]/6)
        old=_right[i]
        alloc=min(_right[0]-init,old-new)
        _right[i]=old-alloc
        init=init+alloc
        i=i+1
    return _right
