import os

from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask

from src.database.database import init_db, close_db
from src.managers.logout import logout_manager
from src.pages.greenhouse.overview import greenhouse_overview_page
from src.pages.greenhouse.sensor import greenhouse_sensor_page
from src.pages.greenhouses import greenhouses_page
from src.pages.landing import landing_page
from src.pages.login import login_page

load_dotenv()

class GrowBoxApp(Flask):
    def __init__(self, root_path=None):
        super().__init__(__name__.split('.')[0], root_path=root_path, template_folder='../templates/', static_folder='../static/')

        self.secret_key = os.getenv("SECRET_KEY")
        self.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)  # Session data will be stored for 1 year

        super().add_url_rule("/", methods=["GET"], view_func=landing_page)
        super().add_url_rule("/login", methods=["POST", "GET"], view_func=login_page)
        super().add_url_rule("/greenhouse", methods=["GET"], view_func=greenhouses_page)
        super().add_url_rule("/greenhouse/<greenhouse_id>/", methods=["POST", "GET"],
                             view_func=greenhouse_overview_page)
        super().add_url_rule("/greenhouse/<greenhouse_id>/sensor/<sensor_id>", methods=["GET"],
                             view_func=greenhouse_sensor_page)
        super().add_url_rule("/greenhouse/<greenhouse_id>/actuator/<actuator_id>", methods=["POST", "GET"],
                             view_func=greenhouse_sensor_page)

        super().add_url_rule("/manager/logout", methods=["POST", "GET"], view_func=logout_manager)

    def before_request(self, *args, **kwargs):
        init_db()

    def teardown_request(self, exception):
        close_db()

    def run(self, *args, **kwargs):
        super().run(debug=True, use_reloader=True, port=5050)


if __name__ == '__main__':
    app = GrowBoxApp()
    app.run()
