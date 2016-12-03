from flashcard_app import app
from flask import request, make_response, render_template, current_app, url_for
from werkzeug import secure_filename
import uuid, os
from tmpfile import tmpfile


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/createcards", methods=["GET", "POST"])
def createcards():
    if request.method == "POST":
        fname = request.form.get('filename')
        title = request.form.get('titulo')
        
        cards = []
        cards.append(title)
        tmpfile.save_new_fname(cards, fname)

        response = make_response(render_template("addcards.html"))
        response.set_cookie("filename", fname)
        return response
    
    random = str(uuid.uuid4())
    return render_template("createcards.html", randname=random)


@app.route("/createcards/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        formdata = request.form.to_dict()
        
        cards = tmpfile.load()
        cards.append(formdata)
        tmpfile.save(cards)

        ok = "Card {} adicionado com sucesso!".format( len(cards) - 1 )
        return render_template('addcards.html', mensagem=ok)
        
    return render_template('addcards.html')


@app.route("/createcards/download_file")
def download_file():
    cards = tmpfile.load()
    new_fname = secure_filename(cards[0])
    tmpfile.save_new_fname(cards, new_fname)

    download = url_for('static', filename=("temp/" + new_fname + ".txt"))
    return render_template('download.html', download=download)


@app.route("/opencards", methods=["GET", "POST"])
def opencards():
    if request.method == "POST":
        thefile = request.files.get('cardsfile')

        fname = str(uuid.uuid4())
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
        thefile.save(path)
        
        try:
            cards = tmpfile.load_path(path) 
            title = cards[0]
            num_itens = len(cards)

            return render_template('showcards.html', cards=cards, num_itens=num_itens, titulo=title)
        
        except:
            return render_template("load_error.html")         

    return render_template('uploadcards.html')
