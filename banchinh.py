import tkinter
import turtle
from time import sleep
import math

screen = turtle.Screen()
screen.setup(1200, 900)
screen.bgcolor("black")

t = turtle.Turtle()
t.speed(0)
t.width(20)

def draw_ellipse(color, x, y, width_factor, height_factor):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    
    for i in range(2):
        t.circle(125 * width_factor, 90)
        t.circle(125 * height_factor, 90)
    t.end_fill()

draw_ellipse("#FF071E", 0, -100, 2.5, 1.2)
draw_ellipse("black", 0, -85, 2.3, 1.0)
draw_ellipse("#FF071E", 0, -80, 2.2, 0.9)
t.penup()
t.goto(-10, -45)
t.color("#E6E6E6")
t.write("Fomo", align="center", font=("Arial", 80, "italic bold"))

sleep(2)
t.hideturtle()
class calculator():
    def open_calculator():
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

        calc_window = tkinter.Toplevel() 
        calc_window.title("Calculator")
        calc_window.resizable(False, False)

        frame = tkinter.Frame(calc_window)
        frame.pack()

        label = tkinter.Label(frame, text="0", font=("Arial", 45), 
                            background=color_black, foreground=color_white,
                            anchor="e", width=10)
        label.grid(row=0, column=0, columnspan=4, sticky="we")

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
            else: 
                if value == ".":
                    if "." not in label["text"]: label["text"] += "."
                else:
                    if label["text"] == "0": label["text"] = value
                    else: label["text"] += value

        for r, row_content in enumerate(button_values):
            for c, value in enumerate(row_content):
                btn = tkinter.Button(frame, text=value, font=("Arial", 40), width=3, height=1,
                                    command=lambda v=value: button_clicked(v))
                btn.grid(row=r + 1, column=c)
                if value in top_symbols: btn.config(bg=color_gray, fg=color_black)
                elif value in right_symbols: btn.config(bg=color_orange, fg=color_white)
                else: btn.config(bg=color_darkGray, fg=color_white)
class converter():
    def open_converter():
        data = {
            "Distance (m)": {
                "m (meter)": 1,
                "km (kilometer)": 1000,
                "cm (centimetre)": 0.01,
                "mm (milimeter)": 0.001,
                "nm (nanometer)": 1e-9
            },
            "Mass (g)": {
                "g (gram)": 1,
                "kg (kilogram)": 1000,
                "mg (miligram)": 0.001,
                "quintals": 100000,
                "tons": 1000000
            },
            "Time (s)": {
                "s (Seconds)": 1,
                "M (Minutes)": 60,
                "H (Hours)": 3600,
                "D (Day)": 86400
            },
            "Voltage (V)": {
                "V (voltage)": 1,
                "kV (kilovoltage)": 1000,
                "mV (milivoltage)": 0.001
            }
        }

        def update_units(*args):
            category = selected_category.get()
            units_list = list(data[category].keys())
            
            menu_from['menu'].delete(0, 'end')
            menu_to['menu'].delete(0, 'end')
            
            for unit in units_list:
                menu_from['menu'].add_command(label=unit, command=lambda u=unit: unit_from.set(u))
                menu_to['menu'].add_command(label=unit, command=lambda u=unit: unit_to.set(u))
            
            unit_from.set(units_list[0])
            unit_to.set(units_list[1] if len(units_list) > 1 else units_list[0])

        def convert():
            try:
                val = float(entry_input.get())
                category = selected_category.get()
                u_from = unit_from.get()
                u_to = unit_to.get()
                
                # Công thức: (Giá trị * Tỷ lệ đơn vị gốc) / Tỷ lệ đơn vị đích
                base_value = val * data[category][u_from]
                result = base_value / data[category][u_to]
                
                # Định dạng hiển thị
                if result < 0.0001 or result > 1000000:
                    res_str = f"{result:.4e}"
                else:
                    res_str = f"{result:,.4f}".rstrip('0').rstrip('.')
                    
                label_result.config(text=f"result: {res_str} {u_to}")
            except Exception as e:
                messagebox.showerror("Error!", "Invalid value!")

        root = tkinter.Tk()
        root.title("Physics Ultra Converter")
        root.geometry("500x450")
        root.config(padx=20, pady=20, bg="#f0f3f5")

        tkinter.Label(root, text="SELECT A UNIT", font=("Arial", 12, "bold"), bg="#f0f3f5").pack()
        selected_category = tkinter.StringVar(root)
        selected_category.set(list(data.keys())[0])
        selected_category.trace("w", update_units)

        cat_menu = tkinter.OptionMenu(root, selected_category, *data.keys())
        cat_menu.config(width=25, font=("Arial", 11))
        cat_menu.pack(pady=10)

        tkinter.Label(root, text="Input Value:", bg="#f0f3f5").pack()
        entry_input = tkinter.Entry(root, font=("Arial", 14), width=20, justify="center")
        entry_input.pack(pady=5)

        frame_units = tkinter.Frame(root, bg="#f0f3f5")
        frame_units.pack(pady=15)

        unit_from = tkinter.StringVar(root)
        unit_to = tkinter.StringVar(root)

        menu_from = tkinter.OptionMenu(frame_units, unit_from, "")
        menu_from.config(width=12)
        menu_from.pack(side="left", padx=10)

        tkinter.Label(frame_units, text="➔", font=("Arial", 15), bg="#f0f3f5").pack(side="left")

        menu_to = tkinter.OptionMenu(frame_units, unit_to, "")
        menu_to.config(width=12)
        menu_to.pack(side="left", padx=10)

        tkinter.Button(root, text="CHUYỂN ĐỔI", font=("Arial", 12, "bold"), bg="#3498db", fg="white", 
                padx=40, pady=10, command=convert).pack(pady=20)

        label_result = tkinter.Label(root, text="Kết quả: 0", font=("Arial", 15, "bold"), fg="#2c3e50", bg="#f0f3f5")
        label_result.pack()

        update_units()
        root.mainloop()
root = tkinter.Tk()
root.title("Main Menu")
root.geometry("7680x4320")

welcome_label = tkinter.Label(root, text="Welcome to Multi-Matical", pady=20, font = ("Arial", 20, "bold"),)
welcome_label.pack()

main_button = tkinter.Button(root, text="CALCULATOR", command=calculator.open_calculator, 
                             bg="#4CAF50", fg="white", padx=100, pady=10)
button_converter = tkinter.Button(root, text=" CONVERTER ", command=converter.open_converter, 
                             bg="#4CAF50", fg="white", padx=100, pady=10)
main_button.pack()
button_converter.pack()
t.hideturtle()
root.mainloop()
