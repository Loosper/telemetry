import sys
import json
import logging
import MySQLdb as mysqldb
from flask import Flask, request, abort
from _mysql_exceptions import OperationalError

logger = logging.getLogger('App_logger')
app = Flask(
    __name__,
    static_url_path='/resource',
    static_folder='resources'
)


@app.route('/')
def load_page():
    return app.send_static_file('telemetry.html')


@app.route('/transfer/', methods=['POST'])  # PUT or POST
def transfer():
    '''Takes a JSON object containing the couple ID and the company name'''
    try:
        data = json.loads(request.get_json())
    except json.JSONDecodeError:
        abort(400)

    keys = ('couple', 'company')
    company_mapping = {
        0: 'Maverick Cardio-Telemetry',
        1: 'Maverick Water-Telemetry'
    }
    return_message = 'Success'

    try:
        assert all(key in data for key in keys)
        assert isinstance(data['couple'], int) and (isinstance(
            data['company'],
            int
        ) or data['company'] is None)
        assert 1000000000 <= data['couple'] <= 9999999999
        if data['company'] is not None:
            assert data['company'] in company_mapping.keys()
    except AssertionError:
        abort(400)
    except:
        ex_type, value, traceback = sys.exc_info()
        logger.error("An {} ocurred. Message: {}")
        # logger.error(traceback)
        # Unhandled exception logging?
        abort(500)
    # print(data)

    # literal strings an 3.6
    querry = 'UPDATE couple SET assigned_to = %s WHERE id = %s'  # .format(
    #     company_mapping.get(data['company'], 'NULL'), data['couple']
    #     mapping table would be nice
    # )
    # print(querry)

    cursor = database.cursor()
    cursor.execute(querry, (
        company_mapping.get(data['company'], 'DEFAULT'), data['couple']
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
