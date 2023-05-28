import table
lr_table = table.lr_table
productions = table.productions
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def top(self):
        if not self.is_empty():
            return self.stack[-1]
        return None


def parse_lr_table(lr_table, input_string):
    stack = Stack()
    stack.push(0)  # 초기 상태(0)를 스택에 푸시

    i = 0  # 입력 문자열의 인덱스
    while True:
        state = stack.top()
        symbol = input_string[i]

        if (state, symbol) in lr_table:
            action = lr_table[(state, symbol)]

            if action[0] == 's':
                # Shift 액션일 경우
                stack.push(symbol)  # 기호를 다시 스택에 푸시
                stack.push(int(action[1:]))  # 다음 상태를 스택에 푸시
                i += 1  # 다음 입력 문자열로 이동
            elif action[0] == 'g':
                # Goto 액션일 경우
                stack.push(symbol)  # 기호를 다시 스택에 푸시
                stack.push(int(action[1:]))  # 다음 상태를 스택에 푸시
            elif action[0] == 'r':
                # Reduce 액션일 경우
                stack.pop()
                reduction = productions[int(action[1:])][0]
                count = productions[int(action[1:])][1]
                del input_string[i - count : i]
                input_string.insert(i - count, reduction)
            elif action == 'acc':
                # Accept 액션일 경우
                return True
        else:
            # 오류 처리
            return False


lr_table = {
    (0, 'vtype'): ('s2'),
    (0, 'VDECL'): ('g1'),
    (1, 'vtype'): ('s6'),
    (1, 'class'): ('s7'),
    # …
}

productions = {
    0: ('S', 'VDECL'),
    1: ('VDECL', 'vtype', 'ID', 'SEMICOLON'),
    # …
}

input_string = input().split()
print(input_string)
result = parse_lr_table(lr_table, input_string)
if result:
    print("파싱 가능합니다.")
else:
    print("파싱 불가능합니다.")