from imgurpython import ImgurClient
from PIL import Image
import cStringIO, os, os.path, urllib2, io

print "Initing client..."
client_id = 'REDACTED'
client_secret = 'REDACTED'
imgur_client = ImgurClient(client_id, client_secret)

def compress_img(img, compression, filename):
	img.save(filename, 'JPEG', quality=compression)

def get_imgur_img(url):
	fixed_url = "000"

	if "/a/" in url:
		pass
	elif "i.imgur" in url:
		fixed_url = url
	elif "/gallery/" in url:
		fixed_url = url.replace("imgur.com", "i.imgur.com").replace("/gallery") + ".png"
	else:
		fixed_url = url.replace("imgur.com", "i.imgur.com")  + ".png"

	print "\t\tOrgnl URL: " + url
	print "\t\tFixed URL: " + fixed_url
	# if os.path.isfile("tmp/download.png"):
	# 	os.remove("tmp/download.png")
	# urllib.urlretrieve(fixed_url, "tmp/download.png")
	# image = Image.open("tmp/download.png");
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(fixed_url)
	img_file = io.BytesIO(response.read())   
	image = Image.open(img_file)
	return image

def upload(img_path):
	config = {
		'album': None,
		'name': 'Added JPEG!',
		'title': 'Added JPEG!'
	}
	ret = imgur_client.upload_from_path(img_path, config=config, anon=True)
	print ret["link"]
	return ret["link"]

def post_compressed_version(original_url):
	if os.path.isfile("tmp/compd.jpeg"):
		os.remove("tmp/compd.jpeg")
	compress_img(get_imgur_img(original_url), 1, "tmp/compd.jpeg")
	return upload("tmp/compd.jpeg")

