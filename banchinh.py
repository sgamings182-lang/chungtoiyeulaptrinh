import tkinter
import turtle
from time import sleep
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from PIL import Image, ImageTk

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
screen.bye()
"-------------------------------------------------------------------------------------------------------------------------"
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
                "nm (nanometer)": 1e-9,
                "mile (Mile)": 1.60934,
                "inch (inch)": 0.0254
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
            },
            "Atmosphere (atm)": {
                "atm": 1,
                "pascal": 1/101325,
                "PSI": 1/14.6959,
                "Bar": 1/1.01325,
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
                TextBox.showerror("Error!", "Invalid value!")

        root = tkinter.Toplevel() 
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
class graph():
    def open_graph():    
        x = np.linspace(-10, 10, 1000)
        a_init, b_init, c_init, d_init = 1.0, 0.0, 0.0, 0.0 

        fig, ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.35)

        line, = ax.plot(x, a_init*x**3 + b_init*x**2 + c_init*x + d_init, 
                        lw=2.5, color='#1f77b4', label='$y = ax^3 + bx^2 + cx + d$')

        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        ax.set_xlabel('x', loc='right', fontsize=12, style='italic')
        ax.set_ylabel('y', loc='top', rotation=0, fontsize=12, style='italic', labelpad=15)

        ax.set_xlim(-10, 10)
        ax.set_ylim(-50, 50)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left')

        class SyncedControl:
            def __init__(self, label, y_pos, vmin, vmax, vinit, color):
                self.ax_slider = plt.axes([0.15, y_pos, 0.65, 0.03], facecolor=color)
                self.ax_text = plt.axes([0.82, y_pos, 0.08, 0.03])
                
                self.slider = Slider(self.ax_slider, label, vmin, vmax, valinit=vinit)
                self.slider.valtext.set_visible(False)
                self.text = TextBox(self.ax_text, '', initial=f"{vinit:.2f}")
                
                self.updating = False
                self.slider.on_changed(self.on_slider_change)
                self.text.on_submit(self.on_text_submit)

            def on_slider_change(self, val):
                if not self.updating:
                    self.updating = True
                    self.text.set_val(f"{val:.2f}")
                    global_update()
                    self.updating = False

            def on_text_submit(self, text):
                if not self.updating:
                    try:
                        val = max(self.slider.valmin, min(self.slider.valmax, float(text)))
                        self.updating = True
                        self.slider.set_val(val)
                        self.text.set_val(f"{val:.2f}")
                        global_update()
                        self.updating = False
                    except ValueError:
                        self.text.set_val(f"{self.slider.val:.2f}")

        ctrl_a = SyncedControl('Hệ số $a$', 0.22, -10.0, 10.0, a_init, 'lightcoral')
        ctrl_b = SyncedControl('Hệ số $b$', 0.16, -20.0, 20.0, b_init, 'lightblue')
        ctrl_c = SyncedControl('Hệ số $c$', 0.10, -50.0, 50.0, c_init, 'lightgreen')
        ctrl_d = SyncedControl('Hệ số $d$', 0.04, -50.0, 50.0, d_init, 'thistle')

        def global_update():
            a = ctrl_a.slider.val
            b = ctrl_b.slider.val
            c = ctrl_c.slider.val
            d = ctrl_d.slider.val
            line.set_ydata(a*x**3 + b*x**2 + c*x + d)
            fig.canvas.draw_idle()

        plt.show()
