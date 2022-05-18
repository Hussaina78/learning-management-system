
from lms import db,login_manager,app, admin
from datetime import datetime
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=True)
    role = db.Column(db.String(120), unique=False, nullable=True, default='user')
    password = db.Column(db.String(250),unique=False, nullable=False)
    email_preference = db.Column(db.String(120), unique=False, nullable=False)
    usercourse = db.relationship('Usercourse', backref='user')

    def __repr__(self):
        return f"User('{self.id}','{self.name}','{self.role}','{self.email}')"



class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    category = db.Column(db.String(120), unique=False, nullable=False)
    duration = db.Column(db.String(120), unique=False, nullable=False)
    instructor = db.Column(db.String(120), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=True)
    usercourse = db.relationship('Usercourse', backref='usercourse')
    def __repr__(self):
        return f"Courses('{self.id}','{self.title}','{self.description}','{self.image}')"

class Usercourse(db.Model):
    __tablename__ = 'usercourse'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    author = db.Column(db.String(120), unique=False, nullable= True)
    progress = db.Column(db.String(120), unique=False, nullable=False)
    def __repr__(self):
        return f"Usercourse('{self.author}','{self.user_id}','{self.course_id}','{self.progress}')"

class Discussion(db.Model):
    __tablename__ = 'discussion'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    example = db.Column(db.String(120), unique=False, nullable=False)
    body = db.Column(db.String(260), unique=False, nullable=False)
    categories = db.Column(db.String(210), unique=False, nullable=False)
    tags = db.Column(db.String(120), unique=False, nullable=False)
    def __repr__(self):
        return f"Discussion('{self.id}', '{self.example}''{self.title}','{self.body}','{self.categories}', '{self.tags}')"

class Subunits(db.Model):
    __tablename__ = 'subunits'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    title = db.Column(db.String(120), unique=False, nullable=False)
    duration = db.Column(db.String(260), unique=False, nullable=False)
    link = db.Column(db.String(210), unique=False, nullable=False)
    
    def __repr__(self):
        return f"Subunits('{self.id}', '{self.course_id}''{self.title}','{self.duration}','{self.link}')"

class Resources(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(260), unique=False, nullable=True)
    type = db.Column(db.String(260), unique=False, nullable=True)
    categories = db.Column(db.String(260), unique=False, nullable=False)
    author = db.Column(db.String(260), unique=False, nullable=True)
    pages = db.Column(db.String(260), unique=False, nullable=True)
    content = db.Column(db.String(260), unique=False, nullable=False)
    img_reference = db.Column(db.String(260), unique=False, nullable=True)
    def __repr__(self):
        return f"Resources('{self.id}', '{self.title}','{self.type}','{self.categories}','{self.author}', '{self.pages}', '{self.content}', '{self.img_reference}')"



admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Usercourse, db.session))
#admin.add_view(ModelView(Courses, db.session))
#admin.add_view(ModelView(Discussion, db.session))
#admin.add_view(ModelView(Subunits, db.session))
#admin.add_view(ModelView(Resources, db.session))
