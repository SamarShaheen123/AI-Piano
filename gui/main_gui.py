import tkinter as tk
import time
from utils.helpers import play_note
from lessons.beginner import get_current_note, check_note, lesson_complete
from database.db import save_practice
from ai.recommender import get_recommendations

# ---------------- GLOBAL STATE ----------------
recorded_notes = []
last_time = None
canvas = None
status = None
lesson_label = None

key_map = {
    'a': 'C',
    's': 'D',
    'd': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'A',
    'j': 'B'
}

# ---------------- BEGINNER HELP ----------------
def highlight_correct_key():
    if canvas is None:
        return
    note = get_current_note()
    items = canvas.find_withtag(note)
    for item in items:
        canvas.itemconfig(item, outline="green", width=4)

# ---------------- KEYBOARD INPUT ----------------
def on_key_press(event):
    global last_time

    key = event.char.lower()
    if key in key_map:
        note = key_map[key]
        play_note(note)

        now = time.time()
        delay = 0 if last_time is None else round(now - last_time, 2)
        last_time = now
        recorded_notes.append((note, delay))

        if check_note(note):
            status.config(text="Correct ✅", fg="green")
        else:
            status.config(text="Wrong ❌ Try again", fg="red")

        if lesson_complete():
            status.config(text="Lesson Complete 🎉", fg="blue")

        lesson_label.config(text=f"Play this note: {get_current_note()}")
        highlight_correct_key()

# ---------------- REPLAY ----------------
def replay():
    for note, delay in recorded_notes:
        time.sleep(delay)
        play_note(note)

# ---------------- CLEAR & SAVE ----------------
def clear_recording():
    global last_time
    save_practice(recorded_notes, lesson_complete())
    recorded_notes.clear()
    last_time = None
    status.config(text="Practice saved ✔", fg="green")

# ---------------- AI RECOMMENDATIONS ----------------
def show_recommendations():
    recs = get_recommendations()
    status.config(
        text=f"Practice these notes: {', '.join(recs)} 🎯",
        fg="purple"
    )

# ---------------- MAIN UI ----------------
def launch_piano():
    global canvas, status, lesson_label, last_time

    root = tk.Tk()
    root.title("AI Piano Tutor")
    root.geometry("950x500")

    root.bind("<KeyPress>", on_key_press)

    lesson_label = tk.Label(
        root,
        text=f"Play this note: {get_current_note()}",
        font=("Arial", 18)
    )
    lesson_label.pack(pady=10)

    status = tk.Label(root, text="", font=("Arial", 14))
    status.pack(pady=5)

    # 🎹 Piano Canvas
    canvas = tk.Canvas(root, width=700, height=260)
    canvas.pack(pady=20)

    white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    black_keys = {'C': 'C#', 'D': 'D#', 'F': 'F#', 'G': 'G#', 'A': 'A#'}

    white_width = 100
    black_width = 60

    # ---------- Animation ----------
    def animate_key(note):
        items = canvas.find_withtag(note)
        for item in items:
            original = canvas.itemcget(item, "fill")
            canvas.itemconfig(
                item,
                fill="lightblue" if original == "white" else "gray"
            )
            root.after(
                150,
                lambda i=item, c=original: canvas.itemconfig(i, fill=c)
            )

    # ---------- Mouse Click ----------
    def play_click(event):
        global last_time
        items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in items:
            tags = canvas.gettags(item)
            if tags:
                note = tags[0]
                play_note(note)

                now = time.time()
                delay = 0 if last_time is None else round(now - last_time, 2)
                last_time = now
                recorded_notes.append((note, delay))

                animate_key(note)

    # ---------- Draw Keys ----------
    for i, note in enumerate(white_keys):
        x1 = i * white_width
        x2 = x1 + white_width

        canvas.create_rectangle(
            x1, 0, x2, 250,
            fill="white",
            outline="black",
            tags=note
        )
        canvas.create_text(x1 + 50, 230, text=note)

        if note in black_keys:
            bx = x2 - (black_width // 2)
            canvas.create_rectangle(
                bx, 0, bx + black_width, 150,
                fill="black",
                tags=black_keys[note]
            )

    canvas.bind("<Button-1>", play_click)
    highlight_correct_key()

    # ---------- Controls ----------
    control_frame = tk.Frame(root)
    control_frame.pack(pady=20)

    tk.Button(
        control_frame,
        text="Get Practice Suggestions",
        command=show_recommendations,
        bg="lightgreen",
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        control_frame,
        text="Replay Recording",
        command=replay,
        bg="lightblue",
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        control_frame,
        text="Clear Recording",
        command=clear_recording,
        bg="lightgray",
        font=("Arial", 12)
    ).pack(side=tk.LEFT, padx=10)

    root.mainloop()