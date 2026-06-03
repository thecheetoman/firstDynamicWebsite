from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # use local SQLite database
db = SQLAlchemy(app)  # initialize database integration

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique task id
    content = db.Column(db.String(200), nullable=False)  # text for the task
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # creation timestamp

    def __repr__(self):
        return '<Task %r>' % self.id  # developer-friendly object string


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # read form input
        new_task = Todo(content=task_content)  # create task object

        try:
            db.session.add(new_task)  # insert task
            db.session.commit()  # save changes
            return redirect('/')  # return to home
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # fetch tasks sorted by date
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  # find task or 404

    try:
        db.session.delete(task_to_delete)  # remove task
        db.session.commit()  # commit deletion
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)  # get task for update

    if request.method == 'POST':
        task.content = request.form['content']  # update text

        try:
            db.session.commit()  # save update
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)  # run app in debug mode
