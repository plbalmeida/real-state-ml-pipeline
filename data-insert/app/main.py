from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel  # noqa 401
import mysql.connector
import pandas as pd
from io import StringIO
from .models import Property


app = FastAPI()


def get_db_connection():
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection: A MySQL database connection.
    """  # noqa 401
    connection = mysql.connector.connect(
        host="mysql",
        user="user",
        password="password",
        database="db01"
    )
    return connection


@app.post("/properties/")
def create_property(property: Property):
    """
    Inserts a new property into the tb01 table in the MySQL database.

    Args:
        property (Property): The property data to be inserted.

    Returns:
        dict: A message indicating the property was inserted successfully.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO tb01 (type, sector, net_usable_area, net_area, n_rooms, n_bathroom, latitude, longitude, price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """  # noqa 401
    cursor.execute(insert_query, (
        property.type,
        property.sector,
        property.net_usable_area,
        property.net_area,
        property.n_rooms,
        property.n_bathroom,
        property.latitude,
        property.longitude,
        property.price
    ))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Property inserted successfully"}


@app.post("/properties/from-csv/")
def create_properties_from_csv(file: UploadFile = File(...)):
    """
    Reads a CSV file and inserts the data into the tb01 table in the MySQL database.

    Args:
        file (UploadFile): The CSV file to be uploaded.

    Returns:
        dict: A message indicating the number of properties inserted successfully.

    Raises:
        HTTPException: If there is an error during the database operation.
    """  # noqa 401
    try:
        contents = file.file.read().decode("utf-8")
        data = pd.read_csv(StringIO(contents))
        connection = get_db_connection()
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO tb01 (type, sector, net_usable_area, net_area, n_rooms, n_bathroom, latitude, longitude, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """  # noqa 401
        for _, row in data.iterrows():
            cursor.execute(insert_query, (
                row['type'],
                row['sector'],
                row['net_usable_area'],
                row['net_area'],
                row['n_rooms'],
                row['n_bathroom'],
                row['latitude'],
                row['longitude'],
                row['price']
            ))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": f"{len(data)} properties inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
