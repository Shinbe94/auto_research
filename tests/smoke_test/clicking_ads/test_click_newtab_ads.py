import math
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from pywinauto import Application
from src.pages.coccoc_common import open_browser
from src.pages.new_tab.new_tab_page import NewTabPage, NewTabPageSel
from playwright.sync_api import Locator, expect, sync_playwright, Route

import pytest
from pytest_pytestrail import pytestrail
import json

from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1214442")
def test_click_video_vast_ads(new_tab_page_sel: NewTabPageSel):
    for url in setting.list_vast_videos:
        new_tab_page_sel.open_page(url)
        new_tab_page_sel.click_vast_video()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215525")
def test_click_all_ads_type_from_new_tab(new_tab_page_sel: NewTabPageSel):
    new_tab_page_sel.click_list_newsfeed_ads()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215525")
def xtest_click_all_ads_type_from_new_tab(new_tab_page: NewTabPage):
    new_tab_page.click_list_newsfeed_ads()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1214442")
def xtest_click_video_vast_ads():
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver: WebDriver = coccoc_instance[0]
    coccoc_window: Application = coccoc_instance[1]
    ntps = NewTabPageSel(driver)
    try:
        for url in setting.list_vast_videos:
            ntps.open_page(url=url)
            sleep(5)
            ntps.click_vast_video()
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215525")
def xtest_click_all_ads_type_from_new_tab(new_tab_page20: NewTabPage):
    new_tab_page20.click_list_newsfeed_ads()


def xtest_new_tab(new_tab_page: NewTabPage):
    # new_tab_page.open_any_page(url="https://coccoc.com/webhp?espv=2&ie=UTF-8&l=en-US")
    new_tab_page.page.evaluate("localStorage.clear();")
    new_tab_page.page.evaluate("sessionStorage.clear();")
    # page = new_tab_page.page.context.new_page()
    # page.evaluate("localStorage.clear();")
    # page.evaluate("sessionStorage.clear();")
    print("\n")
    # page.on(
    #     "request",
    #     lambda request: print(request.url)
    #     if "coccoc.com/webhp/ntp.json" in request.url
    #     else None
    # )

    # with page.expect_response(
    #     lambda response: "coccoc.com/webhp/ntp.json" in response.url
    #     and response.status == 200
    # ) as response_info:
    #     page.goto("https://coccoc.com/webhp?espv=4&ie=UTF-8&l=en-US")

    # assert response_info.value.ok

    # Abort response
    # page.route("**/coccoc.com/webhp/ntp.json", lambda route: route.abort())
    # sleep(5)

    # response = response_info.value
    # page.on("response", lambda response: print("<<", response.status, response.url))
    # page.goto("https://coccoc.com/webhp?espv=4&ie=UTF-8&l=en-US")
    # sleep(15)

    # Modify response
    # def handle_route(route: Route) -> None:
    #     # Fetch original response.
    #     response = route.fetch()
    #     # Add a prefix to the title.
    #     body = response.text()
    #     body = body.replace("<title>", "<title>My prefix:")
    #     route.fulfill(
    #         # Pass all fields from the response.
    #         response=response,
    #         # Override response body.
    #         body=body,
    #         # Force content type to be html.
    #         headers={**response.headers, "content-type": "text/html"},
    #     )

    # with page.expect_response(
    #     lambda response: "coccoc.com/webhp/ntp.json" in response.url
    #     and response.status == 200
    # ) as response_info:
    #     page.goto("https://coccoc.com/webhp?espv=4&ie=UTF-8&l=en-US")

    # assert response_info.value.ok
    # sleep(5)
    new_tab_page.page.route(
        "**/coccoc.com/webhp/ntp.json",
        lambda route: route.fulfill(
            path=r"C:\Users\Taynq\Documents\automation\coccoc_win\tests\smoke_test\clicking_ads\ads.json"
        ),
    )

    # new_tab_page.page.goto("https://coccoc.com/webhp?espv=4&ie=UTF-8&l=en-US")
    with new_tab_page.page.expect_response(
        lambda response: "**/coccoc.com/webhp/ntp.json"
        in response.url
        # and response.status == 200
    ) as response_info:
        new_tab_page.page.goto("https://coccoc.com/webhp?espv=4&ie=UTF-8&l=en-US")

    sleep(4)
    new_tab_page.reload_page()
    # print_list = lambda list: [print(f"Item {x}") for x in [1, 2, 3]]
    # print_list()
    sleep(4)


