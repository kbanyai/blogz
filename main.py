from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:password@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    blog = db.Column(db.String(200))

    def __init__(self, name, blog):
        self.name = name
        self.blog = blog

@app.route('/', methods=['POST', 'GET'])
def index():

    posts = Task.query.all() 

    return render_template('index.html', posts=posts)

@app.route('/entry', methods=['POST', 'GET'])
def entry():
    if request.method == 'POST':
        if request.form['name'] =="":
            return render_template('entry.html')
        if request.form['blog'] =="":
            return render_template('entry.html')
        else:
            a =Task(request.form['name'],request.form['blog'])
            db.session.add(a)
            db.session.commit()


        return redirect('/')

    return render_template('entry.html')

@app.route('/show')
def show():
    post = Task.query.filter_by(id=request.args['id']).first()
    return render_template('show.html', post=post)

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()