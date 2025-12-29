import sqlite3
import os
from pygame import mixer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'jobs.db')

def init_audio():
    mixer.init()

def play_notification():
    try:
        if mixer.music.get_busy():
            print("Audio skipped: Notification already playing")
            return
        
        mixer.music.load('../static/audio/yeat.mp3')
        mixer.music.play()
    except Exception as e:
        print(f"Audio error: {e}")

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
        play_notification()
        return True
    except sqlite3.IntegrityError:
        # triggers if job is a duplicate
        return False
    finally:
        conn.close()