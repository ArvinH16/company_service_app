from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.company import Company
from flask_app.models.client import Client

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/sign_in_page')
def sign_in_page():
    return render_template('sign_in_page.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }

    #company and client login validation is same so we can use either
    if not Company.validation_login(data):
        return redirect('/sign_in_page')
    
    print(request.form['role'])
    #Get the role of the person loging in
    if(request.form['role'] == 'company'):
        role = 'company'
    elif(request.form['role'] == 'client'):
        role = 'client'
    else:
        flash("You need to select if you're a client or a company", "sign_in")
        return redirect('/sign_in_page')
    
    #if the person is a client 
    if(role == 'client'):
        client = Client.check_email(data)
        if not client:
            flash("Invalid email or password for client log in", 'sign_in')
            return redirect('/sign_in_page')

        if not bcrypt.check_password_hash(client.password, data['password']):
            flash("Invalid email or password for client log in", 'sign_in')
            return redirect('/sign_in_page')
        
        session['user_id'] = client.id
        return redirect('/client_dashboard')
    
    #if the person is a company
    if(role == 'company'):
        company = Company.check_email(data)
        if not company:
            flash("Invalid email or password for company log in", 'sign_in')
            return redirect('/sign_in_page')

        if not bcrypt.check_password_hash(company.password, request.form['password']):
            flash("Invalid email or password for company sign in", 'sign_in')
            return redirect('/sign_in_page')
        
        session['user_id'] = company.id
        return redirect('/company_dashboard')
    
    return redirect('/sign_in_page')
    #session['user_id'] = user.id
    #return redirect('/sign_in_page')
