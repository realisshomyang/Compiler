import sys
import table
from anytree.exporter import UniqueDotExporter
from anytree import Node, RenderTree
import os

#get CFG production's information , LR Table information in table.py
lr_table = table.lr_table
productions = table.productions

#list that save the nodes of the parse tree
parsetree = []

""" class Treenode to represent a node in the parse tree
We use anytree Library 
The anytree library is a Python library that provides a simple and flexible way to work with tree data structures.
in anytree library we use Node, RenderTree to show parse tree in terminal , 
And uniqueDotExporter to make export .dot file to draw png file of parse tree in graphviz library
"""
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def create_tree_node(self):
        node = Node(str(self.data))
        for child in self.children:
            child_node = child.create_tree_node()
            child_node.parent = node
        return node

#main feature function
#do same action with slr parser 
def parse_lr_table(lr_table):
    stack = [] #stack is made to deal with the state in slr parser 
    stack.append(0)  # push the initial state (0) to the stack
    i = 0  # index of the input string -> do a role of splitter
    cnt = 0 #variable to represent parsing step
    while True:
        cnt += 1 
        #bring the top of the stack
        state = stack[-1] 
        #bring next character, we save node in parse so .data is needed
        symbol = parsetree[i].data
        """
        If a value matching state and next character exists in the table, do parse
        Else parse failed
        """
        if (state, symbol) in lr_table:
            #get action from lr_table
            action = lr_table[(state, symbol)]
            # Shift action
            if action[0] == 's':
                stack.append(int(action[1:]))  # push the next state to the stack
                i += 1  # move splitter
            # Goto action
            elif action[0] == 'g':
                stack.append(int(action[1:]))  # push the next state to the stack
            #Reduce action
            elif action[0] == 'r':
                #r~~ gives which production in CFG to reduce, 
                #so we bring CFG's data by line-> LHS of production and count of RHS
                reduction = productions[int(action[1:])][0]
                count = productions[int(action[1:])][1]
                #tmp_node is node to draw parse tree 
                #it contains RHS for child node
                #and node's data is LHS of CFG
                tmp_node = TreeNode(reduction)
                #reduce procedure, step 1 :for A -> a pop the |a| contents from the stack
                for j in range(count):
                    stack.pop()
                #add child node in parent node
                for x in parsetree[i - count: i]:
                    tmp_node.add_child(x)
                #parsetree append tmp_node's data
                parsetree.append(tmp_node)
                #reduce -> change RHS to LHS of production in parsetree
                del parsetree[i - count: i]
                parsetree.insert(i - count, tmp_node)
                #step 2 : A->a push GOTO(currentstate,A)
                stack.append(int(lr_table[stack[-1], reduction][1:]))
                #splitter adjust
                i = i - count + 1
            elif action == 'acc':
                # Accept action
                return True
        else:
            # Parsing error
            """ 
            1. print current parsing situation
            2. print Steps in the parsing sequence
            3. print Current splitter position
            4. print current state and next input symbol
            5. print What expected for next input and error input
            """
            print("!!!Current parsing status!!!")
            print("Parsing is not possible in this situation.")
            for x in parsetree:
                if x.data == '$':
                    break
                print(x.data, end=" ")
            
            print("\nLine number (in Parsing sequence): " + str(cnt))
            print("Current splitter position: " + str(i))
            print("State: " + str(state) + " and next symbol: " + symbol)
            print("next input expected for {} is ->".format(parsetree[i-1].data) , end =" ")
            result = [key[1] for key in lr_table.keys() if key[0] == state]
            for x in result:
                print(x, end=" ")
            print(" not {}".format(symbol))
            return False

# Check if the input file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please specify an input file.\n")
    sys.exit(1)
input_file = sys.argv[1]

# Read the contents of the text file
try:
    with open(input_file, "r") as file:
        file_contents = file.read()
except FileNotFoundError:
    print("Input file not found.")
    sys.exit(1)

# Split the input string and append $
input_string = file_contents.split()
input_string.append('$')

# Create tree nodes for each symbol in the input string
for x in input_string:
    parsetree.append(TreeNode(x))

# Perform LR parsing using the LR table
result = parse_lr_table(lr_table)


if result:
    print("Parsing available.")
    print("Print parse tree:")
    root = parsetree[-1].create_tree_node()
    
    # Print the parse tree structure using indentation in terminal
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")
    
    #notice how to open more visualized parse tree
    print("If you open 'parsetree.png' in this directory, you can see a more visualized parse tree from your input.")
    
    # Export the parse tree as an image file
    exporter = UniqueDotExporter(root)
    exporter.to_picture("parsetree.png")
