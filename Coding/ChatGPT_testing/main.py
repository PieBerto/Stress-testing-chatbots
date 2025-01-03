import asyncio
import platform
import re
import time
from typing import TextIO

import nodriver
from nodriver.core.browser import Browser
from nodriver.core.element import Element
from nodriver.core.tab import Tab
from pathlib import Path


def get_questions(file_f: TextIO, messages: list[str]):
    question = ""
    for line in file_f:
        if line == "%%\n":
            messages.append(question)
            return get_questions(file_f, messages)
        elif line == "%%%\n" or line == "%%%%\n" or line == "%%%%":
            messages.append(question)
            return
        else:
            question += line


async def login(page: Tab, browser: Browser):
    try:
        await page.get_content()

        login_button = await page.find("login-button")
        time.sleep(1.5)
        await login_button.click()
        await page.get_content()

        email_txt_box = await page.select("#email-input")
        await email_txt_box.send_keys("mercenari98@gmail.com")
        continue_button = await page.find("continue-btn")
        time.sleep(1.5)
        await continue_button.click()
        await page.get_content()

        psw_txt_box = await page.select("#password")
        await psw_txt_box.send_keys("-gG@E;g$2f:~D_%ytrxtfchk")
        continue_button = await page.find("_button-login-password")
        time.sleep(1.5)
        await continue_button.click()
        await page.get_content()
        print("Login Successful")
    except:
        try:
            await page.select("body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > "
                              "div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > "
                              "div.composer-parent.flex.h-full.flex-col.focus-visible\\:outline-0 > "
                              "div.flex-1.overflow-hidden.\\@container\\/thread > div > div.absolute.left-0.right-0 > "
                              "div > div.gap-2.flex.items-center.pr-1.leading-\\[0\\] > button")
            print("Already logged in")
        except:
            print("Unexpected status")
            browser.stop()
            exit(1)


async def main(question_os: list[str], question_cot: list[str], question_pot: list[str], account: str,
               question_name: str):
    #Opening file with questions
    Path("..\\response\\ChatGPT-4o-mini\\" + account + "\\" + question_name).mkdir(parents=True, exist_ok=True)
    cot_f = open("..\\response\\ChatGPT-4o-mini\\" + account + "\\" + question_name + "\\" + "CoT.txt", 'a+')
    #Opening the page
    browser = await nodriver.start()
    page = await browser.get('https://chatgpt.com/')

    await login(page, browser)
    #Setting the chat as temporary (anonymous) TODO: find a selector!!
    tmp_chat1 = await page.select(
        "body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > "
        "div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > "
        "div.draggable.sticky.top-0.z-10.flex.min-h-\\["
        "60px\\].items-center.justify-center.border-transparent.bg-token-main-surface-primary.pl-0.md\\:hidden > "
        "div:nth-child(2) > button", )
    print(tmp_chat1)
    time.sleep(1000)
    await tmp_chat1.click()

    tmp_chat2 = await page.find("temporary-chat-toggle", timeout=1000)
    time.sleep(1.5)
    await tmp_chat2.click()
    #Start prompting
    txt_box = await page.select("#prompt-textarea")
    response: None | str = None
    question_counter = 0
    for q in question_cot:
        await txt_box.send_keys(q)
        send_button = await page.find("send-button")
        await send_button.click()
        question_counter += 1
        await page.select(".icon-md-heavy", 30)
        response = str((await page.select_all(f"div.markdown:nth-child(1)"))[question_counter])
        print(response)
    #Cleaning the answer
    if response is not None:
        answer = re.sub("[a-zA-Z:|!£$%&/()='§#°ç@;_<>?+*^ ]", "", response).replace(' ', "").replace('\t', "").replace(
            '\n', "").replace('\r', "") + ";"
    else:
        raise ValueError("Response is None")
    #Writing on file
    cot_f.write(answer)

    #Files closing
    cot_f.close()
    #To avoid the immediate window's closing
    time.sleep(8)


if __name__ == '__main__':
    file_name = "..\\questions\\typology1\\Question1.txt"
    file = open(file_name, "r")
    one_shot_msg = []
    get_questions(file, one_shot_msg)
    chain_of_thoughts_msg = []
    get_questions(file, chain_of_thoughts_msg)
    programming_of_thoughts_msg = []
    get_questions(file, programming_of_thoughts_msg)
    file.close()

    question_name = file_name.replace("..\\questions\\typology1\\", "").replace(".txt", "")

    # This option works in Windows but close the page when the main ends
    nodriver.loop().run_until_complete(
        main(one_shot_msg, chain_of_thoughts_msg, programming_of_thoughts_msg, "account1", question_name))

    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(main())
