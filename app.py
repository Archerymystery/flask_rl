from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from models import db, Task, TaskFile
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        new_task = Task(title=title)
        files = request.files.getlist("files")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # На випадок, якщо ми маємо кілька файлів з однаковими іменами
                # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # filename = f"{timestamp}_{filename}"

                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                new_file = TaskFile(filename=filename, task=new_task)
                db.session.add(new_file)

        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task and request.method == "POST":
        task.title = request.form.get("title", "").strip()
        if task.title:
            db.session.commit()
            return redirect(url_for("index"))
    return render_template("edit.html", task=task)
