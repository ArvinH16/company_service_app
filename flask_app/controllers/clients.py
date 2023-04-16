from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.client import Client

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/client_signup_page')
def client_signup_page():
    return render_template('client_signup_page.html')

@app.route('/client_signup', methods=['POST'])
def create_client():
    if not Client.validation_registering(request.form):
        return redirect('/client_signup_page')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    clientAdded = Client.create_client(data)

    return(redirect('/'))