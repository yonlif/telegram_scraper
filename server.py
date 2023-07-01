from flask import Flask, jsonify, request
import mysql.connector

from database_connection import connect_to_db

# Create Flask application
app = Flask(__name__)


# Define a route to fetch data from the database
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Connect to the MySQL database
        conn = connect_to_db()

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Construct the base SELECT query
        query = "SELECT * FROM telegram_messages"

        # Get the filter parameters from the query string
        filters = request.args

        # If filters are provided, build the WHERE clause dynamically
        if filters:
            where_clauses = []
            params = []

            # Process timestamp range filters
            from_date = filters.get('from_date')
            to_date = filters.get('to_date')

            if from_date and to_date:
                where_clauses.append("timestamp BETWEEN %s AND %s")
                params.extend([from_date, to_date])

            # Process other filters
            for key, value in filters.items():
                if key != 'from_date' and key != 'to_date':
                    where_clauses.append(f"{key} = %s")
                    params.append(value)

            # Add the WHERE clause to the query if there are any filters
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            # Execute the query with the provided parameters
            cursor.execute(query, tuple(params))
        else:
            # Execute the query without any filters
            cursor.execute(query)

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries for JSON serialization
        data = []
        for row in rows:
            data.append({
                'message_db_id': row[0],
                'chat_name': row[1],
                'sender_name': row[2],
                'sender_phone': row[3],
                'message': row[4],
                'photo_url': row[5],
                'timestamp': row[6]
                # Add more fields as per your database schema
            })

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return jsonify(data)

    except mysql.connector.Error as error:
        return str(error)


# Run the Flask application
if __name__ == '__main__':
    app.run()
