import requests
from bs4 import BeautifulSoup

import job_searcher
from job_searcher import list_of_jobs

# description_query goes through the list of jobs and retrieves the link. It then scrapes the link and grabs the div tag to get the job description
def description_query(resume):
  for job in list_of_jobs:
    link = job[3]
    #print(link)
    html_text = requests.get("{}".format(link)).text
    soup = BeautifulSoup(html_text, "lxml")
    description = soup.find('div', class_ = "jobsearch-jobDescriptionText").text.strip()
    rating = rate_job(resume, description.lower())
    #print(description.lower())
    #print(rating)
    #print("\n")
    job.append(rating)

    
# resume is an array of strings
def rate_job(resume, description):
  rating = 0
  for word in resume:
    word = word.lower()
    if word in description:
      prev = description.find(word) - 1
      after = description.find(word) + len(word)
      
      if description[prev].isalpha() == False and description[after].isalpha() == False:
        rating = rating + 1
  return rating

  