import random #랜덤한 말들의 전진을 위한 random 모듈 불러오기
import time #경주 결과를 1초 간격으로 쉬었다가 보여주기 위한 time 모듈 불러오기

def select_menu(deposit, loan): #main()
    while True: # 종료를 제외한 모든 작업들(예외 처리, 대출, 상환, 경마) 이후 항상 메뉴 선택창이 떠야하므로 break전까지 항상 코드를 반복하는 While True 문
        print("[예금: {0}, 대출: {1}]".format(deposit,loan)) #변동하는 예금(deposit)과 대출(loan)을 메뉴 선택창에서 항상 표시. 
        print("----------------------------")
        print("1.대출 2.상환 3.경마 4.종료") 
        print("----------------------------")
        menu_selection=input("메뉴 선택: ") #메뉴 선택
        if menu_selection == '1':
            deposit, loan = take_loan(deposit, loan) #take_loan()에서 deposit과 loan의 변경 사항을 return값으로 받아 반영

        elif menu_selection == '2':
            deposit, loan = repay(deposit, loan) #repay()에서 상환한 금액에 따른 deposit과 loan의 변경 사항을 return값으로 받아 반영

        elif menu_selection == '3':
            deposit = run_race(deposit) #run_race()를 통해 얻거나 잃은 금액을 deposit에 return값으로 받아 반영

        elif menu_selection == '4':
            exit_game(deposit,loan) #deposit과 loan의 차이를 반영한 최종 금액을 바탕으로 종료 메시지 출력
            break #exit_game() 실행 이후 break를 통해 while 문에서 빠져나와 게임을 종료

        else:
            print("오류: 1~4 중 하나의 숫자를 입력하세요.\n") #메뉴 선택 시 1~4가 아닌 경우 오류 메시지를 출력, 이후 다시 while문 재개

def take_loan(deposit, loan): #대출을 수행하는 함수. deposit과 loan이라는 매개변수의 값을 바꾸어 return한다.
    loan_taken=int(input("대출 금액: ")) #대출할 금액 입력
    deposit+=loan_taken # 29~30 대출한 금액만큼 예금과 대출 증가
    loan+=loan_taken
    print("대출 완료! 예금: {0}, 대출: {1}\n".format(deposit,loan)) #대출 완료 문구 출력, 현재 예금 및 대출 표시
    return deposit, loan # 변한 예금과 대출 반환

def repay(deposit, loan): #상환을 수행하는 함수. deposit과 loan이라는 매개변수의 값을 바꾸어 return한다.
    loan_repaid=int(input("상환 금액:")) #상환할 금액 입력
    if loan_repaid>deposit:
        print("오류: 예금이 부족하여 상환할 수 없습니다.\n") #상환 금액이 예금보다 클 경우 상환이 불가능하므로 예금과 대출 변동 없이 오류메시지만 출력
    elif loan_repaid>loan:
        print("오류: 상환 금액이 은행 대출보다 많습니다.\n") #상환 금액이 대출보다 클 경우 역시 상환이 불가능하므로 예금과 대출 변동 없이 오류메시지만 출력
    else: #정상적인 상환 금액이 들어오면
        deposit-=loan_repaid #예금에서 상환액만큼 차감
        loan-=loan_repaid #대출에서도 상환액만큼 차감
        print("상환 완료! 예금: {0}, 대출: {1}\n".format(deposit,loan)) #상환 완료 문구 출력, 현재 예금 및 대출 표시
    return deposit, loan #변한 예금과 대출 반환

