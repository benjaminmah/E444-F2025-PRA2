from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

def uoft_domain(email: str) -> bool:
    if not email:
        return False
    e = email.lower().strip()
    return e.endswith('@utoronto.ca') or e.endswith('@mail.utoronto.ca')


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()], render_kw={"required": True})
    email = StringField('What is your UofT Email address?', validators=[DataRequired()], render_kw={"type": "email", "required": True})
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))

    name = session.get('name')
    email = session.get('email')
    if email:
        if uoft_domain(email):
            email_message = f"Your UofT email is {email}"
        else:
            email_message = "Please use your UofT email."
    else:
        email_message = None

    return render_template(
        'index.html',
        form=form,
        name=name,
        email=email,
        email_message=email_message,
        current_time=datetime.utcnow(),
    )

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
