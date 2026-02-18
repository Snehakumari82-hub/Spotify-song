import streamlit as st
import pickle

#Load files
df = pickle.load(open("song_df.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

st.title("Song Recommender System")
user_input = st.text_input("Enter a song name")


def recommend(song_name):
    song_name = song_name.lower().strip()

    try:
        index =  df[df['song'].str.lower()==song_name].index[0]
    except Exception as e:
        st.write("Error:", e)
        return []
    distances = similarity[index]

    song_list = sorted(list(enumerate(distances)),
                       reverse=True,key=lambda x: x[1])[1:6]
    
    rec = []

    for i,score in song_list:
        rec.append({
            "song": df.iloc[i]['song_name'],
            "artist": df.iloc[i]['artist'],
            "thumbnail": df.iloc[i]['thumbnail']
            if'thumbnail' in df.columns else None
        })
    return rec
 
if st.button("Recommend"):
    if user_input=="":
     st.warning("Enter a song name.")
     st.stop()
    try:
        idx = df[df['song_name'].str.lower() == user_input.lower()]
        st.write(idx)
        st.subhearder("You might also like:")
        col1, col2 = st.columns([1,3])
        with col1:
            if "thumbnail" in df.columns:
                st.image(df.iloc[idx]['thumbnail'], width = 50)
        with col2:
            st.write("*Song:*",df.iloc[idx]['song_name'])
            st.write("*Artist:*", df.iloc[idx]['artist'])
            st.subheader("Recommended Songs:")
            result = recommend(user_input)

            if len(result)==0:
                st.error("Song not found")

            for item in result:
                col1, col2 = st.columns([1,3])

                with col1:
                    if item['thumbnail']:
                        st.image(item['thumbnail'], width = 150)

                with col2:
                    st.write("*Song:*", item['song_name'])
                    st.write("*Artist:*", item['artist'])
        
    except: 
          st.error("Song not found. Please check the spelling and try again.")



