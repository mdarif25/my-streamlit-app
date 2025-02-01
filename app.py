import streamlit as st
st.title("Movie Recommendation System")
import pickle
import requests
def fetch_poster(movie_ids):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=a792d59b3ac771ed94b4450e3a70e831&language=en-US".format(movie_ids))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']
#
movies_list=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
def recommend(movie):
    idx_of_movie=movies_list[movies_list['title']==movie].index[0]
    idx_moviesimilarity_pair=list(enumerate(similarity[idx_of_movie]))
    top_movies= sorted(idx_moviesimilarity_pair,reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]

    for tm in top_movies:
        recommended_movies.append(movies_list.iloc[tm[0]].title)
        recommended_movies_poster.append(fetch_poster(movies_list.iloc[tm[0]].movie_id))
    return recommended_movies,recommended_movies_poster

movie_list=movies_list['title'].values

selected_movie = st.selectbox(
    "Which movie you want to watch today?",
    movie_list,
    index=None,
    placeholder="Select movie...",
)

if st.button("Recommend"):

    movie_name, movie_poster = recommend(selected_movie)

 # Create 5 columns with adjusted spacing
    cols = st.columns(5, gap="small")
# Display movie names and posters
    for i in range(5):
        with cols[i]:
            st.text(movie_name[i])
            st.image(movie_poster[i] if movie_poster[i] else placeholder_image, use_container_width=True)


# Add a footer
st.markdown(
    """
    <div style="text-align: center;">
        Powered by <a href="https://www.themoviedb.org/">TMDb API</a> and <a href="https://streamlit.io/">Streamlit</a>
    </div>
    """,
    unsafe_allow_html=True,
)