def xtest_mock_network(new_tab_page: NewTabPage):
    new_tab_page.page.evaluate("localStorage.clear();")
    new_tab_page.page.evaluate("sessionStorage.clear();")

    sleep(2)

    def handle_route(route: Route) -> None:
        response = route.fetch()
        json = response.json()
        # print(json)
        # json["icons"] = []
        # json["rb"] = []
        # json["ntrb"] = [
        #     {
        #         "json": {
        #             "advert_id": 43413170,
        #             "attributes": {
        #                 "banner_src": "https://bid.g.doubleclick.net/xbbe/bid/xpub?deal_id=16824727_808827\u0026max_duration=6\u0026ord=[timestamp]\u0026dc_sdk_apis=[APIFRAMEWORKS]\u0026dc_omid_p=[OMIDPARTNER]\u0026dc_vast=3\u0026dc_rdid=",
        #                 "isMasthead": "2",
        #                 "keepPip": "1",
        #                 "mhHeight": "360",
        #                 "mhNarrowHeight": "90",
        #                 "name": "masthead_video_43413170",
        #                 "narrow_timeout": "3",
        #                 "pip": "1",
        #                 "show_complete_timeout": 2000,
        #                 "show_complete_url": "https://ntrb.qc.coccoc.com/show?show=_0YbS50vdaneUO-5oHBeyB1YKN7GTw9pQdu4iCDlQvePjHa3M*nKpbRJfLl6xPSkTrlGXtMlUNLEDliMtboHIoHMpUrlYzbJZJGYPZ-lRFiPVFFGzvUo7R4bBFyraFv596e7EpSVBTqB03DKjtGAjT9Iq8fLpkU9B91atRUoIUYVR87BnEXfdqbZ9IFlHv6DL890oGRQwd*mW-zCuUd8jSIMC2O8ahpvKtY8xyYQEAedkBqn63w9oOY7mrcpLk54CyE6dmFj7oWA-Rw39nuQklQRFjH-BK2IJceZ8JQ7I-HFToo8r27Vz4-bjJB1WFxbruPVToTg4GQpQcwcaDD-cCikwxDWSLvxmzCO-0EdpB55D1SmhhGgA-p*KyTBidANtv6B50PzJeWh4nbTXC78y5c9sTR1wH2RuZagnw7HvZuMQCFBroe381hgjXIFaBktyEqVH0JAoqGaQujtXJ1tpniBApBjpNiynrsKB17CyA*4knmJKHCwYrmjYmZdMCGDdgpEAl2RjglY1ZAk1vMO8sTeATb9qD4j64gIZs5xstsmfXcI8eQChNFzraqMdmtODWVmIOCRwayXo4DlTu5sohp-IAB0QLT3TJILMQENj0-UzvPwTo3Yj8FgV5lZ0*o0hBvHa38af6VK4F-kB6ptKJGR*SJgiqjiJ2YN4yJ8zArXJpvTRTJUARXv96H3UZ6LwnmAx5mCr*gzKzfEEms6J98ON8Vr1qRTpjNC7BuVeuzpdwxh4veXqSigpnUUqDUGykJ8BxEYk4RNJ8jkW*ya18SqURNgbE6FerUduUuzyIkVOacNAazVHGxAkjx2Ii4mQlK228qEeeoKvha8fjuz1UlXOBYTik0uAQzR30yj5fv0XPja6OUWTzUBo.\u0026reqid=MPrHTpWV",
        #                 "valid_till": 1682873999,
        #             },
        #             "banner_type": "masthead_video",
        #             "campaign_id": 1692758,
        #             "match_id": 477530333,
        #             "show_attempt_url": "https://ntrb.qc.coccoc.com/show_attempt?show_attempt=_0-7S50vdateW8350XBe3xUyCSfdPDbgGIwy9ELlvLVztKqWMOiDakYuFRapFFDj3RWnQe0PirqHLFqlVf11fDDxLE4ja1wgoNtnabHh26mx71-dUhM64Gq4bDyw4eu4c8GqHbEkPO9x-4VLwBaWsKqRjestI5ml9*1YRzwv*9n3V7ifpA-b5YUnQEA4RUwPjaklRcPzn9u8azUuON6dbRtRvYTQNlD4rNpAyH-1KzSBszF9Xp18OIswvbL*Ou8mcYga7qYkKcJYfzbX6HUCBx83DPNL3f8TaQqNK-nYPIdFh5IHBmDc-OrveHm23LWYKdDi8u-7u7DUldI7T9lm9dxZ20wM07Kzs5ZlYNCagDzuq-4srauK7d8WF18iCui5aEGjk99ICfBMi7JTMTI3A*0W0qZ85xETmN1sgVuqhEvfW6fFs63Up08ARRhXIeNUMnDN-XsF4DaMNOa3M7lVoTFB5FCAs1ZrgVaW*hYc*whFY1ZPUc3z6U1v17xup8y46d2KZOf3D9Rc3kDzH4z2NWmPN*smqmFFBmvojczxMla1kdd95upZF1L0G98YC9gNhed0ESOC45X9tEgHppfxrbo0yFeqHcB35O1sIUcyyGVjuXHWR8g1NrkfGp5i0Yc8kwXv8YNfnoYCRVF97Ih2Ec6DEJGafhOsAv9bNkbj*nrv7zvKhOmP9qTuOHJHnW7JG37St0tBVI9IZrHDr7ThzrIal4V*hzGQYxxTUFZgR038gwjJ6cViUlId*5O0qQmBwNI7T93hXj\u0026reqid=MPrHTpWV",
        #             "type": 10,
        #             "valid_till": 1682873999,
        #             "vast": "https://qccoccocmedia.vn/comedia/ntrb?id=477530333\u0026uid=Lc0CqXm_YCddmoOOiIuZBMQv8T-4sZUMivjyhS3sYVu1\u0026bid=B6328033-E730-4918-B4E9-D3D1D4F37A8D.AZFu2_7LQ6G_1OIHt0FijQ..\u0026vid=GbyQT3yy1r9y31oSCT1GorS16y6C6ogy9uT6Wuhg_QE9ecbfECl28m3gI0cWW\u0026md=_0tLa50vdajfms34NnBezxXm6CFvoUC*tnrwrOfnmIXCsMmKOQ13vuMyA5tDQPisp9l6iGa7IMyi1eCGB2bOFh26C-ly6KBqu2FlInDzorHaJZvaRmBV*Yg0bH9X9NZXoSWEyWhV*KxfoPxd6Gv3EtRq-kDQGs6TjAN1x7N*tQ-kOs5bpw46u9J3PQEute*fCMjgJ7mxOQ44cVSks-zJHBbb-4AdreLjN2W98CJaD5XuL2uGcez1rUXPACMA87SBgzU1fkqFD79BPZXjVSJiIAVEgaeKrO0pttOV-*dBQ84LKbc2y6PT4LiiDc\u0026v=1%2E646%2E84\u0026reqid=MPrHTpWV\u0026format=vast\u0026ssp_name=coccoc\u0026qv_age=0",
        #         },
        #         "type": "json",
        #     },
        #     {
        #         "json": {
        #             "advert_id": 33820382,
        #             "attributes": {
        #                 "banner_src": "https://qc-static.coccoc.com/uploaded-files/4e9/01c/4e901c258d26e458f34f32a59ff5034a475e05fa5da31c3045194ecd08a86dd1/index.html"
        #             },
        #             "banner_type": "ntrb_640",
        #             "campaign_id": 1410431,
        #             "link": "https://qccoccocmedia.vn/comedia/ntrb?id=416520389\u0026uid=Lc0CqXm_YCddmoOOiIuZBMQv8T-4sZUMivjyhS3sYVu1\u0026bid=B6328033-E730-4918-B4E9-D3D1D4F37A8D.AZFu2_7LQ6G_1OIHt0FijQ..\u0026vid=GbyQT3yy1r9y31oSCT1GorS16y6C6ogy9uT6Wuhg_QE9ecbfECl28m3gI0cWW\u0026md=_0y7a50vda9Tks3oIXBZUBSJFKznDAsq6rOGd4hqgshcG6PDBVjjsh-Qr5lG2gXoRamKwBvyI--bjshU9B7OcWMGjOI0gHO4XQdetAj-gkXL37pGm0rQhbCKXgu6WWfWFplWEIw3dA2aZc0aQvcUJ3vAzXk79Y30PJBDyg0tiKdsiYqJwk5Ud4Gidmwfprm*lNhIpaZVHiTKVDBZ-M-fyaR89nYaNeXnLykp8MGPUYAUTktqrzVmAsSUhyO65dq*OiMBQCWvuX3kq6i8rHy5rlYAMxx-2FBHer4h66fwr1GEeXqmrNSDMWJCYn*EqND4NLq*84o64FOiEkLPSNdlwtf9XMFq1nL3ZtPtUdZo2nVLPstwmrdF6cOdF8lw..\u0026v=1%2E646%2E84\u0026reqid=MPrHTpWV\u0026ssp_name=coccoc\u0026qv_age=0",
        #             "match_id": 416520389,
        #             "show_attempt_url": "https://ntrb.qc.coccoc.com/show_attempt?show_attempt=_08rS50vdaneWA35oXBezx00KS-Xh7xGCTxyZfYimBFt-zh8o8lPjiN2w2CSgPXpYeNFug*xnp7hQv3IY7eJaAI4-tl1YTZFRu8t-weE-BOsqjPwxZMAO8o5jYvl70yziV1UF4rHQr4CDWI0Y3BXy1OjnbLBTGiN3aVrb4PkrTNfhne1UYSjSPyO7iQBhJKUY7nRbOzM6HNH7k1vm*16s3UTollYEBVTuYVEQHUxdAhWQQmemssY-04KqQWHrbl3FDHQxFBdtCt770rbY1elW-jLeJ9eBrXP0PW5S2A4qNs7OL5B-eKNewyB42YNyhCdImWw9FGESaRpBn3gdig9Kn*JpLdnMwGQC5TSHgvXDTDtKwSvNTUYi4ZNhX2MLrc70G-phIDgWDqc5Oj9rbNBb-7Wshq4hDpWoxbSBzfKhdEcVjhaXv4lhK5U9Wv8uDitkiD1PmNoa875-UiRJetVszalhvq2aGxdEeGSwpB9q3AbUvvf19T-RrW64*kLAh*5bXTW*AdL*SAtTjWBZwAEKAJkL58z3SFSE3eKDOztkm1yX0d24wAruZOUw1VtyilqAk5JvQr1BswFUejTjy-cjAmv-jkBKL167fiDD9LtdPcSTl2OnDnL0*VoTwots3eE2m1bRGmwQAHvgKY2*KFQYj-bNTWafTW*TjQhOZ*07Brfb52Sv*27l8nno2H8e328esz8tvXTzAdDSrtWZJ5F4wxTLKLFHzYwyiW0UQoJSSAN3nEQZudFRF1xTSeN10EZs30cY88wGYsH1f\u0026reqid=MPrHTpWV",
        #             "type": 5,
        #         },
        #         "type": "json",
        #     },
        # ]
        # json["ntrb"] = []
        json = {}
        route.fulfill(
            response=response,
            # Override response body.
            json=json,
        )
        print("=========Fulfill ok ============")

    for i in range(10):
        new_tab_page.page.evaluate("localStorage.clear();")
        new_tab_page.page.evaluate("sessionStorage.clear();")
        new_tab_page.page.route(
            "**/coccoc.com/webhp/ntp.json",
            handle_route,
        )
    new_tab_page.page.goto("https://coccoc.com/webhp?espv=4&ie=UTF-8&l=en-US")
    sleep(10)

    # new_tab_page.page.route(
    #     "**/coccoc.com/webhp/ntp.json",
    #     handle_route,
    # )

    # with new_tab_page.page.expect_response(
    #     lambda response: "coccoc.com/webhp/ntp.json" in response.url
    #     and response.status == 200
    # ) as response_info:
    #     new_tab_page.reload_page()

    # assert response_info.is_done()
    # response = response_info.value
    # print(response.json)
    sleep(4)


