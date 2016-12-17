#!/usr/bin/env python3

import sys
import json
import logging
import MySQLdb as mysqldb
from flask import Flask, request, abort
from voluptuous import Schema, Required, MultipleInvalid, All, Any, Number, In
from _mysql_exceptions import OperationalError


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


@app.route('/new/<thing>')
def enter(thing):
    voluptuous.Schema({

    })


@app.route('/transfer/', methods=['POST'])  # PUT or POST
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
