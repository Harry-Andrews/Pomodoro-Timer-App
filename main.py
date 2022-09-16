import tkinter as tk
import math
from pygame import mixer

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
check_marks = ""
reset = False

# ------------------------- DING NOTIFICATION ---------------------------- #

mixer.init()
mixer.music.load("ding.mp3")


def ding():
    mixer.music.play()
    mixer.music.play(loops=0)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    global reset
    global check_marks
    reps = 0
    reset = True
    timer_label.config(text="Timer", fg=GREEN)
    check_mark_label.config(text="")
    canvas.itemconfig(timer_text, text="00:00")
    check_marks = ""


# --------------------------- TIMER MECHANISM ------------------------------ #
def start_timer():
    global reps
    global reset
    reset = False
    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    reps += 1
    ding()
    if reps % 2 == 1:
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_seconds)
    elif reps % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        count_down(long_break_seconds)

    else:
        timer_label.config(text="Break", fg=PINK)
        count_down(short_break_seconds)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global check_marks
    if not reset:
        minutes = math.floor(count / 60)
        seconds = count % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
        if count > 0:
            window.after(1000, count_down, count - 1)
        else:
            start_timer()
            if reps % 2 == 0:
                check_marks += "✔"
                check_mark_label.config(text=f"{check_marks}")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW, highlightthickness=0)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100,
                                130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

timer_label = tk.Label(text="Timer", fg=GREEN, font=(FONT_NAME, 35, "bold"), bg=YELLOW, pady=10)
timer_label.grid(row=0, column=1)
check_mark_label = tk.Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
check_mark_label.grid(row=4, column=1)

start_button_img = tk.PhotoImage(file="start_button.png")
# This image was taken from the author FreePik on flaticon.com
start_button = tk.Button(highlightthickness=0, image=start_button_img, borderwidth=0, bg=YELLOW, command=start_timer)
start_button.grid(row=3, column=0)
reset_button_img = tk.PhotoImage(file="reset_button.png")
# This image was taken from the author FreePik on flaticon.com
reset_button = tk.Button(highlightthickness=0, image=reset_button_img, borderwidth=0, bg=YELLOW, command=reset_timer)
reset_button.grid(row=3, column=2)

window.mainloop()
