from flask import Flask,render_template,url_for
from graph_data import *
import json
app = Flask(__name__)
@app.route('/')


def getNodes():
    return nodes

def getLinks():
    return links
    

def index():
    graph = {getNodes(),getLinks()}
    return render_template('index.html', data=json.dumps(graph))

if __name__ == "__main__":
    app.run(debug=True)
