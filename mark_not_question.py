import asyncio
from pyppeteer import launch

#assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/965994/review_grades'
#assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/987230/review_grades'
assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/987230/grade'
empypage_placeholder = 'https://www.gradescope.com/assets/missing_placeholder-4d611cea193304f8a8455a58fd8082eed1ca4a0ea2082adb982b51a41eaa0c87.png'

async def setup(assignmentpage):
    browser = await launch({"autoClose":False,'headless': False, 'userDataDir':'./pyppeteer_data'})
    page = await browser.newPage()
    await page.goto(assignmentpage)

    await page.setViewport({ #  maximize window
      "width": 1400,
      "height": 800
      })
    return page

async def get_submissions(page):
    elements = await page.querySelectorAll('div.gradingDashboard--question')
    return elements

async def get_all_grading_links(elements):
    links = []
    for e in elements:
        link_handles = await e.querySelectorAll('a.link-noUnderline')
        link_handle = await link_handles[0].getProperty('href')
        links.append(link_handle.toString()[9:])
    return links

async def has_placeholder_image(page):
    image = await page.querySelector('img')
    image_src = await image.getProperty('src')
    return image_src.toString().find('missing_placeholder') != -1

async def advance_page(page):
    btn = await page.querySelector('.fa-forward')
    await btn.click()

async def get_text(page, element):
     return await page.evaluate('''(element) => {
        element.textContent;
     }''', element)

async def get_link(page, element):
    return await page.evaluate('''(element) => {
        return element.href;
    }''', element)

async def mark_reading_not_selected(page):
    btns = await page.querySelectorAll('.rubricItem--key')
    btn = btns[0]
    if await page.evaluate("(btn) => btn.getAttribute('aria-pressed')", btn) = 'false':
        await btn.click()

async def go_through_pages(page):
    while(1):
     if await has_placeholder_image(page):
        await mark_reading_not_selected(page)
    #sleep(.5)
     current_page = await page.xpath('//*[@id="main-content"]/div/main/section/div/span/span/abbr')
     current_page = current_page[0]
     last_page = await page.xpath('//*[@id="main-content"]/div/main/section/div/strong/a')
     last_page = last_page[0]
     if await get_text(page, last_page) == await get_text(page, current_page):
         break
     await advance_page(page)
     await page.waitForNavigation()

async def main():
    page = await setup(assignmentpage)
    elements = await get_submissions(page)
    links = await get_all_grading_links(elements)

    #check to see if tagButtons are in pageThumbnail selectPagesPage
    #await page.goBack()

