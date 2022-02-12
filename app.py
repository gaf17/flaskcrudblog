from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class blogPost(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable= False, default= 'Author Unknown')
    datePosted = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    
    def __repr__(self):
        return "Blog Post: " + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home/users/<string:name>/posts/<int:id>')
def yourName(name, id):
    return 'Hello '+ name + ", your id is : " + str(id)

@app.route('/posts', methods = ['GET', 'POST'])
def posts():

    if request.method == 'POST':
        postTitle = request.form['title']
        postContent = request.form['content']
        postAuthor = request.form['author']
        newPost = blogPost(title=postTitle, content = postContent, author = postAuthor)
        db.session.add(newPost)
        db.session.commit()
        return redirect('/posts')
    else: 
        allPosts = blogPost.query.order_by(blogPost.datePosted).all()
        return render_template('posts.html', posts= allPosts)

@app.route('/onlyget', methods= ['GET'])
def getReq():
    return 'you can only get this webpage'

@app.route('/product/<int:product_id>')
def showProd(product_id):
    return render_template('productPage.html', id= product_id)

@ app.route('/posts/delete/<int:id>')
def delete(id):
    post = blogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@ app.route('/posts/edit/<int:id>', methods= ['GET', 'POST'])
def edit(id):

    post = blogPost.query.get_or_404(id)

    if request.method == 'POST':

        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

@ app.route('/posts/new', methods= ['GET', 'POST'])
def newPost():
        
    if request.method == 'POST':
        return redirect('/posts')
    else:
        return render_template('newPost.html')

if __name__ == '__main__':
    app.run(debug=True)