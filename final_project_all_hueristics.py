# -*- coding: utf-8 -*-
"""Final Project All Hueristics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o9hGfyEUZwltXuFwqM3lYeQTcCsevPWm

# CS455 Fianl Projcet
## Created By: Garret Wilson
The purpose of this project is to create a 3X3 Rubik’s cube solver from an initial random state. This will be done using artificial intelligence search algorithms includingBreadth First, Depth First, Iterative Depth First, Greedy Best First, and A*.

# Search Algorith Implimentation
    Implementation of the Rubik's Cube using a list to represent the state.
    The indices of the state map to the following unfolded cube. 
    The faces are label with the position and goal color.
    
                 Top-Yellow
                 0  1  2
                 3  4  5
                 6  7  8
                 
    Left-Red     Front-Green  Right-Orange  Back-Blue 
    9  10 11     18 19 20     27 28 29      36 37 38
    12 13 14     21 22 23     30 31 32      39 40 41
    15 16 17     24 25 26     33 34 35      42 43 44
              
                 Bottom-White
                 45 46 47
                 48 49 50
                 51 52 53

## Uninformed Base Classes
"""

from collections import deque

class UninformedSearchClass:
    """
    Abstract implementation of uninformed search algorithm and supporting methods
    """

    def __init__(self):
        """
        Initializes the Search class by creating the open list and closed list.
        """
        self.openL = deque() # python class for queues and stacks
        self.closedL = set() # empty list
        self.goalS = None

    def addOpen(self, node):
        """
        Abstract method to add a new node to the open list.
        @param node - search node to add to the open list
        """
        pass
    
    def getOpen(self):
        """
        Abstract method to return the front of the open list.
        @return front of open list (based on data structure used)
        """
        pass

    def addClosed(self, node):
        """
        Adds a search node's state to the closed list.
        @param node - node that is closed (i.e. visited)
        """
        self.closedL.add(node)

    def isClosed(self, node):
        """
        Determines if a search node is in the closed list
        based upon the node's state.
        @return True if state is closed; False if it is not.
        """
        if node in self.closedL: return True
        return False
    
    def printPath(self, end):
        """
        Prints the solution path.  It builds a string, which 
        it finally prints once it has traversed from the tail of
        the solution path to its head.
        
        Note: a recursive solution could work, but exceeds the 
        Python recursive depth limit for problems with deep solution
        paths.
    
        @param end - last node in the solution path
        """
        strPath = ""
        cur = end
        while cur:
            strPath = "" + str(cur) + "\n" + strPath
            cur = cur.parent
        print(strPath)
       
    def search(self, initialS, goalS):
        """
        Implements search method
        @param initialS - initial state
        @param goal - target goal state (default None)
        @return search node at solution state
        """
        # Initial state Added to front of open list
        self.goalS = goalS
        self.addOpen(initialS)
        counter = 0

        # Loop until open list is empty
        while len(self.openL) > 0:
            
            # Current Node is next open in the open list
            curN = self.getOpen()
            
            # Cycle Avoidance - determines if current node is already
            #   closed.  O(n) operation.
            if not self.isClosed(curN):
                counter += 1
                
                # Add node to closed list
                self.addClosed(curN)

                # Determine if current node is goal
                if curN.goalTest(goalS):
                    print("Solution Found - " + str(counter) + " Nodes Evaluated.")
                    print("Goal depth: " + str(curN.depth))
                    return curN 
                
                # Interate on successors of current node
                for successorS in curN.getSuccessors():
                    self.addOpen(successorS)
                    
        # Return none if no solution found.    
        return None    
        
