import sys
import table
from anytree.exporter import UniqueDotExporter
from anytree import Node, RenderTree
import os

lr_table = table.lr_table
productions = table.productions

parsetree = []

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

def parse_lr_table(lr_table):
    last_parse = 0
    stack = []
    stack.append(0)  # 초기 상태(0)를 스택에 푸시
    i = 0  # 입력 문자열의 인덱스
    cnt = 0
    while True:
        cnt += 1
        state = stack[-1]
        symbol = parsetree[i].data
        if (state, symbol) in lr_table:
            action = lr_table[(state, symbol)]
            if action[0] == 's':
                # Shift 액션일 경우
                stack.append(int(action[1:]))  # 다음 상태를 스택에 푸시
                i += 1  # 다음 입력 문자열로 이동
            elif action[0] == 'g':
                # Goto 액션일 경우
                stack.append(int(action[1:]))  # 다음 상태를 스택에 푸시
            elif action[0] == 'r':
                # Reduce 액션일 경우
                reduction = productions[int(action[1:])][0]
                count = productions[int(action[1:])][1]
                tmp_node = TreeNode(reduction)
                for j in range(count):
                    stack.pop()
                for x in parsetree[i - count : i]:
                    tmp_node.add_child(x)
                last_parse = tmp_node
                parsetree.append(tmp_node)
                del parsetree[i - count : i]
                parsetree.insert(i - count, tmp_node)
                stack.append(int(lr_table[stack[-1], reduction][1:]))
                i = i - count + 1
            elif action == 'acc':
                # Accept 액션일 경우
                return True
        else:
            print("!!!Current parsing status!!!")
            for x in parsetree:
                if x.data == '$' :
                    break
                print(x.data , end=" ")
            
            print("\nLine number(in Parsing sequence) : " + str(cnt))
            print("current spliter position : " + str(i))
            print("state : " + str(state) + " and next symbol : " + symbol)
            return False

# 커맨드 라인 인자로 입력 파일 경로 받기
if len(sys.argv) < 2:
    print("Please specify input file \n")
    sys.exit(1)
input_file = sys.argv[1]
# txt 파일 읽기
with open(input_file, "r") as file:
    file_contents = file.read()

# 문자열 분리
input_string = file_contents.split()
input_string.append('$')

for x in input_string:
    parsetree.append(TreeNode(x))
result = parse_lr_table(lr_table)
if result:
    print("parsing available.")
    print("Print parse tree:")
    root = parsetree[-1].create_tree_node()
    # 트리 그래프 생성 및 출력
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")
    print("if you open !!parsetree.png!! in this directory \nyou can see more visualized parsetree from your input")
    #image 파일 생성
    exporter = UniqueDotExporter(root)
    exporter.to_picture("parsetree.png")
else:
    print("이 상황에서는 파싱 불가능합니다.")
