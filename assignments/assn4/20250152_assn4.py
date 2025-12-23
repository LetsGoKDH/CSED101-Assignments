import tkinter as tk
import random

# ---------------------------------------------------------------------
# Canvas 위에 그려지는 모든 게임 구성요소의 공통 부모 클래스
# ---------------------------------------------------------------------
class CanvasObject:
    def __init__(self, canvas):
        self._canvas = canvas

    def draw(self):
        """자식 클래스에서 반드시 구현해야 하는 메서드"""
        raise NotImplementedError("draw() must be implemented in subclass.")


# ---------------------------------------------------------------------
# 상단 메시지 배너 또는 HUD 를 나타내는 클래스
# ---------------------------------------------------------------------
class Banner(CanvasObject):
    def __init__(self, canvas, text, x, y, size=16):
        super().__init__(canvas)
        
        # 좌표, 텍스트, 폰트 크기 등을 저장
        self._x, self._y = x, y
        self._text = text
        self._size = size
        self._item_id = None  # create_text() 로 생성된 텍스트 객체 ID

    def draw(self):
        """Canvas에 텍스트 객체를 한 번만 생성"""
        self._item_id = self._canvas.create_text(self._x, self._y, text=self._text, font=("Consolas", self._size, "bold"), fill="#f1f5f9")
        # create_txt()를 통해 필요한 정보들을 담은 텍스트 객체를 생성 후 self._item_id에 저장

    def set_text(self, text):
        """배너에 표시되는 텍스트를 변경"""
        self._text = text # 변경될 텍스트를 매개변수로 받아 self._text에 저장(값 재설정)
        self._canvas.itemconfig(self._item_id, text=self._text) 
        # itemconfig를 통해 기존 객체에서 텍스트 부분만 수정


# ---------------------------------------------------------------------
# 셀 행렬에서 플레이어가 클릭하는 한 칸을 나타내는 클래스
# ---------------------------------------------------------------------
class Cell(CanvasObject):
    def __init__(self, canvas, r, c, text_color="#ffffff", rect_color="#ffffff"):   
        CELL_SIZE = 90
        GAP = 10
        MARGIN = 16
        
        super().__init__(canvas)
        # 행/열 인덱스
        self._r = r
        self._c = c

        # 좌상단 / 우하단 좌표 계산
        self._x0 = MARGIN + c * (GAP + CELL_SIZE)
        self._y0 = 106 + r * (GAP + CELL_SIZE)
        self._x1 = self._x0 + CELL_SIZE
        self._y1 = self._y0 + CELL_SIZE

        self._text_color = text_color
        self._rect_color = rect_color

        self._number = None      # 이 셀에 배정된 숫자 (없으면 None), get_number() 및 set_number()로만 접근 가능
        self._text_id = None     # 숫자 텍스트 객체 ID
        self._rect_id = None     # 사각형 객체 ID

    def draw(self):
        """숫자를 표시할 텍스트 객체와 흰색 사각형 객체를 한 번만 생성"""
        self._text_id = self._canvas.create_text((self._x0 + self._x1) / 2, (self._y0 + self._y1) / 2, text="", font=("Consolas", 28, "bold"), fill=self._text_color)
        # canvas의 create_text()를 통해 숫자를 표시할 텍스트 객체를 생성해 self._text_id에 저장
        self._rect_id = self._canvas.create_rectangle(self._x0, self._y0, self._x1, self._y1, fill=self._rect_color, state="hidden")
        # canvas의 create_rectangle()를 통해 사각형 객체를 생성해 self._rect_id에 저장

    def set_number(self, number):
        """이 셀에 배치될 숫자를 설정"""
        self._number = number

    def get_number(self):
        """이 셀에 저장된 숫자를 반환"""
        return self._number

    def show_number(self):
        """텍스트 객체에 숫자를 표시"""
        self._canvas.itemconfig(self._text_id, text=self._number) 
        # itemconfig를 통해 텍스트 객체의 빈 문자열 부분을 해당 숫자로 변경하여 표시되게 함

    def hide_number(self):
        """텍스트 객체의 내용을 빈 문자열로 바꿔 숫자 숨김"""
        self._canvas.itemconfig(self._text_id, text="") 
        # itemconfig를 통해 텍스트 객체의 숫자 텍스트 부분을 빈 문자열로 변경하여 숫자를 숨김
    
    def show_rect(self):
        """흰색 사각형의 상태를 변경하여 표시"""
        self._canvas.itemconfig(self._rect_id, state="normal")
        # itemconfig를 통해 사각형 객체의 상태를 hidden에서 normal로 변경하여 표시되게 함

    def hide_rect(self):
        """흰색 사각형의 상태를 변경하여 숨김"""
        self._canvas.itemconfig(self._rect_id, state="hidden")
         # itemconfig를 통해 사각형 객체의 상태를 normal에서 hidden으로 변경하여 표시되게 함

    def reset(self):
        """셀을 초기상태로 변경"""
        self._number = None # self._number 값 초기화
        self.hide_number() # hide_number() 호출을 통한 숫자 숨기기
        self.hide_rect() # hide_rect() 호출을 통한 사각형 숨기기

    def contains(self, x, y):
        """좌표 (x, y)가 이 셀 영역 안에 있으면 True, 아니면 False 반환"""
        if self._x0 <= x <= self._x1 and self._y0 <= y <= self._y1: # 좌표 비교를 통해 셀 영역 내부에 있는지 판단
            return True
        else:
            return False


