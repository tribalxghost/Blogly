from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
db = SQLAlchemy()

"""Models for Blogly."""

    



class User(db.Model):


    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(), nullable = False)    
    last_name = db.Column(db.String(), nullable = False)    
    image_url = db.Column(db.String())

    use = {id:id, first_name:first_name, last_name:last_name, image_url:image_url}
    @classmethod
    def __repr__(self):
        p = self
        return f"{p.user_id} {p.first_name} {p.last_name} {p.image_url}"
    
    @classmethod
    def getAll(cls,id):
        return cls.query.get(id)
    
    @classmethod
    def deleteUser(cls,id):
        return cls.query.filter_by(user_id=id).delete()
    @classmethod
    def updateUser(cls, id):
        return cls.query.filter(User.user_id == id).first()



class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True
    )
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id')
    )
    user = db.relationship( 'User',cascade="all,delete", backref='users')
    post_tags = db.relationship('Tag', secondary='post_tags', backref='p_tags')
    @classmethod
    def __repr__(self):
        p = self
        return f"{p.user_id} {p.title} {p.content}"

    

    @classmethod
    def getPosts(cls,id):
        return cls.query.filter(Post.user_id == id).all()
    
    @classmethod
    def getPost(cls, id):
        return cls.query.filter(Post.post_id == id).first()
    
    @classmethod
    def deletePost(cls, id):
        return cls.query.filter(Post.post_id == id).delete()
    @classmethod
    def deleteAll(cls, id):
        return cls.query.filter(Post.user_id == id).delete()
    @classmethod
    def getTags(cls, id):
        return cls.query.get(Post.post_tags)

class PostTag(db.Model):
    __tablename__ = "post_tags"
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True,nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True,nullable = False)

    @classmethod
    def getAll(cls):
        return cls.query.all()
    
    @classmethod
    def getPT(cls, id):
        return cls.query.filter(PostTag.post_id == id).all()


class Tag(db.Model):
    __tablename__ = "tags"
    tag_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable=False)
    posts = db.relationship(
    'Post', secondary="post_tags",cascade="all,delete",
    backref="tags",
    )
    
    @classmethod
    def __repr__(self):
        t = self
        return f"{t.name}"


    @classmethod
    def getTags(cls):
        return cls.query.all()
    @classmethod
    def deleteTag(cls, id):
        return cls.query.filter(Tag.tag_id == id).delete()   

    @classmethod
    def getTag(cls, id):
        return cls.query.filter(Tag.tag_id == id).first() 
     


def connect_db(app):
    db.app = app
    db.init_app(app)   

    