import random
# ----------------------------------------------------------------------
# 데이터 상수
# ----------------------------------------------------------------------

ENHANCEMENT_DATA = {
    # 레벨: {이름, 강화비용, 성공확률, 판매가격, 재료레벨}
    0: {"name": "1학년 포닉스", "cost": 10, "rate": 0.95, "sell": 0,   "material_level": None},
    1: {"name": "2학년 포닉스", "cost": 50, "rate": 0.90, "sell": 30,  "material_level": None},
    2: {"name": "3학년 포닉스", "cost": 100, "rate": 0.85, "sell": 500,  "material_level": None},
    3: {"name": "4학년 포닉스", "cost": 150, "rate": 0.75, "sell": 1500, "material_level": None},
    4: {"name": "석사 포닉스", "cost": 220, "rate": 0.65, "sell": 2500, "material_level": 3}, # 3 (4학년) 필요
    5: {"name": "박사 포닉스", "cost": 300, "rate": 0.45, "sell": 5000, "material_level": 4}, # 4 (석사) 필요
    6: {"name": "교수 포닉스", "cost": 450, "rate": 0.30, "sell": 10000, "material_level": 5}, # 5 (박사) 필요
    7: {"name": "총장 포닉스", "cost": 0,  "rate": 0.0,  "sell": 2790000, "material_level": None},  # 최종 레벨
}

LEVEL_COLORS = [
    '\033[2m',                          # 0강: 1학년 (흐릿하게)
    '\033[96m',                         # 1강: 2학년 (시안)
    '\033[96m\033[1m',                  # 2강: 3학년 (밝은 시안)
    '\033[92m\033[1m',                  # 3강: 4학년 (밝은 녹색)
    '\033[93m',                         # 4강: 석사 (노란색)
    '\033[93m\033[1m',                  # 5강: 박사 (밝은 노란색)
    '\033[95m',                         # 6강: 교수 (마젠타)
    '\033[95m\033[1m'                   # 7강: 총장 (밝은 마젠타)
]

# ----------------------------------------------------------------------
# 아이템 클래스
# ----------------------------------------------------------------------


class BaseItem:  # 기본적인 아이템 클래스
    def __init__(self, name, description, price, item_id):
        self.name = name
        self.description = description
        self.price = price
        self.item_id = item_id

    def __str__(self):
        return f"[{self.name}] (가격: {self.price}G)"


class ProtectionScroll(BaseItem):  # 아이템 클래스를 상속 받은 파괴 방지권 클래스
    # 파괴 방지권
    def __init__(self):
        super().__init__(
            name="파괴 방지권",
            description="[석사 포닉스 이상] '다음 1회' 강화 시도 시, 실패해도 파괴되지 않습니다.",
            price=1500,
            item_id="protection_scroll"
        )


class SuccessScroll(BaseItem):  # 아이템 클래스를 상속 받은 확률 증가권 클래스
    # 강화 확률 증가권
    def __init__(self):
        super().__init__(
            name="확률 증가권 (10%)",
            description="'다음 1회' 강화 시도 시, 성공 확률을 10% 올려줍니다.",
            price=1000,
            item_id="success_scroll"
        )

# ----------------------------------------------------------------------
# 포닉스 클래스
# ----------------------------------------------------------------------


class BasePonix:
    # 모든 포닉스의 기본 설계도 (추상 부모 클래스)

    def __init__(self, level=0):
        self.level = level
        # 현재 단계 명칭(석사 포닉스, ...)
        self.name = '' #단계 이름: 초기값 빈문자열
        self.sell_price = 0  # 판매 가격: 초기값=0
        self.update_stats(self.level) # 초기화 시점에 update_stats 메서드 호출하여 상태 갱신

    def update_stats(self, level=0):  # 강화 성공/실패 시 호출 포닉스 내부 변수 변경, #ENHANCEMENT_DATA에서 갱신
        self.level = level 
        self.name = ENHANCEMENT_DATA[self.level]["name"]
        self.sell_price = ENHANCEMENT_DATA[self.level]["sell"]

    def enhance_attempt(self):
        raise NotImplementedError("자식 클래스에서 이 메서드를 구현해야 합니다.")

    def __str__(self):  # 현재 단계에 따라서 포닉스 출력 글자 색 반영해서 문자열 반환, LEVEL_COLORS 변수 사용
        return f'{LEVEL_COLORS[self.level]}[+{self.level}] {self.name}\033[0m (판매가: {self.sell_price}G)'


