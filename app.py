"""Blogly application."""
from flask import Flask,render_template,request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag




app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
 
    db.create_all()


@app.route("/")
def base():
    return render_template('base.html')

@app.route("/user", methods=["POST", "GET"])
def getUser():
    listU = User.query.all()
    return render_template('user.html', list = listU)

@app.route('/user/new',methods=["POST", "GET"])
def addUser():
    return render_template('new.html')
    
@app.route("/user/<int:id>")
def custom(id):
    p = Post.getPosts(id)
    return render_template('custom.html', id = id, u = User.getAll(id), p = p)


@app.route('/delete/<int:id>')
def deleteUser(id):
    
    
    Post.deleteAll(id)
    User.deleteUser(id)
    db.session.commit()
    return redirect('/user')

@app.route('/user/<int:id>/edit',methods=["POST", "GET"])
def edit(id):
    return render_template('edit.html', id = id)

@app.route('/user/editing/<int:id>',methods=["POST", "GET"])
def editing(id):
    u = User.updateUser(id)
    print(u)
    first = request.form.get('first_name')
    last = request.form.get('last_name')
    image = request.form.get('image_url')
    u.first_name = first
    u.last_name = last
    u.image_url = image
    db.session.commit()
    return redirect('/user')


@app.route('/add',methods=["POST", "GET"])
def getinfo():
    first = request.form.get('first_name')
    last = request.form.get('last_name')
    image = request.form.get('image_url')
    db.session.add(User(first_name=first,last_name=last,image_url=image))
    db.session.commit()
    return redirect('/user')

@app.route('/user/<int:id>/posts/new', methods=["POST", "GET"])
def post(id):
    id = request.args['user_id']
    u = User.getAll(id)
    tags = Tag.query.all()
    return render_template('post.html', user = u, id = id, tags=tags)

@app.route('/user/<int:id>/posts/posting', methods=["POST", "GET"])
def addPost(id):
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.tag_id.in_(tag_ids)).all()
    post = Post(title=title,content=content, user_id=id, tags = tags)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/user/{id}')

@app.route('/post/<int:id>')
def showPost(id):
    post = Post.getPost(id)
    userFirst = post.user.first_name
    userLast = post.user.last_name
    user = f'{userFirst} {userLast}'
    tags = post.post_tags
    return render_template('postPage.html', post = post, id = post.post_id, user = user, user_id = post.user_id, tags = tags)

@app.route('/posts/<int:id>/delete')
def deletePost(id):
    p = Post.getPost(id).user_id
    Post.deleteAll(id)
    db.session.commit()
    return redirect(f'/user/{p}')

@app.route('/posts/<int:id>/edit', methods=["POST", "GET"])
def editPage(id):
    return render_template('editPost.html', id = id)

@app.route('/posts/<int:id>/editing', methods=["POST", "GET"])
def editPost(id):
    title = request.form.get('title')
    content = request.form.get('content')
    post = Post.getPost(id)
    post.title = title
    post.content = content
    db.session.commit()
    return redirect(f'/post/{id}')


@app.route('/tags')
def allTags():
    tag = Tag.getTags()
    return render_template('tags.html', tags = tag)


@app.route('/tags/new', methods=["POST","GET"])
def newTag():
    post = Post.query.all()
    print(post)
    return render_template('tag_form.html', posts = post)

@app.route('/tags/adding', methods=["POST","GET"])
def addTag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.post_id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['tag_name'], posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:id>')
def getTagInfo(id):
    tag = Tag.getTag(id)
    return render_template('custom-tag.html', id = tag.tag_id, tag =tag)

@app.route('/tags/<int:id>/deleting')
def deleteTag(id):
    Tag.deleteTag(id)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:id>/editing', methods=["POST","GET"])
def editTag(id):
    tag = Tag.getTag(id)
    tag.name = request.form.get('tag_name')
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:id>/edit', methods=["POST","GET"])
def editTagForm(id):
    tag = Tag.getTag(id)
    return render_template('edit-tag.html', id = id)




    
    
