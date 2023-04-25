#!/usr/bin/env python3

import json
import subprocess

FILE_NAME = ".cache/ol_dump_2023-03-31.txt.gz"

author_regex = '^/type/author.*"bio"'
work_regex = '^/type/work.*"description"'


def lines_with_data(gzipped_src: str, regex: str):
    """
    Generate a list of lines with data from the gzipped source file.
    """

    cmd = f"zcat {gzipped_src} | grep -E '{regex}'"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    while True:
        output = process.stdout.readline()
        if output == b"" and process.poll() is not None:
            break
        if output:
            yield output


def lines_with_useful_data(gzipped_src: str, regex: str):
    """
    Generate a list of lines with useful data from the gzipped source file.
    """

    for line in lines_with_data(gzipped_src, regex):
        line = line.decode("utf-8")

        type_, key, revision, timestamp, data = line.split("\t")

        data = json.loads(data)

        if "latest_revision" in data:
            if data["latest_revision"] == int(revision):
                yield type_, key, data


def create_author_text(file_name: str):
    """
    Generate a list of author ids from the gzipped source file.
    """

    author_keys = set()

    for _type, key, data in lines_with_useful_data(FILE_NAME, author_regex):
        old_keys = author_keys.copy()
        author_keys.update(data.keys())

        if author_keys != old_keys:
            print(author_keys)

    return author_keys


if __name__ == "__main__":
    author_keys = create_author_text(FILE_NAME)

    print(author_keys)
