import sqlite3
import schedule
import time
import pandas as pd

import job_searcher
from job_searcher import list_of_jobs
import job_comparer

resume = ["Javascript","Python","React", "CSS", "Unity", "HTML", " C "]

conn = sqlite3.connect('job_postings.db')
c = conn.cursor()

def web_scraper() :
  job_searcher.jobsearch()
  #print(list_of_jobs)

  # runs comparison on jobs and given list of keywords
  job_comparer.description_query(resume)


  # adds lists from list_of_jobs to a database called job_postings.db

  #c.execute('''DROP TABLE IF EXISTS job_postings''')
  #c.execute('''CREATE TABLE job_postings(position TEXT, company_name TEXT, location TEXT, link TEXT, rating INT)''')

  for job in list_of_jobs:
    c.execute('''SELECT * FROM job_postings WHERE position = "{}" AND company_name = "{}" AND location = "{}" AND link = "{}"'''.format(job[0],job[1],job[2],job[3]))
    query = c.fetchone()
    if query == None:
      c.execute('''INSERT INTO job_postings VALUES(?,?,?,?,?)''', (job[0], job[1], job[2], job[3],job[4]))
      conn.commit()

  #c.execute('''SELECT * FROM job_postings''')
  #print(c.fetchall())

# Returns the top n results, sorted by the rating column
def top(n) :
  #c.execute('''SELECT * FROM job_postings ORDER BY rating DESC LIMIT {}'''.format(n))  
  #print(c.fetchall())
  print(pd.read_sql_query('''SELECT * FROM job_postings ORDER BY rating DESC LIMIT {}'''.format(n), conn))

#Commands to run web_scraper daily
schedule.every().day.at("00:00:00").do(web_scraper)
while True:
  schedule.run_pending()
  time.sleep(1)

conn.close()
