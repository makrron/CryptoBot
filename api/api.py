import collections
import sqlite3
from flask import Flask, json, request

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('cryptobot.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/robosats_alerts/<user_id>/', methods=['GET', 'POST', 'DELETE'])
def robosats_alert(user_id):
    conn = get_db_connection()
    if request.method == 'GET':
        cursor = conn.execute(
            f"SELECT ALERT_ID, FIAT_CURRENCY, AMOUNT, PREMIUM, METHOD, DIRECTION  FROM ROBOSATS_ALERTS "
            f"WHERE USER_ID LIKE '{user_id}'").fetchall()

        objects_list = {"ALERTS": []}
        for row in cursor:
            d = collections.OrderedDict()
            d["ALERT_ID"] = row[0]
            d["FIAT_CURRENCY"] = row[1]
            d["AMOUNT"] = row[2]
            d["PREMIUM"] = row[3]
            d["METHOD"] = row[4]
            d["DIRECTION"] = row[5]
            objects_list["ALERTS"].append(d)

        response = app.response_class(
            response=json.dumps(objects_list),
            mimetype='application/json',
        )
        return response
    elif request.method == 'POST':
        data = request.get_json()
        data = json.loads(data)
        for item in data['ALERTS']:
            try:
                conn.execute(
                    f"INSERT INTO ROBOSATS_ALERTS (USER_ID, FIAT_CURRENCY, AMOUNT, PREMIUM, METHOD, DIRECTION) "
                    f"VALUES ('{item['USER_ID']}', '{item['FIAT_CURRENCY']}', '{item['AMOUNT']}', '{item['PREMIUM']}', "
                    f"'{item['METHOD']}', '{item['DIRECTION']}')")
                conn.commit()
            except Exception as e:
                print(e)
        conn.close()
        return data
    elif request.method == 'DELETE':
        data = request.get_data()
        data = data.decode('utf-8')
        try:
            conn.execute(f"DELETE FROM ROBOSATS_ALERTS WHERE ALERT_ID like '{int(data)}'")
            conn.commit()
        except Exception as e:
            print(e)
        return data


@app.route('/robosats_alerts/', methods=['GET'])
def all_robosats_alerts():
    conn = get_db_connection()
    if request.method == 'GET':
        cursor = conn.execute(
            f"SELECT ALERT_ID, USER_ID, FIAT_CURRENCY, AMOUNT, PREMIUM, METHOD, DIRECTION  FROM ROBOSATS_ALERTS").fetchall()

        objects_list = {"ALERTS": []}
        for row in cursor:
            d = collections.OrderedDict()
            d["ALERT_ID"] = row[0]
            d["USER_ID"] = row[1]
            d["FIAT_CURRENCY"] = row[2]
            d["AMOUNT"] = row[3]
            d["PREMIUM"] = row[4]
            d["METHOD"] = row[5]
            d["DIRECTION"] = row[6]
            objects_list["ALERTS"].append(d)

        response = app.response_class(
            response=json.dumps(objects_list),
            mimetype='application/json',
        )
        return response


if __name__ == '__main__':
    app.run(debug=False)