class UninformedSearchNode:
    """
    Abstract implementation of a search node for uninformed search
    """
    
    def __init__(self, state, parent=None):
        """
        Initializes the node with the current state and parent, if provided.
        @param state - problem state to be stored in node.
        @param parent - parent node (optional)
        """
        self.state = state
        self.parent = parent
        
        # New node's depth is parent's depth + 1
        if parent: 
            self.depth = parent.depth + 1
        else:
            self.depth = 1
            
    def getDepth(self):
        """
        @return depth of node
        """
        return depth
    
    def __eq__(self, other):
        """
        Abstract method to determine if two nodes are storing equal
        state values.
        @param other - other state node
        @return true if equivalent states; false otherwise
        """
        return self.state == other.state
    
    def __str__(self):
        """
        Prepares a string representation of the state
        """
        return ("       " + " ".join(map(str, self.state[0:3])) + "\n       "  
            + " ".join(map(str, self.state[3:6])) + "\n       " 
            + " ".join(map(str, self.state[6:9])) + "\n"
            + " ".join(map(str, self.state[9:12])) + "  " + " ".join(map(str, self.state[18:21])) + "  " + " ".join(map(str, self.state[27:30])) + "  " + " ".join(map(str, self.state[36:39])) + "\n"
            + " ".join(map(str, self.state[12:15])) + "  " + " ".join(map(str, self.state[21: 24])) + "  " + " ".join(map(str, self.state[30:33])) + "  " + " ".join(map(str, self.state[39:42])) + "\n"
            + " ".join(map(str, self.state[15:18])) + "  " + " ".join(map(str, self.state[24: 27])) + "  " + " ".join(map(str, self.state[33:36])) + "  " + " ".join(map(str, self.state[42:45])) + "\n       "
            + " ".join(map(str, self.state[45:48])) + "\n       "  
            + " ".join(map(str, self.state[48:51])) + "\n       " 
            + " ".join(map(str, self.state[51:54])) + "\n"
               )
    
    def __hash__(self):
        """
        Returns has value based on string representation of state.
        """
        return hash(str(self))
    
    def goalTest(self, goal):
        """
        Abstract method for goal test.
        @param goal - goal condition for goal test
        """
        return self.state == goal.state
      
    def getSuccessors(self):
        pass

"""## Breadth First Search"""

class BreadthFirstSearch(UninformedSearchClass):
    """
    Concrete implementation of SearchClass for BreadthFirstSearch algorithm
    
    The open list is a queue.
    """
    
    def addOpen(self, node):
        """
        Appends node to the end of a queue.
        @param node - search node to add to queue.
        """
        self.openL.append(node)
        
    def getOpen(self):
        """
        Dequeues and returns front of open queue.
        @return search node at front of queue
        """
        return self.openL.popleft()

"""## Depth First Search"""

class DepthFirstSearch(UninformedSearchClass):
    """
    Concrete implementation of SearchClass for DepthFirstSearch algorithm
    
    The openlist is a stack implemented using the Python deque class
    """
    
    def addOpen(self, node):
        """
        Adds node to the top of the top of the stack
        @param node - search node to add to stack.
        """
        self.openL.append(node)
        
    def getOpen(self):
        """
        Pops and returns top of the stack.
        @return search node at top of stack.
        """
        return self.openL.pop()

"""## Iterative Depth First Search"""

class IterativeDepthFirstSearch(DepthFirstSearch):
    
    def __init__(self, limit, step=1):
        """
        Overrides the initializer for DepthFirstSearch
        @param limit - depth limit of the search
        @param step - step distance for depth between iterations
        """
        super().__init__() #call intiailizer of base cass
        self.maxdepth = limit
        self.step = step
    
    def search(self, initialS, goal):
        """
        Overrides the search method to implement the IDFS method
        @param initialS - initial state
        @param goal - goal state
        """
        
        # Increment depth limit from 1 to maximum depth with a step distance
        # between iterations
        for lim in range(1, self.maxdepth+1, self.step):
            
            self.addOpen(initialS)
            self.closedL.clear()
            counter = 0

            # Loop until open list is empty
            while len(self.openL) > 0:
                
                # Current Node is next open in the open list
                curN = self.getOpen()
                
                # Cycle Avoidance - determines if current node is already
                #   closed.  O(n) operation
                if not self.isClosed(curN):
                    counter += 1

                    # Add Node to closed list
                    self.addClosed(curN)

                    # Determine if current node is goal
                    if curN.goalTest(goal): 
                        print("Solution Found - " + str(counter) + " Nodes Evaluated.")
                        print("Goal depth: " + str(curN.depth))
                        return curN 
                    
                    # If depth limit has not been reached, interate on successors 
                    # of current node
                    if (curN.depth < lim):
                        for successorS in curN.getSuccessors():
                            self.addOpen(successorS)
        return None

