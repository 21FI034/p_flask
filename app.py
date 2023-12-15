from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    details = db.Column(db.String(100))

@app.route("/")
def index():
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/create", methods=["POST"])
def create():
    title = request.form.get("title")
    details = request.form.get("details")
    new_task = Todo(title=title, details=details)

    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get(id)

    db.session.delete(delete_task)
    db.session.commit()
    return redirect('/')

## TODO
## /update/1のような遷移先を作成する
@app.route('/update/<int:id>', methods=['GET', 'POST'])
## /update/1　に来たときの処理を実装する
def update(id):
    update_task = Todo.query.get(id)
    ## idをもとにデータベースからタスクを取得する
    if request.method == 'POST':
        title = request.form.get("title")
        details = request.form.get("details")
        update_task.title = title
        update_task.details = details
        db.session.commit()
        return redirect('/')
    ## GETのときはupdate.htmlを表示する
    ## update.htmlには元々のタスクの情報を表示したい
    return render_template("update.html", task=update_task)

    
    ## POSTのときはデータベースを更新して/にリダイレクトする
    ## データベースを更新するときは、タスクを取得→取得したタスクの内容を更新→保存する
    
    pass


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)