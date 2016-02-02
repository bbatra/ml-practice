# -*- coding: utf-8 -*-
__author__ = 'Aditya Bansal, Bharat Batra'
__email__ = 'adbansal@ucsd.edu, bbatra@ucsd.edu '



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
