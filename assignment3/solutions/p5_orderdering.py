
# -*- coding: utf-8 -*-
__author__ = 'Aditya Bansal, Bharat Batra'
__email__ = 'adbansal@ucsd.edu, bbatra@ucsd.edu '

 
import operator
 
def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).
 
    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """
 
 
    ls= csp.variables._variable_list
    mrv_index = -1 #holds index of MRV in ls. so we shall return ls[MRV]
    mrv_value = len(ls) #this variable is used to calculate the number of constraint satisfying values for the MRV
 
    all_assigned = True #flag to check if the assignmnet is already complete
    for i in ls:
        if len(i.domain) > 1: #if any variable has more than 1 remaining possible value in its domain, assignment is not complete
            all_assigned =  False
 
 
    if all_assigned == True:
        return 
 
    i = 0
    for var in ls:
 
        num_domain = len(var.domain)
        num_constraints = len(csp.constraints[var])
        values_remaining = num_domain - num_constraints #number of values in domain that don't violate any constraint
        if values_remaining < mrv_value: #this is a better choice for MRV than the previous one
            mrv_index = i
            mrv_value = values_remaining #this is now the MRV
            
        elif values_remaining == mrv_value: #tie for MRV, we shall pick the variable with the largest number of constraints as MRV
            a_constraints = csp.constraints[ls[mrv_index]]
            b_constraints = csp.constraints[var]
            
            if len(a_constraints) < len(b_constraints):
                mrv_index = i
                mrv_value = values_remaining
        i = i + 1
 
 
    return ls[mrv_index] 
    pass
 
 
 
def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.
 
    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """
 
    ls = csp.variables._variable_list #holds all variables in CSP
    unordered_list = [] #will hold the variables with their corresponding number of constraints 
 
    for value1 in variable.domain: #iterate through values in the domain of variable
        violations = 0 #number of violations for this domain variable
        for var in ls: #iterate through each variable in ls
            i = 0
            if not var==variable: #no constraint from a variable to itself
                for constraint in csp.constraints[variable, var]:
                    for value2 in var.domain: #for each pair of values in variable and var's domain, check if the constraint is satisfied
                        if not constraint.is_satisfied(value1, value2):
                            violations = violations + 1
        unordered_list.append({'value':value1, 'number': violations}) 
 
        
    ordered_list = sorted(unordered_list, key=operator.itemgetter('number')) #sort the unsorted pairs by the number of violatons
 
    return_list = []
 
    for k in ordered_list:
        return_list.append(k.get('value')) #we only have to return the variables so we extract these from the list and then return 
 
    return return_list
    pass