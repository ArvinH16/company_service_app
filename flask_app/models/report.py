from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import client, company
from flask import flash, session



class Report:
    def __init__(self, data):
        self.id = data['id']
        self.issue = data['issue']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.service_id = data['service_id']
        self.company_id = data['company_id']

        self.client_id = None

    @classmethod
    def get_this_client_reports(cls):
        data = {
            'user_id' : session['user_id']
        }
        query = "SELECT * FROM reports WHERE reports.client_id = %(user_id)s"
        result = connectToMySQL('services').query_db(query, data)
        report_objects = []
        for report in result:
            report_object = cls(report)
            report_objects.append(report_object)
        return report_objects
