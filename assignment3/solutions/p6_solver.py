# -*- coding: utf-8 -*-
__author__ = 'Aditya Bansal, Bharat Batra'
__email__ = 'adbansal@ucsd.edu, bbatra@ucsd.edu '


from collections import deque

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]

def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""

    # Hint: The list of all variables for the CSP can be obtained by csp.variables.
    # Also, if the variable is assigned, variable.is assigned() will be True.
    # (Note that this can happen either by explicit assignment using variable.assign(value),
    # or when the domain of the variable has been reduced to a single value.)
    
    # Getting list of all variables for csp.
    ls= csp.variables._variable_list

    # Going over each variable
    for i in ls:
        # If any variable has domain >1, it is not assigned yet.
        if len(i.domain) >1:
            # In this case, return false
            return False

    # If all variables satisfy, return True
    return True


def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # getting all constraints
    cons = [c for c in csp.constraints[variable] if c.var2.is_assigned()]

    # for each constraint
    for c in cons:

        # Get the second variabe
        var2 = c.var2

        # If the variable is not satisfied with this value, return False
        if not c.is_satisfied(value , var2.domain[0]):
            return False

    # If all constraints are satisfied, return true
    return True

def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns the successful assignment; otherwise, it returns None.
    """

    # Base Case. If complete, return assignment.
    if is_complete(csp) == True:
        return csp.assignment

    # selected unassigned variable
    var = select_unassigned_variable(csp)

    # get the domain values for variable
    domain_values = order_domain_values(csp , var)

    # for each value in domain
    for value in domain_values:
        # if value is not consistent with assignemnt, just continue
        if not is_consistent(csp , var , value):
            continue

        # begin transaction
        csp.variables.begin_transaction()

        # assign value to variable
        var.assign(value)

        # recursevley call the same function with newly assigned variable
        result = backtrack(csp)

        # if the function returns something other than None, we dont need to backtrack, and just return the result
        if result:
            return result

        # otherwise callback.
        csp.variables.rollback()
    # return None
    return None


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    # creating a queue of arcs
    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # While the queue is not empty
    while len(queue_arcs) > 0:
        # Get the latest arc
        arc = queue_arcs.pop()

        # revise this particular arc, and see if it changes anything
        if revise(csp , arc[0] , arc[1]) == True:

            # if the domain doesnt have any values left, return False
            if len(arc[0].domain) == 0:
                return False
            else:
                # else, get the neighboring constarints.
                neighbs = [cons.var2 for cons in csp.constraints[arc[0]]]
                
                # Append them to the queue.
                queue_arcs.append(neighbs)

    # if everything works, return True
    return True

def revise(csp, xi, xj):
    # Initial flag set to false.
    change = False

    # for each value in the first var's domain.
    for x in xi.domain:
        flag = False

        # check if something satisfies the second var's 
        doms = xj.domain
        for d in doms:
            if x != d:
                # if something does, we're good
                flag = True

        # if there is NO value for xj, we have to make some changes
        if flag == False:
            # set the flag to True
            change = True

            # remove the x value from xi's domain
            xi.domain.remove(x)

    # return flag.
    return change