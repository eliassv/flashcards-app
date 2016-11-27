from flask import Flask

app = Flask("flashcard")
app.config.from_object('settings')

import views