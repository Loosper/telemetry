#!/usr/bin/env python3

import sys
import json
import logging

import database_schema as db

from flask import Flask, request, abort
from flask.views import MethodView
from voluptuous import Schema, Required, MultipleInvalid, All, Any, Number, In


# WORKING PLAN:
# 1. get databse in order
# 2. Make a post endpoint to input data.
# 3. Make a get endpoint to retrieve data.
# 4 UPDATE and DELETE.
# 5. Repeat for every db table.
# 6. Make ng-admin endpoint to test. - happens in prallel with every method

logger = logging.getLogger('App_logger')
app = Flask(
    __name__,
    static_url_path='/resource',
    static_folder='resources'
)
database = None


def load_json():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except json.JSONDecodeError:
        abort(400)
    return data


@app.route('/')
def load_page():
    return app.send_static_file('telemetry.html')


# TODO: transferring
# NOTE: LAN access is assumed and no data validation is provided
class CrudHandler(MethodView):
    def get(self, item):
        session = db.Session()
        limit = int(request.args.get('_perPage'))
        page = int(request.args.get('_page'))
        items = session.query(self.resolve_table(item)).limit(limit).\
            offset(limit * (page - 1)).all()
        return json.dumps([item.serialise() for item in items])

    def post(self, item):
        session = db.Session()
        db_item = load_json()
        session.add(self.resolve_table(item)(**db_item))
        session.commit()
        return ''

    def delete(self, item, id):
        session = db.Session()
        db_item = session.query(self.resolve_table(item)).\
            filter_by(id=id).delete()
        session.commit()
        return ''

    def update(self, item, id):
        pass

    def resolve_table(self, item):
        if item == 'devices':
            return db.Device
        elif item == 'sims':
            return db.Sim
        elif item == 'couples':
            return db.Couple


view = CrudHandler.as_view('devices')
app.add_url_rule(
    '/<item>/',
    view_func=view,
    methods=['GET', 'POST'],
    strict_slashes=False
)
app.add_url_rule(
    '/<item>/<id>',
    view_func=view,
    methods=['DELETE', 'UPDATE'],
    strict_slashes=False
)


# @app.route('/transfer/', methods=['POST'])  # PUT or POST
def transfer():
    """Takes a JSON object containing the couple ID and the company name"""
    data = load_json()

    company_mapping = {
        -1: None,
        0: 'Maverick Cardio-Telemetry',
        1: 'Maverick Water-Telemetry'
    }
    return_message = 'Success'

    schema = Schema({
        'couple': All(int, Number(precision=10)),
        'company': All(int, In(company_mapping.keys()))
        }, required=True)

    try:
        schema(data)
    except MultipleInvalid:
        # print(exc.msg)
        abort(400)

    # literal strings on 3.6
    query = 'UPDATE couple SET assigned_to = %s WHERE id = %s'
    # print(query)

    cursor = database.cursor()
    cursor.execute(query, (
        company_mapping[data['company']], data['couple']
    ))

    if not cursor.fetchall():
        return_message = 'Invalid couple id'
        # perhaps needs to be 400

    return return_message


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        TESTING=True
        # DATABASE=database
    )

    app.run(host='127.0.0.1')
