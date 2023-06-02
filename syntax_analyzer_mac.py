import sys
import table
from anytree.exporter import UniqueDotExporter
from anytree import Node, RenderTree
import os

#get CFG information, LR Table information in table.py
#lr_table -> key(state, next character of splitter) : value(actions)
#production -> key(lefthandside production) : value(sum of non-terminals and terminals count)
lr_table = table.lr_table
productions = table.productions

#list that save the node of the parse tree
parsetree = []

#class Treenode to represent a node in the parse tree
#We use anytree Library
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
    stack = []
    stack.append(0)  # push the initial state (0) to the stack
    i = 0  # index of the input string -> do a role of splitter
    j = 0
    cnt = 0 #variable to represent parsing step
    while True:
        cnt += 1
        state = stack[-1]
        symbol = parsetree[i].data
        if (state, symbol) in lr_table:
            action = lr_table[(state, symbol)]
            if action[0] == 's':
                # Shift action
                stack.append(int(action[1:]))  # push the next state to the stack
                i += 1  # move to the next input symbol
                j+=1
            elif action[0] == 'g':
                # Goto action
                stack.append(int(action[1:]))  # push the next state to the stack
            elif action[0] == 'r':
                # Reduce action
                reduction = productions[int(action[1:])][0]
                count = productions[int(action[1:])][1]
                tmp_node = TreeNode(reduction)
                for j in range(count):
                    stack.pop()
                for x in parsetree[i - count: i]:
                    tmp_node.add_child(x)
                parsetree.append(tmp_node)
                del parsetree[i - count: i]
                parsetree.insert(i - count, tmp_node)
                stack.append(int(lr_table[stack[-1], reduction][1:]))
                i = i - count + 1
                j+=1
            elif action == 'acc':
                # Accept action
                return True
        else:
            # Parsing error
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

# Split the input string
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
    
    # Print the parse tree structure using indentation
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")
    
    print("If you open 'parsetree.png' in this directory, you can see a more visualized parse tree from your input.")
    
    # Export the parse tree as an image file
    exporter = UniqueDotExporter(root)
    exporter.to_picture("parsetree.png")
    os.system("open parsetree.png")
