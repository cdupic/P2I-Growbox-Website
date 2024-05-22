import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, g

from src.database.database import get_db
from src.managers.logout import logout_manager
from src.pages.greenhouse.overview import greenhouse_overview_page
from src.pages.greenhouse.sensor import greenhouse_sensor_page
from src.pages.greenhouses import greenhouses_page
from src.pages.landing import landing_page
from src.pages.login import login_page

load_dotenv()
app = Flask(__name__.split('.')[0], template_folder='../templates/', static_folder='../static/')
app.secret_key = os.getenv("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)  # Session data will be stored for 1 year

app.add_url_rule("/", methods=["GET"], view_func=landing_page)
app.add_url_rule("/login", methods=["POST", "GET"], view_func=login_page)
app.add_url_rule("/greenhouse", methods=["GET"], view_func=greenhouses_page)
app.add_url_rule("/greenhouse/<greenhouse_id>/", methods=["POST", "GET"], view_func=greenhouse_overview_page)
app.add_url_rule("/greenhouse/<greenhouse_id>/sensor/<sensor_id>", methods=["GET"],
                 view_func=greenhouse_sensor_page)
app.add_url_rule("/greenhouse/<greenhouse_id>/actuator/<actuator_id>", methods=["POST", "GET"],
                 view_func=greenhouse_sensor_page)

app.add_url_rule("/manager/logout", methods=["POST", "GET"], view_func=logout_manager)


@app.before_request
def before_request():
    g.db = get_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5050)
