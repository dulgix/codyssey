import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone Calculator")
        self.setFixedSize(320, 500)
        self.setStyleSheet("background-color: black;")

        # 상태 관리 변수
        self.current_input = ""   # 콤마 없는 순수 입력 값
        self.first_operand = None
        self.operator = None
        self.is_typing = False

        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 50))
        self.display.setReadOnly(True)
        self.display.setStyleSheet("color: white; background: black; border: none; padding: 10px;")

        grid = QGridLayout()
        grid.setSpacing(10)

        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for row, line in enumerate(buttons):
            col_offset = 0
            for text in line:
                btn = QPushButton(text)
                btn.setFont(QFont("Arial", 18, QFont.Bold))
                btn.setFixedHeight(65)
                
                if text in ["÷", "×", "-", "+", "="]:
                    color = "#ff9500"
                elif text in ["AC", "+/-", "%"]:
                    color = "#a5a5a5"
                else:
                    color = "#333333"

                btn.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; border-radius: 32px; }}")
                btn.clicked.connect(self.handle_click)

                if text == "0":
                    grid.addWidget(btn, row, col_offset, 1, 2)
                    col_offset += 1
                else:
                    grid.addWidget(btn, row, col_offset)
                col_offset += 1

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.display)
        layout.addLayout(grid)
        self.setLayout(layout)

    # --- 수행과제 요구 메소드 ---
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b): return a / b if b != 0 else "Error"

    def reset(self): #
        self.current_input = ""
        self.first_operand = None
        self.operator = None
        self.is_typing = False
        self.update_display("0")

    def negative_positive(self): #
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display(self.current_input)

    def percent(self): #
        try:
            val = float(self.current_input) / 100
            self.current_input = str(val)
            self.update_display(self.current_input)
        except: pass

    def equal(self): #
        if self.operator and self.first_operand is not None:
            second_operand = float(self.current_input)
            if self.operator == "+": res = self.add(self.first_operand, second_operand)
            elif self.operator == "-": res = self.subtract(self.first_operand, second_operand)
            elif self.operator == "×": res = self.multiply(self.first_operand, second_operand)
            elif self.operator == "÷": res = self.divide(self.first_operand, second_operand)
            
            if res == "Error":
                self.update_display("Error")
            else:
                formatted_res = f"{res:g}" # 과학적 표기법 방지 및 깔끔한 출력
                self.current_input = formatted_res
                self.update_display(formatted_res)
            
            self.first_operand = None
            self.operator = None
            self.is_typing = False

    # --- 유틸리티 메소드 ---
    def update_display(self, text):
        # 천 단위 콤마 추가 로직
        try:
            if "." in text:
                parts = text.split(".")
                formatted = format(int(parts[0]), ",") + "." + parts[1]
            else:
                formatted = format(int(text), ",")
            display_text = formatted
        except:
            display_text = text

        # 폰트 크기 자동 조절
        length = len(display_text)
        if length <= 6: size = 50
        elif length <= 9: size = 40
        elif length <= 13: size = 30
        else: size = 22
        
        self.display.setFont(QFont("Arial", size))
        self.display.setText(display_text)

    def handle_click(self):
        text = self.sender().text()

        if text.isdigit():
            if not self.is_typing:
                self.current_input = text
                self.is_typing = True
            else:
                if len(self.current_input) < 15: # 입력 제한
                    self.current_input += text
            self.update_display(self.current_input)

        elif text == ".": # 소수점 중복 방지
            if "." not in self.current_input:
                self.current_input += "." if self.current_input else "0."
                self.is_typing = True
                self.update_display(self.current_input)

        elif text == "AC": self.reset()
        elif text == "+/-": self.negative_positive()
        elif text == "%": self.percent()
        elif text == "=": self.equal()
        elif text in ["+", "-", "×", "÷"]:
            self.first_operand = float(self.current_input) if self.current_input else 0
            self.operator = text
            self.is_typing = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec_())