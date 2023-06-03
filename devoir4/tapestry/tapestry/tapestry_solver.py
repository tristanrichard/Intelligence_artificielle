from clause import *

"""
For the tapestry problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, fixed_cells=None):

    expression = []
    if fixed_cells!=None:
        for cell in fixed_cells:
            clause= Clause(size)
            clause.add_positive(cell[0], cell[1],cell[2],cell[3])
            expression.append(clause)

    for row in range(size):
        for column in range(size):
            for shape in range(size):
                for color in range(size):
                    clause = Clause(size)
                    clause.add_positive(row,column,shape,color)
                    for other_row in range(size):
                        for other_column in range(size):
                            clause.add_negative(other_row,other_column,shape,color)
                        if other_row==row:
                            pass
                        else:
                            for other_color in range(size):
                                clause.add_negative(other_row,column,shape,other_color)
                            for other_shape in range(size):
                                clause.add_negative(other_row,column,other_shape,color)
                    for other_column in range(size):
                        if other_column==column:
                            pass
                        else:
                            for other_color in range(size):
                                clause.add_negative(row,other_column,shape,other_color)
                            for other_shape in range(size):
                                clause.add_negative(row,other_column,other_shape,color)
                    expression.append(clause)
    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
