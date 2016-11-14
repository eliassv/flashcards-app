from flashcard_app import app
from flask import request, make_response, render_template, current_app, url_for
from werkzeug import secure_filename
import uuid, json, os


@app.route("/")
def index():
    return "<h1>Flashcard App!</h1>"


@app.route("/new")
def new():      
    random = str(uuid.uuid4())
    return render_template("new.html", randname=random)


@app.route("/createcards", methods=["GET", "POST"])
def createcards():
    if request.method == "POST":
        fname = request.form.get('filename')
        title = request.form.get('titulo')
        
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
        cards = []
        cards.append(title)

        with open(path, mode="w") as f:
            json.dump(cards, f)

        response = make_response(render_template("addcards.html"))
        response.set_cookie("filename", fname)

        return response


@app.route("/createcards/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        formdata = request.form.to_dict()
        
        # Carrega arquivo temporário
        fname = request.cookies.get('filename')
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
        cards = []
        with open(path, mode="r") as f:
            cards = json.load(f)
        
        # Acrescenta informação e salva arquivo novamente
        cards.append(formdata)

        with open(path, mode="w") as f:
            json.dump(cards, f)

        num = len(cards) - 1
        ok = "Card {} adicionado com sucesso!".format(num)

        return render_template('addcards.html', mensagem=ok)
        
    return render_template('addcards.html')


@app.route("/createcards/download_file")
def download_file():
    fname = request.cookies.get('filename')
    path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
    cards = []
    with open(path, mode="r") as f:
        cards = json.load(f)
    
    New_fname = secure_filename(cards[0])
    New_path = os.path.join(current_app.config['TEMP'], (New_fname + ".txt"))

    with open(New_path, mode="w") as f:
        json.dump(cards, f)

    download = url_for('static', filename=(New_fname + ".txt"))

    return "<a href='{}' download> Baixar txt </a> ".format(download)


@app.route("/opencards", methods=["GET", "POST"])
def opencards():
    if request.method == "POST":
        thefile = request.files.get('cardsfile')

        fname = str(uuid.uuid4())
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
        thefile.save(path)
        
        cards = []
        
        try:
            with open(path, mode="r") as f:
                cards = json.load(f)
            
            return "<h1> Seus Cards </h1> <p>{}</p>".format(cards)
        
        except:
            return "<h1> Seus Cards </h1> <p>Não foi possível carregar os seus cards</p>"        

    return render_template('uploadcards.html')
