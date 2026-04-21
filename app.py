from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# LOAD DATA

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"lost": [], "found": []}

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"lost": [], "found": []}


# =========================
# SAVE DATA
# =========================
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# HOME (LOGIN PAGE)
# =========================
@app.route('/')
def home():
    return render_template('login.html')


# =========================
# LOGIN ROUTE
# =========================
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Simple validation
    if username and password:
        return redirect(url_for('index'))

    return "Invalid Credentials"


# =========================
# INDEX PAGE
# =========================
@app.route('/index')
def index():
    return render_template('index.html')


# =========================
# LOST ITEM
# =========================
@app.route('/lost', methods=['GET', 'POST'])
def lost():
    data = load_data()

    if request.method == 'POST':
        data["lost"].append({
            "name": request.form.get('name'),
            "desc": request.form.get('desc'),
            "location": request.form.get('location'),
            "date": request.form.get('date')
        })

        save_data(data)
        return redirect(url_for('dashboard'))

    return render_template('lost.html')


# =========================
# FOUND ITEM
# =========================
@app.route('/found', methods=['GET', 'POST'])
def found():
    data = load_data()

    if request.method == 'POST':
        data["found"].append({
            "name": request.form.get('name'),
            "desc": request.form.get('desc'),
            "location": request.form.get('location'),
            "date": request.form.get('date')
        })

        save_data(data)
        return redirect(url_for('dashboard'))

    return render_template('found.html')


# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():
    data = load_data()

    lost_items = data.get("lost", [])
    found_items = data.get("found", [])

    matches = []

    for l in lost_items:
        for f in found_items:
            if l.get("name", "").lower() == f.get("name", "").lower():
                matches.append({
                    "lost": l,
                    "found": f
                })

    return render_template(
        "dashboard.html",
        lost=lost_items,
        found=found_items,
        matches=matches
    )



# RUN SERVER

if __name__ == "__main__":
    app.run(debug=True)