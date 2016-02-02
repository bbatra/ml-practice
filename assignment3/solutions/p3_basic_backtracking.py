# -*- coding: utf-8 -*-
__author__ = 'Aditya Bansal, Bharat Batra'
__email__ = 'adbansal@ucsd.edu, bbatra@ucsd.edu '



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


def inference(csp, variable):
	"""Performs an inference procedure for the variable assignment.

	For P3, *you do not need to modify this method.*
	"""
	return True


def backtracking_search(csp):
	"""Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

	If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
	otherwise, it returns None.

	For P3, *you do not need to modify this method.*
	"""
	return backtrack(csp)


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



