def xtest_mock_respone(new_tab_page: NewTabPage):
    new_tab_page.page.evaluate("localStorage.clear();")
    new_tab_page.page.evaluate("sessionStorage.clear();")
    book_title = "Designing Evolvable Web APIs with ASP.NET"

    def handle_route(route: Route) -> None:
        # Fetch original response.
        response = route.fetch()
        # print(response)
        # Add a prefix to the title.
        json_data = response.json()
        json_data["books"][0]["title"] = "test Edi title"
        json_data["books"][0]["author"] = "John Doe"
        json_data["books"][0]["publisher"] = r"John media!!"
        route.fulfill(
            # Pass all fields from the response.
            response=response,
            # Override response body.
            # json={"books": []},
            json=json_data,
            # path=r"C:\Users\Taynq\Documents\automation\coccoc_win\tests\smoke_test\clicking_ads\ads.json",
        )

    new_tab_page.page.route("**/demoqa.com/BookStore/v1/Books", handle_route)

    with new_tab_page.page.expect_response(
        "**//demoqa.com/BookStore/v1/Books"
    ) as response:
        new_tab_page.page.goto("https://demoqa.com/books")
    assert response.value.ok

    # new_tab_page.page.goto("https://demoqa.com/books")
    # book = new_tab_page.page.wait_for_selector(f"a >> text={book_title}")
    # book.click()
    # visible = new_tab_page.page.wait_for_selector(
    #     f"label >> text={book_title}"
    # ).is_visible()
    # assert visible
    sleep(5)


