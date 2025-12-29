from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import mailer

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'jobs.db')

def get_app_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/jobs')
def get_jobs():
    conn = get_app_connection()
    # only fetch jobs that haven't been saved or deleted
    jobs = conn.execute(
        "SELECT * FROM jobs WHERE status = 'new' ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(job) for job in jobs])

@app.route('/api/action', methods=['POST'])
def job_action():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data sent"}), 400
    
    job_id = data.get('id')
    action = data.get('action') # either save or delete

    conn = get_app_connection()
    if action == 'save':
        job = conn.execute(
            "SELECT * FROM jobs WHERE id = ?", (job_id,)
        ).fetchone()
        # trigger email logic here later
        conn.execute(
            "UPDATE jobs SET status = 'saved' WHERE id = ?", (job_id,)
        )
    else:
        conn.execute(
            "UPDATE jobs SET status = 'deleted' WHERE id = ?", (job_id,)
        )

    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)