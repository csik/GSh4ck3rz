import asyncio
from pyppeteer import launch

async def setup():
    browser = await launch({"autoClose":False,'headless': False, 'userDataDir':'./pyppeteer_data'})
    page = await browser.newPage()
    await page.goto('https://www.gradescope.com/courses/228839/assignments/965994/review_grades')

    await page.setViewport({ #  maximize window
      "width": 1400,
      "height": 800
      })
    return page

async def get_submissions(page):
    elements = await page.querySelectorAll('a.link-gray')
    return elements

async def main():
    page = await setup()
    elements = await get_submissions(page)

    #example of getting to a student submission page
    e = elements[3]
    await e.click()

    # get to a reselect pages page
    btn = await page.waitForXPath('//span[text()="Reselect Pages"]')
    await btn.click()

    #loop through elements here
    #check to see if tagButtons are in pageThumbnail selectPagesPage
    #await page.goBack()

asyncio.get_event_loop().run_until_complete(main())