class UndergradPonix(BasePonix):  # 0강 ~ 3강 포닉스
    def __init__(self, level=0):
        super().__init__(level)
        self.cost = ENHANCEMENT_DATA[self.level]["cost"]
        self.rate = ENHANCEMENT_DATA[self.level]["rate"]

    def enhance_attempt(self, money, item_list):
        if self.cost > money:  # 1. 강화 비용 충분한지 체크
            print("골드가 부족합니다.")
            return False
        if item_list:
            if "확률 증가권 (10%)" in item_list:
                self.rate += 0.1
        print(f'\n... {self.name} 강화 시도 (비용: {self.cost}G, 확률: {int(100*self.rate)}%) ...')
        if random.random() < self.rate:  # 2. 확률에 따라 강화 성공/실패 여부 판정
            self.level += 1
            self.update_stats(self.level)  # 3. update_stats() 호출해서 상태 갱신
            print(f"강화 성공! '{self.name}'(이)가 되었습니다! ")
            return True
        else:
            print('강화 실패... 2단계 하락합니다.')
            self.level -= 2
            if self.level < 0:
                self.level = 0
            self.update_stats(self.level)  # 3. update_stats() 호출해서 상태 갱신
            return True


class GradPonix(BasePonix):  # 4강 ~ 7강 포닉스
    def __init__(self, level=0):
        super().__init__(level)
        self.cost = ENHANCEMENT_DATA[self.level]["cost"]  # 강화 비용 변수
        self.rate = ENHANCEMENT_DATA[self.level]["rate"]  # 강화 확률 변수
        # 요구 재료 레벨 변수
        self.material_level = ENHANCEMENT_DATA[self.level]["material_level"]
        self.defense = False  # 파괴 방지권 여부 반영하는 변수

    def enhance_attempt(self, money, warehouse, item_list):
        # 1. 창고에 해당 단계 포닉스가 있는지 확인
        if not warehouse.has_ponix(self.material_level):
            print(f"재료가 부족합니다! 창고에 '{ENHANCEMENT_DATA[self.material_level]["name"]}'이(가) 필요합니다.")
            return False
        if self.cost > money:  # 2. 강화 비용 충분한지 체크
            print("골드가 부족합니다.")
            return False
        if item_list:
            if "확률 증가권 (10%)" in item_list:
                self.rate += 0.1  # 3.확률 증가권 있으면 반영
            if "파괴 방지권" in item_list:
                self.defense = True  # 파괴 방지권 있으면 반영
        print(f'\n... {self.name} 강화 시도 (비용: {self.cost}G, 확률: {int(100*self.rate)}%) ...')
        print(f"재료로 '{ENHANCEMENT_DATA[self.material_level]["name"]}'(을)를 사용합니다. (남은 개수: {warehouse.materials[ENHANCEMENT_DATA[self.material_level]["name"]]-1})")
        warehouse.remove_ponix(self.material_level)
        if random.random() < self.rate:  # 3. 강화 성공/실패 판정
            self.level += 1  # 4. 성공: +1단계
            self.update_stats(self.level)  # 6. 결과 적용 후 update_stats() 호출
            print(f"강화 성공! '{self.name}'(이)가 되었습니다! ")
            return True
        else:  # 5. 실패: 기본은 파괴(0강으로 리셋)
            if self.defense:  # 단 파괴 방지권이 있으면 파괴되지 않고 현 단계 유지
                print("파괴 방지권이 발동하여 포닉스를 보호했습니다!")
                print("강화에 실패했지만 포닉스는 무사합니다.")
                return True
            else:
                print('강화 실패! 포닉스가 파괴되었습니다.')
                print("새 '새내기 포닉스'로 다시 시작합니다.")
                self.level = 0
                self.update_stats(self.level)  # 6. 결과 적용 후 update_stats() 호출
                return True
