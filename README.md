# chung toi yeu lap trinh
# Multi-Matical Supporter

Multi-Matical Supporter is a versatile desktop application, which is written in Python that integrates mathematical tools, visual physics, and entertainment features all in a single interface.

## Main feature

* **Calculator:** A basic electronic calculator with an intuitive interface, supporting addition, subtraction, multiplication, division, and percentage calculations.
* **Physics Ultra Converter:** A versatile unit converter for distance, mass, time, voltage, and pressure.
* **2D Diagram:** A tool for drawing and interacting with the graph of a cubic function (y = ax^3 + bx^2 + cx + d) with a slider to adjust the coefficients in real time.
* **3D Diagram:** This 3D interactive simulation space between a plane and a sphere allows for changing vectors and parameters to examine relative positions (intersecting, tangent, detached).
* **COLOR TOOLS** This toolkit is specifically designed for in-depth color customization for content creation, supporting HEX and RGB colors code.
* **Snake.io:** This game integrates the classic Snake game, supporting two players simultaneously with specially improved items and features.

## System requirements

To run Multi-Matical Supporter, your computer needs to have **Python 3.8+** and the following libraries installed:

* `tkinter` (usually pre-installed with Python)
* `turtle` (usually pre-installed with Python)
  *Note: Linux users may need to run `sudo apt-get install python-tk` if Tkinter is missing.*
* `numpy`
* `matplotlib`
* `Pillow`
* `pygame`

## Installation instructions

1.  **Clone the source code to your computer:**
    ```bash
    git clone [https://github.com/sgamings182-lang/chungtoiyeulaptrinh](https://github.com/sgamings182-lang/chungtoiyeulaptrinh)
    cd chungtoiyeulaptrinh
    ```

2.  **Install the dependent libraries:**
    You can quickly install libraries using pip:
    ```bash
    pip install numpy matplotlib Pillow pygame
    ```

3.  **Download image resources (Assets):**
    Make sure you have placed the `genshin.png` wallpaper file and the Snake game image folder in the correct directory path `D:\vscode\snake.io\` (or modify the path in the source code to suit your machine).

## User Manual

Run the main source code file using the command:

    ```bash
    python main.py
    When the main menu appears, simply click on the corresponding buttons (CALCULATOR, CONVERTER, DIAGRAM, 3D DIAGRAM, COLOR TOOLS, Snake.io) to open the feature modules as independent windows.
Keyboard controls in Snake.io:

Player 1: Use the W, A, S, D keys to move.

Player 2: Use the Arrow keys to move.

Pause/Resume: Press the SPACE key.

Contributions
All contributions to the project are welcome! If you find bugs or want to suggest new features, please create an Issue or submit a Pull Request.

License
This project is distributed under the MIT license. See the LICENSE file for more details.
