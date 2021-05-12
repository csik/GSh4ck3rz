import asyncio
from pyppeteer import launch

#assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/965994/review_grades'
#assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/1078556/review_grades'
assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/1119721/review_grades'

async def setup():
    browser = await launch({"autoClose":False,'headless': False, 'userDataDir':'./pyppeteer_data'})
    page = await browser.newPage()
    await page.goto(assignmentpage)

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

    # example of getting to a student submission page -- this would be a loop,
    # incrementing through elements, possibly with multiple workers
    links = []
    for element in elements:
        a = await element.getProperty('href')
        link =  a.toString()[9:]
        links.append(link)

    errornum = 0
    for studentcount, link in enumerate(links):
        try:
            await page.goto(link)
        except Exception:
            print('choked on {}'.format(link))
            continue
        await page.setViewport({ #  maximize window
       "width": 1400,
       "height": 800
       })


        # get to a reselect pages page
        try:
            btn = await page.waitForXPath('//span[text()="Reselect Pages"]')
        except Exception:
             print('choked on {}'.format(link))
             continue
        await btn.click()

        # get all instances of page thumbnails
        # get to a reselect pages page
        try:
            thumb = await page.waitForSelector('div.pageThumbnail--bottom')
        except Exception:
              print('choked on {}'.format(link))
              continue
        thumbnails = await page.querySelectorAll('div.pageThumbnail--bottom')
        for pagecount, thumbnail in enumerate(thumbnails, start=1):
            question_assignments = await thumbnail.querySelectorAll('.tagButton--questionNumber')
            if len(question_assignments) == 0:
                print("{enum},Page {pagenum},{url}".format(enum = str(studentcount)+'/'+str(len(links)),pagenum=pagecount, url=page.url))
                errornum = errornum + 1
    print('Total errors = {}'.format(errornum))

    #check to see if tagButtons are in pageThumbnail selectPagesPage
    #await page.goBack()

asyncio.get_event_loop().run_until_complete(main())
