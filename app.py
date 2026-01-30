import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'khadka_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ================= MODELS =================

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    subtitle = db.Column(db.String(250))

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    content = db.Column(db.Text)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    desc = db.Column(db.Text)
    image = db.Column(db.String(200))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.Text)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(120))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=db.func.now())

with app.app_context():
    db.create_all()

# ================= AUTH =================

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin')
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

# ================= PUBLIC =================

@app.route('/')
def index():
    return render_template(
        'index.html',
        hero=Hero.query.first(),
        about=About.query.first(),
        projects=Project.query.all(),
        skills=Skill.query.all(),
        testimonials=Testimonial.query.all(),
        contact=Contact.query.first()
    )

# ================= ADMIN =================

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')

    def log(action):
        db.session.add(Activity(action=action))
        db.session.commit()

    t = request.form.get('type')

    if t == 'hero':
        hero = Hero.query.first() or Hero()
        hero.title = request.form['title']
        hero.subtitle = request.form['subtitle']
        db.session.add(hero)
        db.session.commit()
        log("Updated hero section")

    if t == 'about':
        about = About.query.first() or About()
        about.content = request.form['content']
        img = request.files.get('image')
        if img and img.filename:
            fname = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            about.image = fname
        db.session.add(about)
        db.session.commit()
        log("Updated about section")

    if t == 'delete_about':
        About.query.delete()
        db.session.commit()
        log("Deleted about section")

    if t == 'project':
        img = request.files.get('image')
        fname = None
        if img and img.filename:
            fname = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        db.session.add(Project(
            title=request.form['title'],
            desc=request.form['desc'],
            image=fname
        ))
        db.session.commit()
        log("Added project")

    if t == 'delete_project':
        Project.query.filter_by(id=request.form['id']).delete()
        db.session.commit()
        log("Deleted project")

    if t == 'skill':
        db.session.add(Skill(name=request.form['name']))
        db.session.commit()
        log("Added skill")

    if t == 'delete_skill':
        Skill.query.filter_by(id=request.form['id']).delete()
        db.session.commit()
        log("Deleted skill")

    if t == 'testimonial':
        db.session.add(Testimonial(
            name=request.form['name'],
            message=request.form['message']
        ))
        db.session.commit()
        log("Added testimonial")

    if t == 'delete_testimonial':
        Testimonial.query.filter_by(id=request.form['id']).delete()
        db.session.commit()
        log("Deleted testimonial")

    if t == 'contact':
        c = Contact.query.first() or Contact()
        c.email = request.form['email']
        c.phone = request.form['phone']
        c.location = request.form['location']
        db.session.add(c)
        db.session.commit()
        log("Updated contact info")

    return render_template(
        'admin.html',
        hero=Hero.query.first(),
        about=About.query.first(),
        projects=Project.query.all(),
        skills=Skill.query.all(),
        testimonials=Testimonial.query.all(),
        contact=Contact.query.first(),
        activities=Activity.query.order_by(Activity.timestamp.desc()).limit(6)
    )

if __name__ == '__main__':
    app.run(debug=True)
