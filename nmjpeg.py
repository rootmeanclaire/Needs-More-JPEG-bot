import praw, os
from redditutil import scan_comments
#from imgurutil import init_client

user_agent = "User-Agent: nmpeg:v1.0 (by /u/CyrillicFez)"
username = "needs_more_JPEG_bot"
password = "REDACTED"

if not os.path.isdir("tmp"):
	os.makedirs("tmp")

print "Initializing PRAW..."
r = praw.Reddit(user_agent=user_agent)
print "Logging in..."
r.login(username, password, disable_warning=True)
print "Done!"

sub_test = r.get_subreddit('test')

print "Scanning subreddit..."
for submission in sub_test.get_hot(limit=15):
	print "\tScanning submission..."
	scan_comments(submission, r)