"""## Informed Base Classes"""

class InformedSearchClass(UninformedSearchClass):
    """
    Abstract implementation of informed search algorithm and supporting methods
    """

    def __init__(self):
        """
        Initiazlize
        @param limit - depth limit of the search
        @param step - step distance for depth between iterations
        """
        super().__init__() #call intiailizer of base cass
        self.openL = list()
        
    def addOpen(self, openS):
        """
        Implements addition to the open list as a priority queue in which new items are 
        added to the queue at the appropriate location to maintain ascending order based 
        on search node priority.
        """
        # Iterate through the list
        for i in range(0,len(self.openL)):
            
            # determine if the node at i has a higher priority than the new node
            #  If so, insert the new search node in front of the node at location i.
            if openS.getPriority() <= self.openL[i].getPriority():
                self.openL.insert(i, openS)
                return
            
        # If a the node has the highest priority, it is added to the end.
        self.openL.insert(len(self.openL), openS) 
    
    def getOpen(self):
        """
        @return highest priority state of open list
        """
        return self.openL.pop(0)
    
    def printPath(self, end):
        """
        Prints the solution path.  It builds a string, which 
        it finally prints once it has traversed from the tail of
        the solution path to its head.
        
        Note: a recursive solution could work, but exceeds the 
        Python recursive depth limit for problems with deep solution
        paths.
    
        @param end - last node in the solution path
        """
        strPath = ""
        cur = end
        while cur:
            strPath = "" + str(cur) + "\n" + strPath
            cur = cur.parent
        print(strPath)                     
        
