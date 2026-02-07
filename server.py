import http.server
import json
import os
import csv
import shutil

PORT = 8000
DATA_FILE = 'data.csv'
# The complete list of columns we want to track now
FIELDS = ['id', 'date', 'apt', 'type', 'category', 'amount', 'posFee', 'myShare', 'desc', 'method', 'platform']


def migrate_csv_if_needed():
    """
    Checks if data.csv exists and has the old structure.
    If so, it adds the missing 'method' and 'platform' columns
    so you don't lose your data.
    """
    if not os.path.exists(DATA_FILE):
        return

    # 1. Read the current header
    with open(DATA_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return  # Empty file

    # 2. If header matches new format, we are good
    if header == FIELDS:
        return

    print("🔧 Upgrading data.csv to new format...")

    # 3. Read all existing data
    rows = []
    with open(DATA_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Add default values for missing columns
            if 'method' not in row: row['method'] = '-'
            if 'platform' not in row: row['platform'] = '-'

            # Re-order row to match new FIELDS
            new_row = {field: row.get(field, '-') for field in FIELDS}
            rows.append(new_row)

    # 4. Backup old file just in case
    shutil.copy(DATA_FILE, 'data.csv.bak')

    # 5. Write new file with correct headers
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print("✅ Upgrade complete. Backup saved as data.csv.bak")


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/load':
            data = []
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if self.path == '/save':
            data = json.loads(post_data.decode('utf-8'))
            file_exists = os.path.exists(DATA_FILE)

            with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                if not file_exists:
                    writer.writeheader()

                # Ensure we only write fields that exist in our schema
                row_to_write = {k: data.get(k, '-') for k in FIELDS}
                writer.writerow(row_to_write)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "saved"}')

        elif self.path == '/delete':
            req = json.loads(post_data.decode('utf-8'))
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

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "deleted"}')

        elif self.path == '/reset':
            with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "reset"}')


# Run migration check on startup
migrate_csv_if_needed()

print(f"✅ Dashboard running at http://localhost:{PORT}")
http.server.HTTPServer(('', PORT), RequestHandler).serve_forever()
