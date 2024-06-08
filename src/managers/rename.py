from src.database.database import get_db


def rename_manager():
    pass


def rename_greenhouse(greenhouse_serial, greenhouse_name):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE GreenHouses SET name = %s WHERE serial = %s",
            (greenhouse_serial, greenhouse_name)
        )
        db.commit()

    except Exception as e:
        print(f"Error when renaming greenhouse: {e}")
        return False
