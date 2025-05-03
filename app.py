import os
import pickle
import streamlit as st
import requests

# Function to fetch movie posters from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')  # Using .get() to prevent KeyErrors
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500"  # Placeholder image if no poster is found

# Function to recommend movies based on similarity
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:  # Get top 5 recommendations
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters

    except Exception as e:
        st.error(f"Error: {e}")  # Display errors in Streamlit UI
        return [], []  # Return empty lists if an error occurs

# Streamlit UI
st.header('🎬 Movie Recommender System')

# Load Pickle Files Safely
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory

    movies_path = os.path.join(base_dir, 'movie_list.pkl')
    similarity_path = os.path.join(base_dir, 'similarity.pkl')

    if not os.path.exists(movies_path) or not os.path.exists(similarity_path):
        st.error("Error: Required data files (movie_list.pkl, similarity.pkl) not found.")
    else:
        with open(movies_path, 'rb') as file:
            movies = pickle.load(file)

        with open(similarity_path, 'rb') as file:
            similarity = pickle.load(file)

        movie_list = movies['title'].values
        selected_movie = st.selectbox("🎥 Select a movie:", movie_list)

        if st.button('🔍 Show Recommendations'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

            if recommended_movie_names:
                cols = st.columns(5)  # Create 5 columns for movie recommendations
                for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
                    with col:
                        st.text(name)
                        st.image(poster)
            else:
                st.warning("No recommendations found.")
except Exception as e:
    st.error(f"An error occurred: {e}")  # Display error message in Streamlit