class InformedSearchNode(UninformedSearchNode):
    """
    Abstract implementation of a search node for informed search
    """
    def __init__(self, state, parent=None):
        """
        Initializes the node with the current state and parent, if provided.
        @param state - problem state to be stored in node.
        @param parent - parent node (optional)
        """
        # Initialize class variables
        self.cost = 0
        self.priority = 0
        self.state = state
        self.setParent(parent)
        
    def setParent(self, parent):
        """
        Sets the parent to the SearchNode
        @param parent - parent of search node
        """
        self.parent = parent
        
        # New node's depth is parent's depth + 1
        if parent: 
            self.depth = parent.depth + 1
        else:
            self.depth = 1                                   
    
    def getPriority(self):
        """
        @return priority of search node
        """
        return self.priority
    
    def setPriority(self, newPriority):
        """
        Sets priority of search node
        @param newPriority - new priority of the search node
        """
        self.priority = newPriority
    
    def getHeuristic(self, goalS):
        error = 0;
        """
        Impelements a simple heuristic counting the number of incorrect
        corner squares in the rubik's cube.
        
        
        for i in range(6):
            for j in range(i*9, i*9+9, 2):
                if (self.state[j] != goalS.state[j]):
                    error += 1       
        """
        
        """
        Impelements a simple heuristic counting the number of incorrect
        corner pieces in the rubik's cube.
        
        
        if (self.state[0] != goalS.state[0] and self.state[9] != goalS.state[9] and self.state[38] != goalS.state[38]):
            error += 1
        if (self.state[2] != goalS.state[2] and self.state[29] != goalS.state[29] and self.state[36] != goalS.state[36]):
            error += 1
        if (self.state[6] != goalS.state[6] and self.state[11] != goalS.state[11] and self.state[18] != goalS.state[18]):
            error += 1
        if (self.state[8] != goalS.state[8] and self.state[20] != goalS.state[20] and self.state[27] != goalS.state[27]):
            error += 1
        if (self.state[45] != goalS.state[45] and self.state[17] != goalS.state[17] and self.state[24] != goalS.state[24]):
            error += 1
        if (self.state[47] != goalS.state[47] and self.state[26] != goalS.state[26] and self.state[33] != goalS.state[33]):
            error += 1
        if (self.state[51] != goalS.state[51] and self.state[15] != goalS.state[15] and self.state[44] != goalS.state[44]):
            error += 1
        if (self.state[53] != goalS.state[53] and self.state[35] != goalS.state[35] and self.state[42] != goalS.state[42]):
            error += 1 
        """
        
        """
        Impelements a simple heuristic counting the number of incorrect
        elements in each face cross in the rubik's cube.
            

        for i in range(6):
            if (self.state[i*9+4] != goalS.state[i*9+1]):
                error += 1   
            for j in range(i*9+1, i*9+9, 2):
                if (self.state[j] != goalS.state[j]):
                    error += 1  
        """ 
        
        """
        Impelements a simple heuristic counting the number of incorrect
        edge pieces of each face cross in the rubik's cube.
        """  
        if (self.state[1] != goalS.state[1] and self.state[37] != goalS.state[37]):
            error += 1
        if (self.state[3] != goalS.state[3] and self.state[10] != goalS.state[10]):
            error += 1
        if (self.state[5] != goalS.state[5] and self.state[28] != goalS.state[28]):
            error += 1
        if (self.state[7] != goalS.state[7] and self.state[19] != goalS.state[19]):
            error += 1
        if (self.state[21] != goalS.state[21] and self.state[14] != goalS.state[14]):
            error += 1
        if (self.state[23] != goalS.state[23] and self.state[30] != goalS.state[30]):
            error += 1
        if (self.state[39] != goalS.state[39] and self.state[32] != goalS.state[32]):
            error += 1
        if (self.state[41] != goalS.state[41] and self.state[12] != goalS.state[12]):
            error += 1
        if (self.state[46] != goalS.state[46] and self.state[25] != goalS.state[25]):
            error += 1
        if (self.state[48] != goalS.state[48] and self.state[16] != goalS.state[16]):
            error += 1
        if (self.state[50] != goalS.state[50] and self.state[32] != goalS.state[32]):
            error += 1
        if (self.state[52] != goalS.state[52] and self.state[43] != goalS.state[43]):
            error += 1 
        
        
        return error
    
    def getStepCost(self, nextS):
        """
        @return step cost for rubik's cube is always 1
        """
        return 1
    
    def getCost(self):
        """
        @return cost to reach search node
        """
        return self.cost
    
    def setCost(self, cost):
        """
        Update cost to reach search node
        @param cost - new cost to reach search node
        """
        self.cost = cost
        
    def getSuccessors(self):
        """
        Creates the set of successor nodes. There are twelve successor nodes
        because all six faces can be rotated clockwise or conter-clockwise.
        @return list of successor states
        """
        successorsL = []
        
        # Top Face
        #   Clockwise
        TCW = self.state[:]
        TCW[9:12], TCW[18:21], TCW[27:30], TCW[36:39], TCW[0:3], TCW[3:6], TCW[6:9] \
              = TCW[18:21], TCW[27:30], TCW[36:39], TCW[9:12], [TCW[6], TCW[3], TCW[0]], [TCW[7], TCW[4], TCW[1]], [TCW[8], TCW[5], TCW[2]]
        successorsL.append(InformedSearchNode(TCW, self))
        #   Counter-clockwise
        TCCW = self.state[:]
        TCCW[9:12], TCCW[18:21], TCCW[27:30], TCCW[36:39], TCCW[0:3], TCCW[3:6], TCCW[6:9] \
              = TCCW[36:39], TCCW[9:12], TCCW[18:21], TCCW[27:30], [TCCW[2], TCCW[5], TCCW[8]], [TCCW[1], TCCW[4], TCCW[7]], [TCCW[0], TCCW[3], TCCW[6]]     
        successorsL.append(InformedSearchNode(TCCW, self))
        
        # Left Face
        #   Clockwise
        LCW = self.state[:]
        LCW[0], LCW[3], LCW[6], LCW[18], LCW[21], LCW[24], LCW[38], LCW[41], LCW[44], LCW[45], LCW[48], LCW[51], LCW[9:12], LCW[12:15], LCW[15:18] \
              = LCW[44], LCW[41], LCW[38], LCW[0], LCW[3], LCW[6], LCW[51], LCW[48], LCW[45], LCW[18], LCW[21], LCW[24], [LCW[15], LCW[12], LCW[9]], [LCW[16], LCW[13],LCW[10]], [LCW[17], LCW[14],LCW[11]]                   
        successorsL.append(InformedSearchNode(LCW, self))                 
        #   Counter-clockwise
        LCCW = self.state[:]
        LCCW[0], LCCW[3], LCCW[6], LCCW[18], LCCW[21], LCCW[24], LCCW[38], LCCW[41], LCCW[44], LCCW[45], LCCW[48], LCCW[51], LCCW[9:12], LCCW[12:15], LCCW[15:18] \
              = LCCW[18], LCCW[21], LCCW[24], LCCW[45], LCCW[48], LCCW[51], LCCW[6], LCCW[3], LCCW[0], LCCW[44], LCCW[41], LCCW[38], [LCCW[11], LCCW[14],LCCW[17]], [LCCW[10], LCCW[13],LCCW[16]], [LCCW[9], LCCW[12],LCCW[15]] 
        successorsL.append(InformedSearchNode(LCCW, self))
                           
        # Front Face
        #   Clockwise
        FCW = self.state[:]
        FCW[6:9], FCW[11], FCW[14], FCW[17], FCW[27], FCW[30], FCW[33], FCW[45:48], FCW[18:21], FCW[21:24], FCW[24:27] \
              = [FCW[17], FCW[14], FCW[11]], FCW[45], FCW[46], FCW[47], FCW[6], FCW[7], FCW[8], [FCW[33], FCW[30], FCW[27]], [FCW[24], FCW[21], FCW[18]], [FCW[25], FCW[22], FCW[19]], [FCW[26], FCW[23], FCW[20]] 
        successorsL.append(InformedSearchNode(FCW, self))                   
        #   Counter-clockwise
        FCCW = self.state[:]
        FCCW[6:9], FCCW[11], FCCW[14], FCCW[17], FCCW[27], FCCW[30], FCCW[33], FCCW[45:48], FCCW[18:21], FCCW[21:24], FCCW[24:27] \
              = [FCCW[27], FCCW[30], FCCW[33]], FCCW[8], FCCW[7], FCCW[6], FCCW[47], FCCW[46], FCCW[45], [FCCW[11], FCCW[14], FCCW[17]], [FCCW[20], FCCW[23], FCCW[26]], [FCCW[19], FCCW[22], FCCW[25]], [FCCW[18], FCCW[21], FCCW[24]]                           
        successorsL.append(InformedSearchNode(FCCW, self))
        
        # Right Face
        #   Clockwise
        RCW = self.state[:]
        RCW[2], RCW[5], RCW[8], RCW[20], RCW[23], RCW[26], RCW[36], RCW[39], RCW[42], RCW[47], RCW[50], RCW[53], RCW[27:30], RCW[30:33], RCW[33:36] \
              = RCW[20], RCW[23], RCW[26], RCW[47], RCW[50], RCW[53], RCW[8], RCW[5], RCW[2], RCW[42], RCW[39], RCW[36], [RCW[33], RCW[30], RCW[27]], [RCW[34], RCW[31], RCW[28]], [RCW[35], RCW[32], RCW[29]]                          
        successorsL.append(InformedSearchNode(RCW, self))
        #   Counter-clockwise
        RCCW = self.state[:]
        RCCW[2], RCCW[5], RCCW[8], RCCW[20], RCCW[23], RCCW[26], RCCW[36], RCCW[39], RCCW[42], RCCW[47], RCCW[50], RCCW[53], RCCW[27:30], RCCW[30:33], RCCW[33:36] \
              = RCCW[42], RCCW[39], RCCW[36], RCCW[2], RCCW[5], RCCW[8], RCCW[53], RCCW[50], RCCW[47], RCCW[20], RCCW[23], RCCW[26], [RCCW[29], RCCW[32], RCCW[35]], [RCCW[28], RCCW[31], RCCW[34]], [RCCW[27], RCCW[30], RCCW[33]]                               
        successorsL.append(InformedSearchNode(RCCW, self))
        
        # Back Face
        #   Clockwise
        BCW = self.state[:]
        BCW[0:3], BCW[9], BCW[12], BCW[15], BCW[29], BCW[32], BCW[35], BCW[51:54], BCW[36:39], BCW[39:42], BCW[42:45] \
              = [BCW[29], BCW[32], BCW[35]], BCW[2], BCW[1], BCW[0], BCW[53], BCW[52], BCW[51], [BCW[9], BCW[12], BCW[15]], [BCW[42], BCW[39], BCW[36]], [BCW[43], BCW[40], BCW[37]], [BCW[44], BCW[41], BCW[38]]            
        successorsL.append(InformedSearchNode(BCW, self))
        #   Counter-clockwise
        BCCW = self.state[:]
        BCCW[0:3], BCCW[9], BCCW[12], BCCW[15], BCCW[29], BCCW[32], BCCW[35], BCCW[51:54], BCCW[36:39], BCCW[39:42], BCCW[42:45] \
              = [BCCW[15], BCCW[12], BCCW[9]], BCCW[51], BCCW[52], BCCW[53], BCCW[0], BCCW[1], BCCW[2], [BCCW[35], BCCW[32], BCCW[29]], [BCCW[38], BCCW[41], BCCW[44]], [BCCW[37], BCCW[40], BCCW[43]], [BCCW[36], BCCW[39], BCCW[42]]                       
        successorsL.append(InformedSearchNode(BCCW, self))
        
        # Bottom Face
        #   Clockwise
        DCW = self.state[:]
        DCW[15:18], DCW[24:27], DCW[33:36], DCW[42:45], DCW[45:48], DCW[48:51], DCW[51:54] \
              = DCW[42:45], DCW[15:18], DCW[24:27], DCW[33:36], [DCW[51], DCW[48], DCW[45]], [DCW[52], DCW[49], DCW[46]], [DCW[53], DCW[50], DCW[47]]                  
        successorsL.append(InformedSearchNode(DCW, self))
        #   Counter-clockwise
        DCCW = self.state[:]
        DCCW[15:18], DCCW[24:27], DCCW[33:36], DCCW[42:45], DCCW[45:48], DCCW[48:51], DCCW[51:54] \
              = DCCW[24:27], DCCW[33:36], DCCW[42:45], DCCW[15:18], [DCW[47], DCW[50], DCW[53]], [DCW[46], DCW[49], DCW[52]], [DCW[45], DCW[48], DCW[51]]                       
        successorsL.append(InformedSearchNode(DCCW, self))        
        
        return successorsL

