from ortools.sat.python import cp_model
import random
import math
import os
import time
import gc

fill_rate = 0.06
size = 6


if __name__ == "__main__":
    start = time.time()
    print()
    model = cp_model.CpModel()
    # create a random unfinished sudoku
    x = {}
    y = {}
    for i in range(int(fill_rate*size**4)):
        i = random.randint(0, size*size)
        j = random.randint(0, size*size)
        value = random.randint(1, size*size)
        x[i, j] = model.NewIntVar(value,value, 'x[%i,%i]' % (i, j))
        y[i, j] = value
    # display the start sudoku
    for i in range(size*size):
            for j in range(size*size):
                if (i, j) in x:
                    print(str(y[i,j]).ljust(int(math.log10(size*size)+1)), end=' ')
                else:
                    print(" ", end=' ')
            print()
    print()
    # Create the variables.
    for i in range(size*size):
        for j in range(size*size):
            if (i, j) not in x:
                x[i, j] = model.NewIntVar(1, size*size, 'x[%i,%i]' % (i, j))
    
    # Create the constraints.
    # add constraints for rows
    for i in range(size*size):
        row_constraint = []
        for j in range(size*size):
            row_constraint.append(x[i, j])
        model.AddAllDifferent(row_constraint)
    # add constraints for columns
    for j in range(size*size):
        col_constraint = []
        for i in range(size*size):
            col_constraint.append(x[i, j])
        model.AddAllDifferent(col_constraint)
    # add constraints for boxes
    for i in range(size):
        for j in range(size):
            box_constraint = []
            for k in range(size):
                for l in range(size):
                    box_constraint.append(x[i*size+k, j*size+l])
            model.AddAllDifferent(box_constraint)
    
    # Create the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    print('Status = %s' % solver.StatusName(status))
    stop = time.time()
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print('Solution:')
        for i in range(size*size):
            for j in range(size*size):
                print('%i'.ljust(int(math.log10(size*size)+1)) % solver.Value(x[i, j]), end=' ')
            print()
        solved = time.time()
        print('Time total: %f' % (solved-start))
        print('Time solve: %f' % (solved-stop))
    else:
        notsolved = time.time()
        print('Time to search: %f' % (notsolved-start))
        print('No solution found')
        print("Restarting...")
        gc.collect()
        os.system("python orsudoku.py")
        exit()
        
