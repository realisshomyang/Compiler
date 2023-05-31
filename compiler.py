import table
lr_table = table.lr_table
productions = table.productions


def parse_lr_table(lr_table, input_string):
    stack = []
    stack.append(0)  # 초기 상태(0)를 스택에 푸시
    input_lst = input_string
    i = 0  # 입력 문자열의 인덱스
    while True:
        state = stack[-1]
        symbol = input_lst[i]
        if (state, symbol) in lr_table:
            action = lr_table[(state, symbol)]
            print("-------")
            print(stack)
            print(input_lst)
            print("i :" + str(i))
            print(action)
            print(state)
            print("-------")
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
                for j in range(count):
                    stack.pop()
                del input_lst[i-count: i]
                input_lst.insert(i - count, reduction)
                print(input_lst)
                print(i)
                stack.append(int(lr_table[stack[-1], reduction][1:]))
                i = i-count + 1
                print(stack)
                print(i)
            elif action == 'acc':
                # Accept 액션일 경우
                print(input_lst)
                return True
        else:
            # 오류 처리
            return False


input_string = input().split()
input_string.append('$')
result = parse_lr_table(lr_table, input_string)
if result:
    print("파싱 가능합니다.")
else:
    print("파싱 불가능합니다.")
