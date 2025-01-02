import asyncio
import platform
import time

import nodriver
from nodriver.core.browser import Browser
from nodriver.core.tab import Tab

async def login(page: Tab, browser: Browser):
    try:
        await page.get_content()

        login_button = await page.find("login-button")
        await login_button.click()
        await page.get_content()

        email_txt_box = await page.select("#email-input")
        await email_txt_box.send_keys("mercenari98@gmail.com")
        continue_button = await page.find("continue-btn")
        await continue_button.click()
        await page.get_content()

        psw_txt_box = await page.select("#password")
        await psw_txt_box.send_keys("-gG@E;g$2f:~D_%ytrxtfchk")
        continue_button = await page.find("_button-login-password")
        await continue_button.click()
        await page.get_content()
        print("Login Successful")
    except:
        try:
            await page.select("#radix-\:r4\: > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)")
            print("Already logged in")
        except:
            print("Unexpected status")
            browser.stop()
            exit(1)

async def main():
    #NON FUNZIONA
    # The Windows event loop policy will close it before the program ends without this line
    #if platform.system() == 'Windows':
        #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    browser = await nodriver.start()
    page = await browser.get('https://chatgpt.com/')

    await login(page,browser)

    txt_box = await page.select("#prompt-textarea")
    await txt_box.send_keys("Scrivimi un testo lungo almeno 3 paragrafi su un argomento a tua scelta")
    question_counter = 0
    send_button = await page.find("send-button")
    await send_button.click()
    question_counter += 1
    await page.select(".icon-md-heavy",30)
    response = await page.select(f"div.markdown:nth-child({question_counter})")
    print(response)
    #To avoid the immediate window's closing
    time.sleep(8)

if __name__ == '__main__':

    # This option works in Windows but close the page when the main ends
    nodriver.loop().run_until_complete(main())

    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(main())
