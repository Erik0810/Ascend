import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Users/erikk/OneDrive/Desktop/Klatreproj/app/users.db')  # Replace with your database file
cursor = conn.cursor()

# Run your SQL query
query = "SELECT * FROM users;"  # Replace with your query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()