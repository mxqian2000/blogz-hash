
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Larry528@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(140))
    body =db.Column(db.String(1024))
    def __init__(self, title, body):
        self.title = title
        self.body = body                

@app.route('/')
def index():   
        return redirect('/blog')

@app.route("/blog")
def blog():  
    blog_id = request.args.get('id')
    blogs = Blog.query.all()    
    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body
        return  render_template('entry.html', title="Blog Entry #" + blog_id, blog_title=blog_title, blog_body=blog_body)
    else: 
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
@app.route("/post")
def post():
    return render_template('post.html', title="Add A New Blog Entry")

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':                
        #blog_id = int(request.form['blog_id'])
        blog_title = request.form['blog_title']
        title_error =''
        if len(blog_title) == 0:
            title_error = "Please fill in the title."
        body_error =''    
        blog_body = request.form['blog_body']
        if len(blog_body) == 0:
            body_error = "Please fill in the body."
           
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body) 
            db.session.add(new_blog)
            db.session.commit()    
            blog = new_blog.id          
            return redirect('/blog?id={0}'.format(blog)) 
        else:
            return render_template('post.html', title = "Add A New Blog Entry", blog_title = blog_title, blog_body = blog_body, title_error = title_error, body_error = body_error)
    else:
        return render_template('newpost.html')
        
    

if __name__ == "__main__":
    app.run()   
