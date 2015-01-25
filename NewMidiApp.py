# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, Response, send_file, make_response
from melgen import *

DEBUG = False

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')


# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/information/', methods=['POST'])
def information():
    name = str(request.form['name'])
    tempo = int(request.form['tempo'])
    key = str(request.form['key'])
    m = str(request.form['m'])
    maxD = int(request.form['maxD'])
    root = bool(request.form['root'])
    smallestNote = int(request.form['smallestNote'])
    biggestNote = int(request.form['biggestNote'])
    length = int(request.form['length'])
    startOct = int(request.form['startOct'])
    myMIDI = make_midi(name, tempo, key, m, maxD, root, smallestNote, biggestNote, length, startOct)

    new_file = open('myMIDI.mid', 'wb')
    myMIDI.writeFile(new_file)
    new_file.close()
    new_file = open('myMIDI.mid', 'rb')


    return send_file(new_file, mimetype='audio/midi')

if __name__ == '__main__':
    app.run()