def run_race(deposit): #경주를 실행하는 함수, 예금을 매개변수로 경주 결과에 따라 예금을 업데이트하고 반환한다.
    horse_selected=input("경주마 선택(1~3): ") #베팅할 경주마의 번호를 입력받음
    if horse_selected!='1' and horse_selected!='2' and horse_selected!='3':#베팅할 경주마의 번호가 1,2,3이 아닐 때 오류 메시지 출력
        print("오류: 1~3 중 하나의 숫자를 입력하세요.\n")
        return deposit #바로 deposit을 반환하여 함수를 중단
    bet_amount=int(input("베팅 금액: ")) #베팅 금액 입력받음
    if bet_amount>deposit: #베팅 금액이 예금보다 크면 오류메시지를 출력
        print("오류: 예금이 부족하여 베팅할 수 없습니다.\n")
        return deposit #바로 deposit을 반환하여 함수를 중단
    winner, prediction =show_horse_run(horse_selected) # 반환되는 경주마의 번호와 예측 성사 여부를 winner와 prediction이라는 지역변수를 통해 받음
    print("\n[경주 결과] {0}번 말이 우승했습니다!".format(winner)) #우승한 말의 번호와 함께 경주 결과 출력
    if prediction == True: #예측이 성공하면
        deposit+=2*bet_amount #원금+베팅금액의 2배 얻으므로 예금에서 베팅 금액 차감 없이 그 상태에서 베팅금액의 2배를 예금에 더함
        print("승리! {0}원을 얻었습니다\n".format(3*bet_amount)) #얼마 얻었는지 베팅 결과와 함께 출력
    elif prediction==False: #예측이 실패하면
        deposit-=bet_amount #베팅 실패이므로 예금에서 원금만큼 차감
        print("패배! {0}원을 잃었습니다\n".format(bet_amount)) #얼마 잃었는지 베팅 결과와 함께 출력
    return deposit #변동된 예금을 반환

def exit_game(deposit,loan): #예금과 대출을 매개변수로 종료 메시지를 출력하는 함수
    print("최종 금액: {0}".format(deposit-loan)) #예금에서 대출을 빼어 최종 금액을 출력
    print("게임을 종료합니다. 감사합니다!") #종료 메시지
    
def show_horse_run(horse_selected): #경주 과정을 보여주는 함수,선택한 말의 번호를 받아서 예측 결과와 우승 말의 번호를 반환해준다.
        horse_positions=[0,0,0] #3마리의 말들의 위치를 각각 리스트로 표현, i번째 요소는 i+1번 경주마를 의미한다.
        print("경주 시작!")
        while True: #경주는 어느 말의 위치가 20이 될 때까지 지속되어야 하기에 while True를 통해 break전까지 함수가 반복문이 계속되도록 설정
            for i in range(3): #3가지 말들의 위치를 바꾸기 위해 3번 위치 업데이트를 진행
                horse_positions[i]+=random.randint(1,5) #1부터 5중 랜덤한 수치만큼 해당 요소에 덧셈을 진행
                if horse_positions[i]>20:# 만일 20을 넘어갈 경우 20으로 수치를 조정; 자칫 끝없이 경마를 진행하는 것을 방지하기 위함
                    horse_positions[i]=20
                print("{0}번 말: ".format(i+1)+"■"*(horse_positions[i])+"□"*(20-horse_positions[i])) #i+1번 말을 리스트의 i번째 요소, 즉 i+1번 말의 위치 만큼 ■를 나머지는 □를 표시하여 제시.
            print("--------------------------------------------------")
            time.sleep(1) #모든 말에 대해서 위치를 표시하고 나면 1초 쉬기. 결승선에 도달한 말이 없으면 while에 의한 반복으로 1초 쉰 다음 말들의 바뀐 위치가 출력됨. 결승선에 도달한 말이 있으면 1초 쉰뒤 이 경주 결과 계산
            if max(horse_positions)==20: #만일 세 말의 위치가 모두 표시되고 난후 한 개 이상의 말의 위치가 20일 경우
                if horse_positions.index(max(horse_positions))+1==int(horse_selected): # 선택한 경주마의 번호와 우승한 경주마의 번호, 즉 리스트의 요소 중 값이 20인 위치에다가 1을 더한 값이 같을 때 (.index는 가장 앞의 위치를 반환하기에 말이 동시에 도착해도 앞의 말을 고르지 않으면 실패이므로 말이 2개 이상인 경우와 1개인 경우를 구분할 필요가 없다.)
                    P=True #예측에 성공했으므로 P라는 지역 변수에 참을 할당
                    break #위의 while 반복문으로부터 탈출
                else:
                    P=False #예측에 실패했으므로 P라는 지역변수에 거짓을 할당
                    break #while로부터 탈출
        return horse_positions.index(max(horse_positions))+1 , P #우승한 경주마의 번호와 예측 성사 여부를 반환

select_menu(0,0) #예금과 대출이 각각 0인 상태로 게임을 시작. 위에서 잘 정의한 main 함수인 select_menu()를 실행