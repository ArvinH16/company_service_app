from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.client import Client
from flask_app.models.report import Report
from flask_app.models.company import Company

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
    session['user_id'] = clientAdded

    return(redirect('/'))

@app.route('/client_dashboard')
def client_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : session['user_id']
    }

    client = Client.get_client(data)

    reports = Client.get_this_client_reports_with_company()

    all_companies = Company.get_all_companies()

    return render_template('client_dashboard.html', reports = reports, client = client, all_companies = all_companies)

@app.route('/client_make_report_controller', methods=['POST'])
def client_make_report_controller():

    data = {
        'service': request.form['service'],
        'issue': request.form['issue'],
        'company_id': request.form['company_id'],
        'client_id': session['user_id']
    }
    Report.client_make_report(data)
    print("Hi 1")
    return redirect('/client_dashboard')
