import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):# qwidget 을 상속받아 클래스 만들기
    def __init__(self):
        super().__init__() # 부모 클래스 초기화 메서드 호출
        self.setWindowTitle("iPhone Calculator")# 창 제목 설정
        self.setFixedSize(320, 480)# 창 크기 고정
        self.setStyleSheet("background-color: black;")  #배경 색 설정

        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)#오른쪽 정렬
        self.display.setFont(QFont("Arial", 32))#글자 크기 설정
        self.display.setReadOnly(True)#사용자가 직접 입력 못하게 막아둠
        self.display.setStyleSheet("""
            QLineEdit {
                color: white;
                background: black;
                border: none;
                padding: 20px;
            }
        """)

        grid = QGridLayout() # 버튼을 격자로 배치할 레이아웃
        grid.setSpacing(10) # 버튼 사이 간격 설정

        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ] # 버튼을 리스트로 정의

        for row, line in enumerate(buttons):
            col_offset = 0
            for col, text in enumerate(line):
                btn = QPushButton(text)
                btn.setFont(QFont("Arial", 16))
                btn.setFixedHeight(60) #buttons 리스트를 한 줄씩 꺼냄.

                # 버튼 종류에 따라 색상 구분
                if text in ["÷", "×", "-", "+", "="]:
                    color = "#ff9500"
                elif text in ["AC", "+/-", "%"]:
                    color = "#a5a5a5" 
                else:
                    color = "#333333" 

                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: white;
                        border-radius: 30px;
                    }
                """) #버튼 색깔 + 모양 꾸밈

                btn.clicked.connect(self.click) # 버튼 클릭 시 click 함수 실행

                # 0 버튼만 가로 2칸
                if text == "0":
                    grid.addWidget(btn, row, col_offset, 1, 2) # 0버튼은 가로로 2칸 차지
                    col_offset += 1 # 2칸 사용했으므로 위치 보정 ( 추가 이동 )
                else:
                    grid.addWidget(btn, row, col_offset) # 일반 버튼 배치 1칸 배치
                col_offset += 1 # 다음 열로 이동

        layout = QVBoxLayout() # 세로로 쌓는 레이아웃 만들기
        layout.addWidget(self.display) # 위에 디스플레이 추가
        layout.addLayout(grid) # 아래에 버튼 그리드 추가
        self.setLayout(layout) # 최종 레이아웃 설정

    def click(self):
        text = self.sender().text() # 어떤 버튼 눌렀는지 가져옴 -> sender().text() : 클릭된 버튼 객체에 적힌 글자를 가져옴

        if text == "AC":
            self.display.setText("0") # AC 누르면 초기화
        else:
            if self.display.text() == "0":
                self.display.setText(text) # 0이면 새 값으로 교체
            else:
                self.display.setText(self.display.text() + text) # 기존 값 뒤에 이어붙임

if __name__ == "__main__":
    app = QApplication(sys.argv)# 앱 실행 객체 생성
    win = Calculator() # 계산기 객체 생성
    win.show() # 화면에 표시
    sys.exit(app.exec_()) # 이벤트 루프 실행 ( 앱 종료까지 유지 ) 
