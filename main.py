import click
import sqlite3


# Create a connection to the database
conn = sqlite3.connect('mydatabase.db')

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create a table in the database to store data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        id INTEGER PRIMARY KEY,
        name TEXT,
        value INT
    )
''')

# Save the changes to the database
conn.commit()


### Commands for the application ###


# Define a function to create a new row in the table
@click.command()
@click.option('--name', prompt='Name')
@click.option('--value', prompt='Value', type=int)
def create(name, value):
    cursor.execute('''
        INSERT INTO mytable (name, value)
        VALUES (?, ?)
    ''', (name, value))
    conn.commit()


# Define a function to read all rows from the table
@click.command()
def read():
    cursor.execute('''
        SELECT * FROM mytable
    ''')
    for row in cursor:
        print(row)


# Define a function to update a row in the table
@click.command()
@click.option('--id', prompt='ID')
@click.option('--name', prompt='Name')
@click.option('--value', prompt='Value')
def update(id, name, value):
    cursor.execute('''
        UPDATE mytable
        SET name=?, value=?
        WHERE id=?
    ''', (name, value, id))
    conn.commit()


# Define a function to delete a row from the table
@click.command()
@click.option('--id', prompt='ID')
def delete(id):
    cursor.execute('''
        DELETE FROM mytable WHERE id=?
    ''', (id,))
    conn.commit()


# Define a function to search the database
@click.command()
@click.option('--search-term', prompt='Enter the search term')
def search(search_term):
    # build the SQL query to search for the given term in the name and value columns
    sql = f"SELECT * FROM mytable WHERE name LIKE '%{search_term}%' OR value LIKE '%{search_term}%'"
    # execute the query
    results = cursor.execute(sql).fetchall()
    # If there are no results, print a message
    if len(results) == 0:
        print(f"No results found for '{search_term}'")
    # If there are results, print them
    elif len(results) == 1:
        for row in results:
            print(row)
            # print the only result found
            print(f"Only {len(results)} result found")
    else:
        for row in results:
            print(row)
            # print the number of results found
        print(f"{len(results)} results found")


# Define a function to read all column headers from the database
@click.command()
def columns():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    query = 'PRAGMA table_info(mytable)'
    c.execute(query)
    column_names = [row[1] for row in c.fetchall()]
    click.echo(f'{column_names}')


# Defines a group of commands to interact with the database
@click.group()
def export():
    pass

#  Defines a function to export the database to a text file
@export.command()
def txt():
    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Fetch all rows from the database
    c.execute('SELECT * FROM mytable')
    rows = c.fetchall()

    # Write the rows to a text file
    with open('mytextfile.txt', 'w') as f:
        for row in rows:
            f.write(str(row) + '\n')

    # Close the connection
    conn.close()

    click.echo('Successfully exported data to mytextfile.txt')


# Defines a function to export the database to a CSV file
@export.command()
def csv():
    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Fetch all rows from the database
    c.execute('SELECT * FROM mytable')
    rows = c.fetchall()

    # Write the rows to a CSV file
    with open('mycsvfile.csv', 'w') as f:
        for row in rows:
            # escape the comma with a backslash
            f.write(','.join([str(i).replace(',', '\\,') for i in row]) + '\n')
  
    # Close the connection
    conn.close()

    click.echo('Successfully exported data to mycsvfile.csv')


# Define a main function to add all the other functions as commands
@click.group()
def main():
    pass


# Add functions as commands
main.add_command(create)
main.add_command(read)
main.add_command(update)
main.add_command(delete)
main.add_command(export)
main.add_command(search)
main.add_command(columns)


# Run the main function
if __name__ == '__main__':
    main()
