import time

from playwright.sync_api import expect
from pytest_pytestrail import pytestrail
from src.pages.onboarding.onboarding import OnBoarding
from src.pages.sidebar.sidebar import Sidebar

from tests import setting

lang = setting.coccoc_language


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474135")
def test_content_youtube_at_first_time(
    copy_sidebar_icon_files: None,
    reset_sidebar_on_boarding: None,
    on_boarding: OnBoarding,
    sidebar: Sidebar,
):
    # Remove YouTube icon first as: https://coccoc.atlassian.net/browse/PF-2103?focusedCommentId=158337
    sidebar.remove_custom_icon_by_its_name(icon_name="Youtube")

    on_boarding.open_on_boarding_url(url="https://www.youtube.com/")
    on_boarding.check_on_boarding_is_shown()
    if lang == "en":
        expect(
            on_boarding.page.get_by_text("Suggestion from Cốc Cốc", exact=True)
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Smooth like sidebar - Stay groovy with music", exact=True
            )
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Add YouTube to the sidebar to find and play your favorite music videos right away!"
            )
        ).to_be_visible()
    else:
        expect(
            on_boarding.page.get_by_text("Đề xuất từ Cốc Cốc", exact=True)
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Thanh bên mượt mà - Thưởng nhạc mê say", exact=True
            )
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Thêm ngay YouTube vào thanh bên để nhanh chóng tìm và chơi video nhạc bạn thích!"
            )
        ).to_be_visible()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474144")
def test_content_translate_at_first_time(
    copy_sidebar_icon_files: None,
    reset_sidebar_on_boarding: None,
    on_boarding: OnBoarding,
):
    on_boarding.open_on_boarding_url(url="https://translate.google.com/")
    on_boarding.check_on_boarding_is_shown()
    if lang == "en":
        expect(
            on_boarding.page.get_by_text("Suggestion from Cốc Cốc", exact=True)
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Find languages hard? Let sidebar help you", exact=True
            )
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Open Google Translate in sidebar window to translate languages 2x faster. Just one click to access, no need to switch between multiple tabs."
            )
        ).to_be_visible()
    else:
        expect(
            on_boarding.page.get_by_text("Đề xuất từ Cốc Cốc", exact=True)
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text("Ngoại ngữ khó? Có thanh bên lo", exact=True)
        ).to_be_visible()
        expect(
            on_boarding.page.get_by_text(
                "Mở Google Dịch trong cửa sổ thanh bên để dịch ngoại ngữ nhanh hơn gấp 2 lần. Truy cập trong 1 click, không cần chuyển qua lại giữa nhiều tab."
            )
        ).to_be_visible()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474153")
def test_content_facebook_messenger_zalo_telegram_skype_at_first_time(
    reset_sidebar_on_boarding: None, on_boarding: OnBoarding
):
    for icon_name in list(setting.list_on_boarding_feature_icons.keys()):
        on_boarding.open_on_boarding_url(
            url=setting.list_on_boarding_feature_icons.get(icon_name)
        )
        on_boarding.check_on_boarding_is_shown()
        if lang == "en":
            expect(
                on_boarding.page.get_by_text("Suggestion from Cốc Cốc", exact=True)
            ).to_be_visible()
            expect(
                on_boarding.page.get_by_text(
                    "More than one feature... It is the Sidebar.", exact=True
                )
            ).to_be_visible()
            expect(
                on_boarding.page.get_by_text(
                    "Facebook Messenger, Telegram, Skype and Zalo are all integrated on the sidebar for your extra convenience. Go chat now!"
                )
            ).to_be_visible()
        else:
            expect(
                on_boarding.page.get_by_text("Đề xuất từ Cốc Cốc", exact=True)
            ).to_be_visible()
            expect(
                on_boarding.page.get_by_text(
                    "Hơn cả một tính năng... Đó là thanh bên", exact=True
                )
            ).to_be_visible()
            expect(
                on_boarding.page.get_by_text(
                    "Facebook Messenger, Telegram, Skype, Zalo đều được tích hợp vào thanh bên Cốc Cốc. Vào chat ngay thôi!"
                )
            ).to_be_visible()
        on_boarding.click_close_on_boarding()
        time.sleep(3)
