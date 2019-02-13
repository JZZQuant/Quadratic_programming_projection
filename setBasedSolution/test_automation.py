import unittest

import numpy as np
from cvxopt import solvers
from system1 import make_infeasible, _system1
from system2 import _system2_old, _system2
from scipy.sparse import random
import datetime


class AutomationTests(unittest.TestCase):
    def test_if_system_2_new_is_different_than_system_2_old(self):
        solvers.options['show_progress'] = False

        sparse=np.array([[0, 0, 0, 1, 0, 1, 0, 1],
                         [0, 0, 0, 1, 1, 1, 1, 1],
                         [0, 0, 1, 0, 1, 1, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0, 0],
                         [1, 1, 1, 0, 0, 0, 0, 0],
                         [1, 1, 1, 1, 1, 1, 1, 1]])

        down=np.array([92,32,93,83,78,138,55,75], dtype = int)
        right=np.array([96,149,90,28,81,202])

        sol2_old=_system2_old(sparse, down, right)
        _sparse=sparse[:-1,:]
        _right=right[:-1]
        if sol2_old["status"]=="optimal":
            # print(np.array(sol2_old["x"].T))
            _down=(down-np.array(sol2_old["x"].T))[0]
            #remove the solution of last row after reduction and solve again using linear programming
            _sparse=_sparse[np.where(_right!=0)[0],:][:,np.where(_down!=0)[0]]
            _right=_right[np.where(_right!=0)[0]]
            _down=_down[np.where(_down!=0)[0]]
            sol3_old = _system1(_sparse,_down,_right)

        sol2_new=_system2(sparse, down, right)
        _sparse=sparse[:-1,:]
        _right=right[:-1]
        if sol2_new["status"]=="optimal":
            # print(np.array(sol2_new["x"].T))
            _down=(down-np.array(sol2_new["x"].T))[0]
            #remove the solution of last row after reduction and solve again using linear programming
            _sparse=_sparse[np.where(_right!=0)[0],:][:,np.where(_down!=0)[0]]
            _right=_right[np.where(_right!=0)[0]]
            _down=_down[np.where(_down!=0)[0]]
            sol3_new = _system1(_sparse,_down,_right)

        self.assertTrue(sol3_old["status"] != sol3_new["status"])

    def test_if_system_2_is_in_sync_with_system_1_and_system_3(self):

        solvers.options['show_progress'] = False
        is_solved=True
        i=0
        is_solved_list = []

        for i in range(100000000):
            m=np.random.randint(15,17)
            n=np.random.randint(15,17)
            #create sparse matrix
            down, right, sparse = self.get_sparse(m, n)

            sol1=_system1(sparse,down,right)
            #solve using swapnil reduction
            start_time = datetime.datetime.now()
            sol2=_system2(sparse, down, right)
            end_time = datetime.datetime.now()
            #print(end_time - start_time)
            _sparse=sparse[:-1,:]
            _right=right[:-1]

            if sol2[0]=="optimal":
                # print(np.array(sol2["x"].T))
                _down=(down-np.array(sol2[1].T))[0]
                #remove the solution of last row after reduction and solve again using linear programming
                _sparse=_sparse[np.where(_right!=0)[0],:][:,np.where(_down!=0)[0]]
                _right=_right[np.where(_right!=0)[0]]
                _down=_down[np.where(_down!=0)[0]]
                sol3 = _system1(_sparse,_down,_right)

            is_solved=False
            if sol1["status"]=="optimal":
                is_solved = (sol2[0]=="optimal") and (sol3["status"]=="optimal")
            else:
                is_solved = sol2[0]!="optimal"

            is_solved_list.append(is_solved)

            if is_solved == False:
                print(sparse, down, right)
                break

        print(is_solved_list)
        self.assertEqual(all(is_solved_list), True)

    def test_failed_case_analysis(self):
        solvers.options['show_progress'] = False

        sparse=np.array([[0,0,0,0,0,1,0]
                        ,[0,0,0,1,0,0,0]
                        ,[0,0,1,0,0,0,0]
                        ,[0,0,1,0,0,0,1]
                        ,[0,0,1,0,1,0,0]
                        ,[0,1,0,0,0,0,0]
                        ,[1,0,1,0,0,0,0]
                        ,[1,1,1,1,1,1,1]])

        down=np.array([111 ,163 ,271, 152 ,129 ,111  ,98], dtype = int)
        right=np.array([ 73  ,85 , 17  ,46 ,151,  75  ,82 ,506])

        sol1=_system1(sparse, down, right)

        sol2=_system2(sparse, down, right)
        _sparse=sparse[:-1,:]
        _right=right[:-1]
        if sol2[0]=="optimal":
            # print(np.array(sol2["x"].T))
            _down=(down-np.array(sol2[1].T))[0]
            #remove the solution of last row after reduction and solve again using linear programming
            _sparse=_sparse[np.where(_right!=0)[0],:][:,np.where(_down!=0)[0]]
            _right=_right[np.where(_right!=0)[0]]
            _down=_down[np.where(_down!=0)[0]]
            sol3 = _system1(_sparse,_down,_right)

        is_solved=False

        if sol1["status"]=="optimal":
            is_solved = (sol2[0]=="optimal") and (sol3["status"]=="optimal")
        else:
            is_solved = sol2[0]!="optimal"

        self.assertEqual(is_solved, True)

    def get_sparse(self, m, n):
        # create sparse matrix
        mat = random(m, n, density=0.04, format="csr") * 100
        mat = mat.toarray().astype(int)
        mat = np.vstack([mat, np.reshape(np.random.randint(10, 100, mat.shape[1]), (1, mat.shape[1]))])
        p = mat[:-1, :]
        # remove void rows and columns
        rs = np.sum(p, axis=1)
        cs = np.sum(p, axis=0)
        rows = np.where(rs != 0)[0]
        rows = np.append(rows, m )
        cols = np.where(cs != 0)[0]
        mat = mat[:, cols][rows, :]
        right = mat.sum(axis=1)
        down = mat.sum(axis=0)
        sparse = np.copy(mat)
        sparse[sparse > 0] = 1
        full_rank = np.unique(sparse, axis=0, return_index=True)
        sparse = full_rank[0]
        right = right[full_rank[1]]
        right[-1] = down.sum() - right[:-1].sum()
        return down, right, sparse



