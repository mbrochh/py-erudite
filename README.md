# PyErudite

This is a little side project for now. 

Current status: Not functional.

## Goal

### Summarizing all kinds of content

* One shall be able to clone this repo and run `docker-compose up`
* One shall be able to browse to `localhost:4000` and see a web page
* One shall be able to add Youtube URLs to a queue and the system will summarize 
  the videos
* One shall be able to load a Kindle book and the suystem will summarize the 
  book
* One shall be able to upload a PDF and the system will summarize the PDF
* One shall be able to link to a web page and the system will summarize the web 
  page
* The summaries will be created with GPT4, until an equally smart open source 
  LLM comes along
* The summaries will be formatted such that they can be copied into Logseq

At this stage, you should be able to consume content at a rapid pace and retain
the gist of all that knowledge that you consume in the form of concise
summaries.

### Answering questions about the summarized content

* One shall be able to generate vector embeddings for all the summaries
* The system will use either sBERT or OpenAI embeddings
* One shall be able to ask any question
* The system shall retrieve vectors that are related to the question
* The system shall construct a prompt that will be sent to GPT4, until an 
  equally smart open source LLM comes along
* The prompt will be such that the LLM will answer the question based on the
  provided context from the local summaries

At this stage you can ask anything about anything you have ever consumed and
the system will provide a meaningful answer and lilst the quoted sources so
that you can also read the original source again if you need to.

# How to run

* clone this repo
* run `cd backend && cp local_settings.py.sample local_settings.py`
* edit `local_settings.py` and insert the necessary values
* run `docker-compose build`
* run `docker-compose up`
* run `docker-compose exec backend python /app/pyerudite/manage.py createsuperuser`
* enter username, email and password
* browse to `localhost:8000/admin` and try to login

Note: After this, there should be a folder `artefacts` which contains a file
`django.sqlite3`. This is the Django database file.