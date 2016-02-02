# -*- coding: utf-8 -*-
__author__ = 'Aditya Bansal, Bharat Batra'
__email__ = 'adbansal@ucsd.edu, bbatra@ucsd.edu '


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