# ---------------------------------------------------------------------
# 게임 전체를 관리하는 클래스: 화면 구성, 이벤트 처리, 라운드 진행
# ---------------------------------------------------------------------
class ChimpTestGame:
    def __init__(self, root):
        self._root = root
               
        # 게임 화면 크기, 상태, 점수 등 초기 설정
        self._width = 822
        self._height = 612

        # Canvas 생성
        self._canvas = tk.Canvas(root, width=self._width, height=self._height, bg="#1e293b")
        self._canvas.pack()

        # 게임 진행을 위한 상태 변수들
        self._state = "idle"          # "idle", "show", "input"
        self._score = 0
        self._lives = 3
        self._sequence_length = 4
        self._expect_next = 1

        # 셀 / 배너 관련 변수
        self._cells = []      # 40개의 Cell 객체
        self._sequence = []   # 이번 라운드에서 숫자가 배정된 셀들
        self._banner = None   # 상단 메시지 배너
        self._hud = None      # 점수/기회 HUD 배너

        # TODO: Banner, HUD, Cell 초기화 및 draw() 호출
        #  - self._banner = Banner(...)
        #  - self._hud = Banner(...)
        #  - 셀 5x8 생성 후 self._cells 에 추가
        self._banner = Banner(self._canvas, "Press SPACE to Start", 411, 28) # 배너 클래스의 인스턴스 생성
        self._banner.draw() # 배너 객체 생성
        self._hud = Banner(self._canvas, f"Score: {self._score} Lives: {self._lives}", 411, 58) # 배너 클래스의 인스턴스 생성
        self._hud.draw() # 배너 객체 생성
        for i in range(5): # 5x8 셀 생성
            for j in range(8):
                cell = Cell(self._canvas, i, j)
                cell.draw()
                self._cells.append(cell) # self._cells 리스트에 cell 객체들 추가
        
        # 이벤트 바인딩
        root.bind("<space>", self.start_game)
        self._canvas.bind("<Button-1>", self.on_click)

    # -----------------------------------------------------------------
    # 아래 모든 메서드는 과제 문서를 참고하여 직접 구현합니다.
    # -----------------------------------------------------------------
    def update_hud(self):
        """현재 점수와 남은 기회를 HUD 배너에 반영"""
        self._hud.set_text(f"Score: {self._score} Lives: {self._lives}") # HUD 텍스트 업데이트
   
    def start_game(self, event): 
        """게임 시작 또는 재시작 (idle 상태에서만 동작)"""
        if self._state == "idle": # idle 상태일 때만 실행
            self._score = 0 # 점수 초기화
            self._lives = 3 # 기회 초기화
            self._sequence_length = 4 # 시퀀스 길이 초기화
            self._expect_next = 1 # 기대 숫자 초기화
            self.update_hud() # HUD 갱신
            self.start_round() # 첫 라운드 시작

    def start_round(self):
        """새 라운드를 시작하고 숫자를 1초 보여준 뒤 input 단계로 넘김"""
        self.build_sequence() # 숫자 시퀀스 생성 및 셀에 배정
        self._state = "show" # 상태를 show로 변경
        self._banner.set_text("Memorize the numbers...") # 메시지 변경
        for cell in self._sequence: # 시퀀스의 각 셀에 대해
            cell.show_number() # 숫자 표시
        self._canvas.after(1000, self.start_input) # 1초 후 start_input() 호출

    def start_input(self):
        """숫자를 숨기고 사각형을 표시한 뒤 input 상태로 전환"""
        self._state = "input" # 상태를 input으로 변경
        self._expect_next = 1 # 기대 숫자를 1로 초기화
        for cell in self._sequence: # 시퀀스의 각 셀에 대해
            cell.hide_number() # 숫자 숨김
            cell.show_rect() # 사각형 표시
        self._banner.set_text("Click 1 -> 2 -> ... in order!") # 메시지 변경

    def build_sequence(self):
        """이번 라운드에서 사용할 숫자 시퀀스를 무작위 셀에 배정"""
        for cell in self._sequence: # 이전 라운드의 셀들 초기화
            cell.reset()
        self._sequence = random.sample(self._cells, self._sequence_length) # 무작위로 셀 선택
        for i in range(self._sequence_length): # 선택된 셀에 숫자 배정
            self._sequence[i].set_number(i+1)

    def on_click(self, event):
        """input 상태에서 마우스 클릭 처리"""
        if self._state == "input": # input 상태일 때만 실행
            clicked_cell = None # 클릭된 셀 초기화
            for cell in self._sequence: # 시퀀스의 각 셀에 대해
                if cell.contains(event.x, event.y): # 클릭 좌표가 셀 내부에 있으면
                    clicked_cell = cell # 클릭된 셀로 지정
                    break
            if clicked_cell is None or clicked_cell.get_number() is None or clicked_cell.get_number() < self._expect_next: # 유효하지 않은 클릭이면
                return # 아무 동작 하지 않음
            if clicked_cell.get_number() == self._expect_next: # 올바른 순서로 클릭한 경우
                clicked_cell.hide_rect() # 사각형 숨김
                clicked_cell.show_number() # 숫자 표시
                self._score += 1 # 점수 1 증가
                self.update_hud() # HUD 갱신
                self._expect_next += 1 # 다음 기대 숫자로 증가
                if self._expect_next > self._sequence_length: # 시퀀스를 모두 맞힌 경우
                    if self._sequence_length < 10: # 시퀀스 길이가 10 미만이면
                        self._sequence_length += 1 # 시퀀스 길이 1 증가
                    self.start_round() # 다음 라운드 시작
            else: # 잘못된 순서로 클릭한 경우
                self.fail_round() # 라운드 실패 처리  

    def fail_round(self):
        """라운드 실패 처리: 기회 차감, 게임 오버/재도전 처리"""
        self._lives -= 1 # 기회 1 차감
        self.update_hud() # HUD 갱신
        if self._lives == 0: # 남은 기회가 0인 경우
            self._state = "idle" # 상태를 idle로 변경
            self._banner.set_text("Game Over! SPACE to Restart") # 게임 오버 메시지
            for cell in self._sequence: # 시퀀스의 각 셀 초기화
                cell.reset()
        else: # 남은 기회가 있는 경우
            self._banner.set_text("Try again! Watch carefully...") # 재도전 메시지
            self.start_round() # 같은 길이의 새 라운드 시작


# ---------------------------------------------------------------------
# 메인 루프
# ---------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chimp Memory Test (학번: 20250152)") # 프로그램 이름 설정(본인 학번으로 수정)
    game = ChimpTestGame(root) # 게임 인스턴스 생성
    root.mainloop()            # 이벤트 루프 시작