def xtest_print_request(new_tab_page: NewTabPage):
    new_tab_page.page.evaluate("localStorage.clear();")
    new_tab_page.page.evaluate("sessionStorage.clear();")
    print("\n")
    new_tab_page.page.on(
        "request",
        lambda request: print(
            request.url if "coccoc.com/webhp/ntp.json" in request.url else ""
        ),
    )
    # new_tab_page.reload_page()
    # sleep(5)
    # with new_tab_page.page.expect_response(
    #     lambda response: "**/coccoc.com/webhp/ntp.json" in response.url
    #     and response.status == 200
    # ) as response_info:
    #     new_tab_page.reload_page()

    # print(response_info.value.url)

    # new_tab_page.page.on(
    #     "request", lambda request: print(">>", request.method, request.url)
    # )
    # new_tab_page.page.on(
    #     "response", lambda response: print("<<", response.status, response.url)
    # )
    new_tab_page.reload_page()
    sleep(60)


def xtest_print_request_nre(new_tab_page: NewTabPage):
    new_tab_page.page.evaluate("localStorage.removeItem('lastFetchId');")
    new_tab_page.page.evaluate("localStorage.removeItem('ntp_shown_news_storage');")

    logs = list()
    new_tab_page.page.on(
        "request",
        lambda request: logs.append(
            request.url if "feed/v2/nre" in request.url else None
        ),
    )

    for i in range(20):  # make the range as long as needed
        new_tab_page.page.mouse.wheel(0, 3000)
        sleep(2)
        i += 1
    new_tab_page.page.wait_for_timeout(5_000)
    # print(logs)

    print(len(list(filter(lambda a: a != None, logs))))
    for i in range(20):
        logs2 = list()
        new_tab = new_tab_page.open_new_tab()

        new_tab.goto(setting.coccoc_homepage_newtab)
        new_tab.evaluate("localStorage.removeItem('lastFetchId');")
        new_tab.evaluate("localStorage.removeItem('ntp_shown_news_storage');")
        new_tab.on(
            "request",
            lambda request: logs2.append(
                request.url if "feed/v2/nre" in request.url else None
            ),
        )

        for i in range(20):  # make the range as long as needed
            new_tab.mouse.wheel(0, 3000)
            sleep(2)
            i += 1
        new_tab.wait_for_timeout(5_000)
        print(len(list(filter(lambda a: a != None, logs2))))


