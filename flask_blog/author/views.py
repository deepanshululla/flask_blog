from flask_blog import app
from flask import render_template, redirect, url_for, flash, session, request, abort
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm();
    error = None;
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
        
    if form.validate_on_submit():
        author = Author.query.filter_by(
            username=form.username.data,
            ).first()
        
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username']=form.username.data;
                session['is_author']= author.is_author;
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error= "Incorrect username/password"
        else:
            error= "Incorrect username/password"
            
    return render_template('author/login.html', form = form, error = error)
    
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        author = Author.query.filter_by(username=form.username.data).limit(1)
        # checking if username already exists
        if author.count():
            error = "Username already exists. Please choose another username"
            return render_template('author/register.html', form = form)
        else:
        
            return redirect(url_for('success'))
    return render_template('author/register.html', form = form)    
            
    


@app.route('/success')
def success():
    return "Author registered";
    


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('is_author', None)
    return redirect(url_for('index'))