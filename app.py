import pandas as pd
import streamlit as st
import pickle
import requests

def fetchposter(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=48eca0bc48978c7ce292043731467bf8".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendedm = []
    recommendedp = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        # Fetch poster from API
        recommendedp.append(fetchposter(movie_id))
        recommendedm.append(movies.iloc[i[0]].title)
    return recommendedm, recommendedp  # Return both movie titles and poster paths

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Want help finding similar movies?', movies['title'].values)

if st.button('Show Recommendation'):
    recommendedm, recommendedp = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommendedm[i])
            st.image(recommendedp[i], use_column_width=True)
