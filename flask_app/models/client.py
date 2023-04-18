from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import report, company

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Client:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.reports = []
    
    @classmethod
    def create_client(cls, data):
        query = "INSERT INTO clients(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('services_reports').query_db(query, data)
        return result

    
    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM clients WHERE email = %(email)s"
        result = connectToMySQL('services_reports').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod 
    def get_client(cls, data):
        query = "SELECT * FROM clients WHERE id = %(id)s"
        result = connectToMySQL('services_reports').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_this_client_reports_with_company(cls):
        query = "SELECT * FROM reports LEFT JOIN clients ON clients.id = reports.client_id LEFT JOIN companies ON companies.id = reports.company_id;"
        result = connectToMySQL('services_reports').query_db(query)
        print(result)
        this_client_reports_with_company = []

        for report_each in result:
            '''
            report_object = {
                'id': report['id'],
                'issue': report['issue'],
                'service': report['service'],
                'created_at': report['created_at'],
                'updated_at': report['updated_at']
            }
            '''
            if report_each['client_id'] == session['user_id']:

                one_report_object = report.Report(report_each)

                report_company_object = {
                    'id': report_each['companies.id'],
                    'company_name': report_each['company_name'],
                    'email': report_each['companies.email'],
                    'password': report_each['companies.password'],
                    'created_at': report_each['companies.created_at'],
                    'updated_at': report_each['companies.updated_at']
                }

                report_company = company.Company(report_company_object)
                one_report_object.company = report_company

                this_client_reports_with_company.append(one_report_object)

        return this_client_reports_with_company


    @staticmethod
    def validation_registering(data):
        is_valid = True

        query = "SELECT * FROM clients WHERE email = %(email)s"
        result = connectToMySQL('services_reports').query_db(query, data)
        if len(result) >= 1:
            flash("This email is already in use for a different account", 'client_register')
            is_valid = False

        if len(data['first_name']) < 1:
            flash("first name can't be left empty", 'client_register')
            is_valid = False
        
        if len(data['last_name']) < 1:
            flash("last name can't be left empty", 'client_register')
            is_valid = False

        if len(data['email']) < 1:
            flash("email field can't be left empty", 'client_register')
            is_valid = False    

        if len(data['password']) < 8:
            flash("Password needs to be at least 8 characters long", 'client_register')
            is_valid = False

        if data['password'] != data['confirm_pass']:
            flash("Passwords don't match", 'client_register')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email. Please enter a valid email", 'client_register')
            is_valid = False

        return is_valid

    @staticmethod
    def validation_login(data):
        is_valid = True

        if len(data['password']) < 1:
            flash("pasword fied is required", 'sign_in')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email. Please enter a valid email", 'sign_in')
            is_valid = False

        return is_valid