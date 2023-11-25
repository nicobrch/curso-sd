#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import redis
import re


def redis_connect():
    try:
        connection = redis.StrictRedis(
            host="redis",
            port=6379,
            decode_responses=True
        )
        return connection
    except Exception as e:
        print("Error connecting to Redis:", e)
        sys.exit(1)


def process_input(line):
    doc = line.lower()

    # Extract name and document parts
    name, doc = doc.split('<splittername>')
    name, url = name.split()

    # Remove punctuation and numeric values
    doc = re.sub(r'\W+', ' ', doc.replace("\n", ' ')).strip()
    for char in [",", ".", '"', "'", "(", ")", "\\", ";", ":", "$1", "$", "&", "="]:
        doc = doc.replace(char, '')

    # Process each word in the document
    word_list = []
    for word in doc.split():
        if word.isalpha():
            word_list.append('{}\t{}\t{}'.format(word, name, 1))

    return word_list, name, url


def insert_paginas(redis_conn, name, url):
    try:
        for _ in range(30):
            redis_conn.hsetnx("paginas", name, url)
    except Exception as err:
        print("Error during paginas table insertion:", err)


def main_execution():
    redis_conn = redis_connect()

    try:
        for line in sys.stdin:
            word_list, name, url = process_input(line)

            # Sort and print the processed words
            for word_entry in sorted(word_list):
                print(word_entry)

            insert_paginas(redis_conn, name, url)

    finally:
        if redis_conn:
            redis_conn.close()


if __name__ == "__main__":
    main_execution()
