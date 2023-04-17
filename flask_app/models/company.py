from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Company:
    def __init__(self, data):
        self.id = data['id']
        self.company_name = data['company_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.reports = []
        self.services = []
        self.responses = []

    @classmethod
    def create_company(cls, data):
        query = "INSERT INTO companies(company_name, email, password) VALUES(%(company_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('services').query_db(query, data)
        return result

    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM companies WHERE email = %(email)s"
        result = connectToMySQL('services').query_db(query, data)
        if len(result) < 1:
            return False
        
        return cls(result[0])

    @staticmethod
    def validation_registering(data):
        is_valid = True

        query = "SELECT * FROM companies WHERE email = %(email)s"
        result = connectToMySQL('services').query_db(query, data)
        if len(result) >= 1:
            flash("This email is already in use for a different account", 'company_register')
            is_valid = False

        if len(data['company_name']) < 1:
            flash("Company name can't be left empty", 'company_register')
            is_valid = False

        if len(data['email']) < 1:
            flash("email field can't be left empty", 'company_register')
            is_valid = False    

        if len(data['password']) < 8:
            flash("Password needs to be at least 8 characters long", 'company_register')
            is_valid = False

        if data['password'] != data['confirm_pass']:
            flash("Passwords don't match", 'company_register')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email. Please enter a valid email", 'company_register')
            is_valid = False

        return is_valid

    @staticmethod
    def validation_login(data):
        is_valid = True

        if len(data['password']) < 1:
            flash("pasword field is required", 'sign_in')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email. Please enter a valid email", 'sign_in')
            is_valid = False

        return is_valid