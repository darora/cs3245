#! /usr/bin/python2

# One option would have been to use the pyparsing library, which comes
# with a boolean query parser as an example. But I doubt we're allowed
# to use it... (http://pyparsing.wikispaces.com/Examples).

# Therefore, regexp galore it is!

# we recursively construct a tree, which we'll evaluate in a
# bottom-to-top fashion. Therefore, the operations with the least
# precedence are at the top of the tree. One problem with this
# approach is that it is *very* hard to hoist things around to
# minimize the working set in memory...

import re

class Operation:
    OR          = 0
    AND         = 1
    NOT         = 2
    PARANTHESIS = 3

    def self.get(string):
        if string == "OR":
            return Operation.OR
        elif string == "AND":
            return Operation.AND
        elif string == "NOT":
            return Operation.NOT
        else:
            raise "Invalid operator cast: " + string

p_scan = re.compile(r"(.*)\(([^\(\)]+)\)(.*)") # blah OP (...) OP blah
not_scan = re.compile(r"^\s*NOT ([^\s]+)\s*$")
and_scan = re.compile(r"(.+) AND (.+)")
or_scan = re.compile(r"(.+) OR (.+)")

scanners = [p_scan, not_scan, and_scan, or_scan] # in order
# of precedence ;)

class Tree(object):
    def __init__(self, string):
        self.processed = False
        self.construct(string)

    def construct(self, string):
        p = p_scan.match(string)
        initial_op = re.compile(r"(.*) ?(AND|OR|NOT) ") # in case of
# NOT, no previous clause
        later_op = re.compile(r" (AND|OR) (.+)")

        if p != None and p.groups()[1]:
                # construct for paranthesis
            g = p.groups()

            init = initial_op.match(g[0])
            later = later_op.match(g[2])
            init_operator = Operation.get(init.groups()[1])
            later_operator = Operation.get(later.groups()[0])

            if g[0] and g[2]:
                # both clauses exist, figure out where to root the tree...
                raise "TODO"
            elif g[0]:
                if init_operator == Operation.NOT:
                    if init.groups()[0]:
                        # redistribute the right to be NOT (...)
                        raise "TODO"
                    else:
                        # no child on the left, just a plain ol' NOT.
                        self.operator = init_operator
                        self.left = g[1]
                else:
                    pass
                raise "TODO"
            elif g[2]:
                self.operator = later_operator
                self.left = Tree(g[1])
                self.right = Tree(later.groups()[1])
            return
        
        n = not_scan.match(string)
        if n != None and n.groups()[0]:
            # construct for NOT
            return

        a = and_scan.match(string)
        if a != None and a.groups()[0] and a.groups()[1]: # TODO::add another check!
            # construct for AND
            return

        o = or_scan.match(string)
        if o != None and o.groups()[0] and o.groups()[1]:
            # construct for OR
            return
        

        

        
        