"""## Greedy Best First Search"""

class GreedySearch(InformedSearchClass):
    """
    Impelmentation of greedy best first search by extending SearchClass base class
    """
    def __init__(self):
        """
        Initializes GreedySearch class calling parent constructor
        """
        super().__init__() #call intiailizer of base cass
        
    def addOpen(self, openS):
        """
        Adds state to the open list ordered by the heuristic distance from
        the goal.
        @param openS - open state to add to open list
        """
        
        # Sets the priority of the new node to its heuristic value
        heuristic = openS.getHeuristic(self.goalS)
        openS.setPriority(heuristic)
        
        # Calls the base class add method to add to the open list
        super().addOpen(openS)

"""## A* Search"""

class AStarSearch(InformedSearchClass):
    """
    Implementation of the A* search algorithm by extending the base class.
    """
    def __init__(self):
        """
        Initializes A* class calling parent constructor
        """
        super().__init__() #call intiailizer of base cass
        
    def findMatchingOpen(self, target):
        """
        Finds the matching search node from the open set and returns it.
        @param target - node to locate
        """
        for i in range(0,len(self.openL)):
            if self.openL[i] == target:
                return self.openL[i]
        return None

    def removeMatchingOpen(self, target):
        """
        Finds matching node from open set and returns it.
        @param target - node to remove.
        """
        for i in range(0,len(self.openL)):
            if self.openL[i] == target:
                self.openL.pop(i)
                return

    def getOpen(self):
        """
        Returns the front of the open list (i.e. node with highest priority)
        """
        state = self.openL.pop(0)
        return state
    
    def search(self, initialS, goal=None):
        """
        Executes A* search
        @param initialS - initial state node
        @param goal - goal of the search (if required)
        @return solution node
        """
        self.goalS = goal
        self.addOpen(initialS)
        self.counter = 0

        while len(self.openL) > 0:
            
            curN = self.getOpen()
            
            if not self.isClosed(curN):
                self.counter += 1
                
                self.addClosed(curN)

                if curN.goalTest(goal):
                    print("Solution Found - " + str(self.counter) + " Nodes Evaluated.")
                    print("Goal depth: " + str(curN.depth))
                    return curN 
                
                for successorS in curN.getSuccessors():
                    
                    if self.isClosed(successorS): 
                        continue
                    
                    oldS = self.findMatchingOpen(successorS) 
                    tmpG = curN.getCost() + curN.getStepCost(successorS)
                    
                    if not oldS:
                        h = successorS.getHeuristic(goal)
                        successorS.setCost(tmpG)
                        successorS.setPriority(h + tmpG)
                        self.addOpen(successorS)
                    
                    elif tmpG < oldS.getCost():
                        self.removeMatchingOpen(oldS)
                        oldS.setParent(curN) 
                        oldS.setCost(tmpG)
                        oldS.setPriority(successorS.getHeuristic(goal) + tmpG)
                        self.addOpen(oldS)
        return None

