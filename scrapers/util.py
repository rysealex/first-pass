import sqlite3
import os
from pygame import mixer

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/jobs.db')

def init_audio():
    mixer.init()

def play_notification():
    try:
        mixer.music.load('../static/audio/notify.mp3')
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
        """, job_id, company, role, link, source)

        conn.commit()
        print(f"New Job Found: {company} - {role}")
        play_notification()
        return True
    except sqlite3.IntegrityError:
        # triggers if job is a duplicate
        return False
    finally:
        conn.close()