# ----------------------------------------------------------------------
# 창고 클래스
# ----------------------------------------------------------------------


class Warehouse:  # 4학년, 석사 박사 포닉스만 보관 가능
    def __init__(self):  # 각각 몇개 있는지 저장.
        self.materials = {}

    def add_ponix(self, ponix):  # 현재 강화 대상 포닉스를 보관(추가)하는 함수
        name = ponix.name
        self.materials[name] = self.materials.get(name, 0) + 1

    def has_ponix(self, level):  # 특정 강화 단계의 포닉스가 존재하는지 확인하는 함수
        name = ENHANCEMENT_DATA[level]["name"]
        return self.materials.get(name, 0) > 0  # 존재하면 True, 없으면 False 반환

    def remove_ponix(self, level):  # 강화 재료로 사용되는 포닉스 하나를 차감하는 함수
        name = ENHANCEMENT_DATA[level]["name"]
        if name in self.materials:
            self.materials[name] -= 1
            if self.materials[name] == 0:
                del self.materials[name]
        else:
            print('강화 재료 부족')  # 만약 재료가 없을 경우에 대한 예외 처리

    def __str__(self):
        if self.materials:
            warehouse_list = ''
            for name, number in self.materials.items():
                level = None
                for lev, data in ENHANCEMENT_DATA.items():
                    if data["name"] == name:
                        level = lev
                        break
                warehouse_list += f'  -{name} ({level} 강): {number}개\n'
            warehouse_list = warehouse_list[:-1]
            return '--- 창고 / 인벤토리 ---\n' + warehouse_list  # 현 창고 상황에 출력을 위한 문자열 반환
        else:
            return '--- 창고 (비어있음) ---'


# ----------------------------------------------------------------------
# 상점 클래스
# ----------------------------------------------------------------------

class Store:
    # 아이템을 판매하는 상점 클래스
    def __init__(self):  # 판매 가능한 아이템 목록
        self.catalog = [
            ProtectionScroll(),  # ProtectionScroll: 4강(석사) 이상부터 구매 가능
            SuccessScroll()  # SuccessScroll: 단계 제한 없음
        ]

    def show_catalog(self, money, ponix):  # 상점에서 판매하고 있는 아이템 목록을 출력
        print('\n==================================================')
        print(f'--- 상점 (보유 골드: {money}G) ---')
        if ponix.level < 4:  # 현재 강화 대상 포닉스가 0~3강일 때는 파괴 방지권을 구매할 수 없다고 출력.
            print(" 1. [파괴 방지권] (석사 포닉스(4강)부터 구매 가능)")
        else:
            print(" 1. [파괴 방지권] (가격: 1500G)")
            print("    [석사 포닉스 이상] '다음 1회' 강화 시도 시, 실패해도 파괴되지 않습니다.")
        print(" 2. [확률 증가권(10%)] (가격: 1000G)")
        print("    '다음 1회' 강화 시도 시, 성공 확률을 10% 올려줍니다.")
        print("--------------------------------------------------")
        print(' 3. 상점 나가기')
        print('==================================================')

    def buy_item(self, selection, money, ponix,):  # 플레이어가 선택한 아이템을 구매하고 적용
        if selection == '1':
            if ponix.level < 4:  # [파괴 방지권]: 현재 강화 대상이 4강 이상인 경우만 구매 가능
                print("'석사 포닉스'(4강) 이상이 되어야 구매할 수 있습니다.")
                return None
            elif money < 1500:
                print("골드가 부족합니다.")  # - 보유 골드가 아이템 가격보다 적으면 “골드가 부족합니다.” 출력
                return None
            else:
                print("'파괴 방지권'(을)를 구매했습니다. (다음 강화 시 자동 적용됩니다)")
                return 1
        # [확률 증가권]: 다음 1회 강화 시 성공 확률을 10% 증가시킴 (합 연산으로 적용됨. 예: 80% -> 90%)
        elif selection == '2':
            if money < 1000:
                print("골드가 부족합니다.")  # - 보유 골드가 아이템 가격보다 적으면 “골드가 부족합니다.” 출력
                return None
            else:
                print("'확률 증가권 (10%)'(을)를 구매했습니다. (다음 강화 시 자동 적용됩니다)")
                return 2

    # 상점 기능을 총괄하는 함수로 플레이어 입력을 받아 아이템 구매 및 상점 나가기 기능을 수행
    def enter_store(self, money, ponix, product):
        while True:
            self.show_catalog(money, ponix)
            selection = input('선택: ')
            if selection == '3':
                return 'Q'
            elif selection == '1' or selection == '2':
                # 아이템 구매 시도시 이미 구매 내역에 존재하면 이미 존재함을 알리는 메시지 먼저 출력
                if self.catalog[int(selection)-1].name in product:
                    print(
                        "이미 " + self.catalog[int(selection)-1].name + "이 적용되어 있습니다.")
                    return None  # return 함으로써 buy_item 메서드 호출 전에 중지
                item_number = self.buy_item(selection, money, ponix)
                return item_number
            else:
                print("잘못된 입력입니다.")
                continue
