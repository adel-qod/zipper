#!/usr/bin/python2.7 -tt

"""
Copyright (c) 2013, Adel Qodmani
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import tarfile # For the compression
import os # For everything related to path
import logging 
import sys # For the argv and exit
import datetime

def main():
  """ zipper source-dir-full-path dest-dir-full-path
      Tars and zips the source-dir and put it in the dest-dir with the name:
      source-dir-name_date_time.tar.gz
  """
  check_args()
  source_path = sys.argv[1]
  source_path = source_path.rstrip('/')
  logging.debug("source_path: %s" % source_path)
  dest_path = sys.argv[2]
  dest_path = dest_path.rstrip('/')
  logging.debug("dest_path: %s" % dest_path)
  # source name is the name of the dir to be archived
  source_name = source_path.split("/")[-1]
  logging.debug("source_name: %s" % source_name)
  # tar_path 
  tar_path = create_tar_path(source_name, dest_path)
  logging.debug("tar_path: %s" % tar_path)
  create_tar_file(tar_path, source_path)
 
def check_args():
  """ Checks if the args supplied to the script are what it expects """
  if len(sys.argv) > 1 and sys.argv[1] == "--help":
    help_text = ("zipper creates a zipped tar-ball of the <source> directory"
                + "and puts it in \nthe <destination> directory ")
    usage = "e.g: zipper /tmp/ /home/sally/Desktop/"
    result = "will create a file called tmp_date_time.tar.gz in "
    result += "/home/sally/Desktop/ which has all the contents of /tmp/"
    print(help_text)
    print(usage)
    print(result)
    sys.exit(0)
  elif len(sys.argv) < 3:
    print("Missing arguments!")
    print("Usage:")
    print("\tzipper source destination")
    print("You can get the help by: zipper --help")
    logging.error("Missing arguments!")
    logging.error("Shutting down!")
    sys.exit(1)
  elif not os.path.isabs(sys.argv[1]):
    print("Source directory is not an absolute path")
    print("You can get the help by: zipper --help")
    logging.error("Source is not absolute")
    logging.error("Shutting down")
    sys.exit(2)
  elif not os.path.isabs(sys.argv[2]):
    print("Destination directory is not an absolute path")
    print("You can get the help by: zipper --help")
    logging.error("Destination is not absolute")
    logging.error("Shutting down")
    sys.exit(3)
  elif not os.path.isdir(sys.argv[1]):
    print("Path given as a source directory is not a directory")
    print("You can get the help by: zipper --help")
    logging.error("Source is not a directory")
    logging.error("Shutting down")
    sys.exit(4)
  elif not os.path.isdir(sys.argv[2]):
    print("Path given as destination directory is not a directory")
    print("You can get the help by: zipper --help")
    logging.error("Destination is not a directory")
    logging.error("Shutting down")
    sys.exit(5)
  
def create_tar_path(source_name, dest_path):
  """ Creates a path for a backup that will be in the desktop of the user
      and the file name will be the /path/to/desktktop/source_name_date.tar.gz
  """
  # Get the path to the desktop ready
  path = os.path.expanduser('~') # changes ~ to home dir path
  logging.debug(path)
  path = os.path.join(path, dest_path+"/")
  logging.debug(path)
  # string from time(strftime): %Year %month %day %Hour %Minute $Second
  now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  logging.debug(now)
  # The dest path is the path + source_name + date + extension
  path = os.path.join(path, source_name)
  logging.debug(path)
  path += '_' + now + ".tar.gz"
  logging.debug(path)
  return path

def create_tar_file(tar_path, source_path):
  # "w:gz" is open for writing a gz tarball
  try:
    tar = tarfile.open(tar_path, "w:gz")
    tar.add(source_path)
    tar.close()
    logging.debug("Tar ball [%s] created for directory [%s]" % (tar_path, 
                                                               source_path))
  except IOError:
    logging.critical("IOError exception! Aborting ..")
    sys.exit(6)
  except TarError:
    logging.critical("TarError exception! Aborting ...")
    sys.exit(7)

if __name__ == "__main__":
  # Set up the logging env
  # Format: (asctime) (filename) (funcname) (linenumber) (level) (msg)
  # The time can be formated with the datefmt parameter
  FORMAT = "%(asctime)s %(filename)s::%(funcName)s::%(lineno)d"
  FORMAT += " [%(levelname)s]:  %(msg)s"
  DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
  try:
    STREAM = open("/home/aral/learn/zipper/log", "a+")
  except IOError:
    print("Can't create a log file in [%s]" % STREAM)
    sys.abort()
  # Setting the log stream to go to stderr and print all log info from debug
  # and higher levels (debug, info, warning, error, critical)
  logging.basicConfig(stream=STREAM, level=logging.DEBUG, format=FORMAT, 
                     datefmt=DATE_FORMAT)
  main()
