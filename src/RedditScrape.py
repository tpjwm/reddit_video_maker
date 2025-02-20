# RedditScrape.py
# Last edited: June 28th 2021
# 
# Called from run.py
# Given a URL and an argument for number of posts to scrape, Class will connect to reddit API
# and scrape the content from the post returning a title, authors, and replies
#


# importing the config.py file to connect to PRAW
from config import reddit_api

# Pre process can let us exchange words. ie: exchanging curse words for others
from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols

import sys

sys.path.append("../")

# Words that we will exchange for others in text scraping
# To ensure no terrible words are used in the video
gtts.tokenizer.symbols.SUB_PAIRS.append(
    ('fuck', '*uck')
)


class RedditScrape:

    def __init__(self, url, num_replies=0):
        """url: the link of the reddit post to scrape comments/title from
        num_replies: the number of top replies program will take to make video
        path: path to folder: [audio] which stores audio files created or used"""

        self.url = url
        self.num_replies = num_replies
        self.path = '../audio/'  # Creating a directory to hold the audio in

    def scrape_post(self):
        """Takes the link passed into the class constructor
        to scrape the reddit post for the title and the top comments
        then the function loops through the strings of text turning them into
        a text to speech mp3 files and writes them to an mp3"""

        charsInCommentLimit = 1500

        # Creating an instance of reddit api
        reddit = reddit_api()

        text_used = []  # Creating list filled with strings of the title and all comment text
        authors = []  # Creating a list of authors from the post strings

        submission = reddit.submission(id=self.url)  # Getting submission post
        submission.comment_sort = 'top'  # Sorting the comments on the post to top voted
        submission.comments.replace_more(limit=0)  # removing weird 'more' comments

        # creates the comment list without including links, long comments or deleted/removed comments
        comments = []
        counter = 0

        while len(comments) < self.num_replies:
            comment = submission.comments.list()[counter]
            content = comment.body
            if "[" in content or "www" in content or "http" in content or len(content) >= charsInCommentLimit:
                pass
            else:
                comments.append(comment)
            counter += 1

        # adding title to text_used as well as the submission text and author again if available
        clean_title = pre_processors.word_sub(submission.title)
        text_used.append(clean_title)

        if len(submission.selftext) > 15:  # arbitrary number
            text_used.append(submission.selftext)
            authors.append(submission.author.name)

        # adding post author and replies authors
        authors.append(submission.author.name)
        for comment in comments:
            try:
                authors.append(comment.author.name)
            except AttributeError:
                authors.append('deleted')

        for i in range(0, len(comments)):
            # Push cleaned string into text_used
            data = comments[i]
            clean_str = pre_processors.word_sub(data.body)
            text_used.append(clean_str)  # .encode('utf-8', 'replace'))

        # Returns text used: [title & replies], and [authors]
        return text_used, authors

    def get_url(self):
        reddit = reddit_api()
        submission = reddit.submission(id=self.url)  # Getting submission post
        return submission.url
