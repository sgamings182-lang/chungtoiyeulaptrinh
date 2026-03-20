import tkinter
import turtle
from time import sleep
import math

# Thiết lập màn hình
screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0) # Tốc độ nhanh nhất
t.width(2)

def draw_ellipse(color, x, y, width_factor, height_factor):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    # Vẽ elip bằng cách xoay và tiến tới với tỉ lệ khác nhau
    for i in range(2):
        t.circle(100 * width_factor, 90)
        t.circle(100 * height_factor, 90)
    t.end_fill()

# 1. Vẽ hình Oval màu xanh dương bên ngoài
# Tỉ lệ width=2.5, height=1.2 để tạo hình elip dẹt
draw_ellipse("#003399", 0, -100, 2.5, 1.2)

# 2. Vẽ một viền trắng mỏng bên trong để giống logo thật hơn
draw_ellipse("white", 0, -85, 2.3, 1.0)

# 3. Vẽ hình Oval xanh dương nhỏ hơn bên trong cùng
draw_ellipse("#003399", 0, -80, 2.2, 0.9)

# 4. Viết chữ "Ford"
t.penup()
t.goto(-10, -45) # Căn chỉnh vị trí chữ
t.color("white")
# Sử dụng font 'Brush Script MT' hoặc 'Italic' để giống kiểu chữ nghệ thuật của Ford
t.write("Ford", align="center", font=("Arial", 80, "italic bold"))

# Hoàn thành
t.hideturtle()
sleep(2)

# --- PHẦN 1: ĐỊNH NGHĨA HÀM MỞ MÁY TÍNH ---
def open_calculator():
    # Toàn bộ logic máy tính của bạn nằm ở đây
    button_values = [
        ["AC", "+/-", "%", "÷"], 
        ["7", "8", "9", "×"], 
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "√", "="]
    ]

    right_symbols = ["÷", "×", "-", "+", "="]
    top_symbols = ["AC", "+/-", "%", "cls"]
    
    color_gray = "#D4D4D2"
    color_black = "#1C1C1C"
    color_darkGray = "#505050"
    color_orange = "#FF9500"
    color_white = "white"

    # Tạo cửa sổ máy tính mới (Toplevel là cửa sổ con)
    calc_window = tkinter.Toplevel() 
    calc_window.title("Calculator")
    calc_window.resizable(False, False)

    frame = tkinter.Frame(calc_window)
    frame.pack()

    # Nhãn hiển thị của máy tính
    label = tkinter.Label(frame, text="0", font=("Arial", 45), 
                          background=color_black, foreground=color_white,
                          anchor="e", width=10)
    label.grid(row=0, column=0, columnspan=4, sticky="we")

    # Các biến lưu trữ giá trị tính toán
    state = {"A": "0", "operator": None, "B": None}

    def clear_all():
        state["A"], state["operator"], state["B"] = "0", None, None
        
    def remove_zero_decimal(num):
        return str(int(num)) if num % 1 == 0 else str(num)

    def button_clicked(value):
        if value in right_symbols:
            if value == "=":
                if state["A"] is not None and state["operator"] is not None:
                    state["B"] = label["text"]
                    numA, numB = float(state["A"]), float(state["B"])
                    if state["operator"] == "+": res = numA + numB
                    elif state["operator"] == "-": res = numA - numB
                    elif state["operator"] == "×": res = numA * numB
                    elif state["operator"] == "÷": res = numA / numB
                    label["text"] = remove_zero_decimal(res)
                    clear_all()
            elif value in "+-×÷":
                state["A"] = label["text"]
                state["operator"] = value
                label["text"] = "0"
        elif value in top_symbols:
            if value == "AC":
                clear_all(); label["text"] = "0"
            elif value == "+/-":
                label["text"] = str(float(label["text"]) * -1)
            elif value == "%":
                label["text"] = str(float(label["text"]) / 100)
        else: # Số và dấu chấm
            if value == ".":
                if "." not in label["text"]: label["text"] += "."
            else:
                if label["text"] == "0": label["text"] = value
                else: label["text"] += value

    # Tạo các nút bấm
    for r, row_content in enumerate(button_values):
        for c, value in enumerate(row_content):
            btn = tkinter.Button(frame, text=value, font=("Arial", 30), width=3, height=1,
                                 command=lambda v=value: button_clicked(v))
            btn.grid(row=r + 1, column=c)
            if value in top_symbols: btn.config(bg=color_gray, fg=color_black)
            elif value in right_symbols: btn.config(bg=color_orange, fg=color_white)
            else: btn.config(bg=color_darkGray, fg=color_white)

# --- PHẦN 2: CỬA SỔ CHÍNH ---
root = tkinter.Tk()
root.title("Menu Chính")
root.geometry("3000x2000")

welcome_label = tkinter.Label(root, text="Chào bạn! Đây là App chính.", pady=20, font = ("Arial", 20, "bold"))
welcome_label.pack()

# Khi bấm nút này, hàm open_calculator sẽ được thực thi
main_button = tkinter.Button(root, text="CALCULATOR", command=open_calculator, 
                             bg="#4CAF50", fg="white", padx=10, pady=5)
main_button.pack()

root.mainloop()