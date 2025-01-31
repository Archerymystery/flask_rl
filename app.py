from flask import Flask, render_template, request, redirect, url_for

from models import Task, db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)
