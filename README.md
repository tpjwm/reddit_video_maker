# reddit_video_maker
This project searches reddit for content and compiles it into either:
* TTS videos (reading post and comments) 
* Image compilations
* Video compilations (with music added to videos without sound)


# Usage
* Use virtual environment and download requirements
* Use config.py folder in src folder to create matching environment variables which you can get help with below
  - Generate Praw API key and list the details there
  - see: https://www.reddit.com/prefs/apps and https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/
* Post reddit links inside of `src/list.txt` or customize and run `populateList.py` to generate links for desired content
* In order to change the type of compilation/content change CONTENT_TYPE variable to desired output in `run.py`
* Set up a configuration for `run.py` using `list.txt` as a parameter and the corresponding environment variables from `config.py`

## Example list.txt file
```
<reddit post link> <number of comments to scrape> <title of mp4 video>
<reddit post link> <number of comments to scrape> <title of mp4 video>
...
```

## How it works
* Depending on user settings, creates compilations of either images, videos, or TTS
* Uses a Reddit api to scrape posts, external links, and top comments
### TTS 
* Scrapes the content from post/comments to create images for each post and combine them into an mp4 file
* Puts the text into text to speech to create mp3 file for soundtrack behind clips
### Images
* Scrapes user submitted images and links to images for each post using requests api and turns them into image clips
* Combines image clips into mp4 video compilation
### Videos
* Scrapes user submitted videos and audio for each post using youtube-dl api and ffmpeg to recombine audio and video files.
* Compiles the video clips into one large video, adding music to those clips who did not have audio


## TODO
- [x] Create a way to populate list.txt
- [x] Remove unsuitable comments (deleted, reliant on links, too long)
- [x] Increase comment length limit
- [x] Add more backgrounds / randomly select from them
- [x] Support for making video compilation of images and videos found on reddit
- [x] Add background music (royalty free) with random assortment to choose from
