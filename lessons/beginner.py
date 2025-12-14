lesson_notes = ["C", "D", "E", "F"]
current_step = 0

def get_current_note():
    return lesson_notes[current_step]

def check_note(played_note):
    global current_step
    if played_note == lesson_notes[current_step]:
        current_step += 1
        return True
    return False

def lesson_complete():
    return current_step >= len(lesson_notes)