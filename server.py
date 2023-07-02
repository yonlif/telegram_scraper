from flask import Flask, jsonify, request, send_from_directory, make_response
import mysql.connector

from database_connection import connect_to_db

# Create Flask application
app = Flask(__name__)


# Define a route to fetch data from the database
@app.route('/data', methods=['GET', 'OPTIONS'])
def get_data():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
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
                where_clauses.append("date(timestamp) BETWEEN %s AND %s")
                params.extend([from_date, to_date])

            # Process other filters
            for key, value in filters.items():
                if key not in ['from_date', 'to_date']:
                    if key == 'message':
                        # Split the message value into individual words
                        words = value.split(',')
                        sub_clauses = []
                        for word in words:
                            sub_clauses.append("message LIKE %s")
                            params.append(f"%{word}%")
                            sub_clauses.append("translated_message LIKE %s")
                            params.append(f"%{word}%")
                        where_clauses.append("(" + " OR ".join(sub_clauses) + ")")
                    else:
                        where_clauses.append(f"{key} = %s")
                        params.append(value)

            # Add the WHERE clause to the query if there are any filters
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            # Print the query
            print(f'Query: {query}')
            # Print the parameters
            print(f'Params: {params}')

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
                'translated_message': row[5],
                'photo_url': row[6],
                'timestamp': row[7]
                # Add more fields as per your database schema
            })

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return _corsify_actual_response(jsonify(data))

    except mysql.connector.Error as error:
        return str(error)

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Define a route to serve static photos
@app.route('/downloaded_photos/<path:filename>')
def serve_photo(filename):
    return send_from_directory('downloaded_photos', filename)


# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0")
