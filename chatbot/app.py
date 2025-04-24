from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load movie dataset
movies = pd.DataFrame()  # Initialize an empty DataFrame

try:
    if not os.path.exists('movies.csv'):
        raise FileNotFoundError("movies.csv file not found.")
    
    movies = pd.read_csv('movies.csv', on_bad_lines='skip')
    movies.columns = movies.columns.str.strip()
    print("Columns in the DataFrame:", movies.columns.tolist())  # Debug
except Exception as e:
    print(f"Error loading CSV file: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre'].lower()

    # Ensure column names are valid
    if 'genre' not in movies.columns or 'title' not in movies.columns:
        return render_template('index.html', recommendations=["Required columns not found in the dataset."])

    filtered_movies = movies[movies['genre'].str.contains(genre, case=False, na=False)]

    if filtered_movies.empty:
        return render_template('index.html', recommendations=["No movies found for this genre."])

    num_recommendations = min(10, len(filtered_movies))
    recommendations = filtered_movies.sample(n=num_recommendations)[['title', 'genre']].to_dict(orient='records')

    return render_template('index.html', recommendations=recommendations)
    print(recommendations)

if __name__ == '__main__':
    app.run(debug=True)