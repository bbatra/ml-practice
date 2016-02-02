# -*- coding: utf-8 -*-
__author__ = 'Aditya Bansal, Bharat Batra'
__email__ = 'adbansal@ucsd.edu, bbatra@ucsd.edu '


from collections import deque


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
