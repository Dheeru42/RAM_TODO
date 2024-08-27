from datetime import datetime
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy # import database
app = Flask(__name__)

# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ram.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
class ram(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_create = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'
        
        
@app.route('/',methods=['GET', 'POST'])
def db1():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        to = ram(title=title,desc=desc)
        db.session.add(to)
        db.session.commit()
    all = ram.query.all()
    # print(all)
    return render_template('index.html',all=all)

@app.route('/delete/<int:sno>',methods=['GET', 'POST'])
def delete(sno):
    todo = ram.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        to = todo = ram.query.filter_by(sno = sno).first()
        to.title = title
        to.desc = desc
        db.session.add(to)
        db.session.commit()
        return redirect("/")
    todo = ram.query.filter_by(sno = sno).first()
    return render_template('update.html',all1=todo)

if __name__=='__main__':
    app.run(debug=True,port=8000)