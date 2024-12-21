from flask import Flask, request, jsonify, render_template
import json
from datetime import time, date, datetime
import os

import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST")
    )
    return conn


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (time, datetime)):
            return obj.strftime('%H:%M:%S')
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


# Register the custom encoder
app.json_encoder = CustomJSONEncoder


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/events', methods=['GET', 'POST'])
def manage_events():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        # Handle adding regular events
        data = request.json
        cursor.execute(
            "INSERT INTO events (member_id, event_name, event_date, event_time, description) VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (data['member_id'], data['event_name'], data['event_date'], data['event_time'], data['description'])
        )
        new_event = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(new_event), 201

    elif request.method == 'GET':
        # Fetch today's regular and recurring events
        today = date.today()
        day_of_week = today.strftime('%A')  # Get day of the week (e.g., 'Monday')

        # Fetch regular events for today
        cursor.execute("""
            SELECT events.id, events.event_name, events.event_date, events.event_time, events.description,
                   family_members.name AS member_name
            FROM events
            JOIN family_members ON events.member_id = family_members.id
            WHERE event_date = %s
            ORDER BY event_time ASC
        """, (today,))
        regular_events = cursor.fetchall()

        # Fetch recurring events for today's day of the week
        cursor.execute("""
            SELECT recurring_events.id, recurring_events.event_name, recurring_events.event_time, recurring_events.description,
                   family_members.name AS member_name
            FROM recurring_events
            JOIN family_members ON recurring_events.member_id = family_members.id
            WHERE day_of_week = %s
            ORDER BY event_time ASC
        """, (day_of_week,))
        recurring_events = cursor.fetchall()

        cursor.close()
        conn.close()

        # Combine both regular and recurring events
        all_events = sorted(regular_events + recurring_events, key=lambda x: x['event_time'])

        return jsonify(all_events)


@app.route('/recurring-events', methods=['POST'])
def add_recurring_event():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recurring_events (member_id, event_name, event_time, description, day_of_week)
        VALUES (%s, %s, %s, %s, %s) RETURNING *
    """, (data['member_id'], data['event_name'], data['event_time'], data['description'], data['day_of_week']))
    new_event = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_event), 201


@app.route('/members', methods=['GET'])
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM family_members")
    members = cursor.fetchall()
    cursor.close()
    conn.close()

    # Return members as a JSON list
    return jsonify([{"id": member[0], "name": member[1]} for member in members])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

