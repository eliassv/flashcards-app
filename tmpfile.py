import os, json
from flask import current_app, request

class tmpfile:

    @staticmethod
    def load():
        fname = request.cookies.get('filename')
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))
        content = []
        with open(path, mode="r", encoding="utf-8") as f:
            content = json.load(f)    
        return content
    
    
    def load_path(path):
        with open(path, mode="r", encoding="utf-8") as f:
            content = json.load(f)    
        return content


    @staticmethod
    def save(data):
        fname = request.cookies.get('filename')
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))

        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(data, f)


    @staticmethod
    def save_new_fname(data, fname):
        path = os.path.join(current_app.config['TEMP'], (fname + ".txt"))

        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(data, f)