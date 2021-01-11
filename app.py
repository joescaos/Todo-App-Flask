from flask import Flask, render_template, request, redirect, url_for
from database import db   
from models import Todo
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

#db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    print(title)
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    Todo.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    
    app.run(port=3000, debug=True)