from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Client:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.responses = []
        self.reports = []
    
    @classmethod
    def create_client(cls, data):
        query = "INSERT INTO clients(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('services').query_db(query, data)
        return result

    
    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM clients WHERE email = %(email)s"
        result = connectToMySQL('services').query_db(query, data)
        if len(result) < 1:
            return False
        
        return cls(result[0])

    @classmethod 
    def get_client(cls, data):
        query = "SELECT * FROM clients WHERE id = %(id)s"
        result = connectToMySQL('services').query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validation_registering(data):
        is_valid = True

        query = "SELECT * FROM clients WHERE email = %(email)s"
        result = connectToMySQL('services').query_db(query, data)
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