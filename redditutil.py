from imgurutil import post_compressed_version
import re, praw, os.path

def get_parent_comment(comment, r):
	parent = r.get_info(thing_id=comment.parent_id)
	if type(parent) is praw.objects.Submission:
		return -1
	else:
		return parent

def scan_comments(submission, r):
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments:
		if "needs more jpeg" in comment.body.lower():
			print "\t\tMatch found!"
			matches = []
			#image in post
			if get_parent_comment(comment, r) == -1:
				if not already_replied(comment):
					print "\t\tReplying with jpeg'd version of " + submission.url
					comment.reply(post_compressed_version(submission.url))
					add_to_history(comment)
				else:
					print "\t\tComment already responded to"
			#image in other comment
			else:
				for match in findall("imgur.com/", get_parent_comment(comment, r).body):
					matches.append(match)

				if len(matches) == 1:
					if not already_replied(comment):
						print "\t\tReplying with jpeg'd version of " + matches[0]
						comment.reply(post_compressed_version(matches[0]))
						add_to_history(comment)
					else:
						print "\t\tComment already responded to"

				elif len(matches) > 1:
					pass
				else:
					pass

def already_replied(comment):
	if not os.path.isfile("history.txt"):
		return False

	f = open('history.txt', 'r')

	for line in f:
		if comment.permalink == line[:-1]:
			return True

	return False

def add_to_history(comment):
	with open('history.txt', 'a+') as f:
		f.write(comment.permalink + "\n")