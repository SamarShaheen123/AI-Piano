import pygame
import os

pygame.mixer.init()

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
SOUND_PATH = os.path.join(BASE_PATH, "sound", "notes")

def play_note(note):
    file_path = os.path.join(SOUND_PATH, f"{note}.wav")
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()