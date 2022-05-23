from instagramy import InstagramUser
import pandas as pd
from datetime import datetime
# Import sys dependency to extract command line arguments
import sys
import os
session_id = os.getenv('INSTAGRAM_SESSION_ID')


def get_analysis(usernames=['hamaki','mekkystyle','hanadymehanna']):
    """
    It takes a list of Instagram usernames, and returns a dataframe containing the data of the last 12
    posts of each user
    
    :param usernames: A list of usernames to get the data for
    :return: A dataframe
    """
    
    
    usernames = usernames.split(',')
    
    results = pd.DataFrame()

    users_data = []
    for user in usernames:
        account = InstagramUser(user, sessionid=session_id, from_cache=True)
        username = []
        biography = []
        is_verified = []
        websites = []
        full_names = []
        username_profile_pic = []
        followers = []
        following = []
        number_of_uploads = []
        post_url = []
        post_number_of_likes = []
        post_number_of_comments = []
        date = []
        time = []
        eng_rate = []
        for post in account.posts:

            username.append(user)
            full_names.append(account.fullname)
            biography.append(account.biography)
            is_verified.append(account.is_verified)
            websites.append(account.website)
            post_url.append(post.post_url)
            post_number_of_likes.append(post.likes)
            post_number_of_comments.append(post.comments)
            date.append(datetime.fromtimestamp(post.timestamp).strftime('20%y-%b-%d'))
            time.append(datetime.fromtimestamp(post.timestamp).strftime('%I %p'))
            eng_rate = ((post.likes+post.comments)/account.number_of_followers)*100
            followers.append(account.number_of_followers)
            following.append(account.number_of_followings)
            username_profile_pic.append(account.profile_picture_url)
            number_of_uploads.append(account.number_of_posts)

        data = {
            'Username':username,
            'Full name':full_names,
            'Biography':biography,
            'Verified':str(is_verified),
            'Website':websites,
            'No. of followers':followers,
            'No. of Following':following,
            'No. of Uploads':number_of_uploads,
            'Post Url':post_url,
            'Likes':post_number_of_likes,
            'Comments':post_number_of_comments,
            'Date':date,
            'Time':time,
            'Engagement rate':eng_rate,
            'Profile Picture':username_profile_pic
        }

        user_dataframe = pd.DataFrame(data)
        users_data.append(user_dataframe)
        results = pd.concat([results,user_dataframe])

    results['Website'] = results['Website'].str.replace('None','N/A')

    users_stats = []
    for user_data in users_data:
        data = {}
        data['Username'] = str(user_data['Username'].iloc[0])
        data['Full Name']= str(user_data['Full name'].iloc[0])
        data['Biography'] = str(user_data['Biography'].iloc[0])
        data['is Verfied'] = user_data['Verified'].iloc[0]
        data['Website'] = user_data['Website'].iloc[0]
        data['# Followers'] = str(user_data['No. of followers'].iloc[0])
        data['# Followings'] = str(user_data['No. of Following'].iloc[0])
        data['# Uploads'] = str(user_data['No. of Uploads'].iloc[0])
        data['Profile Picture'] = user_data['Profile Picture'].iloc[0]
        data['Average Likes'] = int(round(user_data['Likes'].mean()))
        data['Average Comments'] = int(round(user_data['Comments'].mean()))
        data['Average Engagment Rate'] = user_data['Engagement rate'].mean()
        by_day_df = user_data.groupby('Date')
        avg_by_day_df = by_day_df.mean()
        best_day_df = avg_by_day_df[avg_by_day_df['Engagement rate']==
                              avg_by_day_df['Engagement rate'].max()]
        data['Best day'] = str(best_day_df.index.values[0])

        #BY TIME
        time_df = user_data.groupby('Time')
        avg_by_time_df = time_df.mean()
        time_df = avg_by_time_df[avg_by_time_df['Engagement rate']==
                              avg_by_time_df['Engagement rate'].max()]
        data['Best Time'] = str(time_df.index.values[0])


        users_stats.append(data)
    stats = pd.DataFrame(users_stats)
    stats.to_csv('stats.csv',index=False)
    results.to_csv('results.csv',index=False)

if __name__ == '__main__':
    get_analysis(sys.argv[1])