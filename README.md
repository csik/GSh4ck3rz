# GSh4ck3rz
Hacks for gradescope

Stub for adding functionality to gradescope. Uses pyppeteer and asyncio. 

Authentication currently just using the user data feature of pyppeteer -- it will fail the first time, then log in with your credentials, and it will work for [n] hours.

Create a python 3.6+ virtualenv in the directory, activate, then 

```
  > virtualenv venv
  > source venv/bin/activate
  > pip install pyppeteer
```

Run the script once:

```
  > python gs.py
```

Authenicate, then quit the browser. Run it again, you're good until the authentication expires.


