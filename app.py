import pandas as pd
import streamlit as st
import pickle
import requests

import zipfile
import io

def getSimilarityfile():
    zip_file_path = 'similarity.zip'

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:

        file_name = 'similarity.pkl'  # Replace with the actual file name inside the ZIP
        with zip_ref.open(file_name) as file:

            file_contents = pickle.load(file)
    return file_contents

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c44305560298bd92442e71a1d0c241fe'.format(movie_id))
    data = response.json()
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']

movies_list = pickle.load(open('movie_dictk.pkl','rb'))
movies = pd.DataFrame(movies_list)

similarity = getSimilarityfile()


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    recommended_poster =[]
    for i in movies_list:
        recommended.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended, recommended_poster


st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Type a movie',
    (movies['title'].values)
)

if st.button("Recommend"):
    # Assuming `recommend` returns two lists: `names` and `posters`
    names, posters = recommend(selected_movie_name)

    # Create 5 columns
    cols = st.columns(5)

    # Loop through the movies and their posters
    for i in range(len(names)):
        with cols[i % 5]:  # Use modulo to handle wrapping if more than 5 items
            st.image(posters[i], caption=names[i])
