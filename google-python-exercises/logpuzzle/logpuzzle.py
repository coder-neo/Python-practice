#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import webbrowser

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def image_sort(urlstring):
  match = re.search('-\w+-(\w+).jpg',urlstring)
  if match:
    return match.group(1)
  else:
    return urlstring



def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  f = open(filename,'rU')
  file_text = f.read()
  image_list = re.findall('GET\s(/edu\S+jpg)',file_text)
  images = []
  for image in image_list:
    if not image in images:
      images.append(image)
  #print '\n'.join(sorted(images))
  return sorted(images, key=image_sort)


  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  url = 'http://code.google.com'
  count = 0
  index_file = ['<html>','<body>']
  for image in img_urls:
    image_name = dest_dir+'/img'+str(count)+'.jpg'
    urllib.urlretrieve(url+image,image_name)
    print 'Retrieving file '+url+image
    index_file.append('<img src="img'+str(count)+'.jpg">')
    count += 1
  index_file.append('</body>')
  index_file.append('</html>')

  f = open(dest_dir+'/index.html','w')
  f.write('\n'.join(index_file))
  f.close()
  # Code to open image in browser
  #webbrowser.open(dest_dir+'/index.html',new=1)
  return  


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
