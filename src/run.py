# This file will be the main driver function and run the entire program
# This will import the Reddit Scraping Class and the Video Editing Class

import argparse  # Used to handle command line arguments
import os
import shutil
import sys
import requests

from RedditScrape import RedditScrape  # Importing reddit scraping class to acquire posts and authors

from TextToSpeech import TextToSpeech  # Importing tts class to make mp3 of posts

from ImageCreator import ImageCreator  # Generates images of posts

from VideoEdit import VideoEditor  # Edits all the tts mp3 and Images into a mp4 video

# images, videos, tts
CONTENT_TYPE = "images"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file path of input file')
    args = parser.parse_args()

    ''' input_metadata holds the meta data from each entry in the input file
    is a list of dicts that will be used to build each video
    [ {link: <link>, n_entries: <n_entries>, title: <name> }, ...]
    '''
    input_metadata = []

    # Open the file from argument and build the list of meta data for each link to build videos 
    try:
        # Reading file, ignoring empty lines 
        with open(args.file, 'r') as f_in:
            lines = list(line for line in (l.strip() for l in f_in) if line)

        # iterate through the lines of content and create the meta objects
        for entry in lines:
            data = entry.split(' ', 2)  # split string at spaces... file format is: link num_comments title
            whitelist = set(
                'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-')  # maybe regex could be used instead
            data[2] = ''.join(filter(whitelist.__contains__, data[2]))
            input_metadata.append({'id': data[0], 'n_entries': int(data[1]), 'title': data[2]})

    except FileNotFoundError:
        print('Invalid path to file')
        return 1

    if CONTENT_TYPE == "tts":
        makeTTS(input_metadata)
    elif CONTENT_TYPE == "videos":
        makeVideos(input_metadata)
    elif CONTENT_TYPE == "images":
        makeImages(input_metadata)

    return 0


def makeTTS(input_metadata):
    # Loop through each video meta object and create videos
    for video_meta in input_metadata:
        print(video_meta)

        reddit_scraper = RedditScrape(video_meta['id'], video_meta['n_entries'])

        # Returns 2 lists of strings, [all posts] [authors of posts]
        # index 0 of both are associated with the title, the rest are replies to the thread
        posts, authors = reddit_scraper.scrape_post()

        try:
            assert (len(posts) == len(authors))
            print(len(posts))

        except AssertionError:
            print(f'''Something went wrong in the Reddit Scrape...
                    length of posts: {str(len(posts))} != len authors: {str(len(authors))}
                    Exiting Program.''')
            return -1

        for i, post in enumerate(posts):
            print(f'{i}: {post}')

        # Text to speech
        tts = TextToSpeech()  # Creating tts class
        tts.create_tts(posts)  # Creating all tts mp3 files for video

        # Image Creation
        # Creating image for title
        ImageCreator.create_image_for(posts[0], authors[0], 'title')

        # Creating image post for the replies: reply0.jpg, reply1.jpg, ...
        for i in range(1, len(posts)):
            ImageCreator.create_image_for(posts[i], authors[i], f'reply{str(i - 1)}')

        # Creating a Video Editing object
        # Passing n_entries + 1, for # of images, since we have title + n replies

        Editor = VideoEditor(video_meta['title'], len(posts) - 1)
        Editor.create_movie()
        print('movie created')


import youtube_dl


def makeVideos(input_metadata):
    videos_path = '../videos/'

    try:
        os.makedirs(videos_path)
        print(f'directory: {videos_path} created')
    except FileExistsError:
        pass

    try:
        for item in input_metadata:
            reddit_scraper = RedditScrape(item['id'])
            link_to_post = reddit_scraper.get_url()

            if 'v.redd' in link_to_post:
                ydl_opts = {'outtmpl': videos_path + item["title"] + '.%(ext)s'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link_to_post, ])
    except Exception as err:
        print("Error:", sys.exc_info()[0])
        print(err)  # __str__ allows args to be printed directly,
        raise

    editor = VideoEditor("Compilation video")
    editor.create_compilation_of_videos()


def makeImages(input_metadata):
    image_path = '../reddit_images/'

    try:
        os.makedirs(image_path)
        print(f'directory: {image_path} created')
    except FileExistsError:
        pass

    try:
        for item in input_metadata:
            reddit_scraper = RedditScrape(item['id'])
            link_to_post = reddit_scraper.get_url()

            if 'v.redd' not in link_to_post:
                filename = link_to_post.split('/')[-1]
                r = requests.get(link_to_post, stream=True)
                if r.status_code == 200:
                    r.raw_decode_content = True
                    with open(image_path + filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    print("Image download failed: ", link_to_post)

    except Exception as err:
        print("Error:", sys.exc_info()[0])
        print(err)  # __str__ allows args to be printed directly,
        raise

    editor = VideoEditor("Compilation video of images")
    editor.create_compilation_of_images()


if __name__ == '__main__':
    exit(main())
