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

from app import application
```

Replace both instances of `YOUR_USERNAME` with your PythonAnywhere username (e.g. `jenia` → `/home/jenia/rental-manager`).

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

## Troubleshooting

| Problem | Fix |
|--------|-----|
| 500 Internal Server Error | Open **Web** → **Error log**; check the latest error message |
| Module not found | Ensure virtualenv path is set and `pip install -r requirements.txt` ran successfully |
| Data not saving | Free tier allows writes to your home directory; `data.csv` will be in `~/rental-manager/` |
| Logo missing | Upload `logo.png` to the project folder; the app hides it gracefully if missing |

## Run locally with Flask (optional)

To run the same app locally:

```bash
cd rental-manager
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

Then open http://127.0.0.1:5000
