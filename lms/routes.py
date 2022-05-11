from flask import render_template, url_for, flash, redirect, request 
from lms import app,db,bcrypt
from .forms import Logininstructor, Registration,Login,Registerinstructor, Addcourse
from .models import User, Courses, Usercourse, Discussion, Subunits, Resources
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import array, os, json


@app.route('/')
def home():
    courses = Courses.query.all()
    return render_template('index.html', data = courses)

@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        course = Usercourse.query.join(User, Usercourse.user_id == User.id).join(Courses, Usercourse.course_id == Courses.id).filter(Usercourse.user_id == current_user.id).all()
        return render_template('dashboard/index.html', data = course)
    else:
        return redirect(url_for('login'))

@app.route('/chat')
def chat(): 
     return render_template('dashboard/chat.html')
 
       


def enroll_checker(courseid, userid):
    data = Usercourse.query.filter_by(user_id = userid).filter_by(course_id = courseid).first()
    if data:
        return True
    else:
        return False

@app.route('/courses', methods=['GET' ,'POST'])
def courses():
    if current_user.is_authenticated:
        courses = Courses.query.all()
        data = []
        for i in courses:
            data.append([i, enroll_checker(i.id, current_user.id)])
        print(data)
        if request.method == "POST":
            form = request.form
            userid = request.form['user_id']
            courseid = request.form['course_id']
            user = Usercourse(user_id=userid,course_id=courseid,progress = '0')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('courses'))
        return render_template('dashboard/courses.html',data=data)
    else:
        return redirect(url_for('login'))


@app.route('/courseinfo/<id>')
def courseinfo(id=""):
    if current_user.is_authenticated:
        course = Courses.query.filter_by(id = id).first()
        subunits = Subunits.query.all()

        return render_template('dashboard/course_details.html', course = course, sub = subunits)
    else:
        return redirect(url_for('login'))

@app.route('/discussion',methods=['GET' ,'POST'])
def discussion():
    if current_user.is_authenticated:
        courses = Courses.query.all()
        discussion = Discussion.query.all()
        if request.method == "POST":
            form = request.form
            title = request.form['title']
            body = request.form['body']
            categories = request.form['categories']
            tags = request.form['tags']
            user = Discussion(title=title,example=body,body='max.jpg',categories=categories,tags=tags)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('discussion'))
        return render_template('dashboard/discussion.html', data=courses, discussion=discussion)
    else:
        return redirect(url_for('login'))

@app.route('/resources')
def resources():
    if current_user.is_authenticated:
        resource = Resources.query.all()
        return render_template('dashboard/resources.html', resource = resource)
    else:
        return redirect(url_for('login'))



@app.route('/challenge')
def challenge():
    if current_user.is_authenticated:
     
        return render_template('dashboard/challenge.html')
    else:
        return redirect(url_for('login'))











@app.route('/admindashboard')
def admindashboard():
    if current_user.is_authenticated:
        return render_template('admindashboard.html')
    else:
        return redirect(url_for('login'))











@app.route('/instructordashboard', methods=['GET' ,'POST'])
#@login_required
def instructordashboard():
    if current_user.is_authenticated:
        return render_template('instructordashboard/index.html')
    else:
        return redirect(url_for('logininstructor'))











#Authentication 
@app.route('/register', methods=['GET' ,'POST'])
def register():
    register = Registration()
    if request.method == "POST":
        form = request.form
      
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['confirmpassword']
        if User.query.filter_by(email=email).first():
            flash('Email Address already Exists', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=name.lower(),email=email.lower(),password=hashed_password,email_preference = 'yes')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html',form = register)
    

