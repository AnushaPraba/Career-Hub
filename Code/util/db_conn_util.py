import mysql.connector
from util.db_property_util import DBPropertyUtil
from exception.database_conn_exception import DatabaseConnectionException

class DBConnUtil:
    @staticmethod
    def get_connection(prop_file_name: str):
        try:
            # Get the full connection string
            conn_str = DBPropertyUtil.get_connection_string(prop_file_name)

            # Parse the connection string into a dictionary
            conn_params = {}
            for item in conn_str.split(';'):
                if '=' in item:
                    key, value = item.split('=', 1)
                    conn_params[key.strip()] = value.strip()

            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host=conn_params.get('host'),
                user=conn_params.get('user'),
                password=conn_params.get('password'),
                database=conn_params.get('database')
            )
            return conn

        except mysql.connector.Error as err:
            raise DatabaseConnectionException(err)

        except Exception as e:
            raise DatabaseConnectionException(f"Unexpected database error: {str(e)}")

