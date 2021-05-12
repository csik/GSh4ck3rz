import asyncio
from pyppeteer import launch
import csv
import os, os.path
import time
import applescript

test_file = 'Chris Csikszentmihalyi'
grades_dir = '/Users/csik/Downloads/Grade_PDFs'

assignmentpage = 'https://www.gradescope.com/courses/228839/assignments/1235754/submissions'

# field for student name, to click
student_name_input_field = '//*[@id="submissions-manager-upload-form"]/div[1]/div/div[1]'
# field for student name, to type
student_name_input_field2 = '//*[@id="owner_id-selectized"]'

# assignment upload button
assignment_submit_button = '//*[@id="submissions-manager-upload-form"]/div[2]/label/span[2]/span'

# assignment final upload button in modal window
upload = '//*[@id="submit"]'

# master upload button
master_upload = '//*[@id="actionBar"]/ul/li[2]/button/span/span'

# student name path
student_name='//*[@id="submissions-manager-upload-form"]/div[2]/label/span[1]'

async def setup(assignmentpage):
    browser = await launch({"autoClose":False,'headless': False, 'userDataDir':'./pyppeteer_data'})
    page = await browser.newPage()
    await page.goto(assignmentpage)

    await page.setViewport({ #  maximize window
      "width": 1400,
      "height": 800
      })
    return page

async def get_text(page, element):
     return await page.evaluate('(element) => element.textContent', element)

async def get_link(page, element):
    return await page.evaluate('''(element) => {
        return element.href;
    }''', element)

def insert_clicks(numclicks):
    s = ""
    text = """
         tell application "System Events" to key code 125
         delay 0.1
         """
    for i in range(numclicks):
         s = s + text
    return s

async def upload_assignment(page):

    # get number of pdfs in target directory
    number_of_files = (len([name for name in os.listdir(grades_dir)]) + 1)

    """
    These next three steps are to ensure that the correct directory
     comes up in the system file chooser
    """

    # step 1: open modal dialog
    m_upload = await page.xpath(master_upload)
    clicked = await m_upload[0].click()

    # step 2: open system file chooser
    file_upload = await page.xpath(assignment_submit_button)
    get_dialog = await file_upload[0].click()

    # step 3: ask user to select something then escape out of the modal dialogs
    input("Click a file in the correct directory and click enter: ")


    """
    Now the loop.
        1. Open the modal dialog
        2. Open the second system modal file chooser
        3. Create an applescript that will send keycode down key [number of indes] times
            and send keycode enter
            NB: codes are apple codes
        4. Run applescript, second modal should close
        5. The page will have updated a field based on the pdf name.
            Pull the name and formate it correctly.
        6. Click on the student name field. Backspace, fill it, hit return.
        7. Hit the upload button, close the first modal
    """

    for i in range(number_of_files):

        # open first modal dialog
        await page.waitForXPath(master_upload)
        m_upload = await page.xpath(master_upload)
        clicked = await m_upload[0].click()

        # open second modal -- the system file chooser
        await page.waitForXPath(assignment_submit_button)
        file_upload = await page.xpath(assignment_submit_button)
        get_dialog = await file_upload[0].click()

        print('should ready to click down files')
        time.sleep(1)

        # type down arrow to get the next file
        # first click is ignored, so that's hard coded
        numclicks = insert_clicks(i)
        command = """
        activate application "Chromium"
            delay(1)
            tell application "System Events" to key code 125
            delay 0.1
            {numclicks}
            tell application "System Events" to key code 36
            delay 0.1
        end
        """.format(numclicks=numclicks)

        print("command being sent = " + command)
        print('should be clicking down files...')
        try: applescript.AppleScript(command).run()
        except Exception:
            print('applescript did not work')

        print('should have found file, closed first modal')
        time.sleep(1)

        # get student name from pdf name field
        # this may be overly complex
        sname = ''
        while True:
            print(type(sname))
            print(sname)
            sname = await page.xpath(student_name)
            try:
                if type(sname) == list and len(sname) == 1:
                    break
            except Exception: pass
            time.sleep(0.2)
        print(type(sname))
        s = sname[0]
        s = await get_text(page,s)
        s = s.split('.')[0].replace('_',' ')

        print("should be printing name: "+s)
        # enter name in student name field
        # click, send a backspace to clear it, type the student name, hit return
        autofill = await page.xpath(student_name_input_field)
        clicked = await autofill[0].click()
        print('should be clicking backspace')
        clicked = await page.keyboard.press('Backspace')
        time.sleep(0.1)
        print('should be autofilling')
        a = await page.xpath(student_name_input_field2)
        clicked = await a[0].type(s)
        time.sleep(0.1)
        print('should be hitting return')
        clicked = await a[0].type('\r')
        time.sleep(0.1)

        # click upload to close modal dialog box
        up = await page.xpath(upload)
        clicked = await up[0].click()
        time.sleep(3)


async def main():
    page = await setup(assignmentpage)
    run = await upload_assignment(page)

if '__main__' == __name__:
    asyncio.get_event_loop().run_until_complete(main())

