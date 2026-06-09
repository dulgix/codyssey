import csv
from datetime import datetime

import pymysql


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "dmsnco129!!"
DB_NAME = "codyssey"
TABLE_NAME = "mars_weather"
CSV_FILE_NAME = "mars_weathers_data.csv"


def connect_mysql():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4"
    )


def change_datetime(date_text):
    if date_text is None:
        raise ValueError("날짜 값이 없습니다.")

    date_text = date_text.strip()

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d"
    ]

    for date_format in formats:
        try:
            return datetime.strptime(date_text, date_format)
        except ValueError:
            pass

    raise ValueError("날짜 형식이 올바르지 않습니다: " + date_text)


def change_float(value):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def change_int(value):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    lower_value = value.lower()

    if lower_value in ["true", "yes", "y"]:
        return 1

    if lower_value in ["false", "no", "n"]:
        return 0

    try:
        return int(float(value))
    except ValueError:
        return None


def read_csv_file():
    weather_data = []

    with open(CSV_FILE_NAME, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            mars_date = change_datetime(row.get("mars_date"))
            temp = change_float(row.get("temp"))
            storm = change_int(row.get("storm"))

            weather_data.append((mars_date, temp, storm))

    return weather_data


def insert_weather_data(connection, weather_data):
    sql = f"""
        INSERT INTO {TABLE_NAME}
        (mars_date, temp, storm)
        VALUES (%s, %s, %s)
    """

    with connection.cursor() as cursor:
        for data in weather_data:
            cursor.execute(sql, data)

    connection.commit()


def main():
    connection = connect_mysql()

    weather_data = read_csv_file()
    insert_weather_data(connection, weather_data)

    connection.close()

    print("CSV 데이터를 MySQL에 저장했습니다.")


if __name__ == "__main__":
    main()