import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}',
            params={
                'api_key': '5bbed2df17047c6f8fc00c70be5c8a00',
                'language': 'en-US',
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        st.warning(f'Could not fetch the poster for movie ID {movie_id}: {error}')
        return None

    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return None

    return f'https://image.tmdb.org/t/p/w500/{poster_path}'


movies_list = pickle.load(open('movies.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movies_list['title'].values

st.title("Movie Recommendation System")

st.write("Welcome to the Movie Recommendation System!")

slected_movie_name = st.selectbox(
    'Select a movie genre:',
    movie_titles
)

def recommend(movie):
    movie_index = movies_list[movies_list['title']==movie].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in recommended_indices:
        movie = movies_list.iloc[i[0]]
        movie_id = movie['movie_id']
        recommended_movies.append(movie['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

if st.button('Recommend'):
    
    names, posters = recommend(slected_movie_name)
    
    st.write("Recommended Movies:")
    columns = st.columns(len(names))
    for column, name, poster in zip(columns, names, posters):
        with column:
            st.subheader(name)
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.info('Poster not available.')