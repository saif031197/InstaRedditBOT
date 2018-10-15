'''
v0.03 of the bot repurposed again as a multipurpose bot to post content from multiple
subreddits instead of a singular one and makes sure to not repeat the content and parses
through 5 new feeds of a subreddit at a time before moving on to another subreddit and
repeating the process, 0 crashes yet but due for an overnight test, made in the morning of
October 14th 2018
Made by - saif031197
'''
import praw
import datetime as dt
import time
import urllib.request
from InstagramAPI import InstagramAPI
import os
from PIL import Image
os.chdir('F:\\InstaBOT\\images')  #directory where images are going to be saved [Posted ID's file will also be saved here]
#Follow this guide - http://www.storybench.org/how-to-scrape-reddit-with-python/ for reddit parse
reddit = praw.Reddit(client_id='PERSONAL_USE_SCRIPT_14_CHARS', \
                     client_secret='SECRET_KEY_27_CHARS ', \
                     user_agent='YOUR_APP_NAME', \
                     username='YOUR_REDDIT_USER_NAME', \
                     password='YOUR_REDDIT_LOGIN_PASSWORD')
print("reddit logged in.")
api=InstagramAPI("YOUR_INSTA_USERNAME", "YOUR_INSTA_PASSWORD")
api.login()
print("instagram logged in")
posted=[] #list to store posted content ID
#main function which parses through subreddit's
def redditX(sub):
    print("Parsing ",sub)
    subreddit = reddit.subreddit(sub)
    with open('posted.txt', 'r') as filehandle:   #To read posted ID's from file and append to list
        for line in filehandle:
            currentPlace = line[:-1]
            posted.append(currentPlace)
    temp=subreddit.hot(limit=20)        # .hot, .new arguments check the reddit guide for more
    for x in temp:                      # limit can take max argument of 1000
        if x not in posted:
            if(post(x,sub)):
                with open('posted.txt', 'a') as filehandle:  
                    filehandle.write('%s\n' % x)            #Save ID in file if post successful
        else:
            print(x.title+" posted already.")           
def post(sub,name):      
    if(sub.url[-3:] == 'jpg' or sub.url[-3:]=='png'):       #only png and jpg files
        print(sub.url)
        print(sub.title)
        try:
            urllib.request.urlretrieve(sub.url, sub.url.split('/')[-1])     #saving the image to disk
        except urllib.error.HTTPError:
            print('Downloading image failed')
            return False
        photo_path = sub.url.split('/')[-1]             #assigning image filename to var
        if(photo_path[-3:]=='png'):                     #InstagramAPI doesnt accept png so convert to jpg
            print("Converting png to jpg")
            im=Image.open(photo_path)
            rgb_im=im.convert('RGB')
            photo_path=photo_path[:-3]+'jpg'
            rgb_im.save(photo_path)
            print("Photo Converted")
        caption = sub.title+' - '+name+'INSERT APPROPRIATE CAPTION WITH HASHTAGS AND LINEBREAKS'
        #caption is posted as post_name - subreddit_name 'REST OF THE CAPTION'
        im=Image.open(photo_path)
        width,height=im.size
        height=float(height)
        width=float(width)
        if(width/height>0.8 and float(width/height<1.91)):  #insta only accepts images that have a w/h
            if(upload_photo(photo_path,caption)):           #ratio between 0.8 and 1.91
                return True
            else:
                return False
        else:
            print("Image size incorrect,skipping.")
            return False
    else:
        print("not a jpeg or png, skipping")
        return False

def upload_photo(path,cap):
    try:
        api.uploadPhoto(path, caption=cap)
        print("Upload success!")
        time.sleep(300)                     #5 minute timer as to avoid spam
        return True
    except RuntimeError:
        print("Runtime Error Occured")      #pretty common for this to occur, unkown why currently
        time.sleep(60)                      #happens mostly with imgur posts
        return False
subreddits=[]  #input the subreddits you want to parse as a list over here
while(True):
    for subs in subreddits:
        redditX(subs)
        print(subs+" parse Done")
        currentDT = dt.datetime.now()
        print (str(currentDT))
        time.sleep(60)
#Above function goes on as an infinite loop until its explicitly stopped with an error or with ctrl+c