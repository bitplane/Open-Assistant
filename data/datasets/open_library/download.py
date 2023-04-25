#!/usr/bin/env python3

import logging
import os

import pycurl
import requests

URL = "https://openlibrary.org/data/ol_dump_latest.txt.gz"
HERE = os.path.split(__file__)[0]
CACHE_DIR = os.path.join(HERE, ".cache")


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_latest_version() -> str:
    """
    Get the latest version name of the dataset
    """
    response = requests.head(URL)

    # for example:
    # https://archive.org/download/ol_dump_2023-03-31/ol_dump_2023-03-31.txt.gz
    location = response.headers["location"]

    file_name = location.split("/")[-1]
    logger.info(f"Version is {file_name}")

    return file_name


def download_file() -> str:
    """
    Download the file if necessary.
    If not, don't bother. Returns the path to the tgz file.
    """

    version = get_latest_version()

    dest_filename = os.path.join(CACHE_DIR, version)

    if os.path.exists(dest_filename):
        logger.info("Already downloaded, use cached version")
        return dest_filename
    else:
        logger.info("Downloading file.")

    temp_filename = dest_filename + ".tmp"

    c = pycurl.Curl()

    if os.path.exists(temp_filename):
        mode = "ab"
        c.setopt(pycurl.RESUME_FROM, os.path.getsize(temp_filename))
    else:
        mode = "wb"

    with open(temp_filename, mode) as f:
        c.setopt(c.URL, URL)
        c.setopt(c.WRITEDATA, f)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.NOPROGRESS, False)
        c.perform()
        c.close()

    logger.info("Done!")
    os.rename(temp_filename, dest_filename)

    return dest_filename


if __name__ == "__main__":
    download_file()
