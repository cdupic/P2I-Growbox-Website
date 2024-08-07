import os
from datetime import timedelta

from flask import Flask

from src.database.database import init_db, close_db
from src.managers.associate import associate_manager
from src.managers.login import login_manager
from src.managers.logout import logout_manager
from src.managers.permission import permission_manager
from src.managers.plant import plant_manager
from src.managers.processed_measures import processed_measures_manager
from src.managers.signup import signup_manager
from src.managers.timestamp import timestamp_manager
from src.pages.greenhouse.actuator import greenhouse_actuator_page
from src.pages.greenhouse.collaborator import greenhouse_collaborator_page
from src.pages.greenhouse.notifications import greenhouse_notification_page
from src.pages.greenhouse.overview import greenhouse_overview_page
from src.pages.greenhouse.plants import greenhouse_plants_page
from src.pages.greenhouse.sensor import greenhouse_sensor_page
from src.pages.greenhouses import greenhouses_page
from src.pages.landing import landing_page
from src.pages.legal import cgu_page
from src.pages.login import login_page
from src.pages.signup import signup_page


class GrowBoxApp(Flask):
    def __init__(self, root_path=None):
        print("Starting GrowBoxApp with root path: ", root_path)
        super().__init__(__name__.split('.')[0], root_path=root_path + '/src', template_folder='../templates/',
                         static_folder='../static/')

        self.secret_key = os.getenv("SECRET_KEY")
        self.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)  # Session data will be stored for 1 year

        super().add_url_rule("/", methods=["GET"], view_func=landing_page)
        super().add_url_rule("/cgu", methods=["GET"], view_func=cgu_page)
        super().add_url_rule("/login", methods=["GET"], view_func=login_page)
        super().add_url_rule("/signup", methods=["GET"], view_func=signup_page)
        super().add_url_rule("/greenhouse", methods=["GET"], view_func=greenhouses_page)
        super().add_url_rule("/greenhouse/<greenhouse_serial>/", methods=["GET"],
                             view_func=greenhouse_overview_page)
        super().add_url_rule("/greenhouse/<greenhouse_serial>/plants", methods=["GET"],
                             view_func=greenhouse_plants_page)
        super().add_url_rule("/greenhouse/<greenhouse_serial>/sensor/<sensor_id>", methods=["GET"],
                             view_func=greenhouse_sensor_page)
        super().add_url_rule("/greenhouse/<greenhouse_serial>/actuator/<actuator_id>", methods=["GET"],
                             view_func=greenhouse_actuator_page)
        super().add_url_rule("/greenhouse/<greenhouse_serial>/collaborators", methods=["GET"],
                             view_func=greenhouse_collaborator_page)
        super().add_url_rule("/greenhouse/<greenhouse_serial>/notifications", methods=["GET"],
                             view_func=greenhouse_notification_page)

        super().add_url_rule("/manager/logout", methods=["POST", "GET"], view_func=logout_manager)
        super().add_url_rule("/manager/login", methods=["POST"], view_func=login_manager)
        super().add_url_rule("/manager/signup", methods=["POST"], view_func=signup_manager)
        super().add_url_rule("/manager/associate", methods=["GET"], view_func=associate_manager)
        super().add_url_rule("/manager/plant", methods=["POST"], view_func=plant_manager)
        super().add_url_rule("/manager/timestamp", methods=["POST"], view_func=timestamp_manager)
        super().add_url_rule("/manager/permission", methods=["POST"], view_func=permission_manager)
        super().add_url_rule("/manager/processed_measures", methods=["POST"], view_func=processed_measures_manager)

    def before_request(self, *args, **kwargs):
        init_db()

    def teardown_request(self, exception):
        close_db()

    def run(self, *args, **kwargs):
        super().run(debug=True, use_reloader=True, port=5050)