"""# Rubik's Cube Demonstration

### Rubik's Cube Initialization
"""

#Define initial state and goal state   

# Top, Front, Right, Bottom
initialS = InformedSearchNode(['Y', 'B', 'B', 'Y', 'Y', 'O', 'R', 'R', 'O',
                                  'O', 'G', 'W', 'Y', 'R', 'W', 'Y', 'R', 'W',
                                  'G', 'G', 'B', 'G', 'G', 'W', 'G', 'G', 'W',
                                  'Y', 'Y', 'R', 'O', 'O', 'W', 'O', 'O', 'W',
                                  'Y', 'Y', 'G', 'B', 'B', 'R', 'B', 'B', 'R',
                                  'O', 'O', 'B', 'W', 'W', 'B', 'G', 'R', 'R']) 
""" 

#Front, Right, Left, Front, Top, Right
initialS = InformedSearchNode(['W', 'B', 'Y', 'R', 'Y', 'G', 'R', 'G', 'O',
                                  'R', 'Y', 'Y', 'R', 'R', 'O', 'W', 'W', 'B',
                                  'B', 'Y', 'Y', 'G', 'G', 'B', 'W', 'W', 'B',
                                  'G', 'R', 'R', 'O', 'O', 'B', 'O', 'O', 'W',
                                  'G', 'R', 'G', 'Y', 'B', 'W', 'B', 'B', 'O',
                                  'O', 'O', 'Y', 'G', 'W', 'Y', 'G', 'W', 'R']) 
""" 
""" 
#Scrambled a little bit
initialS = InformedSearchNode(['G', 'B', 'B', 'Y', 'Y', 'W', 'B', 'R', 'R',
                                  'R', 'B', 'W', 'W', 'R', 'G', 'W', 'Y', 'O',
                                  'R', 'Y', 'Y', 'R', 'G', 'O', 'G', 'R', 'B',
                                  'B', 'G', 'O', 'G', 'O', 'W', 'O', 'G', 'G',
                                  'W', 'O', 'Y', 'B', 'B', 'O', 'O', 'R', 'G',
                                  'Y', 'W', 'Y', 'O', 'W', 'Y', 'R', 'B', 'W']) 
"""

goalS = InformedSearchNode(['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y',
                                  'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',
                                  'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
                                  'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
                                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                                  'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'])

"""### BFS Demonstration"""

#Execute Search and Print Results
search = BreadthFirstSearch()
solution = search.search(initialS, goalS)
search.printPath(solution)

"""### DFS Demonstration"""

#This search method never finishes due to the fact that it might have to run through all 4.3252X10^19 states a Rubik's cube has
"""#Execute Search and Print Results
search = DepthFirstSearch()
solution = search.search(initialS, goalS)
search.printPath(solution)"""

"""### IDFS Demonstration"""

#Execute Search and Print Results
search = IterativeDepthFirstSearch(10)
solution = search.search(initialS, goalS)
search.printPath(solution)

"""### Greedy Best First Demonstration"""

#Execute Search and Print Results
search = GreedySearch()
result = search.search(initialS, goalS)
search.printPath(result)

"""### A* Demonstration"""

#Execute Search and Print Results
search = AStarSearch()
result = search.search(initialS, goalS)
search.printPath(result)