#!/usr/bin/env python3
#
# RDuran - 18 May, 2017
# Udacity Full Stack Nanodegree - Log Analysis Project
#
import psycopg2

DBNAME = "news"


def print_most_popular_3_articles():
    """return the most popular three articles of all time"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("select title, views \
               from articles, v_log_top3 \
               where v_log_top3.path like \
               ('/article/' || articles.slug) \
               order by views desc")
    results = c.fetchall()
    db.close()

    print("The top 3 articles of all time\n")
    for result in results:
        print('"' + result[0] + '" - ' + str(result[1]) + ' views')
    print("\n\n")


def print_most_popular_authors():
    """return a list of authors and views
       sorted with the most popular author
       listed first, followed by the other
       authors, in decending order of popularity
       as determined by the number of views each
       has received on all articles each has written"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # temp query to check that function works
    c.execute("select name, sum(views) as views \
              from v_author_slug_views \
              group by name \
              order by views desc")
    results = c.fetchall()
    db.close()

    print("The top authors of all time\n")
    for result in results:
        print(result[0] + ' - ' + str(result[1]) + ' views')
    print("\n\n")


def print_request_errors_1percent():
    """return the Mongth DD, YYYY (July 28, 2016)
       and percentage of errors where the errors
       where the errors are greater than 1% of
       requests lead to errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from v_high_error_dates")
    results = c.fetchall()
    db.close()

    print("Days where request errors > 1% of request\n")
    for result in results:
        print(" ".join(result[0].split()) + " - " +
              str(result[1]) + "% errors")
    print("\n\n")


print_most_popular_3_articles()
print_most_popular_authors()
print_request_errors_1percent()
