#!/usr/bin/env python3

import sys
import json
import logging
import schemas
import MySQLdb as mysqldb
from flask import Flask, request, abort
from _mysql_exceptions import OperationalError
from voluptuous import MultipleInvalid

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


@app.route('/new/<thing>', methods=['POST'])
def enter(thing):
    mapping = {
        'sim': schemas.enter_sim_schema,
        'device': schemas.enter_device_schema
    }
    if thing not in mapping.keys():
        abort(404)
    data = load_json()

    try:
        mapping[thing](data)
    except MultipleInvalid as e:
        print(e.error_message)
        abort(400)

    query = 'INSERT INTO %s ({}) VALUES ({})'

    return 200


@app.route('/transfer/', methods=['POST'])  # PUT or POST
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
    try:
        database = mysqldb.connect(
            user='user',
            passwd='user',
            db='telemetry'
        )
    except OperationalError:
        print("Database not found!")
        sys.exit()

    app.config.update(
        DEBUG=True,
        TESTING=True
        # DATABASE=database
    )
    # app.config['DATABASE'] = database

    app.run(host='127.0.0.1')
    database.close()