class snake_game():
    def open_snake():
        import pygame
        from random import randint
        pygame.init()

        screen = pygame.display.set_mode((1200, 900))

        IMG_DIR = r"D:\vscode\snake.io\\"
        #Head
        head_up = pygame.image.load(IMG_DIR + "snake_head_up.png").convert_alpha()
        head_down = pygame.image.load(IMG_DIR + "snake_head_down.png").convert_alpha()
        head_left = pygame.image.load(IMG_DIR + "snake_head_left.png").convert_alpha()
        head_right = pygame.image.load(IMG_DIR + "snake_head_right.png").convert_alpha()
                # 2. Tail
        tail_up = pygame.image.load(IMG_DIR + "snake_tail_up.png").convert_alpha()
        tail_down = pygame.image.load(IMG_DIR + "snake_tail_down.png").convert_alpha()
        tail_left = pygame.image.load(IMG_DIR + "snake_tail_left.png").convert_alpha()
        tail_right = pygame.image.load(IMG_DIR + "snake_tail_right.png").convert_alpha()
                # 3. Body and cross
        body_vertical = pygame.image.load(IMG_DIR + "snake_body_vertical.png").convert_alpha()
        body_horizontal = pygame.image.load(IMG_DIR + "snake_body_horizontal.png").convert_alpha()
        body_tl = pygame.image.load(IMG_DIR + "body_tl.png").convert_alpha() # Cua góc trên-trái
        body_tr = pygame.image.load(IMG_DIR + "body_tr.png").convert_alpha() # Cua góc trên-phải
        body_bl = pygame.image.load(IMG_DIR + "body_bl.png").convert_alpha() # Cua góc dưới-trái
        body_br = pygame.image.load(IMG_DIR + "body_br.png").convert_alpha() # Cua góc dưới-phải

        #Head2
        head_up2 = pygame.image.load(IMG_DIR + "snake_head_up2.png").convert_alpha()
        head_down2 = pygame.image.load(IMG_DIR + "snake_head_down2.png").convert_alpha()
        head_left2 = pygame.image.load(IMG_DIR + "snake_head_left2.png").convert_alpha()
        head_right2 = pygame.image.load(IMG_DIR + "snake_head_right2.png").convert_alpha()
                # 2. Tail2
        tail_up2 = pygame.image.load(IMG_DIR + "snake_tail_up2.png").convert_alpha()
        tail_down2 = pygame.image.load(IMG_DIR + "snake_tail_down2.png").convert_alpha()
        tail_left2 = pygame.image.load(IMG_DIR + "snake_tail_left2.png").convert_alpha()
        tail_right2 = pygame.image.load(IMG_DIR + "snake_tail_right2.png").convert_alpha()
                # 3. Body and cross2
        body_vertical2 = pygame.image.load(IMG_DIR + "snake_body_vertical2.png").convert_alpha()
        body_horizontal2 = pygame.image.load(IMG_DIR + "snake_body_horizontal2.png").convert_alpha()
        body_tl2 = pygame.image.load(IMG_DIR + "body_tl2.png").convert_alpha()
        body_tr2 = pygame.image.load(IMG_DIR + "body_tr2.png").convert_alpha()
        body_bl2 = pygame.image.load(IMG_DIR + "body_bl2.png").convert_alpha()
        body_br2 = pygame.image.load(IMG_DIR + "body_br2.png").convert_alpha()

        apple_img = pygame.image.load(r"D:\vscode\snake.io\apple.png").convert_alpha()
        apple_img = pygame.transform.scale(apple_img, (30, 30))
        bomb_img = pygame.image.load(r"D:\vscode\snake.io\bomb.png").convert_alpha()
        bomb_img = pygame.transform.scale(bomb_img, (30, 30))
        ice_img = pygame.image.load(r"D:\vscode\snake.io\iceberg.png").convert_alpha()
        ice_img = pygame.transform.scale(ice_img, (30, 30))
        bolt_img = pygame.image.load(r"D:\vscode\snake.io\bolt.png").convert_alpha()
        bolt_img = pygame.transform.scale(bolt_img, (30, 30))

        head_up = pygame.transform.scale(head_up, (30, 30))
        head_down = pygame.transform.scale(head_down, (30, 30))
        head_left = pygame.transform.scale(head_left, (30, 30))
        head_right = pygame.transform.scale(head_right, (30, 30))
        body_tl = pygame.transform.scale(body_tl, (30, 30))
        body_tr = pygame.transform.scale(body_tr, (30, 30)) 
        body_bl = pygame.transform.scale(body_bl, (30, 30)) 
        body_br = pygame.transform.scale(body_br, (30, 30)) 

        head_up2 = pygame.transform.scale(head_up2, (30, 30))
        head_down2 = pygame.transform.scale(head_down2, (30, 30))
        head_left2 = pygame.transform.scale(head_left2, (30, 30))
        head_right2 = pygame.transform.scale(head_right2, (30, 30))
        body_tl2 = pygame.transform.scale(body_tl2, (30, 30))
        body_tr2 = pygame.transform.scale(body_tr2, (30, 30)) 
        body_bl2 = pygame.transform.scale(body_bl2, (30, 30)) 
        body_br2 = pygame.transform.scale(body_br2, (30, 30)) 

        bg_img = pygame.image.load(IMG_DIR + "grass_field.png").convert() 
        bg_img = pygame.transform.scale(bg_img, (1200, 900))

        pygame.display.set_caption('snake')
        running = True
        GREEN = (0, 200, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        Light_blue = (145, 240, 255)
        YELLOW = (241, 240, 93)
        BROWN = (144, 88, 26)
        RAINBOW_COLORS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), 
                        (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

        clock = pygame.time.Clock()

        snakes = [[20, 15], [20,16], [20, 17]]
        snakes2 = [[15, 6], [15,7], [15, 8]]

        direction = "right"
        direction2 = "Right"

        apple = [randint(0, 39), randint(0, 29)]
        freeze = [randint(0, 39), randint(0, 29)]
        freeze2 = [randint(0, 39), randint(0, 29)]
        bolt = [randint(0, 39), randint(0, 29)]
        bolt2 = [randint(0, 39), randint(0, 29)]
        bomb = [randint(0, 39), randint(0, 29)]
        bomb2 = [randint(0, 39), randint(0, 29)]

        rainbow_apple = [-1, -1]
        rainbow_active = False
        apples_eaten = 0

        font_small = pygame.font.SysFont('your score:', 30)
        font_big = pygame.font.SysFont('your score:', 50)
        score = 3
        score2 = 3

        is_frozen1 = False
        is_frozen2 = False
        freeze_time1 = 0
        freeze_time2 = 0 

        paralyse1 = False
        paralyse2 = False
        paralyse_time1 = 0
        paralyse_time2 = 0

        pause = True
        pause2 = True

        last_item_move_time = pygame.time.get_ticks()

        while running:    
            clock.tick(10)
            screen.blit(bg_img, (0, 0))
            
            current_time = pygame.time.get_ticks()
            
            if current_time - last_item_move_time >= 10000:
                freeze = [randint(0, 39), randint(0, 29)]
                freeze2 = [randint(0, 39), randint(0, 29)]
                bolt = [randint(0, 39), randint(0, 29)]
                bolt2 = [randint(0, 39), randint(0, 29)]
                bomb = [randint(0, 39), randint(0, 29)]
                bomb2 = [randint(0, 39), randint(0, 29)]
                
                last_item_move_time = current_time
            if is_frozen1 == True and current_time - freeze_time1 >= 3000:
                is_frozen1 = False
            if is_frozen2 == True and current_time - freeze_time2 >= 3000:
                is_frozen2 = False
            
            if paralyse1 == True and current_time - paralyse_time1 >= 1500:
                paralyse1 = False 
            if paralyse2 == True and current_time - paralyse_time2 >= 1500:
                paralyse2 = False 
                
            tail_x = snakes[0][0]
            tail_y = snakes[0][1]
            
            tail_x2 = snakes2[0][0]
            tail_y2 = snakes2[0][1]
            
            for index, segment in enumerate(snakes):
                rect = pygame.Rect(segment[0]*30, segment[1]*30, 30, 30)
                        
                        # 1. Draw head
                if index == len(snakes) - 1:
                    if direction == "up": screen.blit(head_up, rect)
                    elif direction == "down": screen.blit(head_down, rect)
                    elif direction == "left": screen.blit(head_left, rect)
                    elif direction == "right": screen.blit(head_right, rect)
                        
                        # 2. Draw tail
                elif index == 0:
                            
                    next_seg = snakes[1]
                            
                    if next_seg[0] > segment[0]: screen.blit(tail_right, rect) 
                    elif next_seg[0] < segment[0]: screen.blit(tail_left, rect)
                    elif next_seg[1] > segment[1]: screen.blit(tail_down, rect)
                    elif next_seg[1] < segment[1]: screen.blit(tail_up, rect)

                        # 3. Draw body
                else:
                    previous_seg = snakes[index - 1]
                    next_seg = snakes[index + 1]    

                    prev_rel = (previous_seg[0] - segment[0], previous_seg[1] - segment[1])
                    next_rel = (next_seg[0] - segment[0], next_seg[1] - segment[1])
                            
                    dirs = {prev_rel, next_rel}
                    if previous_seg[0] == next_seg[0]:
                        screen.blit(body_vertical, rect)
                    elif previous_seg[1] == next_seg[1]:
                        screen.blit(body_horizontal, rect)
                                
                    else:
                        if dirs == {(0, -1), (-1, 0)}:
                            screen.blit(body_tl, rect)
                        elif dirs == {(0, -1), (1, 0)}:
                            screen.blit(body_tr, rect)
                        elif dirs == {(0, 1), (-1, 0)}:
                            screen.blit(body_bl, rect)
                        elif dirs == {(0, 1), (1, 0)}:
                            screen.blit(body_br, rect)
                
            for index, segment in enumerate(snakes2):
                rect = pygame.Rect(segment[0]*30, segment[1]*30, 30, 30)
                        
                if index == len(snakes2) - 1:
                    if direction2 == "Up": screen.blit(head_up2, rect)
                    elif direction2 == "Down": screen.blit(head_down2, rect)
                    elif direction2 == "Left": screen.blit(head_left2, rect)
                    elif direction2 == "Right": screen.blit(head_right2, rect)

                elif index == 0:
                    next_seg = snakes2[1]
                    if next_seg[0] > segment[0]: screen.blit(tail_right2, rect) 
                    elif next_seg[0] < segment[0]: screen.blit(tail_left2, rect)
                    elif next_seg[1] > segment[1]: screen.blit(tail_down2, rect)
                    elif next_seg[1] < segment[1]: screen.blit(tail_up2, rect)

                else:
                    previous_seg = snakes2[index - 1] 
                    next_seg = snakes2[index + 1]     
                            
                    prev_rel = (previous_seg[0] - segment[0], previous_seg[1] - segment[1])
                    next_rel = (next_seg[0] - segment[0], next_seg[1] - segment[1])
                            
                    dirs = {prev_rel, next_rel}

                    if previous_seg[0] == next_seg[0]:
                        screen.blit(body_vertical2, rect)
                    elif previous_seg[1] == next_seg[1]:
                        screen.blit(body_horizontal2, rect)

                    else:
                        if dirs == {(0, -1), (-1, 0)}:
                            screen.blit(body_tl2, rect)
                        elif dirs == {(0, -1), (1, 0)}:
                            screen.blit(body_tr2, rect)
                        elif dirs == {(0, 1), (-1, 0)}:
                            screen.blit(body_bl2, rect)
                        elif dirs == {(0, 1), (1, 0)}:
                            screen.blit(body_br2, rect)
                
            screen.blit(apple_img, (apple[0]*30, apple[1]*30))
            screen.blit(bomb_img, (bomb[0]*30, bomb[1]*30))
            screen.blit(bomb_img, (bomb2[0]*30, bomb2[1]*30))
            screen.blit(ice_img, (freeze[0]*30, freeze[1]*30))
            screen.blit(ice_img, (freeze2[0]*30, freeze2[1]*30))
            screen.blit(bolt_img, (bolt[0]*30, bolt[1]*30))
            screen.blit(bolt_img, (bolt2[0]*30, bolt2[1]*30))
                
            if rainbow_active == True:
                color_index = (current_time // 150) % len(RAINBOW_COLORS)
                pygame.draw.rect(screen, RAINBOW_COLORS[color_index], (rainbow_apple[0]*30, rainbow_apple[1]*30, 30, 30))
                
            

        #get point   
            if snakes[-1][0] == apple [0] and snakes[-1][1] == apple [1]:
                snakes.insert(0,[tail_x,tail_y])
                apple = [randint(0, 39), randint(0, 29)]
                score += 1
                apples_eaten += 1
                if apples_eaten % 10 == 0:
                    rainbow_apple = [randint(0, 39), randint(0, 29)]
                    rainbow_active = True
                    
            if (snakes[-1][0] == freeze[0] and snakes[-1][1] == freeze[1]) or (snakes[-1][0] == freeze2[0] and snakes[-1][1] == freeze2[1]):
                if snakes[-1][0] == freeze[0]:
                    freeze = [randint(0, 39), randint(0, 29)]
                else:
                    freeze2 = [randint(0, 39), randint(0, 29)]
                is_frozen1 = True
                freeze_time1 = current_time   
            if (snakes[-1][0] == bolt[0] and snakes[-1][1] == bolt[1]) or (snakes[-1][0] == bolt2[0] and snakes[-1][1] == bolt2[1]):
                if snakes[-1][0] == bolt[0]:
                    bolt = [randint(0, 39), randint(0, 29)]
                else:
                    bolt2 = [randint(0, 39), randint(0, 29)]
                paralyse1 = True
                paralyse_time1 = current_time
                if len(snakes) > 1:
                    snakes.pop(0)
                score -= 1
            if rainbow_active == True and snakes[-1][0] == rainbow_apple[0] and snakes[-1][1] == rainbow_apple[1]:
                snakes.insert(0,[tail_x,tail_y])
                snakes.insert(0,[tail_x,tail_y]) 
                snakes.insert(0,[tail_x,tail_y])
                snakes.insert(0,[tail_x,tail_y])
                snakes.insert(0,[tail_x,tail_y])
                score += 5                    
                rainbow_active = False
            if (snakes[-1][0] == bomb[0] and snakes[-1][1] == bomb[1]) or (snakes[-1][0] == bomb2[0] and snakes[-1][1] == bomb2[1]):
                if snakes[-1][0] == bomb[0]:
                    bomb = [randint(0, 39), randint(0, 29)]
                else:
                    bomb2 = [randint(0, 39), randint(0, 29)]
                for _ in range(5):
                    if len(snakes) > 1:
                        snakes.pop(0)
                score -= 5
            for i in range(len(snakes2) -1):
                if snakes[-1][0] == snakes2[i][0] and snakes[-1][1] == snakes2[i][1]:
                    if len(snakes) > 1:
                        snakes.pop(0)
                    score -= 1
            
                

                
            if snakes2[-1][0] == apple [0] and snakes2[-1][1] == apple [1]:
                snakes2.insert(0,[tail_x2,tail_y2])
                apple = [randint(0, 39), randint(0, 29)] 
                score2 += 1
                apples_eaten += 1
                if apples_eaten % 10 == 0:
                    rainbow_apple = [randint(0, 39), randint(0, 29)]
                    rainbow_active = True
                
            if (snakes2[-1][0] == freeze[0] and snakes2[-1][1] == freeze[1]) or (snakes2[-1][0] == freeze2[0] and snakes2[-1][1] == freeze2[1]):
                if snakes2[-1][0] == freeze[0]:
                    freeze = [randint(0, 39), randint(0, 29)]
                else:
                    freeze2 = [randint(0, 39), randint(0, 29)]
                is_frozen2 = True
                freeze_time2 = current_time
                
            if (snakes2[-1][0] == bolt[0] and snakes2[-1][1] == bolt[1]) or (snakes2[-1][0] == bolt2[0] and snakes2[-1][1] == bolt2[1]):
                if snakes2[-1][0] == bolt[0]:
                    bolt = [randint(0, 39), randint(0, 29)]
                else:
                    bolt2 = [randint(0, 39), randint(0, 29)]
                paralyse2 = True
                paralyse_time2 = current_time
                if len(snakes2) > 1:
                    snakes2.pop(0)
                score2 -= 1
            if rainbow_active == True and snakes2[-1][0] == rainbow_apple[0] and snakes2[-1][1] == rainbow_apple[1]:
                snakes2.insert(0,[tail_x,tail_y])
                snakes2.insert(0,[tail_x,tail_y]) 
                snakes2.insert(0,[tail_x,tail_y])
                snakes2.insert(0,[tail_x,tail_y])
                snakes2.insert(0,[tail_x,tail_y])
                score2 += 5                    
                rainbow_active = False
            if (snakes2[-1][0] == bomb[0] and snakes2[-1][1] == bomb[1]) or (snakes2[-1][0] == bomb2[0] and snakes2[-1][1] == bomb2[1]):
                if snakes[-1][0] == bomb[0]:
                    bomb = [randint(0, 39), randint(0, 29)]
                else:
                    bomb2 = [randint(0, 39), randint(0, 29)]
                for _ in range(5):
                    if len(snakes2) > 1:
                        snakes2.pop(0)
                score2 -= 5
            for i in range(len(snakes) -1):
                if snakes2[-1][0] == snakes[i][0] and snakes2[-1][1] == snakes[i][1]:
                    if len(snakes2) > 1:
                        snakes2.pop(0)
                    score2 -= 1
            
            if snakes[-1][0] < 0 or snakes[-1][0] > 39 or snakes[-1][1] < 0 or snakes[-1][1] > 29:
                game_over = font_small.render(f"game over SCORE of player 1: {score} ", True, GREEN)
                screen.blit(game_over, (100, 70))
                pause = True
            if score <= 1:
                game_over = font_small.render(f"game over SCORE of player 1: {score} ", True, GREEN)
                screen.blit(game_over, (100, 70))
                pause = True
                
            if snakes2[-1][0] < 0 or snakes2[-1][0] > 39 or snakes2[-1][1] < 0 or snakes2[-1][1] > 29:
                game_over = font_small.render(f"game over SCORE of player 2: {score2} ", True, WHITE)
                screen.blit(game_over, (800, 70))
                pause2 = True
            if score2 <= 1:
                game_over = font_small.render(f"game over SCORE of player 2: {score} ", True, WHITE)
                screen.blit(game_over, (800, 70))
                pause2 = True
            
            
            if pause == True and pause2 == True:
                game_continue = font_big.render("press space to continue ", True, WHITE)
                screen.blit(game_continue, (400, 500))
                
            if pause == False and is_frozen1 == False and paralyse1 == False:     
                if direction == "right":
                    snakes.append([snakes[-1][0]+1, snakes[-1][1]])
                    snakes.pop(0)
                if direction == "left":
                    snakes.append([snakes[-1][0]-1, snakes[-1][1]])
                    snakes.pop(0)
                if direction == "up":
                    snakes.append([snakes[-1][0], snakes[-1][1]-1])
                    snakes.pop(0)
                if direction == "down":
                    snakes.append([snakes[-1][0], snakes[-1][1]+1])
                    snakes.pop(0)
            
            if pause2 == False and is_frozen2 == False and paralyse2 == False:
                if direction2 == "Right":
                    snakes2.append([snakes2[-1][0]+1, snakes2[-1][1]])
                    snakes2.pop(0)
                if direction2 == "Left":
                    snakes2.append([snakes2[-1][0]-1, snakes2[-1][1]])
                    snakes2.pop(0)
                if direction2 == "Up":
                    snakes2.append([snakes2[-1][0], snakes2[-1][1]-1])
                    snakes2.pop(0)
                if direction2 == "Down":
                    snakes2.append([snakes2[-1][0], snakes2[-1][1]+1])
                    snakes2.pop(0)
            
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and direction != "down":
                        direction = "up"
                    if event.key == pygame.K_s and direction != "up":
                        direction = "down"
                    if event.key == pygame.K_a and direction != "right":
                        direction = "left"
                    if event.key == pygame.K_d and direction != "left":
                        direction = "right"
                        
                    if event.key == pygame.K_UP and direction2 != "Down":
                        direction2 = "Up"
                    if event.key == pygame.K_DOWN and direction2 != "Up":
                        direction2 = "Down"
                    if event.key == pygame.K_LEFT and direction2 != "Right":
                        direction2 = "Left"
                    if event.key == pygame.K_RIGHT and direction2 != "Left":
                        direction2 = "Right"
                    if event.key == pygame.K_SPACE and pause == True and pause2 == True:
                        pause = False
                        pause2 = False
                        snakes = [[5, 6], [5,7], [5, 8]]
                        snakes2 = [[10, 6], [10,7], [10, 8]]
                        score = 3
                        score2 = 3
                        rainbow_active = False 
                        apples_eaten = 0
                        apple = [randint(0, 39), randint(0, 29)]
                        freeze = [randint(0, 39), randint(0, 29)]
                        freeze2 = [randint(0, 39), randint(0, 29)]
                        bolt = [randint(0, 39), randint(0, 29)]
                        bolt2 = [randint(0, 39), randint(0, 29)]
                
            pygame.display.flip()
            
        pygame.quit()
class graph_3D():
    def open_graph3d():
        fig = plt.figure(figsize=(15, 10))
        plt.subplots_adjust(bottom=0.4) 
        ax = fig.add_subplot(111, projection='3d')

        vA_init, vB_init = np.array([4.0, 0.0, 2.0]), np.array([0.0, 5.0, 3.0])
        P_A, P_B, P_C, P_D = 1.0, 1.0, 1.0, -5.0
        S_a, S_b, S_c, S_R = 0.0, 0.0, 5.0, 3.0
        def draw_scene(vA, vB, A, B, C, D, a, b, c, R):
            ax.cla()
            
            Sum = vA + vB
            ax.quiver(0, 0, 0, vA[0], vA[1], vA[2], color='blue', linewidth=2, arrow_length_ratio=0.1, label='Vector A')
            ax.quiver(0, 0, 0, vB[0], vB[1], vB[2], color='green', linewidth=2, arrow_length_ratio=0.1, label='Vector B')
            ax.quiver(0, 0, 0, Sum[0], Sum[1], Sum[2], color='red', linewidth=2.5, arrow_length_ratio=0.1, label='Sum A+B')
            ax.plot([vA[0], Sum[0]], [vA[1], Sum[1]], [vA[2], Sum[2]], color='green', linestyle='--', alpha=0.6)
            ax.plot([vB[0], Sum[0]], [vB[1], Sum[1]], [vB[2], Sum[2]], color='blue', linestyle='--', alpha=0.6)

            n_vec = np.array([A, B, C])
            norm = np.linalg.norm(n_vec)
            
            if norm > 0:
                d = abs(A*a + B*b + C*c + D) / norm

                n_hat = n_vec / norm
                v_arb = np.array([1, 0, 0]) if abs(n_hat[0]) < 0.9 else np.array([0, 1, 0])
                u_vec = np.cross(n_hat, v_arb)
                u_vec /= np.linalg.norm(u_vec)
                v_vec = np.cross(n_hat, u_vec)
                P0 = -D * n_hat / norm
                
                s_grid, t_grid = np.meshgrid(np.linspace(-10, 10, 5), np.linspace(-10, 10, 5))
                ax.plot_surface(P0[0] + s_grid*u_vec[0] + t_grid*v_vec[0], 
                                P0[1] + s_grid*u_vec[1] + t_grid*v_vec[1], 
                                P0[2] + s_grid*u_vec[2] + t_grid*v_vec[2], color='cyan', alpha=0.2, edgecolor='none')

                U, V = np.meshgrid(np.linspace(0, 2*np.pi, 20), np.linspace(0, np.pi, 15))
                Xs, Ys, Zs = a + R*np.cos(U)*np.sin(V), b + R*np.sin(U)*np.sin(V), c + R*np.cos(V)
                
                if abs(d-R) < 0.05: color_s, status = 'green', "CONTACT"
                elif d < R:         color_s, status = 'red', "CUTTING EACH OTHER"
                else:               color_s, status = 'gray', "SEPARATE"
                ax.plot_wireframe(Xs, Ys, Zs, color=color_s, alpha=0.3)
                
                H = np.array([a, b, c]) - ((A*a + B*b + C*c + D) / np.sum(n_vec**2)) * n_vec
                ax.scatter(a, b, c, color='black', s=50, label='Center I')
                ax.scatter(*H, color='red', s=40, zorder=5, label='Projection H')
                ax.plot([a, H[0]], [b, H[1]], [c, H[2]], 'k--', alpha=0.6, linewidth=1.5)
                
                title_text = f"Mixed Spaces | Spherical and Flat: {status} (d={d:.2f}, R={R:.1f})"
            else:
                title_text = "The coefficients A, B, and C cannot all be equal to 0 at the same time!"

            ax.set_xlim([-12, 12]); ax.set_ylim([-12, 12]); ax.set_zlim([-12, 12])
            ax.set_xlabel('X axis'); ax.set_ylabel('Y axis'); ax.set_zlabel('Z axis')
            ax.set_title(title_text, weight='bold')
            
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize='small')

        class SyncedControl:
            def __init__(self, label, x_slider, x_text, y, w_slider, w_text, h, vmin, vmax, vinit, color):
                self.ax_slider = plt.axes([x_slider, y, w_slider, h], facecolor=color)
                self.ax_text = plt.axes([x_text, y, w_text, h])
                
                self.slider = Slider(self.ax_slider, label, vmin, vmax, valinit=vinit)
                self.slider.valtext.set_visible(False)
                self.text = TextBox(self.ax_text, '', initial=f"{vinit:.1f}")
                
                self.updating = False
                self.slider.on_changed(self.on_slider_change)
                self.text.on_submit(self.on_text_submit)

            def on_slider_change(self, val):
                if not self.updating:
                    self.updating = True
                    self.text.set_val(f"{val:.1f}")
                    global_update()
                    self.updating = False

            def on_text_submit(self, text):
                if not self.updating:
                    try:
                        val = max(self.slider.valmin, min(self.slider.valmax, float(text)))
                        self.updating = True
                        self.slider.set_val(val)
                        self.text.set_val(f"{val:.1f}")
                        global_update()
                        self.updating = False
                    except ValueError:
                        self.text.set_val(f"{self.slider.val:.1f}")

        plt.figtext(0.05, 0.32, 'Vector A', weight='bold', color='blue')
        plt.figtext(0.28, 0.32, 'Vector B', weight='bold', color='green')
        plt.figtext(0.52, 0.32, 'Flat (Ax+By+Cz+D=0)', weight='bold', color='darkcyan')
        plt.figtext(0.77, 0.32, 'Shpere (center I, radius R)', weight='bold', color='maroon')

        y_pos = [0.25, 0.20, 0.15, 0.10]

        def make_col(labels, x_base, color, inits, bounds, is_radius=False):
            ctrls = []
            w_slider, w_text, spacing = 0.08, 0.04, 0.01
            for i, (lbl, init) in enumerate(zip(labels, inits)):
                vmin, vmax = bounds[i]
                c = SyncedControl(lbl, x_base, x_base + w_slider + spacing, y_pos[i], 
                                w_slider, w_text, 0.02, vmin, vmax, init, color)
                ctrls.append(c)
            return ctrls

        col1 = make_col(['X', 'Y', 'Z'], 0.05, 'lightblue', vA_init, [(-10,10)]*3)
        col2 = make_col(['X', 'Y', 'Z'], 0.28, 'lightgreen', vB_init, [(-10,10)]*3)
        col3 = make_col(['A', 'B', 'C', 'D'], 0.52, 'lightcyan', [P_A, P_B, P_C, P_D], [(-5,5), (-5,5), (-5,5), (-15,15)])
        col4 = make_col(['X', 'Y', 'Z', 'R'], 0.77, 'mistyrose', [S_a, S_b, S_c, S_R], [(-10,10)]*3 + [(1,10)])
        col4[3].ax_slider.set_facecolor('honeydew')

        def global_update():
            vA = np.array([c.slider.val for c in col1])
            vB = np.array([c.slider.val for c in col2])
            P = [c.slider.val for c in col3]
            S = [c.slider.val for c in col4]
            draw_scene(vA, vB, P[0], P[1], P[2], P[3], S[0], S[1], S[2], S[3])
            fig.canvas.draw_idle()
            
        draw_scene(vA_init, vB_init, P_A, P_B, P_C, P_D, S_a, S_b, S_c, S_R)
        plt.show()
class colorpicker():
    def open_picker():
        cp_window = tkinter.Toplevel()
        cp_window.title("color studio")
        cp_window.geometry("1000x650")
        cp_window.configure(bg="#2c3e50")

        r_var = tkinter.IntVar(value=100)
        g_var = tkinter.IntVar(value=100)
        b_var = tkinter.IntVar(value=100)

        color_display = tkinter.Frame(cp_window , width=350, height= 80, relief="sunken", bd=5)
        color_display.pack(pady=20)

        hex_entry = tkinter.Entry(cp_window, font=("consolas", 14), justify="center")
        hex_entry.pack(pady=10)

        def update_color(*args):
            
            # Trong Python, *args là một cách nói với hàm rằng: "Tôi không biết người ta sẽ truyền bao nhiêu tham số vào đây, nên cậu cứ gom tất cả chúng lại thành một cái danh sách (tuple) cho tôi."
            # *: Dấu sao này là toán giả "unpacking".
            # args: Chỉ là cái tên (viết tắt của arguments). Cậu đặt là *keo_ngot hay *thong_tin cũng được, nhưng dân lập trình hay dùng *args cho đúng chuẩn. 
            
            try:
                # Lấy giá trị từ các biến IntVar
                r, g, b = [max(0, min(255, v.get())) for v in (r_var, g_var, b_var)]
                hex_val = f"#{r:02x}{g:02x}{b:02x}".upper()
                color_display.configure(bg=hex_val)
                hex_entry.delete(0, tkinter.END)
                hex_entry.insert(0, hex_val)
            except: 
                pass

        def CreateRow(label, var, color): # Sửa lại tên hàm cho đúng
            f = tkinter.Frame(cp_window, bg="#2c3e50")
            f.pack(fill="x", padx=30, pady=5)
            tkinter.Label(f, text=label, fg=color, bg="#2c3e50", font=("Arial", 10, "bold"), width=5).pack(side="left")
            
            # Thanh trượt Scale
            scale = tkinter.Scale(f, from_=0, to=255, orient="horizontal", variable=var, 
                                 bg="#2c3e50", fg="white", highlightthickness=0, command=update_color)
            scale.pack(side="left", fill="x", expand=True, padx=10)
            
            # Ô nhập số
            entry = tkinter.Entry(f, textvariable=var, width=5)
            entry.pack(side="right")
            var.trace_add("write", update_color)

        CreateRow("Red", r_var, "#ff1900")
        CreateRow("Green", g_var, "#00ff6a")
        CreateRow("Blue", b_var, "#001aff")

        update_color()

root = tkinter.Tk()
root.title("Main Menu")
root.attributes('-zoomed', True)
                    
def set_dynamic_background(root_window, image_path):
    try:
        original_img = Image.open(image_path)
        root_window.original_bg_image = original_img 
        placeholder_photo = ImageTk.PhotoImage(original_img.resize((1, 1)))
        bg_label = tkinter.Label(root_window, image=placeholder_photo)
        bg_label.photo = placeholder_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        def resize_image(event):
            curr_width = root_window.winfo_width()
            curr_height = root_window.winfo_height()
            
            if curr_width < 10 or curr_height < 10:
                return
            resized_img = root_window.original_bg_image.resize((curr_width, curr_height), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_img, master=root_window)
            bg_label.config(image=tk_image)
            root_window.tk_background_image = tk_image
        root_window.bind('<Configure>', resize_image)
        
    except Exception as e:
        print(f"Lỗi: {e}")
        root_window.config(bg="white")

set_dynamic_background(root, r"D:\vscode\snake.io\genshin.png")
# ------------------------------

top_frame = tkinter.Frame(root, bg="black") 
top_frame.place(relx=0.5, y=50, anchor="n") 

welcome_label = tkinter.Label(top_frame, text="Welcome to Multi-Matical", 
                              font=("Arial", 20, "bold"), fg="white", bg="black")
welcome_label.pack()

button_frame = tkinter.Frame(root, bg="")

main_button = tkinter.Button(root, text="CALCULATOR", command=calculator.open_calculator, 
                             bg="#4CAF50", font=("Arial", 12, "bold"), width=20, pady=10)

button_converter = tkinter.Button(root, text=" CONVERTER ", command=converter.open_converter, 
                             bg="#4CAF50", font=("Arial", 12, "bold"), width=20, pady=10)

button_graph = tkinter.Button(root, text="  DIAGRAM  ", command=graph.open_graph, 
                             bg="#4CAF50", font=("Arial", 12, "bold"), width=20, pady=10)

button_graph3d = tkinter.Button(root, text="  3D DIAGRAM  ", command=graph_3D.open_graph3d, 
                             bg="#4CAF50", font=("Arial", 12, "bold"), width=20, pady=10)

button_snake = tkinter.Button(root, text="  Snake.io  ", command=snake_game.open_snake,
                             bg="#ff0000", font=("Arial", 12, "bold"), width=15, pady=10)

button_color = tkinter.Button(root, text="COLOR TOOLS", command=colorpicker.open_picker,
                              bg="#4CAF50", font=("Arial", 12, "bold"), width=20, pady=10)

main_button.place(x=50, y=150)
button_converter.place(x=50, y=230)
button_graph.place(x=50, y=310)
button_graph3d.place(x=50, y=390)
button_color.place(x=50, y=470)
button_snake.place(relx=1.0, y=150, anchor="ne", x=-50)
root.mainloop()