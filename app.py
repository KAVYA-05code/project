from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Database configuration - change these as per your MySQL setup
db_config = {
    'host': 'localhost',
    'database': 'animalshelter',
    'user': 'root',
    'password': '12345'  # CHANGE THIS
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None

@app.route('/')
def index():
    # Show list of animals available for adoption
    conn = get_db_connection()
    animals = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM animals WHERE status='Available'")
        animals = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('index.html', animals=animals)


@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        age = request.form['age']
        description = request.form['description']
        status = 'Available'
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO animals (name, species, age, description, status) VALUES (%s, %s, %s, %s, %s)",
                (name, species, age, description, status)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Animal added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Database connection error.', 'danger')

    return render_template('add_animal.html')


@app.route('/adopt/<int:animal_id>', methods=['GET', 'POST'])
def adopt(animal_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('index'))

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM animals WHERE id = %s", (animal_id,))
    animal = cursor.fetchone()

    if not animal:
        flash("Animal not found.", 'warning')
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        adopter_name = request.form['adopter_name']
        adopter_contact = request.form['adopter_contact']

        # Insert adoption record
        cursor.execute(
            "INSERT INTO adoptions (animal_id, adopter_name, adopter_contact) VALUES (%s, %s, %s)",
            (animal_id, adopter_name, adopter_contact)
        )
        # Update animal status to Adopted
        cursor.execute(
            "UPDATE animals SET status = 'Adopted' WHERE id = %s",
            (animal_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Adoption successful! Thank you for giving a loving home.', 'success')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('adopt.html', animal=animal)

@app.route('/shelter_care')
def shelter_care():
    # Show all animals with their care status
    conn = get_db_connection()
    animals = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM animals")
        animals = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('shelter_care.html', animals=animals)


if __name__ == '__main__':
    app.run(debug=True)
