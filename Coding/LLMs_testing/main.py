import asyncio
import platform
import time

import nodriver

async def main():
    #NON FUNZIONA
    # The Windows event loop policy will close it before the program ends without this line
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    browser = await nodriver.start()
    page = await browser.get('https://chatgpt.com/')

    await page.get_content()
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
