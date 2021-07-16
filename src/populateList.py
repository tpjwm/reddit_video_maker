from config import reddit_api

reddit = reddit_api()
SUBREDDIT = 'funny'  # Replace with the name of the subreddit to pull submissions and comments from
NUM_COMMENTS = 1  # Replace with desired number of comments
NUM_ENTRIES = 50  # Replace with number of videos/links desired

list_file = open(r"list.txt", "w+")
for submission in reddit.subreddit(SUBREDDIT).top("day", limit=NUM_ENTRIES):
    try:
        list_entry = submission.id + " " + str(NUM_COMMENTS) + " " + submission.title + '\n'
        list_file.write(list_entry)
    except UnicodeEncodeError:
        pass

list_file.close()