def xtest_scroll_to_last_newfeed_card(new_tab_page: NewTabPage, n: int = 50):
    # new_tab_page.scroll_to_view_of_last_newfeed_card()
    stay_at_newtab = math.floor(65 * n / 100)
    page_1: int = math.floor(6.4 * n / 100)
    page_2: int = math.floor(6 * n / 100)
    page_3: int = math.floor(2.8 * n / 100)
    page_4: int = math.floor(1.9 * n / 100)
    page_5: int = math.floor(1.4 * n / 100)
    page_6: int = math.floor(1.1 * n / 100)
    page_20: int = math.floor(
        n - (stay_at_newtab + page_1 + page_2 + page_3 + page_4 + page_5 + page_6)
    )
    total_request_page1: int = 0
    total_request_page2: int = 0
    total_request_page3: int = 0
    total_request_page4: int = 0
    total_request_page5: int = 0
    total_request_page6: int = 0
    total_request_page20: int = 0
    total_request_stay_at_newtab: int = 0

    for _ in range(page_1):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 1)

    for _ in range(page_2):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 2)

    for _ in range(page_3):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 3)

    for _ in range(page_4):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 4)
    for _ in range(page_5):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 5)
    for _ in range(page_6):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 6)
    for _ in range(page_20):
        new_tab = new_tab_page.open_new_tab()
        new_tab.goto(setting.coccoc_homepage_newtab)
        scroll_n_page(new_tab, 20)
    new_tab_page.open_n_newtab_at_the_same_time(n=stay_at_newtab)

    # sleep(10)


