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
and_scan = re.compile(r"(.+?) AND (.+)") # deprecated
or_scan  = re.compile(r"(.+?) OR (.+)")  # deprecated

class Tree(object):
    def __init__(self, string = None):
        self.processed = False
        self.operator = None
        self.left = None
        self.right = None
        self.string = None
        # try:
        while string != None and self.construct(string) == True:
            pass
        # except AttributeError as e:
        #     print string
        #     raise e

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

    def preprocess(self):
        # de morgan's law, sort of
        # we don't want to end up creating a whole bunch of NOTs
        # TODO

        # cancelling nested NOTs by hoisting
        # by convention, NOT has a right child.
        if self.operator == Operation.NOT and self.right.operator == Operation.NOT:
            self = self.right.right
            self.preprocess()

        # TODO::using result sizes to move subtrees around...
            
    def isWithinParantheses(self, string, position):
        """
        Returns True if the given *position* in the *string* lies within a pair of parantheses.
        """
        fst = string.rfind('(', 0, position)
        if fst != -1:
            cls = string.rfind(')', fst, position)
            if cls == -1:
                return True
        return False
    
    def construct(self, string):
        """
        Construct the tree based on a string. This method scans for operators in this order--
        * Or (lowest to highest precedence)
        * And
        * Not
        * Parantheses
        on the basis of which it chooses its own operator, and then splits the string accordingly. It first tries all possible OR|AND matches, to see if there are any occurrences that would be considered "top-level". If not, it moves on to NOT|().

        The substrings thus obtained are used as the input to recursively create Trees for its right or left children. If none of the operators match, the string is considered to be a base token and stored.

        Some complexity is introduced when handling cases such as "NOT (...)" or "NOT NOT (...)", as the unary NOT needs to be distributed to the right child Tree.

        Creating a tree--

        * makes it more difficult to optimize the query order based on individual result sizes
        * makes it very easy to optimize the query by cancelling nested NOTs, or De Morgan's rule
        """
        string.strip()

        for match in re.finditer(r" OR ", string):
            pos = match.start()
            if string[:pos] and string[pos+4:] and not self.isWithinParantheses(string, pos):
                logging.debug("parsing OR")
                self.operator = Operation.OR
                self.left = Tree(string[:pos])
                self.right = Tree(string[pos+4:])
                return False

        for match in re.finditer(r" AND ", string):
            pos = match.start()
            if string[:pos] and string[pos+5:] and not self.isWithinParantheses(string, pos):
                logging.debug("parsing AND")
                self.operator = Operation.AND
                self.left = Tree(string[:pos])
                self.right = Tree(string[pos+5:])
                return False

        n = not_scan.match(string)
        if n != None and n.groups()[0] and not self.isWithinParantheses(string, len(n.groups()[0])):
            logging.debug("parsing NOT")
            self.operator = Operation.NOT
            self.right = Tree(n.groups()[0])
            return False



        # here we start the matching of () operators. A few things are
        # to be done here, ergo the ugly mess.
        # First, we must decide whether the tree is to be rooted by
        # the operator on the left, or the right of the () [mostly an
        # artifact due to legacy design decisions]
        # This procedure's complexity can be *significantly* reduced,
        # if I have time to get back to it...
        
        p = p_scan.match(string)
        # in case of NOT, no previous clause is to be created.
        #
        initial_op = re.compile(r"(.*) ?(AND|OR|NOT) ") 
        
        later_op = re.compile(r" (AND|OR) (.+)")

        if p != None and p.groups()[1]:
            g = p.groups()

            init = initial_op.match(g[0])
            later = later_op.match(g[2])
            logging.debug("INITIAL GROUPS ARE: "+str(g))

            if g[0].strip() and g[2].strip():
                # both clauses exist, figure out where to root the
                # tree
                init_operator = Operation.get(init.groups()[1])
                later_operator = Operation.get(later.groups()[0])
                while init_operator == Operation.NOT:
                    if init.groups()[0]:
                        # redistribute the right child to be "NOT ..."
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
                    self.left = Tree(lft_str)
                    self.right = Tree(later.groups()[1]) if later.groups()[1].strip() != "" else None
                else:
                    self.operator = later_operator
                    self.left = Tree(init.groups()[0]) if init.groups()[0].strip() != "" else None
                    right_str = "{0} {1} {2}".format(g[1], Operation.str(later_operator), later.groups()[1])
                    logging.debug("INIT less than LATER")
                    logging.debug(right_str)
                    logging.debug(init.groups()[0])
                    self.right = Tree(right_str)
            elif g[0].strip():
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
            elif g[2].strip():
                self.operator = Operation.get(later.groups()[0])
                self.left = Tree(g[1]) if g[1].strip() != "" else None
                self.right = Tree(later.groups()[1]) if later.groups()[1].strip() != "" else None
            else:
                self.construct(g[1])
            return False
        


        self.string = string.strip()
        return False
        
