from mysql.connector import (connect)

config = {
    "user": "rony",
    "password": "Yuval_300207",
    "host": "localhost",
    "database": "todo_db"
}

cnx = connect(**config)