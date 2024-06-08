from datetime import datetime, time, timedelta

from src.database.database import get_db
from src.database.measure import get_sensor_id


def analysis_02(sensor_id):
    db = get_db()
    cursor = db.cursor()
    dates = []

    if int(sensor_id) == int(get_sensor_id('O2')):
        try:
            cursor.execute(
                "SELECT date "
                "FROM Measures WHERE sensor_id = %s ",
                (sensor_id,)
            )
            for (date,) in cursor:
                dates.append(date)

            # Calculate min, max, and mean values for each day
            data_night = {}
            data_day = {}

            for date in dates:
                day = date.date()

                if day not in data_night:
                    day_start = datetime.combine(day, time(20, 0, 0))
                    data_measures = get_min_max_avg_o2(sensor_id, day_start, day_start + timedelta(hours=12))
                    if data_measures != (None, None, None):
                        data_night[day] = {'min': data_measures[1] / 10, 'max': data_measures[0] / 10,
                                           'avg': data_measures[2] / 10}
                    else:
                        data_night[day] = {'min': None, 'max': None, 'avg': None}

                if day not in data_day:
                    day_start = datetime.combine(day, time(8, 0, 0))
                    data_measures = get_min_max_avg_o2(sensor_id, day_start, day_start + timedelta(hours=12))
                    if data_measures != (None, None, None):
                        data_day[day] = {'min': data_measures[1] / 10, 'max': data_measures[0] / 10,
                                         'avg': data_measures[2] / 10}
                    else:
                        data_day[day] = {'min': None, 'max': None, 'avg': None}

            return data_night, data_day

        except Exception as e:
            print(f"Error when getting O2 values: {e}")

    return None


def get_min_max_avg_o2(sensor_id, date_start, date_end):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT MAX(value), MIN(value), AVG(value) "
            "FROM Measures WHERE sensor_id = %s and date BETWEEN (%s) and  (%s)",
            (sensor_id, date_start, date_end)
        )
        for (max_O2, min_O2, avg) in cursor:
            return max_O2, min_O2, avg

    except Exception as e:
        print(f"Error when getting O2 values: {e}")