def wait_for_lastcard_appeared_1(page, timeout: float = 10):
    total_delay: float = 0.0
    interval_delay: float = 0.01
    while total_delay < timeout:
        try:
            wait_for_all_current_datafeed_appended(page)
            current_last_card_id = page.evaluate(
                "[...document.querySelectorAll('.nf-card')].at(-1).getAttribute('data-id')"
            )
            if current_last_card_id is not None:
                # print(current_last_card_id)
                return current_last_card_id
        except Exception:
            sleep(interval_delay)
            total_delay += interval_delay
            pass


def wait_for_lastcard_appeared(page, timeout: float = 10):
    total_delay: float = 0.0
    interval_delay: float = 0.01
    card_id = None
    while total_delay < timeout:
        wait_for_all_current_datafeed_appended(page)
        try:
            current_last_card_id = page.evaluate(
                "[...document.querySelectorAll('.nf-card')].at(-1).getAttribute('data-id')"
            )
            if current_last_card_id is not None:
                print(current_last_card_id)
                card_id = current_last_card_id
        except Exception:
            sleep(interval_delay)
            total_delay += interval_delay
            pass

        try:
            if card_id == None and current_last_card_id != None:
                card_id = current_last_card_id
                break
            elif card_id != None and card_id != current_last_card_id:
                card_id = current_last_card_id
                break
        except Exception:
            sleep(interval_delay)
            total_delay += interval_delay
            pass


def open_newtab(new_tab_page: NewTabPage) -> int:
    logs2 = list()
    new_tab = new_tab_page.open_new_tab()
    new_tab.on(
        "request",
        lambda request: logs2.append(
            request.url if "feed/v2/nre" in request.url else None
        ),
    )
    new_tab.goto(setting.coccoc_homepage_newtab)
    new_tab.wait_for_load_state()
    return len(list(filter(lambda a: a != None, logs2)))


def scroll_n_page(new_tab, n: int) -> int:
    total_request: int = 0
    for _ in range(n):
        logs2 = list()
        new_tab.on(
            "request",
            lambda request: logs2.append(
                request.url if "feed/v2/nre" in request.url else None
            ),
        )
        # wait_for_lastcard_appeared(new_tab)
        wait_for_lastcard_appeared_1(new_tab)
        new_tab.evaluate(
            "[...document.querySelectorAll('.nf-card')].at(-1).scrollIntoView({behavior: 'smooth'});"
        )
        if n >= 17:
            click_btn_xem_them(new_tab)
        wait_for_all_next_datafeed_pulled(new_tab)
        # wait_for_lastcard_appeared(new_tab)
        # new_tab.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # new_tab.wait_for_timeout(5_000)
        # print(len(list(filter(lambda a: a != None, logs2))))
        # wait_for_lastcard_appeared(new_tab)
        # sleep(2)
        total_request = total_request + len(list(filter(lambda a: a != None, logs2)))
    return total_request


def wait_for_all_current_datafeed_appended(new_tab):
    while True:
        try:
            if "display: block;" == new_tab.evaluate(
                "document.getElementById('newsfeed-intersection-target').getAttribute('style')"
            ):
                break
        except Exception:
            sleep(0.01)
            pass


def wait_for_all_next_datafeed_pulled(new_tab):
    while True:
        try:
            if "display: none;" == new_tab.evaluate(
                "document.getElementById('newsfeed-intersection-target').getAttribute('style')"
            ):
                break
        except Exception:
            sleep(0.01)
            pass


def click_btn_xem_them(page):
    try:
        if page.locator('//button[text()=" Xem thêm"]').is_visible():
            page.locator('//button[text()=" Xem thêm"]').click()
    except Exception:
        pass
    # print(
    #     new_tab.evaluate(
    #         "document.getElementById('newsfeed-intersection-target').getAttribute('style')"
    #     )
    # )


def xtest_print(new_tab_page: NewTabPage):
    sleep(3)
    # wait_for_all_current_datafeed_appended(new_tab_page.page)
    print(open_newtab(new_tab_page))