@app.route('/login', methods=['GET' ,'POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        form = Login()
        form = request.form
        email = request.form['email']
        password = request.form['password']
        if request.form.get('rememberme'):
            remember = request.form['rememberme']
        else:
            remember = 'no'
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember= remember)
            if current_user.role== "user":
              #  next_page = request.args.get('next')#requests current url and redirects to next page otherwise it returns to the dashboard
                return redirect(url_for('dashboard'))
            elif current_user.role== "instructor":
              #  next_page = request.args.get('next')#requests current url and redirects to next page otherwise it returns to the dashboard
                return redirect(url_for('instructordashboard'))
            elif current_user.role== "admin":
              #  next_page = request.args.get('next')#requests current url and redirects to next page otherwise it returns to the dashboard
                return redirect(url_for('admindashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',form = form)



## instructor contents
@app.route('/logininstructor', methods=['GET' ,'POST'])
def logininstructor():
    form = Logininstructor()
    if current_user.is_authenticated:
        return redirect(url_for('instructordashboard'))
    if request.method == "POST":
        form = request.form
        email = request.form['email']
        password = request.form['password']
        if request.form.get('rememberme'):
            remember = request.form['rememberme']
        else:
            remember = 'no'
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            if current_user.role== "user":
                #  next_page = request.args.get('next')#requests current url and redirects to next page otherwise it returns to the dashboard
                return redirect(url_for('dashboard'))
            elif current_user.role== "instructor":
            #  next_page = request.args.get('next')#requests current url and redirects to next page otherwise it returns to the dashboard
                return redirect(url_for('instructordashboard'))
            elif current_user.role== "admin":
            #  next_page = request.args.get('next')#requests current url and redirects to next page otherwise it returns to the dashboard
                return redirect(url_for('admindashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('logininstructor.html',form = form)


#@app.route('/registerinstructor')
#def registerinstructor():
    #return render_template('registerinstructor.html')


@app.route('/registerinstructor', methods=['GET','POST'])
def registerinstructor():
    register = Registerinstructor()#am getting an error here
    #if request.method =='GET':
    #   return "Register via the Registration Page"
    if request.method == "POST":
        form = request.form #is this right
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        username = request.form['username']
        coursecode = request.form['coursecode']
       
        role = 'instructor'
        if User.query.filter_by(email=email).first():
            flash('Email Address already Exists', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=username.lower(),email=email.lower(),password=hashed_password,role='instructor',email_preference = 'yes')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('instructordashboard'))
    return render_template('registerinstructor.html',form = Registerinstructor())# alternatively you can use form = register


def save_picture(picture_file):
    picture = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/img', picture)
    picture_file.save(picture_path)
    return picture


@app.route('/addcourse', methods=['GET' ,'POST'])
@login_required
def addcourse():
    form = Addcourse()
    if request.method == "POST":
        form = request.form #is this right
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        duration = request.form['duration']
        file = request.files["image"]
        if file.filename == "":
            flash('Please select a file', 'danger')
        if file:
            picture_file = save_picture(file)
            image_url = url_for('static', filename='img/' + picture_file)
            file = secure_filename(file.filename)
        user = Courses(title =title, description = description, category = category, duration = duration, image = picture_file, instructor = current_user.name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('instructorcourses'))
    return render_template('instructordashboard/addcourse.html',form = Addcourse())# alternatively you can use form = register

@app.route('/account')
def account():
    if current_user.is_authenticated:
     
        return render_template('instructordashboard/account.html')
    else:
        return redirect(url_for('login'))

@app.route('/instructor/students')
@login_required
def instructorstudent():
    if current_user.is_authenticated:
        students = User.query.filter_by(role = "user").all()
        return render_template('instructordashboard/students.html', user = students)
    else:
        return redirect(url_for('login'))

@app.route('/instructor/courses')
@login_required
def instructorcourses():
    if current_user.is_authenticated:
        courses = Courses.query.filter_by(instructor = current_user.name).all()
        return render_template('instructordashboard/courses.html', course = courses)
    else:
        return redirect(url_for('login'))

@app.route('/subunits/<id>', methods=['GET' ,'POST'])
@login_required
def subunits(id=''):
    id = id
    courses = Courses.query.filter_by(id = id).first()
    form = Subunits()
    if request.method == "POST":
        form = request.form #is this right
        title = request.form['title']
        duration = request.form['duration']
        link = request.form['link']
        user = Subunits(title =title, duration = duration, link = link, course_id = id)
        db.session.add(user)
        db.session.commit()
        return redirect('/subunits/{}'.format(id))
    return render_template('instructordashboard/subunits.html',form = Addcourse(), course = courses)# alternatively you can use form = register
       
        

    
    
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Logged Out Successfully! Remember to keep track of your progress")
    return redirect(url_for('login'))
