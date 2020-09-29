from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# setup the app
app = Flask (__name__)

all_posts = [
    {
        'name' : "ayat",
        'email' :"ayat@gmail.com"
    },
    {
        'name': "Ali",
        'email' :"Ali@gmail.com"
    }

]

# setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(200), nullable= False)

    def __repr__(self):
        return 'Blog post ' + str(self.id)



@app.route('/home')
def hello():
    return "hello word"


@app.route('/')
def index():
      return render_template('posts.html')


@app.route('/posts', methods=['GET', "POST"])
def posts():

    if request.method == 'POST':
        post_name = request.form['name']
        post_email = request.form['email']
        new_user = UserPost(name = post_name, email=post_email)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/posts')
    else:  
        all_posts = UserPost.query.all()
        return render_template('posts.html', posts = all_posts )

@app.route('/posts/delete/<int:id>')
def delete(id):
    post=UserPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post=UserPost.query.get_or_404(id)
   
    if request.method== 'POST':
        post.name = request.form['name']
        post.email = request.form['email']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('/edit.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)