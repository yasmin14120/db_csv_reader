from flask import Flask, current_app
import json
import csv
import logging

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

logger = logging.getLogger(__name__)
data = {}


@app.before_first_request
def set_configures():
    with current_app.app_context():
        with open('data/DBNetz-Betriebsstellenverzeichnis-Stand2021-10.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            global data
            for row in reader:
                if row.get("RL100-Code"):
                    data[row["RL100-Code"]] = {
                        "Name": row["RL100-Langname"],
                        "Kurzname": row["RL100-Kurzname"],
                        "Typ": row["Typ Lang"]
                    }


@app.route('/betriebsstelle/<short_name>', methods=["GET"])
def get_betriebsstelle(short_name):
    try:
        global data
        if data[short_name]:
            return json.dumps(data[short_name], ensure_ascii=False), 200

    except KeyError:
        message = "The code {} does not exists".format(short_name)
        logger.error(message)
        return {"message": message}, 404
    except Exception:
        current_app.logger.error(
            "A not explicitly handled exception occurred: ", exc_info=True)
        return {"message": "An internal server error occurred."}, 500


if __name__ == '__main__':
    app.run(host="localhost", port="6000")
