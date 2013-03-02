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

import logging
import re

class Operation:
    OR          = 0
    AND         = 1
    NOT         = 2
    PARANTHESES = 3

    @staticmethod
    def get(string):
        if string == "OR":
            return Operation.OR
        elif string == "AND":
            return Operation.AND
        elif string == "NOT":
            return Operation.NOT
        else:
            raise "Invalid operator cast: " + string
        
    @staticmethod
    def str(op):
        if op == Operation.OR:
            return "OR"
        elif op == Operation.AND:
            return "AND"
        elif op == Operation.NOT:
            return "NOT"
        else:
            raise "Invalid Operator"        

p_scan   = re.compile(r"(.*)\(([^\(\)]+)\)(.*)") # blah OP (...) OP blah
not_scan = re.compile(r"^\s*NOT ([^\s]+)\s*$")
and_scan = re.compile(r"(.+) AND (.+)")
or_scan  = re.compile(r"(.+) OR (.+)")

class Tree(object):
    def __init__(self, string = None):
        self.processed = False
        self.operator = None
        self.left = None
        self.right = None
        self.string = None
        while string != None and self.construct(string) == True:
            pass

    def __str__(self):
        string = ""
        if self.left != None:
            string += self.left.__str__() + " <--- "
        val = ""
        if self.operator != None:
            val = self.operator
        else:
            val = self.string
        string += str(val)
        if self.right != None:
            string += " +++> " + self.right.__str__()
        return string

    def __repr__(self):
        return self.__str__()

    def process(self):
        pass
    
    def construct(self, string):
        string.strip()
        p = p_scan.match(string)
        initial_op = re.compile(r"(.*) ?(AND|OR|NOT) ") # in case of
# NOT, no previous clause
        later_op = re.compile(r" (AND|OR) (.+)")

        if p != None and p.groups()[1]:
                # construct for parantheses
            g = p.groups()

            init = initial_op.match(g[0])
            later = later_op.match(g[2])
            logging.debug("INITIAL GROUPS ARE: "+str(g))

            if g[0].strip() and g[2].strip():
                # both clauses exist, figure out where to root the
                init_operator = Operation.get(init.groups()[1])
                later_operator = Operation.get(later.groups()[0])
                # tree...
                while init_operator == Operation.NOT:
                    if init.groups()[0]:
                        # redistribute the right to be NOT ...
                        g = (g[0], "NOT ("+g[1]+")", g[2])
                        o = init
                        init = initial_op.match(init.groups()[0])
                        if init == None:
                            init = o
                            break
                        init_operator = Operation.get(init.groups()[1])
                    else:
                        break
                if init_operator > later_operator:
                    self.operator = later_operator
                    lft_str = "{0} {1} {2}".format(init.groups()[0], Operation.str(init_operator), g[1])
                    logging.debug("INIT more than LATER")
                    logging.debug(lft_str)
                    logging.debug(later.groups()[1])
                    self.left = Tree(lft_str) # TODO::init_operator casting!
                    self.right = Tree(later.groups()[1]) if later.groups()[1].strip() != "" else None
                else:
                    self.operator = later_operator
                    self.left = Tree(init.groups()[0]) if init.groups()[0].strip() != "" else None
                    right_str = "{0} {1} {2}".format(g[1], Operation.str(later_operator), later.groups()[1])
                    logging.debug("INIT less than LATER")
                    logging.debug(right_str)
                    logging.debug(init.groups()[0])
                    self.right = Tree(right_str) # TODO::init_operator casting!
            elif g[0]:
                init_operator = Operation.get(init.groups()[1])
                while init_operator == Operation.NOT:
                    if init.groups()[0]:
                        # redistribute the right to be NOT (...)
                        g = (g[0], "NOT ("+g[1]+")")
                        init = initial_op.match(init.groups()[0])
                        if init == None:
                            break
                        init_operator = Operation.get(init.groups()[1])
                    else:
                        # no child on the left, just a plain ol' NOT.
                        self.operator = init_operator
                        break
                # The following also take care of the case where the
                # operator isn't NOT
                logging.debug(init.groups()[0])
                logging.debug(g[1])
                self.left = Tree(init.groups()[0]) if init.groups()[0].strip() != "" else None
                self.right = Tree(g[1]) if g[1].strip() != "" else None
                self.operator = init_operator
            elif g[2]:
                self.operator = Operation.get(later.groups()[0])
                self.left = Tree(g[1]) if g[1].strip() != "" else None
                self.right = Tree(later.groups()[1]) if later.groups()[1].strip() != "" else None
            else:
                self.construct(g[1])
            return False
        

        
        o = or_scan.match(string)
        if o != None and o.groups()[0] and o.groups()[1]:
            # construct for OR
            self.operator = Operation.OR
            self.left = Tree(o.groups()[0])
            self.right = Tree(o.groups()[1])
            return False
        
        a = and_scan.match(string)
        if a != None and a.groups()[0] and a.groups()[1]:
            # construct for AND
            self.operator = Operation.AND
            self.left = Tree(a.groups()[0])
            self.right = Tree(a.groups()[1])
            return False

        n = not_scan.match(string)
        if n != None and n.groups()[0]:
            # construct for NOT
            self.operator = Operation.NOT
            self.right = Tree(n.groups()[0])
            return False

        self.string = string.strip()
        return False
        

        

        
        
