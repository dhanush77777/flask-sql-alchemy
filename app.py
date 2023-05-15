from flask import Flask,redirect,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os
project_dir=os.path.dirname(os.path.abspath(__file__))
database_file= "sqlite:///{}".format(os.path.join(project_dir,"mydatabase2.db"))
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get("DATABASE_URL")
db=SQLAlchemy(app)

class Book(db.Model):
    name=db.Column(db.String(100),nullable=False,primary_key=True)
    author=db.Column(db.String(100),nullable=False)
    link=db.Column(db.String(500),nullable=False)
  
    
@app.route('/delete',methods=['POST'])
def delete():
    name= request.form['name']
    book=Book.query.filter_by(name=name).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('updatebooks')
    
    
@app.route('/updatebooks')
def updatebooks():
    books=Book.query.all()
    return render_template('updatebooks.html', books=books)

@app.route('/update',methods=['POST'])
def update():
    newname=request.form['newname']
    oldname=request.form['oldname']
    newauthor=request.form['newauthor']
    newlink=request.form['newlink']
    
    book = Book.query.filter_by(name=oldname).first()
    book.name=newname
    book.author=newauthor
    book.link=newlink
    db.session.commit()
    return redirect('/showbooks')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books' , methods=['POST'])
def books():
    bookname=request.form['name']
    authorname=request.form['author']
    booklink=request.form['link']
    book=Book(name=bookname,author=authorname,link=booklink)
    db.session.add(book)
    db.session.commit()
    return redirect('/showbooks')

@app.route('/showbooks')
def showbooks():
    bookss=Book.query.all()
    return render_template('books.html',books=bookss)
    

if __name__ == ('__main__'):
    app.run(debug=True)

