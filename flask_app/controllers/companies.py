from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.company import Company

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/company_signup_page')
def company_signup_page():
    return render_template('company_signUp.html')

@app.route('/company_signup', methods=['POST'])
def create_company():
    if not Company.validation_registering(request.form):
        return redirect('/company_signup_page')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'company_name' : request.form['company_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    companyAdded = Company.create_company(data)
    session['user_id'] = companyAdded

    return(redirect('/'))

@app.route('/company_dashboard')
def company_dashboard():
    return render_template('company_dashboard.html')

