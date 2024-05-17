# PyErudite

This is a little side project for now.

Current status: Functional. Creating summaries of Youtube videos and webpages
works, but "talking to your own notes" is not yet implemented.

At this stage, I am using this daily to summarize videos and webpages and copy
the summaries into my [Obsidian Graph](https://obsidian.md/).

There is even a little Chrome extension that pushes the current webpage into
the job queue.

## Goal

### Summarizing all kinds of content

- DONE: One shall be able to clone this repo and run `docker-compose up`
- DONE: One shall be able to browse to `localhost:4242/admin/` and see a web page
- DONE: One shall be able to add Youtube URLs to a queue and the system will summarize
  the videos
- TODO: One shall be able to load a Kindle book and the system will summarize the
  book
- TODO: One shall be able to upload a PDF and the system will summarize the PDF
- DONE: One shall be able to link to a web page and the system will summarize the web
  page
- TODO: The summaries will be created with GPT-4o, until an equally smart open
  source LLM comes along
- DONE: The summaries will be formatted such that they can be copied into Obsidian
- TODO: Instead of the Django admin, everything should have a nice reactive
  frontend

At this stage, you should be able to consume content at a rapid pace and retain
the gist of all that knowledge that you consume in the form of concise
summaries.

### Answering questions about the summarized content

- TODO: One shall be able to generate vector embeddings for all the summaries
- TODO: The system will use either sBERT or OpenAI embeddings
- TODO: Additionally to embedings, the system shall also generate a knowledge
  graph of all summaries
- TODO: One shall be able to ask any question
- TODO: The system shall retrieve vectors that are related to the question
- TODO: The system shall query the knowledge graph related to the question
- TODO: The system shall construct a prompt that will be sent to the LLM
- TODO: The prompt will be such that the LLM will answer the question based on
  the provided context from the local summaries

At this stage you would be able ask anything about anything you have ever
consumed and the system will provide a meaningful answer and lilst the quoted
sources so that you can also read the original source again if you need to.

# How to run this on your local machine

- clone this repo
- run `cd backend && cp local_settings.py.sample local_settings.py`
- edit `local_settings.py` and insert the necessary values
- run `docker-compose build`
- run `docker-compose up`
- run `docker-compose exec backend python /app/pyerudite/manage.py createsuperuser`
  - NOTE: You only need to do this the very first time you run the container
  - enter username, email and password
- browse to `http://localhost:4242/admin` and login
- browse to `http://localhost:4242/admin/ingest/ingestfromsource/` and click at
  `Add Ingest From Source`
- As `Source type` select `Youtube` and as `Source url` enter the URL of a
  Youtube video and click `SAVE`
- On the list view you can refresh the browser. Within the next minute, the
  status of the object that you have just created will change from `Pending`
  to `In Progress`. While the status is `In Progress`, the sustem will:
  - Download the audio of the video
  - Run Whisper to transcribe the video
  - Create a `SummarizeFromIngest` instance with status `Pending`
- Once the status is `Completed` you can click into that object again and
  read the transcript.
- Now you can browse to `http://localhost:4242/admin/summarize/summarizefromingest/`
  and you will see another object which will get it's status to `In Progress`
  within the next minute. During this process, the system willl send a prompt
  to OpenAI and save the summary in a file.
- Once the status is `Completed`, you can click into that object and read
  the summary.

# How to use the Chrome extension

- Browse to `chrome://extensions` and click at `Load unpacked`
- Select the `chrome-extension` folder that you have cloned with this repo
- Make sure that the backend is running (`docker-compose up`)
- Browse to any site, click the extension, a popup will appear, click `Send`
  and you should see a new `IngestFromSource` object appear in your Django
  admin.

# The `artefacts` folder

Note: After you have used the tool for summarizing at least one video, there
should be a folder `artefacts` which contains the following files:

- `django_media`
  - This folder contains files that the system has downloaded or generated
  - For now, these are the audio files, the Whisper transcripts and the
    GPT summaries
- `logs/backend/cron/`
  - This folder contains logfiles of the cronjobs that run every minute.
  - This can be useful for debugging, ie when a job seems to be in the
    `Pending` state for too long. Note that during the Whisper transcription
    there is no output, so this step can indeed take up to 20 minutes depending
    on how long the video is.
- `tmp`
  - This folder contains lockfiles
  - These files make sure that the cronjobs that run every minute only every
    run once at a time. Often, the job will take longer than a minute, so
    when the job triggers again in the next minute and it finds a lockfile
    to be still present in this folder, the job will immediately terminate.
- `django.sqlite3`
  - This file is the Django database file.
