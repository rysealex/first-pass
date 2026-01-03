import sqlite3
import os
import random
import time
from pygame import mixer

MP3_PLAYLIST = [
    '../static/audio/yeat.mp3',
    '../static/audio/espeak.mp3',
    '../static/audio/topgun.mp3'
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'jobs.db')

def init_audio():
    mixer.init()

def play_notification():
    try:
        if mixer.music.get_busy():
            print("Audio skipped: Notification already playing")
            return
        
        # pick a song to play at random
        song_to_play = random.choice(MP3_PLAYLIST)
        mixer.music.load(song_to_play)
        mixer.music.play()

        print(f"Playing: {song_to_play}")

        while mixer.music.get_busy():
            time.sleep(0.1) # wait for music to finish playing

    except Exception as e:
        print(f"Audio error: {e}")

def is_snoozed():
    if not os.path.exists('../snooze.txt'):
        return False
    with open('../snooze.txt', 'r') as f:
        return f.read().strip() == '1'

def save_job(job_id, company, role, link, source):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO jobs (job_id, company, role, link, source)
            VALUES (?, ?, ?, ?, ?)
        """, (job_id, company, role, link, source))

        conn.commit()
        print(f"New Job Found: {company} - {role}")
        # check if the user has snoozed notifications
        if not is_snoozed():
            play_notification()
        return True
    except sqlite3.IntegrityError:
        # triggers if job is a duplicate
        return False
    finally:
        conn.close()