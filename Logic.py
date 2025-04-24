from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load your movie dataset
movies = pd.read_csv('movies.csv', engine="python")  # or use 'latin1'

def get_recommendations(genre):
    # Simple filtering based on genre
    recommendations = movies[movies['genre'].str.contains(genre, case=False)]
    return recommendations[['title', 'description', 'rating']].to_dict(orient='records')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['genre']
    recommendations = get_recommendations(user_input)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)