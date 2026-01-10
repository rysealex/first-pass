import sqlite3
import os
import random
import time
from pygame import mixer

AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/audio'))

def get_dynamic_playlist():
    if not os.path.exists(AUDIO_DIR):
        print(f"Audio directory not found: {AUDIO_DIR}")
        return []

    # gather all mp3 files in the audio directory
    return [
        os.path.join(AUDIO_DIR, f) 
        for f in os.listdir(AUDIO_DIR) 
        if f.lower().endswith('.mp3')
    ]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'jobs.db')

def init_audio():
    mixer.init()

def play_notification():

    MP3_PLAYLIST = get_dynamic_playlist()
    
    if not MP3_PLAYLIST:
        print("No audio files found for notification")
        return

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