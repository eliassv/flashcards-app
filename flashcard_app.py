from flask import Flask

app = Flask("flashcard", static_folder='temp', static_url_path="/temp")
app.config.from_object('settings')

import views