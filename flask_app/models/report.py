from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import client, company
from flask import flash, session



class Report:
    def __init__(self, data):
        self.id = data['id']
        self.issue = data['issue']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.service = data['service']

        self.company = None
        self.client = None

    #this method might be redundant
    @classmethod
    def get_all_client_reports(cls):
        data = {
            'client_id' : session['user_id']
        }
        query = "SELECT * FROM reports WHERE reports.client_id = %(client_id)s;"
        result = connectToMySQL('services_reports').query_db(query, data)
        report_objects = []
        for report in result:
            report_object = cls(report)
            report_objects.append(report_object)
        return report_objects

    @classmethod
    def client_make_report(cls, data):
        print("Hi 2")
        query = "INSERT INTO reports(service, issue, company_id, client_id) VALUES(%(service)s, %(issue)s, %(company_id)s, %(client_id)s);"
        result = connectToMySQL('services_reports').query_db(query, data)
        return result

    @classmethod
    def get_all_company_reports(cls):
        data = {
            'company_id': session['user_id']
        }
        query = "SELECT * FROM reports WHERE reports.company_id = %(company_id)s"
        result = connectToMySQL('services_reports').query_db(query, data)

        all_company_reports = []

        for report_each in result:
            one_report = cls(report_each)

            all_company_reports.append(one_report)

        return all_company_reports

