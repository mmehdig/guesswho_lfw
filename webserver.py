# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory
import json
import pickle
from parser_imp import parser, attributes

app = Flask(__name__)
app.secret_key = 'the session secret !"#€%"'

"""
1. application GUI:
    / (initial form)
    /game (the game interface)
    /game/quit reset the session and

2. internal requests: (application layer)
    /game/i/update

3. the logic

"""

# read the preprocessed embeddings from file:
with open('dataset/embeddings/embeddings_align', 'rb') as f:
    embeddings = pickle.load(f, encoding='latin1')

# image paths
with open('dataset/embeddings/imgpaths', 'rb') as f:
    imgpaths = pickle.load(f)

### GAME INTERFACE ###
@app.route("/")
def index():
    return render_template('start.html')

@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'POST' and 'username' in request.form:
        session["username"] = request.form['username']

        # initialize with a set of random images:
        import random
        random_context = random.sample(imgpaths, 10)
        session["status"] = {
            'context': random_context, # random context
            'guesswhos': random_context, # initialize the guess with all possible items
            'clues': [0 for _ in attributes]
        }

    if "username" in session and len(session["username"])>0:
        return render_template('layout.html', username=session["username"])
    else:
        return redirect(url_for('index'))

@app.route("/game/quit")
def quit():
    session.pop('username', None)
    session.pop('status', None)
    return redirect(url_for('index'))

### show an image from dataset ###
@app.route('/img/<path:filename>')
def show_image(filename):
    return send_from_directory("dataset/", filename)

### All the interactions with GUI and server lands here ###
@app.route('/game/i/update', methods=['POST'])
def update():
    """
    This function takes messages coming from web interface, then updates "status" on the server and the web interface.
    The message needs to be parsed in order to infer its meaning.
    """
    status = session["status"]

    # using parser to infer the intended clue, then update the old clue.
    # if new clue has contradiction with old one, it will remove both of them.
    import numpy as np
    new_clue = np.array(parser(request.form["clue"]))
    old_clue = np.array(status["clues"])
    infered_clue = np.sign(new_clue + old_clue)
    status["clues"] = list(np.asscalar(i) for i in infered_clue)

    # TODO: BASED ON THE CURRENT CLUES UPDATE THE GUESSWHOS AND THE STATUS
    # a sub set of the context, use classifier to guesswho, based on the clues
    #
    
    #get the embeddings for the images
    chosenimgpaths = status["context"]
    faceembeddings = [embeddings[imgpaths.index(path)] for path in chosenimgpaths]
    with open("classifiers", 'rb') as f:
         classifier_list = pickle.load(f)
    
    
    
    #classify the faces
    results = []
    for i,classifier in enumerate(classifier_list):
         clf = classifier
         y_guess =clf.predict(faceembeddings)
         results.append(y_guess)
    
    #combine face with classification
    classifiedface = []
    for i,path in enumerate(chosenimgpaths):
        classifiedface.append((path,[]))
        for result in results:
            classifiedface[i][1].append(result[i])
     
    #remove the faces that are inconsistent with the current clue       
    not_ok = []
    for i, attribute in enumerate(status["clues"]):
        #print(attributes[i])
        #print(attribute)
        for face in classifiedface:
            #print(face[0])
            #print(face[1][i])
            if attribute*face[1][i]<0:
                not_ok.append(face)
    
    new_context = [face[0] for face in classifiedface if face not in not_ok]
    
    status["guesswhos"] = new_context
    

    # update the server status:
    session["status"] = status

    # send it to the web interface in order to update its status:
    return json.dumps(session["status"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context='adhoc', debug=True)
