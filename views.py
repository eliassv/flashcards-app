from flashcard_app import app

@app.route("/")
def index():
    return "<h1>Flashcard App!</h1>"