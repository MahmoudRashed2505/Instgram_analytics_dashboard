# Import base streamlit dependency
import streamlit as st
# Import pandas to load the analytics data
import pandas as pd
# Import subprocess to run tiktok script from command line
from subprocess import call
# Import plotly for viz
import plotly.express as px
# Import numpy for math
import numpy as np
# Import time 
import time
# Import base64 for encoding
import base64
# Import zipfile for zipping
import zipfile

# Set page width to wide
st.set_page_config(layout='wide')

# Set Page title
st.title('Instagram Analytics by Voomo')

# Create sidebar
st.sidebar.markdown("<div><img src='https://github.com/ayahhhany/Instagram-Dashboard/raw/main/assets/insta.png' width=100 /><br><h1 style='display:inline-block'>Instagram Analytics</h1></div>", unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows you to analyse Multiple Instgram accounts using Python and Streamlit.")
st.sidebar.markdown("To get started <ol><li>Enter the <i>Usernames</i> you wish to analyse separated by (' , ') </li> <li>Hit <i>Get Data</i>.</li> <li>Get analyzing</li></ol>",unsafe_allow_html=True)

def filedownload(df,stats):
    complete = df.to_csv('./output/csv/complete.csv',index=False)
    stats_file = stats.to_csv('./output/csv/statistics.csv',index=False)
    fig.write_image("./output/images/histogram.png")
    scatter1.write_image("./output/images/scatter.png")
    followers_Bar.write_image("./output/images/followers.png")
    postsNum_Bar.write_image("./output/images/posts.png")
    er_Bar.write_image("./output/images/er.png")
    zip_file = zipfile.ZipFile('./output/zip/output.zip', 'w')
    zip_file.write('./output/csv/complete.csv')
    zip_file.write('./output/csv/statistics.csv')
    zip_file.write('./output/images/histogram.png')
    zip_file.write('./output/images/scatter.png')
    zip_file.write('./output/images/followers.png')
    zip_file.write('./output/images/posts.png')
    zip_file.write('./output/images/er.png')
    zip_file.close()
    with open("./output/zip/output.zip", "rb") as f:
        btn = st.download_button(
            label="Download ZIP",
            data=f,
            file_name="report.zip",
            mime="application/zip"
        )
        return btn

# Input 
usernames = st.text_input('Search for a accounts here', value="")

if st.button('Get Data'):
    # Run get data function here
    
    call(['python', 'instagram.py', usernames])
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success('Done!')
    
    # Load in existing state data to test it out
    stats = pd.read_csv('stats.csv')

    stats0 = stats.sort_values(by=['# Followers'])
    followers_Bar = px.bar(stats0 , y= 'Full Name', x='# Followers',  orientation='h', height=500, width=800, title='Who is Followed the most?',color_discrete_sequence= px.colors.sequential.Plasma)

    stats0 = stats.sort_values(by=['# Uploads'])
    postsNum_Bar = px.bar(stats0 , x= 'Full Name', y='# Uploads', orientation='v', height=500, width=800, title='Who has the most posts?',color_discrete_sequence= px.colors.sequential.Plasma)

    stats0 = stats.sort_values(by=['Average Engagment Rate'])
    er_Bar = px.bar(stats0 , x= 'Full Name', y='Average Engagment Rate',  orientation='v', height=500, width=800, title='Who has the highest Engagement Rate?',color_discrete_sequence= px.colors.sequential.Plasma)


    # Load in existing data to test it out
    df = pd.read_csv('results.csv')
    df['date']= pd.to_datetime(df['Date'])

    # lucky hour
    alllikes = [] 
    max_like = []
    hours = []
    lucky_hour = []
    for user in df['Username'].unique():
        alllikes = df[df['Username'] == user]['Likes'].tolist()
        max_like.append(max(alllikes))
        hours = df[df['Username'] == user]['Time'].tolist()
        lucky_hour.append(hours[np.argmax(alllikes)])

    # Plotly viz here
    fig = px.histogram(stats, x='Full Name', hover_data=['Full Name'], y='# Followers', height=500,title='Histogram between # of followers') 
    st.plotly_chart(fig, use_container_width=True)
    

    # Split columns
    left_col, right_col = st.columns(2)

    
    # First Chart - video stats
    scatter1 = px.scatter(df, x='Date', y='Likes', hover_data=['Username'], color='Username',title='Date vs Likes',symbol='Username',color_discrete_sequence= px.colors.sequential.Plasma)
    left_col.plotly_chart(scatter1, use_container_width=True)
    left_col.plotly_chart(er_Bar, use_container_width=True)

    # Second Chart
    right_col.plotly_chart(followers_Bar, use_container_width=True)
    right_col.plotly_chart(postsNum_Bar, use_container_width=True)

    filedownload(df,stats)
    # Show tabular dataframe in streamlit





