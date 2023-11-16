import psycopg2

conn = None

def init_db(host, dbname, user, password):
    """
    Initialize the PostgreSQL database connection.
    """
    global conn
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password
    )

def save(response):
    """
    Save the form response to the PostgreSQL database.
    """
    global conn
    try:
        # Create a cursor object
        cur = conn.cursor()

        # SQL query to insert the response into the table
        query = "INSERT INTO responses (response_data) VALUES (%s);"

        # Execute the query
        cur.execute(query, (response,))

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in save operation:", error)
    finally:
        if conn is not None:
            conn.close()
