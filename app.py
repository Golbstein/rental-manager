"""
Flask WSGI app for PythonAnywhere deployment.
Mirrors the API from server.py for use with the existing frontend.
"""
import json
import os
import csv
import shutil

from flask import Flask, request, send_from_directory

app = Flask(__name__, static_folder='.')

# Use project directory for data file (works on PythonAnywhere)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.csv')
FIELDS = ['id', 'date', 'apt', 'type', 'category', 'amount', 'posFee', 'myShare', 'desc', 'method', 'platform']


def migrate_csv_if_needed():
    """Upgrade data.csv if it has old structure (add method, platform columns)."""
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return
    if header == FIELDS:
        return
    rows = []
    with open(DATA_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'method' not in row:
                row['method'] = '-'
            if 'platform' not in row:
                row['platform'] = '-'
            new_row = {field: row.get(field, '-') for field in FIELDS}
            rows.append(new_row)
    shutil.copy(DATA_FILE, DATA_FILE + '.bak')
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


# Run migration on import
migrate_csv_if_needed()


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/logo.png')
def logo():
    path = os.path.join(BASE_DIR, 'logo.png')
    return send_from_directory(BASE_DIR, 'logo.png') if os.path.exists(path) else ('', 404)


@app.route('/load')
def load():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    return data


@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        row_to_write = {k: data.get(k, '-') for k in FIELDS}
        writer.writerow(row_to_write)
    return {'status': 'saved'}


@app.route('/delete', methods=['POST'])
def delete():
    req = request.get_json()
    target_id = str(req['id'])
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if str(row['id']) != target_id:
                    rows.append(row)
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return {'status': 'deleted'}


@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    target_id = str(data.get('id', ''))
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if str(row['id']) == target_id:
                    row = {k: data.get(k, row.get(k, '-')) for k in FIELDS}
                rows.append(row)
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return {'status': 'updated'}


@app.route('/reset', methods=['POST'])
def reset():
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
    return {'status': 'reset'}


# WSGI entry point for PythonAnywhere
application = app
