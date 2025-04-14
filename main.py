from flask import Flask, request, render_template, redirect, url_for, flash # type: ignore
import random
import string
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File to store the short links and original URLs
CSV_FILE = 'url_database.csv'

# In-memory database to store short links and their original URLs
url_database = {}

# Load data from the CSV file into the in-memory database
def load_data():
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    short_link, original_url = row
                    url_database[short_link] = original_url

# Save a new short link and its original URL to the CSV file
def save_data(short_link, original_url):
    with open(CSV_FILE, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([short_link, original_url])

# Function to generate a random short link
def generate_short_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        if original_url:
            short_link = generate_short_link()
            url_database[short_link] = original_url
            save_data(short_link, original_url)  # Save to CSV
            flash(f'Short link generated: {request.host_url}{short_link}', 'success')
        else:
            flash('Please enter a valid URL.', 'error')
    return render_template('home.html')

@app.route('/<short_link>')
def redirect_to_original(short_link):
    original_url = url_database.get(short_link)
    if original_url:
        return redirect(original_url)
    else:
        return "Short link not found!", 404

if __name__ == '__main__':
    load_data()  # Load data from CSV when the app starts
    app.run(debug=True)