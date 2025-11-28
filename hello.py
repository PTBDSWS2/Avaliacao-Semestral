import os
import sys
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from datetime import datetime

import requests
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_URL'] = os.environ.get('API_URL')
app.config['API_FROM'] = os.environ.get('API_FROM')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64),)

    def __repr__(self):
        return '<Course %r>' % self.name

# def send_simple_message(to, subject, newUser):
#     print('Enviando mensagem (POST)...', flush=True)
#     print('URL: ' + str(app.config['API_URL']), flush=True)
#     print('api: ' + str(app.config['API_KEY']), flush=True)
#     print('from: ' + str(app.config['API_FROM']), flush=True)
#     print('to: ' + str(to), flush=True)
#     print('subject: ' + str(app.config['FLASKY_MAIL_SUBJECT_PREFIX']) + ' ' + subject, flush=True)
#     print('text: ' + "Novo usuário cadastrado: " + newUser, flush=True)

#     resposta = requests.post(app.config['API_URL'],
#                              auth=("api", app.config['API_KEY']), data={"from": app.config['API_FROM'],
#                                                                         "to": to,
#                                                                         "subject": app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                                                                         "text": "Novo usuário cadastrado: " + newUser})

#     print('Enviando mensagem (Resposta)...' + str(resposta) + ' - ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
#     return resposta


class CourseForm(FlaskForm):
    name = StringField('Qual é o nome do curso?', validators=[DataRequired()])
    description = TextAreaField('Descrição (250 caracteres)', validators=[DataRequired()])    
    submit = SubmitField('Cadastrar')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Course=Course)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/cursos', methods=['GET', 'POST'])
def course():
    form = CourseForm()
    if request.method == 'POST':
        course = Course.query.filter_by(name=form.name.data).first()
        print(course)
        if course is None:
            course = Course(name=form.name.data, description=form.description.data)
            print(form.name.data) 
            print(form.description.data)
            db.session.add(course)
            db.session.commit()
            session['known'] = False  
            return redirect(url_for('course'))
        else:
            session['known'] = True
            session['name'] = form.name.data
            flash('Curso já existe na base de dados!')
            return redirect(url_for('course'))
    return render_template('course.html', form=form, name=session.get('name'), course_list=Course.query.all(), known=session.get('known', False))

@app.route('/professores')
def teachers():
    return render_template('not_available.html', current_time=datetime.utcnow())

@app.route('/disciplinas')
def diciplines():
    return render_template('not_available.html', current_time=datetime.utcnow())

@app.route('/alunos')
def students():
    return render_template('not_available.html', current_time=datetime.utcnow())

@app.route('/ocorrencias')
def occurrences():
    return render_template('not_available.html', current_time=datetime.utcnow())

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             role = Role.query.filter_by(name='User').first()
#             user = User(username=form.name.data, role=role)
#             db.session.add(user)
#             db.session.commit()
#             session['known'] = False

#             print('Verificando variáveis de ambiente: Server log do PythonAnyWhere', flush=True)
#             print('FLASKY_ADMIN: ' + str(app.config['FLASKY_ADMIN']), flush=True)
#             print('URL: ' + str(app.config['API_URL']), flush=True)
#             print('api: ' + str(app.config['API_KEY']), flush=True)
#             print('from: ' + str(app.config['API_FROM']), flush=True)
#             print('to: ' + str([app.config['FLASKY_ADMIN'], "flaskaulasweb@zohomail.com"]), flush=True)
#             print('subject: ' + str(app.config['FLASKY_MAIL_SUBJECT_PREFIX']), flush=True)
#             print('text: ' + "Novo usuário cadastrado: " + form.name.data, flush=True)

#             if app.config['FLASKY_ADMIN']:
#                 print('Enviando mensagem...', flush=True)
#                 email_list = [app.config['FLASKY_ADMIN']]
#                 print(email_list)
#                 if form.flask_mail.data is True:
#                     email_list.append("flaskaulasweb@zohomail.com")
#                 send_simple_message(email_list, 'Novo usuário', form.name.data)
#                 #send_simple_message([app.config['FLASKY_ADMIN'], "flaskaulasweb@zohomail.com"], 'Novo usuário', form.name.data)
#                 print('Mensagem enviada...', flush=True)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, name=session.get('name'), user_list= User.query.all(),
#                            known=session.get('known', False))
