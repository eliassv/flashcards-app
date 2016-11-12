from flashcard_app import app
from flask import request, make_response, render_template, current_app, url_for
import uuid, json, os

@app.route("/")
def index():
    return "<h1>Flashcard App!</h1>"

@app.route("/new")
def new():      
    random = str(uuid.uuid4())
    return render_template("new.html", randname=random)

@app.route("/createfile", methods=["GET", "POST"])
def createfile():
    if request.method == "POST":
        fname = request.form.get('filename')
        titulo = request.form.get('titulo')

        response = make_response("Filename Salvo!")
        response.set_cookie("filename", fname)
        
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
        cards = []
        cards.append(titulo)

        with open(path, mode="w") as f:
            json.dump(cards, f)

        return response

@app.route("/read")
def read():
    f = request.cookies.get('filename')
    print(f)
    return "OK"