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
  
  # Note: v_log_top3 is a view
  # 
  c.execute("select title, views \
             from articles, v_log_top3 \
             where v_log_top3.path like \
             '%' || articles.slug || '%' \
             order by views desc")
  results = c.fetchall()
  db.close()
  #for now just print each result
  #need to format so that it is printed neatly
  #results should be:
  #"article title" - 0000 views
  print("The top 3 articles of all time\n")
  for result in results:
    print('"' + result[0] + '"\t' + str(result[1]) + ' - views')
  print()
#test with 10
#actual should be 3
print_most_popular_3_articles()