# ----------------------------------------------------------------------
# 플레이어 클래스
# ----------------------------------------------------------------------


class Player:
    def __init__(self, player_name):
        self.player_name = player_name  # 플레이어 이름 변수
        self.money = 200  # 플레이어 보유 골드 변수(초기값 = 200)
        self.warehouse = Warehouse()  # 창고 클래스 인스턴스
        self.store = Store()  # 상점 클래스 인스턴스
        self.Ponix = UndergradPonix()  # 현재 강화 대상 포닉스 클래스 인스턴스, 초기값: 학부 클래스의 새내기 포닉스
        self.product = []  # 상점 구매 내역을 저장하는 변수

    # 포닉스 클래스에 존재하는 강화 매서드를 호출하여 전반적인 강화를 관리하는 함수입니다.
    def enhance(self, item_list):
        if self.Ponix.level <= 3:  # 0~3강 강화 담당
            # 학부(Undergrad) 클래스의 enhance_attempt 메서드를 호출하여 강화 시도
            if self.Ponix.enhance_attempt(self.money, item_list):
                self.money -= self.Ponix.cost  # 강화가 정상적으로 수행된 경우 보유 골드에서 강화 비용을 차감
        else:  # 4강 이상 강화 담당
            # 학부 졸업(Grad) 클래스의 enhance_attempt 메서드를 호출하여 강화 시도
            if self.Ponix.enhance_attempt(self.money, self.warehouse, item_list):
                self.money -= self.Ponix.cost

    def store_current_ponix(self):  # 현재 강화 대상인 포닉스를 창고에 보관하는 함수(3~5강만 보관 가능)
        if 3 <= self.Ponix.level <= 5:
            self.warehouse.add_ponix(self.Ponix)
            print(f'{self.Ponix.name}을(를) 창고에 보관했습니다. (현재: {self.warehouse.materials[self.Ponix.name]}개)')
            # 보관 후에는 새로운 0강(1학년 포닉스)가 현재 강화 대상 포닉스로 리필.
            self.Ponix = UndergradPonix()
            print("새 '새내기 포닉스'로 강화를 시작합니다.")
        else:
            print('이 포닉스는 보관할 수 없습니다.')

    def sell_current_ponix(self):  # 현재 강화 대상인 포닉스를 판매하여 골드를 버는 함수
        if self.Ponix.level > 0:  # 0강 초과만 판매하도록 조건문 사용
            self.money += self.Ponix.sell_price
            print(f"'{self.Ponix.name}'(을)를 {self.Ponix.sell_price}에 판매했습니다. (현재 골드: {self.money}G)")
            self.Ponix = UndergradPonix()  # 판매 후 새로운 0강 포닉스 리필
            print("새 '새내기 포닉스'로 다시 시작합니다.")
        else:
            print("'새내기 포닉스'는 판매할 수 없습니다. 먼저 강화를 시도하세요")

    def show_status(self):  # 플레이어의 현재 상태를 출력합니다.
        print('\n==================================================')
        print(f'플레이어: {self.player_name} | 보유 골드: {self.money}G')  # 이름, 보유 골드
        print(self.warehouse)  # 창고의 보관 현황
        if self.product:  # 만일 구매한 아이템이 있는 경우 이를 ,로 연결한 문자열로 바꾸어 표기
            item_list = ''
            for item in self.product:
                item_list = item_list + item + ', '
            item_list = item_list[:-2]
            print(f'적용 중인 아이템: {item_list}')  # 적용 중인 아이템
        print(f'\n▶ 현재 강화 대상: {str(self.Ponix)}')  # 현재 강화 중인 포닉스
        print('==================================================\n')

    def play(self):  # 텍스트 UI 출력을 포함하여 게임의 진행을 담당하는 함수
        while True:
            self.show_status()  # 먼저 현재 상태 출력
            if self.Ponix.level == 7:  # 만일 현재 강화중인 포닉스가 최종 상태에 도달하면 break
                print("축하합니다! 마침내 '총장 포닉스' 강화에 성공했습니다!")
                break
            print('무엇을 하시겠습니까?')  # 아니라면 계속 게임 진행
            if self.Ponix.level > 3:
                if "확률 증가권 (10%)" in self.product:  # 확률 증가권이 존재한다면 증가된 확률을 반영하여 1번(강화 메뉴) 안내
                    if "파괴 방지권" in self.product:
                        print(f' 1. 강화 시도 (비용: {ENHANCEMENT_DATA[self.Ponix.level]["cost"]}G, 확률: {int(100*ENHANCEMENT_DATA[self.Ponix.level]["rate"])}%, 재료: {ENHANCEMENT_DATA[self.Ponix.material_level]["name"]}) (파괴방지, 확률+10% 적용됨)')
                    else:
                        print(f' 1. 강화 시도 (비용: {ENHANCEMENT_DATA[self.Ponix.level]["cost"]}G, 확률: {int(100*ENHANCEMENT_DATA[self.Ponix.level]["rate"])}%, 재료: {ENHANCEMENT_DATA[self.Ponix.material_level]["name"]}) (확률+10% 적용됨)')
                elif "파괴 방지권" in self.product:
                    print(f' 1. 강화 시도 (비용: {ENHANCEMENT_DATA[self.Ponix.level]["cost"]}G, 확률: {int(100*ENHANCEMENT_DATA[self.Ponix.level]["rate"])}%, 재료: {ENHANCEMENT_DATA[self.Ponix.material_level]["name"]}) (파괴방지 적용됨)')
                else:  # 존재하지 않는다면 원래 확률 반영하여 1번(강화 메뉴) 안내
                    print(f' 1. 강화 시도 (비용: {ENHANCEMENT_DATA[self.Ponix.level]["cost"]}G, 확률: {int(100*ENHANCEMENT_DATA[self.Ponix.level]["rate"])}%, 재료: {ENHANCEMENT_DATA[self.Ponix.material_level]["name"]})')
            else:
                if "확률 증가권 (10%)" in self.product:  # 확률 증가권이 존재한다면 증가된 확률을 반영하여 1번(강화 메뉴) 안내
                    print(f' 1. 강화 시도 (비용: {ENHANCEMENT_DATA[self.Ponix.level]["cost"]}G, 확률: {int(100*ENHANCEMENT_DATA[self.Ponix.level]["rate"])}%) (확률+10% 적용됨)')
                else:  # 존재하지 않는다면 원래 확률 반영하여 1번(강화 메뉴) 안내
                    print(f' 1. 강화 시도 (비용: {ENHANCEMENT_DATA[self.Ponix.level]["cost"]}G, 확률: {int(100*ENHANCEMENT_DATA[self.Ponix.level]["rate"])}%)')
            print(' 2. 현재 포닉스 보관 (3-5 강 재료 전용)')  # 2번 메뉴 소개
            print(' 3. 상점 방문')  # 3번 메뉴 소개
            print(' 4. 현재 포닉스 판매하기')  # 4번 메뉴 소개
            print(' 5. 게임 종료')  # 5번 메뉴 소개
            menu = input('> ')  # 사용자로부터 메뉴 입력받음
            if menu == '1':
                if self.product:  # 구매한 아이템이 있는 경우
                    if "확률 증가권 (10%)" in self.product:  # 구매한 아이템에 확률 증가권이 있으면
                        # 확률 증가권이 적용됨을 알림
                        print("확률 증가권의 효과가 적용됩니다! (확률 +10%)")
                    if "파괴 방지권" in self.product:  # 구매한 아이템에 파괴 방지권이 있으면
                        # 파괴 방지권이 적용됨을 알림
                        print("파괴 방지권이 이번 강화에 적용됩니다! (성공/실패 무관 1회 소모)")
                self.enhance(self.product)  # enhance 메서드를 통해 강화 수행
                if self.Ponix.level < 4: # 강화 후 레벨이 0~3이라면
                    self.Ponix = UndergradPonix(self.Ponix.level) # 현재 레벨에 맞는 학부생 포닉스로 인스턴스 재설정
                else: #아니라면
                    self.Ponix = GradPonix(self.Ponix.level) # 현재 레벨에 맞는 학부 졸업생 포닉스로 인스턴스 재설정
                self.product = []  # 강화를 시도했으므로 구매한 아이템 초기화
                continue
            elif menu == '2':
                self.store_current_ponix()  # store_current_ponix 메서드를 호출하여 현재 포닉스 저장
                continue
            elif menu == '3':
                while True:
                    # store클래스의 인스턴스의 enter_store 메서드를 호출하여 그 상점에 진입. 이후 해당 메서드가 반환하는 신호를 selected_signal 변수에 할당
                    selected_signal = self.store.enter_store(self.money, self.Ponix, self.product)
                    if not selected_signal:  # 유의미한 신호가 없다면 다시 상점 진입
                        continue
                    if selected_signal == 'Q':  # 상점 나가기 선택시 나가도록 구현
                        print("상점에서 나옵니다.")
                        break
                    else:  # 정상적인 상황에서 아이템 구매시 
                        # 보유 금액에서 가격만큼을 차감
                        self.money -= self.store.catalog[selected_signal-1].price
                        # 구매 리스트에 해당 항목의 이름 추가
                        self.product.append(
                            self.store.catalog[selected_signal-1].name)
            elif menu == '4':
                self.sell_current_ponix()  # sell_current_ponix 메서드를 호출하여 현재 포닉스 판매
                continue
            elif menu == '5':
                print("게임을 종료합니다.")
                break  # 게임 종료 메시지 출력 후 break
            else:
                # 잘못된 입력임을 알리고 continue를 통해 while문을을 통해 다시 메뉴로 돌아옴
                print("잘못된 입력입니다.")
                continue


# ----------------------------------------------------------------------
# 게임 실행 (프로그램 시작점)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("="*50)
    print(f"포닉스 강화하기 (2025년 2학기 ASSN3, 20250152)")  # 자신의 학번으로 변경할 것!
    print("="*50)
    player_name = input("플레이어의 이름을 입력하세요: ")
    player = Player(player_name)
    player.play()
