import asyncio
import os
from pathlib import Path
import shutil
import zipfile
from pyppeteer import launch

""" Watcher to download gradesheets for an assignment automatically to specified folder.
    Must set WATCH_DIR and DOWNLOAD_DIR.
"""

ASSN_PAGE = 'https://www.gradescope.com/courses/288777/assignments/1451657/'
REVIEW_PAGE = ASSN_PAGE + "review_grades"
WATCH_DIR = '/Users/ianarawjo/Documents/GSh4ck3rz/watch_data' # be careful --the script removes files automatically at the dir
DOWNLOAD_DIR = '/Users/ianarawjo/Downloads/' # where Chromium will d/l its files
SLEEP_INTERVAL = 60 # time between downloads; in seconds

async def setup(reviewpage):
    browser = await launch({"autoClose":False,'headless': False, 'userDataDir':'./pyppeteer_data'})
    page = await browser.newPage()
    await page.goto(REVIEW_PAGE)

    await page.setViewport({ #  maximize window
      "width": 1400,
      "height": 800
      })
    return page

async def main():
    page = await setup(REVIEW_PAGE)

    while(True):

        action_btns = await page.querySelectorAll('.actionBar--action')
        export_eval_btn = None
        download_csv_btn = None
        for btn in action_btns:
            title = await page.evaluate("(btn) => btn.getAttribute('title')", btn)
            if title == "Download marked rubrics for each question":
                export_eval_btn = btn
                break
        action_btns = await page.querySelectorAll('.popover--listItem')
        for btn in action_btns:
            href = await page.evaluate("(btn) => btn.getAttribute('href')", btn)
            print(href)
            if href[-10:] == "scores.csv":
                download_csv_btn = btn
                break

        # Download eval sheets
        await export_eval_btn.click()

        # Wait
        await asyncio.sleep(2)

        # Download scores csv
        download_btn = await page.querySelectorAll('#download-grades-tooltip-link')
        await download_btn[0].click()
        await asyncio.sleep(1)
        await download_csv_btn.click()

        # Wait
        await asyncio.sleep(5)

        # Delete contents of watch folder
        for root, dirs, files in os.walk(WATCH_DIR):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

        # Move downloaded files to watch folder + unzip
        paths = sorted(Path(DOWNLOAD_DIR).iterdir(), key=os.path.getmtime, reverse=True)
        for path in paths[:2]:
            print(path)
            if str(path)[-4:] == ".csv":
                shutil.copy2(path, WATCH_DIR)
            elif str(path)[-4:] == ".zip":
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(WATCH_DIR)

        await page.goto(REVIEW_PAGE)
        await asyncio.sleep(SLEEP_INTERVAL)

if '__main__' == __name__:
    asyncio.get_event_loop().run_until_complete(main())
