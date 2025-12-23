import time, random, os, copy

def remove_n(line): #문자열 맨 마지막에 이스케이프 문자 \n을 제거해주는 함수
    while len(line)>0 and line[-1]=='\n':
        line = line[:-1]
    return line

def confirm_space(line): # 끝에 공백이 없으면 맨 끝에 공백을 추가해주는 함수
    if not (len(line) > 0 and line[-1] == ' '):
        line += ' '
    return line

def computer_move_easy(board): #easy 난이도에서 컴퓨터가 선택하는 알고리즘을 구현합니다.
    while True:
        column_selected_by_computer = random.randint(0,6) #랜덤으로 열 선택
        if board[1][2*column_selected_by_computer+1]=='   ':
            print("- column {0} selected.\n".format(column_selected_by_computer))
            drop_stone(board,column_selected_by_computer,'X')
            print_board(board) #보드 출력
            return column_selected_by_computer
        else:
            continue

def computer_move_normal(board): #normal 난이도에서 컴퓨터가 선택하는 알고리즘을 구현합니다.
    column_selected_by_computer=simulate_drop(board) #승리 가능성 판단 후 열 선택
    print("- column {0} selected.\n".format(column_selected_by_computer))
    drop_stone(board,column_selected_by_computer,'X')
    print_board(board) #보드 출력
    return column_selected_by_computer

def initialize_board(): #게임 보드를 초기화하여 2차원 리스트를 반환합니다.
    return [ [('+' if j%2==0 else '---') if i%2==0 else ('|' if j%2==0 else '   ') for j in range(15)] for i in range(13) ]

def winner_decision(R,board):
    if R == 1: #플레이어 승리
        print("\nYou win!\n")
        return 'Q'
    elif R == -1 : #컴퓨터 승리
        print("\nYou lose!\n") 
        return 'Q'
    elif R == 0:#무승부 가능성
        check_empty = [ board[i][j]  for i in range(len(board)) for j in range(len(board[i])) ] #빈칸있는지 검사
        if '   ' not in check_empty: #보드에 빈칸 없으면 무승부
            print("\nDraw!\n")
            return 'Q'

def file_saving(game_record,difficulty):
    filename=input("Game paused. Enter file name to save: ") #파일 이름 입력받음
    file=open(filename,'w') #파일 열기
    if difficulty == '1': 
        file.write('mode=Easy\n')#난이도:쉬움
    elif difficulty == '2':
        file.write('mode=Normal\n')#난이도:보통
    if not (len(game_record)>0 and game_record[-1]==' '):#게임 기록의 마지막에 공백 추가
        game_record += ' '
    file.write(game_record) #게임 기록 작성
    file.close() #파일 닫기

def print_board(board): #현재 게임 보드를 출력합니다.
    for i in range(len(board)+1):
        if i>=13:
            print('  0   1   2   3   4   5   6  ') #열 번호 출력
        else:
            for j in range(len(board[i])):
                print(board[i][j],end='')
            print()

def drop_stone(board,col,mark): #선택된 열에 돌을 떨어뜨립니다.
    for row in range(6) :
        if board[12-(2*row+1)][2*int(col)+1] == '   ':
            board[12-(2*row+1)][2*int(col)+1] = ' {0} '.format(mark)
            break

def load_game(board): #저장된 파일을 읽어 난이도(mode)와 돌의 진행 상태(moves)를 불러와, 게임 보드를 복원합니다.
    file_name = input('Enter file name to load: ')
    if os.path.exists(file_name): #파일이 존재하는지 확인(존재 case)
        file=open(file_name,'r')
        data=file.readlines() #난이도와 게임 기록 문자열로 구성된 리스트 생성
        mode_line = remove_n(data[0][5:]) # 난이도 문자열에서 Easy/Normal만 따로 추출
        mode = '1' if mode_line == 'Easy' else '2' #난이도에 맞는 모드 숫자 문자열 할당
        data2=data[1][6:].split() #게임 기록 문자열에서 앞의 'moves=' 부분 날리고 나머지 부분을 공백 기준으로 나누어 리스트로 저장
        for i in range(len(data2)):
            if i%2==0:
                drop_stone(board,data2[i],'O') #홀수번째는 플레이어 입력이므로 O를 보드에
            else:
                drop_stone(board,data2[i],'X') #짝수번째는 컴퓨터 입력이므로 X를 보드에 떨굼
        record_line=confirm_space(remove_n(data[1])) #게임 기록 문자열을 이어가야하기에 혹시 모를 이스케이프 문자 \n을 삭제, 또한 공백이 없을 경우 공백 하나만 끝에 추가
        return mode,board,record_line #난이도,반영된 게임보드, 게임 기록 반환
    else: #파일이 존재 X case
        print("File not found!") #파일 못찾음 메시지 출력
        return 'n','n','n' #파일이 없음을 외부에 알리는 신호 출력

