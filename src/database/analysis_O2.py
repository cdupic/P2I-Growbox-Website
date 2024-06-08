from datetime import datetime, time, timedelta

from src.database.database import get_db
from src.database.measure import get_sensor_id


def analysis(sensor_id):
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
                day_start = datetime.combine(date.date(), time(0, 0, 0))

                if day_start not in data_night:
                    data_measures = get_min_max_avg_o2(sensor_id, day_start - timedelta(hours=6),
                                                       day_start + timedelta(hours=6))
                    if data_measures != (None, None, None):
                        data_night[day_start] = {'min': data_measures[1] / 10, 'max': data_measures[0] / 10,
                                                 'avg': data_measures[2] / 10}
                    else:
                        data_night[day_start] = {'min': None, 'max': None, 'avg': None}

                day_start = datetime.combine(date.date(), time(12, 0, 0))

                if day_start not in data_day:
                    data_measures = get_min_max_avg_o2(sensor_id, day_start - timedelta(hours=6),
                                                       day_start + timedelta(hours=6))
                    if data_measures != (None, None, None):
                        data_day[day_start] = {'min': data_measures[1] / 10, 'max': data_measures[0] / 10,
                                               'avg': data_measures[2] / 10}
                    else:
                        data_day[day_start] = {'min': None, 'max': None, 'avg': None}

            return data_night, data_day

        except Exception as e:
            print(f"Error when getting O2 values: {e}")

    return None, None


def get_min_max_avg_o2(sensor_id, date_start, date_end):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT MAX(value), MIN(value), AVG(value) "
            "FROM ProcessedMeasures WHERE sensor_id = %s and date BETWEEN (%s) and  (%s)",
            (sensor_id, date_start, date_end)
        )
        for (max_O2, min_O2, avg) in cursor:
            return max_O2, min_O2, avg

    except Exception as e:
        print(f"Error when getting O2 values: {e}")


def order_data(sensor_id):
    data_night, data_day = analysis(sensor_id)

    if data_night is not None and data_day is not None:
        days_night = list(data_night.keys())
        days_day = list(data_day.keys())
        night_min = [data['min'] for data in data_night.values()]
        night_max = [data['max'] for data in data_night.values()]
        night_avg = [data['avg'] for data in data_night.values()]

        day_min = [data['min'] for data in data_day.values()]
        day_max = [data['max'] for data in data_day.values()]
        day_avg = [data['avg'] for data in data_day.values()]

        data_night = {"date_values": days_night, "min_values": night_min, "max_values": night_max,
                      "avg_values": night_avg}
        data_day = {"date_values": days_day, "min_values": day_min, "max_values": day_max, "avg_values": day_avg}

        return data_night, data_day

    return None, None
