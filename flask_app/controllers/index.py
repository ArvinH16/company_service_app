from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/sign_in_page')
def sign_in_page():
    return render_template('sign_in_page.html')

'''
@app.route('/sign_in', methods=['POST'])
def sign_in():
    if not User.validation_login(request.form):
        return redirect('/sign_in_page')

    user = User.check_email(request.form)
    if not user:
        flash("Invalid email or password", 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email or password", 'login')
        return redirect('/')

    #session['user_id'] = user.id
    return redirect('/dashboard')
'''