from flask import Flask, render_template, session, request, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'the session secret !"#€%"'

"""
1. application GUI:
    / (initial form)
    /game (the game interface)
    /game/quit reset the session and

2. internal requests: (application layer)
    /game/i/new
    /game/i/update
    /game/i/status

3. ai logic

"""

### GAME INTERFACE ###
@app.route("/")
def index():
    return render_template('start.html')

@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'POST' and 'username' in request.form:
        session["username"] = request.form['username']
        session["status"] = {
            'candidates': [],
            'guesswhos': [],
            'clues': []
        }

    if "username" in session and len(session["username"])>0:
        print(len(session["username"]))
        return render_template('layout.html', username=session["username"])
    else:
        return redirect(url_for('index'))

@app.route("/game/quit")
def quit():
    session.pop('username', None)
    session.pop('status', None)
    return redirect(url_for('index'))


###  ###
@app.route('/game/i/update', methods=['POST'])
def update():
    if request.method == 'POST':
        if 'clue' in request.form:
            session["status"]["clues"].append(request.form["clue"])

    # TODO: BASED THE CLUES, UPDATE THE STATUS

    return json.dumps(session["status"])
