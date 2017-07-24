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
# the couple table has relationships. Will it work as it does now or does it
# require sprecial attention?
class CrudHandler(MethodView):
    def get(self, item, id):
        session = db.Session()
        if id is None:
            limit = int(request.args.get('_perPage'))
            page = int(request.args.get('_page'))
            items = session.query(self.resolve_table(item)).limit(limit).\
                offset(limit * (page - 1)).all()
            return json.dumps([item.serialise() for item in items])
        else:
            return json.dumps(session.query(
                self.resolve_table(item)
            ).filter_by(id=id).first().serialise())

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

    def put(self, item, id):
        session = db.Session()
        session.query(self.resolve_table(item)).\
            filter_by(id=id).update(load_json())
        session.commit()
        return ''

    def resolve_table(self, item):
        if item == 'devices':
            return db.Device
        elif item == 'sims':
            return db.Sim
        elif item == 'couples':
            return db.Couple


view = CrudHandler.as_view('devices')
app.add_url_rule(
    '/<item>/<id>',
    view_func=view,
    methods=['GET', 'POST', 'DELETE', 'PUT'],
    strict_slashes=False
)
app.add_url_rule(
    '/<item>',
    view_func=view,
    methods=['GET', 'POST'],
    strict_slashes=False,
    defaults={'id': None}
)
# app.add_url_rule(
#     '/<item>/<id>',
#     view_func=view,
#     methods=['DELETE', 'UPDATE'],
#     strict_slashes=False
# )


# @app.route('/transfer/', methods=['POST'])  # PUT or POST
def transfer():
    """Takes a JSON object containing the couple ID and the company name"""
    data = load_json()
    return_message = 'Success'

    try:
        schemas.transfer_schema(data)
    except MultipleInvalid:
        abort(400)

    query = 'UPDATE couple SET assigned_to = %s WHERE id = %s'
    # print(query)

    cursor = database.cursor()
    cursor.execute(query, (
        schemas.company_mapping[data['company']], data['couple']
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