def check_win(board): #가로나 세로, 대각선으로 4개가 연결되었는지 검사합니다.
    #1. 가로 검사
    for i in range(1,12,2):
        counter1=0
        for j in range(1,12,2):
            if board[i][j] == board[i][j+2] and board[i][j] != '   ':
                counter1 += 1
                if counter1 == 3 and board[i][j]==' O ':
                    return 1
                elif counter1 == 3 and board[i][j]==' X ':
                    return -1                   
            else:
                counter1 = 0
    #2. 세로 검사            
    for j in range(1,14,2):
        counter2=0
        for i in range(1,10,2):
            if board[i][j] == board[i+2][j] and board[i][j] != '   ':
                counter2 += 1
                if counter2 == 3 and board[i][j] == ' O ':
                    return 1
                elif counter2 == 3 and board[i][j] == ' X ':
                    return -1                
            else:
                counter2 = 0
    #3. 우상향 방향 대각선 검사
    point1 = [(i,1) for i in range(11,4,-2)] + [(11,j) for j in range(3,8,2)] #시작점 모음
    for row,col in point1: #시작점중 하나에 대해 진행
        counter3=0 #카운터 초기화
        i,j=row,col
        while  i-2 >= 1 and j+2<= 13 :#보드의 경계에 이를때까지 작동
            if board[i][j] == board[i-2][j+2] and board[i][j] != '   ':
                counter3 += 1 #같으면 카운터에 더함
                if counter3 == 3 and board[i][j] == ' O ':
                    return 1
                elif counter3 == 3 and board[i][j] == ' X ':
                    return -1
            else:
                counter3 = 0 #다르면 카운터 초기화
            i-=2 #다음칸으로 이동
            j+=2
    #4. 우하향 방향 대각선 검사
    point2 = [(i,1) for i in range(1,6,2)] + [(1,j) for j in range(3,8,2)] #시작점 모음
    for row,col in point2: #시작점중 하나에 대해 진행
        counter4=0 #카운터 초기화
        i,j=row,col
        while i+2 <= 11 and j+2 <= 13: #보드의 경계에 이를때까지 작동
            if board[i][j] == board[i+2][j+2] and board[i][j] != '   ':
                counter4 += 1 #같으면 카운터에 더함
                if counter4 == 3 and board [i][j] == ' O ':
                    return 1
                elif counter4 == 3 and board[i][j] == ' X ':
                    return -1
            else:
                counter4 = 0 #다르면 카운터 초기화
            i+=2 #다음칸으로 이동
            j+=2
    return 0
def simulate_drop(board): #특정 열에 가상으로 돌을 떨어뜨려 승리 가능성을 판단합니다.
    candidate_win=[] #컴퓨터 즉시 승리 가능 수들의 리스트
    candidate_lose=[] #플레이어 즉시 승리 가능 수들의 리스트
    for col in range(7):
        if board[1][2*col+1]!='   ': #만일 맨위가 차있다면 -> 
            continue #다음 col에 대해서 실행
        testboard=copy.deepcopy(board) #시뮬레이션 위한 가상의 보드 복사     
        drop_stone(testboard,col,'X') #돌 한번 떨궈보기
        R1=check_win(testboard)
        if R1==-1: #컴퓨터가 즉시 이기면
            candidate_win.append(col) #추가
            continue #밑의 코드 무시하고 다음 col에 대해 작동

        testboard=copy.deepcopy(board) #컴퓨터가 즉시 이기지 않음 -> 다시 가상 보드 세팅
        drop_stone(testboard,col,'O') #돌 떨구기
        R2=check_win(testboard)
        if R2==1: #상대가 즉시 이기면
            candidate_lose.append(col) #추가
    if candidate_win: #컴퓨터 즉시 승리 가능 수 존재
        return random.choice(candidate_win) #그중 뽑기
    elif candidate_lose: #컴퓨터 승리 불가능 & 플레이어 즉시 승리 가능
        return random.choice(candidate_lose) #그중 뽑기
    else: #둘다 아니면
        random_available_number_list=[i for i in range(7) if board[1][2*i+1] == '   '] #가득 안찬 열 들의 목록
        return random.choice(random_available_number_list) #중 하나 랜덤으로 뽑음

