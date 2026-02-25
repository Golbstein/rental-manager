# Deploy SkiLuxe Dashboard to PythonAnywhere

This guide walks you through deploying the rental-manager app to PythonAnywhere (free tier works).

## 1. Create a PythonAnywhere account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account

## 2. Upload your project

### Option A: Clone from Git (if your repo is on GitHub)

In the **Consoles** tab → start a **Bash** console:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/rental-manager.git
cd rental-manager
```

### Option B: Upload files manually

1. Go to **Files** tab
2. Create a folder: `rental-manager`
3. Upload these files into it:
   - `app.py`
   - `index.html`
   - `data.csv` (optional – will be created empty if missing)
   - `requirements.txt`
   - `wsgi.py`
   - `logo.png` (optional)

## 3. Create a virtualenv and install dependencies

In a **Bash** console:

```bash
cd ~/rental-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Create the Web app

1. Go to the **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration** (not the Flask wizard)
4. Select **Python 3.10** (or whatever version is offered)
5. Click **Next** until the app is created

## 5. Configure the WSGI file

1. In the **Web** tab, scroll to **Code** → **WSGI configuration file**
2. Click the link (e.g. `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. Replace the contents with:

```python
import sys
import os

# Replace YOUR_USERNAME with your PythonAnywhere username
project_home = '/home/YOUR_USERNAME/rental-manager'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

# Admin password for full access; others see read-only viewer mode
os.environ.setdefault('ADMIN_PASSWORD', 'choose-a-strong-password')
os.environ.setdefault('SECRET_KEY', 'change-this-to-a-random-32-char-string')

from app import application
```

Replace `YOUR_USERNAME` with your PythonAnywhere username. **Change** `ADMIN_PASSWORD` and `SECRET_KEY` to your own values before going live.

**Important:** After setting the virtualenv path in Step 6, PythonAnywhere will automatically use it when loading the app. No need to activate it in the WSGI file.

4. Save the file

## 6. Set virtualenv path

1. Back in the **Web** tab
2. Find **Virtualenv**
3. Enter: `/home/YOUR_USERNAME/rental-manager/venv`
4. Click the checkmark

## 7. Reload the app

Click **Reload** under your web app. Your dashboard should be live at:

**https://YOUR_USERNAME.pythonanywhere.com**

---

## Admin access

- By default, everyone sees the dashboard in **viewer mode** (read-only).
- To add, edit, delete, or reset data: click **Unlock admin**, enter the `ADMIN_PASSWORD` you set in the WSGI file.
- After unlocking, click **Lock (viewer mode)** to switch back.

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| 500 Internal Server Error | Open **Web** → **Error log**; check the latest error message |
| Module not found | Ensure virtualenv path is set and `pip install -r requirements.txt` ran successfully |
| Data not saving | Free tier allows writes to your home directory; `data.csv` will be in `~/rental-manager/` |
| Logo missing | Upload `logo.png` to the project folder; the app hides it gracefully if missing |
| Unlock not working | Ensure `ADMIN_PASSWORD` is set in the WSGI file (before `from app import application`) |

## Run locally with Flask (optional)

To run the same app locally:

```bash
cd rental-manager
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

Set `ADMIN_PASSWORD` and `SECRET_KEY` env vars before running, e.g.:

```bash
export ADMIN_PASSWORD="your-password"
export SECRET_KEY="a-random-32-char-string"
flask run
```

Then open http://127.0.0.1:5000
