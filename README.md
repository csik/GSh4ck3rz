# GSh4ck3rz
Hacks for gradescope

Stub for adding functionality to gradescope. Uses pyppeteer and asyncio. 

Authentication currently just using the user data feature of pyppeteer -- it will fail the first time, then log in with your credentials, and it will work for [n] days.

Create a python 3.6+ virtualenv in the directory, activate, then 

```
  > virtualenv venv
  > source venv/bin/activate
  > pip install -r requirements.txt
```

Run the script once:

```
  > python find_unmatched_submissions.py
  _or_
  > python mark_not_question.py
```

Authenicate, then quit the browser. Run it again, you're good until the authentication expires, 3-4 days.

mark_not_question detects the "The student did not submit any pages..." image, then clicks the "this reading was not selected" button.

find_unmatched_submissions finds any uploaded documents that are not assigned to a question. These may simply be blank pages, etc. 

graders_questions has been replaced by Ian Arawjo's scripts.