def game(board,difficulty,game_record):
    while True:
        column_selected=input("Player's turn (O) - choose a column (0-6 or Q to quit): ") #플레이어로부터 열 혹은 중단 여부 입력 받음
        if column_selected == 'Q': #플레이어가 중단 하면
            file_saving(game_record,difficulty) #파일에 게임보드와 게임 난이도 저장하고
            print("File saved.\n") #저장 완료 메시지 출력 후
            return 'Q' #함수 탈출
        elif column_selected in ['0','1','2','3','4','5','6'] and board[1][2*int(column_selected)+1] == '   ': #플레이어가 정상적인 열 입력하면
            drop_stone(board,column_selected,'O') #그 열에 돌 떨어뜨림
            game_record+="{0} ".format(column_selected) #게임 기록에 해당 행동을 기록(열)
            print() #줄 바꿈
            print_board(board) #바뀐 현재 게임 보드 출력
            R=check_win(board) #게임 결과 검사
            q=winner_decision(R,board) 
            if q == 'Q': #결판(승리,실패,무승부)나면
                return 'Q' #결판 신호(Q) 리턴하면서 함수 탈출
            print("Computer's turn (X)", end=' ') #컴퓨터 차례임을 출력
            time.sleep(1) #1초 쉬기
            computer_selection=computer_move_easy(board) if difficulty=='1' else computer_move_normal(board) #난이도에 따라 컴퓨터가 행동
            game_record+='{0} '.format(computer_selection) #게임 기록에 컴퓨터 기록 저장
            R=check_win(board) #게임 결과 검사
            q=winner_decision(R,board)
            if q == 'Q': #결판(승리,실패,무승부)나면
                return 'Q'#결판 신호(Q) 리턴하면서 함수 탈출
        else:
            print("Wrong Input!\n") #잘못된 입력시 오류메시지 출력

def start_game(board=0, difficulty=0,game_record=0): #난이도 선택, 턴 진행, 종료 판정 등 전체 게임을 진행합니다.
    if difficulty == '1': #난이도가 쉬움일때
        if board==0: #만일 게임보드가 0, 즉 처음 시작이라면
            game_record="moves=" #게임 기록 시작하기
            board=initialize_board() #빈보드 생성
        else:
            print("Game loaded. (Mode: Easy)") #게임 불러오기 성공 안내 문구 출력 | 난이도: 쉬움
        print("\n<< Start Game: Difficulty = Easy >>") #게임 시작 문구 | 난이도: 쉬움
        print_board(board)  # 현재 보드 출력
        R = check_win(board) #혹시나 불러온 게임이 이미 결판이 났는지를 검사하기 위해
        q = winner_decision(R, board) # check_win()과 winner_decision()을 통해
        if q == 'Q': #이미 결판 났으면 게임 진행하지 않음
            return 'Q'
        q=game(board,difficulty,game_record) #그런게 아니라면 game()을 통해 게임 진행
        if q== 'Q': #게임 결판났거나 저장을 통해 게임 중단시 게임 진행 멈추고 Q반환
            return 'Q' 

    elif difficulty == '2': #난이도가 보통일 때
        if board==0:
            board=initialize_board()
            game_record="moves="
        else:
            print("Game loaded. (Mode: Normal)") #게임 불러오기 성공 안내 문구 출력
        print("\n<< Start Game: Difficulty = Normal >>") #게임 시작 문구
        print_board(board)
        R = check_win(board)
        q = winner_decision(R, board)
        if q == 'Q':
            return 'Q'
        q=game(board,difficulty,game_record)
        if q == 'Q':
            return 'Q'

def main():
    while True:
        print("[Connect Four]") # 선택창 출력
        print("---------------------------------------")
        print(" 1. New Game 2. Load Game 3. Exit")
        print("---------------------------------------")
        while True: # menu 선택
            menu=input("Select a menu: ")
            if menu in ['1','2','3']:  #1,2,3 중 하나를 제대로 입력하면 밑의 코드 실행하도록 반복문 break
                break
            print('Wrong Input!\n') #잘못된 값 입력 시 제대로 된 값을 입력받을 때까지 반복
        if menu == '1':
            while True:
                difficulty_selected = input("Select difficulty (1: Easy, 2: Normal): ") #난이도 선택
                if difficulty_selected not in ['1', '2']: #1,2 외의 입력값이 주어지면
                    print('Wrong Input!\n') #오류 메시지 출력 후
                    continue #다시 반복문으로 돌아가 난이도 선택 입력 받음
                q=start_game(difficulty=difficulty_selected) #제대로 된 난이도 입력값이 주어지면 게임을 시작. 난이도는 아까 입력받은 것대로
                if q == 'Q': #start_game의 리턴값이 Q, 즉 게임이 결판이 나면 while문 탈출 -> 다시 메뉴 선택창으로 복귀
                    break
        elif menu == '2':
            board0=initialize_board() #먼저 빈 보드 생성
            mode_saved,board_saved,gamerecord=load_game(board0) #빈보드를 바탕으로 저장 내용을 변수에 할당
            if mode_saved == 'n': #파일이 존재하지 않을때 다시 메뉴창으로 복귀
                continue
            else:    
                q=start_game(board=board_saved,difficulty=mode_saved,game_record=gamerecord) #위에서 할당된 변수를 바탕으로 게임 진행
                if q == 'Q': #게임 결판나면 메뉴창으로 복귀
                    continue
        elif menu == '3': #Exit 선택시
            print("Program ended. Bye!") #프로그램 종료 메시지 출력 후
            break #main의 전체 while문을 탈출. 프로그램 종료
main()