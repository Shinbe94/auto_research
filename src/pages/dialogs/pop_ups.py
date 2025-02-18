from time import sleep
from typing import Tuple
from selenium.webdriver.common.by import By
from src.pages.base import BaseAppium
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocSettingTitle, CocCocTitles
from src.pages.toolbar.toolbar import Toolbar
from tests import setting

lang = setting.coccoc_language


class WarningClosingTabs(BaseAppium):
    # Locators
    if "en" in lang:
        CHECKBOX_ALWAYS_CLOSE_ALL = (
            By.XPATH,
            '//CheckBox[@Name="Always close all tabs"]',
        )
    else:
        CHECKBOX_ALWAYS_CLOSE_ALL = (
            By.XPATH,
            '//CheckBox[@Name="Luôn đóng tất cả các thẻ"]',
        )
    if "en" in lang:
        BTN_YES = (
            By.XPATH,
            '//Button[@Name="Yes"]',
        )
    else:
        BTN_YES = (
            By.XPATH,
            '//Button[@Name="Có"]',
        )
    if "en" in lang:
        BTN_CANCEL = (
            By.XPATH,
            '//Button[@Name="Cancel"]',
        )
    else:
        BTN_CANCEL = (
            By.XPATH,
            '//Button[@Name="Hủy"]',
        )

    def title_locator(self, total_tabs: int) -> tuple:
        if "en" in lang:
            return (
                By.XPATH,
                f'//Text[@Name="You are closing {str(total_tabs)} tabs. Do you want to continue?"]',
            )
        else:
            return (
                By.XPATH,
                f'//Text[@Name="Bạn đang đóng {str(total_tabs)} thẻ. Bạn có muốn tiếp tục?"]',
            )

    def check_popup_title(self, total_tabs: int):
        assert self.is_element_appeared(self.title_locator(total_tabs))

    def verify_popup_ui(self, total_tabs: int):
        self.check_popup_title(total_tabs)
        assert self.is_element_appeared(self.CHECKBOX_ALWAYS_CLOSE_ALL)
        assert self.is_element_appeared(self.BTN_CANCEL)
        assert self.is_element_appeared(self.BTN_YES)

    def verify_popup_not_appeared(self):
        assert self.is_element_disappeared(self.CHECKBOX_ALWAYS_CLOSE_ALL)
        assert self.is_element_disappeared(self.BTN_YES)

    def click_btn_cancel(self):
        self.click_element(self.BTN_CANCEL)

    def click_btn_yes(self):
        self.click_element(self.BTN_YES)


class OpenPickApplication(Toolbar):
    # Locators
    if "en" in lang:
        CHECKBOX_ALWAYS_CLOSE_ALL = (
            By.XPATH,
            '//TitleBar[@Name="Open Pick an application?"]',
        )
    else:
        CHECKBOX_ALWAYS_CLOSE_ALL = (
            By.XPATH,
            '//TitleBar[@Name="Mở Pick an app?"]',
        )

    if "en" in lang:
        TEXT_DES = (
            By.NAME,
            "A website wants to open this application.",
        )
    else:
        TEXT_DES = (
            By.NAME,
            "Một trang web muốn mở ứng dụng này.",
        )
    if "en" in lang:
        BTN_OPEN_PICK_AN_APP = (
            By.XPATH,
            '//Button[@Name="Open Pick an application"]',
        )
    else:
        BTN_OPEN_PICK_AN_APP = (
            By.XPATH,
            '//Button[@Name="Mở Pick an app"]',
        )
    if "en" in lang:
        BTN_CANCEL = (
            By.XPATH,
            '//Button[@Name="Cancel"]',
        )
    else:
        BTN_CANCEL = (
            By.XPATH,
            '//Button[@Name="Hủy"]',
        )

    # Interaction methods
    def open_ftp_link(self, url: str = "ftp://browser3v.dev.itim.vn/corom/") -> None:
        self.make_search_value(search_str=url, is_press_enter=True)

    def verify_ui_ftp(self) -> None:
        """Verify popup appears"""
        self.open_ftp_link()
        assert self.is_element_appeared(self.TEXT_DES)
        assert self.is_element_appeared(self.BTN_CANCEL)


class ReportIssue(BaseAppium):
    # Locators
    if "en" in lang:
        REPORT_ISSUE_DIALOG = (
            By.XPATH,
            '//Window[@ClassName="Chrome_WidgetWin_1"][@Name="Report an issue"]/Document[@ClassName="Chrome_RenderWidgetHostHWND"][@Name="Feedback"]',
        )
    else:
        REPORT_ISSUE_DIALOG = (
            By.XPATH,
            '//Window[@ClassName="Chrome_WidgetWin_1"][@Name="Báo cáo sự cố"]/Document[@ClassName="Chrome_RenderWidgetHostHWND"][@Name="Phản hồi"]',
        )
    # Interaction methods

    def check_report_issue_appeared(self) -> None:
        assert self.is_element_appeared(self.REPORT_ISSUE_DIALOG)

    @staticmethod
    def check_report_issue_appeared_by_pywinauto() -> None:
        assert open_browser.is_coccoc_window_appeared(
            title=CocCocTitles.REPORT_ISSUE, control_type=50032
        )


class Adblock(BaseAppium):
    # Locators
    if "en" in lang:
        ADBLOCK_POP_UP = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Adblock"]',
        )
    else:
        ADBLOCK_POP_UP = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chặn quảng cáo"]',
        )
    if "en" in lang:
        TITLE_BAR = (By.XPATH, '//Pane/TitleBar[@Name="Adblock"]')
    else:
        TITLE_BAR = (By.XPATH, '//Pane/TitleBar[@Name="Chặn quảng cáo"]')

    if "en" in lang:
        ADBLOCK_MODE_STANDARD = (By.XPATH, '//Pane/Text[@Name="Standard mode"]')
    else:
        ADBLOCK_MODE_STANDARD = (By.XPATH, '//Pane/Text[@Name="Tiêu chuẩn"]')

    if "en" in lang:
        ADBLOCK_MODE_STRICT = (By.XPATH, '//Pane/Text[@Name="Strict mode"]')
    else:
        ADBLOCK_MODE_STRICT = (By.XPATH, '//Pane/Text[@Name="Nâng cao"]')

    SETTINGS_BTN = (By.XPATH, '//Pane/Button[@Name="SettingButton"]')
    WEBSITE_FAVICON = (By.XPATH, '//Pane/Button[@Name="WebsiteSettingFavicon"]')
    if "en" in lang:
        BLOCK_ADS_ON_THIS_SITE_LABEL = (
            By.XPATH,
            '//Pane/Text[@Name="Block ads on this site"]',
        )
    else:
        BLOCK_ADS_ON_THIS_SITE_LABEL = (
            By.XPATH,
            '//Pane/Text[@Name="Chặn quảng cáo trên trang này"]',
        )

    if "en" in lang:
        TOGGLE_DESCRIPTION = (
            By.XPATH,
            '//Pane/Text[@Name="Try pausing this feature if the site looks broken"]',
        )
    else:
        TOGGLE_DESCRIPTION = (
            By.XPATH,
            '//Pane/Text[@Name="Hãy thử tạm dừng tính năng nếu giao diện của trang bị vỡ"]',
        )
    WEBSITE_SETTING_TOGGLE_BTN = (
        By.XPATH,
        '//Pane//Button[@Name="WebsiteSettingToggleButton"]',
    )

    if "en" in lang:
        ITEMS_BLOCK_ON_THIS_PAGE = (
            By.XPATH,
            '//Pane/Text[@Name="on this page"]',
        )
    else:
        ITEMS_BLOCK_ON_THIS_PAGE = (
            By.XPATH,
            '//Pane/Text[@Name="trên trang này"]',
        )
    if "en" in lang:
        ITEMS_BLOCK_IN_TOTAL = (
            By.XPATH,
            '//Pane/Text[@Name="in total"]',
        )
    else:
        ITEMS_BLOCK_IN_TOTAL = (
            By.XPATH,
            '//Pane/Text[@Name="Tổng số"]',
        )

    if "en" in lang:
        POWERED_BY_ADBLOCK = (
            By.XPATH,
            '//Pane/Text[@Name="Powered by AdblockPlus"]',
        )
    else:
        POWERED_BY_ADBLOCK = (
            By.XPATH,
            '//Pane/Text[@Name="Cung cấp bởi AdblockPlus"]',
        )

    if "en" in lang:
        DISABLE_ON_THIS_SITE = (
            By.XPATH,
            '//Pane/Text[@Name="Disabled on this site"]',
        )
    else:
        DISABLE_ON_THIS_SITE = (
            By.XPATH,
            '//Pane/Text[@Name="Đã tắt trên trang này"]',
        )
    if "en" in lang:
        REFRESH_TO_APPLY_THE_CHANGE = (
            By.XPATH,
            '//Pane/Text[@Name="Click Refresh page to apply the changes"]',
        )
    else:
        REFRESH_TO_APPLY_THE_CHANGE = (
            By.XPATH,
            '//Pane/Text[@Name="Nhấn Làm mới để thay đổi có hiệu lực"]',
        )
    if "en" in lang:
        REFRESH_PAGE_BTN = (
            By.XPATH,
            '//Pane/Button[@Name="Refresh page"]',
        )
    else:
        REFRESH_PAGE_BTN = (
            By.XPATH,
            '//Pane/Button[@Name="Làm mới"]',
        )

    # Interaction methods

    def verify_adblock_popup_ui(self) -> None:
        assert self.is_element_appeared(self.ADBLOCK_POP_UP)
        assert self.is_element_appeared(self.TITLE_BAR)
        assert self.is_element_appeared(self.SETTINGS_BTN)
        assert self.is_element_appeared(self.WEBSITE_FAVICON)
        assert self.is_element_appeared(self.WEBSITE_SETTING_TOGGLE_BTN)
        assert self.is_element_appeared(self.BLOCK_ADS_ON_THIS_SITE_LABEL)
        assert self.is_element_appeared(self.TOGGLE_DESCRIPTION)
        assert self.is_element_appeared(self.ITEMS_BLOCK_ON_THIS_PAGE)
        assert self.is_element_appeared(self.ITEMS_BLOCK_IN_TOTAL)
        # assert self.is_element_appeared(self.POWERED_BY_ADBLOCK) # remove since new UI https://coccoc.atlassian.net/browse/BR-3770

    def click_btn_settings(self) -> None:
        self.double_click_element(self.SETTINGS_BTN)

    def get_adblock_toggle_state_of_current_site(self) -> str:
        """Return the value of toggle state
        Returns:
            str: '1' is ON, '0' is OFF
        """
        return self.get_element_attribute_by_its_name_and_locator(
            self.WEBSITE_SETTING_TOGGLE_BTN, "Toggle.ToggleState"
        )

    def toggle_off_for_this_site(self) -> None:
        if self.get_adblock_toggle_state_of_current_site() == "1":
            # self.click_element(self.WEBSITE_SETTING_TOGGLE_BTN) # This do not work, dont know why, workaround below
            self.move_to_element(self.WEBSITE_SETTING_TOGGLE_BTN)
            self.click_and_hold(self.WEBSITE_SETTING_TOGGLE_BTN)
            self.release_element(self.WEBSITE_SETTING_TOGGLE_BTN)
            # update since https://coccoc.atlassian.net/browse/BR-3770
            # assert self.get_adblock_toggle_state_of_current_site() == "0"
            # assert self.is_element_appeared(self.DISABLE_ON_THIS_SITE)
            # assert self.is_element_appeared(self.REFRESH_TO_APPLY_THE_CHANGE)
            # assert self.is_element_appeared(self.REFRESH_PAGE_BTN)

    def toggle_on_for_this_site(self) -> None:
        if self.get_adblock_toggle_state_of_current_site() == "0":
            self.click_element(self.WEBSITE_SETTING_TOGGLE_BTN)
            # update since https://coccoc.atlassian.net/browse/BR-3770
            # assert self.get_adblock_toggle_state_of_current_site() == "1"
            # assert self.is_element_appeared(self.REFRESH_TO_APPLY_THE_CHANGE)
            # assert self.is_element_appeared(self.REFRESH_PAGE_BTN)

    @staticmethod
    def verify_adblock_setting_page_opening() -> None:
        assert open_browser.is_coccoc_window_appeared(
            title=CocCocSettingTitle.SETTINGS_ADBLOCK_TITLE
        )


class AdblockOnboarding(BaseAppium):
    # Locators
    if "en" in lang:
        LOGO = (By.XPATH, '//Pane/Image[@Name="Cốc Cốc tip"]')
    else:
        LOGO = (By.XPATH, '//Pane/Image[@Name="Mẹo khi dùng Cốc Cốc"]')
    if "en" in lang:
        TEXT = (By.XPATH, '//Pane/Text[@Name="Adblock"]')
    else:
        TEXT = (By.XPATH, '//Pane/Text[@Name="Chặn quảng cáo"]')
    if "en" in lang:
        POP_UP = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][starts-with(@Name,"Adblock. Cốc Cốc has just blocked")]/Pane/Pane/Pane/Pane',
        )
    else:
        POP_UP = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][starts-with(@Name,"Chặn quảng cáo. Cốc Cốc vừa chặn")]/Pane/Pane/Pane/Pane',
        )
    if "en" in lang:
        BTN_CLOSE = (By.XPATH, '//Pane/Button[@Name="Close help bubble"]')
    else:
        BTN_CLOSE = (By.XPATH, '//Pane/Button[@Name="Đóng bong bóng trợ giúp"]')
    if "en" in lang:
        BTN_UNDERSTAND = (By.XPATH, '//Pane/Button[@Name="I understand"]')
    else:
        BTN_UNDERSTAND = (By.XPATH, '//Pane/Button[@Name="Tôi đã hiểu"]')

    if "en" in lang:
        VIDEOS_DES = (
            By.XPATH,
            '//Text[contains(@Name,"ads on this page so that you can watch videos without annoying ads.")]',
        )
    else:
        VIDEOS_DES = (
            By.XPATH,
            '//Text[contains(@Name,"quảng cáo trên trang này để bạn xem video không bị quảng cáo làm phiền.")]',
        )

    if "en" in lang:
        COMICS_DES = (
            By.XPATH,
            '//Text[contains(@Name,"ads on this page so that you can read comics without annoying ads.")]',
        )
    else:
        COMICS_DES = (
            By.XPATH,
            '//Text[contains(@Name,"quảng cáo trên trang này để bạn đọc truyện không bị quảng cáo làm phiền.")]',
        )
    # Interaction methods

    def verify_ui(self) -> None:
        assert self.is_element_appeared(self.POP_UP, timeout=30)
        assert self.is_element_appeared(self.LOGO)
        assert self.is_element_appeared(self.TEXT)
        assert self.is_element_appeared(self.BTN_CLOSE)
        assert self.is_element_appeared(self.BTN_UNDERSTAND)

    def click_btn_i_understand(self) -> None:
        self.click_element(self.BTN_UNDERSTAND)

    def wait_for_onboarding_displays(self) -> bool:
        if self.is_element_appeared(self.POP_UP, timeout=30):
            return True
        else:
            return False

    def verify_no_onboarding_shown(self) -> None:
        assert self.is_element_disappeared(self.POP_UP, timeout=10)

    def verify_video_ui(self) -> None:
        assert self.is_element_appeared(self.POP_UP, timeout=30)
        assert self.is_element_appeared(self.LOGO)
        assert self.is_element_appeared(self.TEXT)
        assert self.is_element_appeared(self.VIDEOS_DES)
        assert self.is_element_appeared(self.BTN_CLOSE)
        assert self.is_element_appeared(self.BTN_UNDERSTAND)

    def verify_comics_ui(self) -> None:
        assert self.is_element_appeared(self.POP_UP, timeout=30)
        assert self.is_element_appeared(self.LOGO)
        assert self.is_element_appeared(self.TEXT)
        assert self.is_element_appeared(self.COMICS_DES)
        assert self.is_element_appeared(self.BTN_CLOSE)
        assert self.is_element_appeared(self.BTN_UNDERSTAND)


class SafeBrowsingTooltip(Toolbar):
    # Locators
    if "en" in lang:
        WARNING = (By.NAME, "Warning")
    else:
        WARNING = (By.NAME, "Cảnh báo")
    if "en" in lang:
        WEBSITE_IS_VERIFIED = (By.NAME, "Website is verified")
    else:
        WEBSITE_IS_VERIFIED = (By.NAME, "Trang web đã được xác thực")
    WEBSITE_IS_VERIFIED2 = (By.XPATH, '//Text[@Name="Website is verified"]')
    if "en" in lang:
        VERIFIED_SITE_TEXT_DES = (
            By.NAME,
            "This link is verified as the official website of this company or brand.",
        )
    else:
        VERIFIED_SITE_TEXT_DES = (
            By.NAME,
            "Đường dẫn đã được xác minh là trang web chính thức của công ty hoặc thương hiệu này.",
        )
    # if "en" in lang:
    #     BTN_CONNECTION_IS_SECURED = (
    #         By.XPATH,
    #         '//Button[@Name="Connection is secure "]',
    #     )
    # else:
    #     BTN_CONNECTION_IS_SECURED = (By.XPATH, '//Button[@Name="Kết nối này an toàn "]')

    if "en" in lang:
        BTN_CONNECTION_IS_SECURED = (
            By.NAME,
            "Connection is secure ",
        )
    else:
        BTN_CONNECTION_IS_SECURED = (By.NAME, "Kết nối này an toàn ")

    if "en" in lang:
        BTN_COOKIES_AND_SITE_DATA = (
            By.XPATH,
            '//Button[@Name="Cookies and site data "]',
        )
    else:
        BTN_COOKIES_AND_SITE_DATA = (
            By.XPATH,
            '//Button[@Name="Cookie và dữ liệu trang web "]',
        )
    if "en" in lang:
        BTN_SITE_SETTINGS = (
            By.XPATH,
            '//Button[@Name="Site settings "]',
        )
    else:
        BTN_SITE_SETTINGS = (
            By.XPATH,
            '//Button[@Name="Cài đặt trang web "]',
        )
    if "en" in lang:
        SECURITY_TITLE = (By.NAME, "Security")
    else:
        SECURITY_TITLE = (By.NAME, "Bảo mật")

    if "en" in lang:
        CONNECTION_IS_SECURE = (By.NAME, "Connection is secure")
    else:
        CONNECTION_IS_SECURE = (By.NAME, "Kết nối này an toàn")

    # if "en" in lang:
    #     CONNECTION_SECURE_DES = (
    #         By.NAME,
    #         "Your information (for example, passwords or credit card numbers) is private when it is sent to this site.",
    #     )
    # else:
    #     CONNECTION_SECURE_DES = (
    #         By.NAME,
    #         "Thông tin của bạn (ví dụ: mật khẩu hoặc số thẻ tín dụng) sẽ được bảo mật khi được gửi tới trang web",
    #     )

    if "en" in lang:
        CONNECTION_SECURE_DES = (
            By.XPATH,
            '//Pane/Text[starts-with(@Name,"Your information (for example, passwords or credit card numbers)")]/Text[@Name="Your information (for example, passwords or credit"]',
        )
    else:
        CONNECTION_SECURE_DES = (
            By.XPATH,
            '//Pane/Text[starts-with(@Name,"Thông tin của bạn (ví dụ: mật khẩu hoặc số thẻ tín dụng) sẽ được")]/Text[@Name="Thông tin của bạn (ví dụ: mật khẩu hoặc số thẻ tín"]',
        )
    if "en" in lang:
        BTN_LEARN_MORE = (By.NAME, "Learn more")
    else:
        BTN_LEARN_MORE = (By.NAME, "Tìm hiểu thêm")

    if "en" in lang:
        BTN_CERTIFICATE_IS_VALID = (By.NAME, "Certificate is valid ")
    else:
        BTN_CERTIFICATE_IS_VALID = (By.NAME, "Chứng chỉ hợp lệ ")

    if "en" in lang:
        WARNING_BTN_GOT_IT = (By.NAME, "Got it")
    else:
        WARNING_BTN_GOT_IT = (By.NAME, "Tôi đã hiểu")

    if "en" in lang:
        WARNING_BTN_CLOSE_TAB = (By.NAME, "Close tab")
    else:
        WARNING_BTN_CLOSE_TAB = (By.NAME, "Đóng thẻ")

    if "en" in lang:
        WARNING_TITLE = (By.NAME, "Website is dangerous or suspicious")
    else:
        WARNING_TITLE = (By.NAME, "Trang web nguy hiểm hoặc đáng ngờ")

    if "en" in lang:
        WARNING_DES = (
            By.NAME,
            "This website may contain unsafe content (for example, malware, scams, fake news, or disturbing content). You should not continue using this site.",
        )
    else:
        WARNING_DES = (
            By.NAME,
            "Trang web này có thể chứa nội dung không an toàn (ví dụ: phần mềm độc hại, yếu tố lừa đảo, tin tức giả mạo, hoặc nội dung phản cảm). Bạn không nên tiếp tục sử dụng trang này.",
        )
    if "en" in lang:
        BTN_CLOSE_POPUP = (By.XPATH, '//Pane/Button[@Name="Close"]')
    else:
        BTN_CLOSE_POPUP = (By.XPATH, '//Pane/Button[@Name="Đóng"]')

    if "en" in lang:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE = (
            By.NAME,
            "Your connection to this site is not secure",
        )
    else:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE = (
            By.NAME,
            "Kết nối của bạn tới trang web này không an toàn",
        )
    if "en" in lang:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES1 = (
            By.NAME,
            "You should not enter any sensitive information on",
        )
    else:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES1 = (
            By.NAME,
            "Bạn không nên nhập bất kỳ thông tin nhạy cảm",
        )
    if "en" in lang:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES2 = (
            By.NAME,
            "this site (for example, passwords or credit cards),",
        )
    else:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES2 = (
            By.NAME,
            "nào trên trang web này (ví dụ: mật khẩu hoặc thẻ",
        )

    if "en" in lang:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES3 = (
            By.NAME,
            "because it could be stolen by attackers. ",
        )
    else:
        YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES3 = (
            By.NAME,
            "tín dụng), vì những kẻ tấn công có thể đánh cắp",
        )

    YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES4 = (By.NAME, "thông tin đó. ")
    WARNING_BTN_LEARN = (By.NAME, "Learn")
    WARNING_BTN_MORE = (By.NAME, "more")
    WARNING_BTN_TIM_HIEU_THEM = (By.NAME, "Tìm hiểu thêm")

    if "en" in lang:
        NOT_SECURE_TITLE = (By.NAME, "Your connection to this site is not secure")
    else:
        NOT_SECURE_TITLE = (By.NAME, "Kết nối của bạn tới trang web này không an toàn")
    # Interaction Methods

    def click_X_btn_to_close_popup(self) -> None:
        self.click_element(self.BTN_CLOSE_POPUP)

    def click_warning(self) -> None:
        self.click_element(self.WARNING)

    def verify_secure_page_ui(self) -> None:
        self.click_view_site_infomation()
        assert self.is_element_appeared(self.WEBSITE_IS_VERIFIED)
        assert self.is_element_appeared(self.BTN_CONNECTION_IS_SECURED)
        assert self.is_element_appeared(self.VERIFIED_SITE_TEXT_DES)
        assert self.is_element_appeared(self.BTN_COOKIES_AND_SITE_DATA)
        assert self.is_element_appeared(self.BTN_SITE_SETTINGS)

    def verify_popup_unsecure_page_ui(self) -> None:
        self.click_view_site_infomation()
        assert self.is_element_appeared(self.NOT_SECURE_TITLE)
        if "en" in lang:
            assert self.is_element_appeared(self.WARNING_BTN_LEARN)
            assert self.is_element_appeared(self.WARNING_BTN_MORE)
        else:
            assert self.is_element_appeared(self.WARNING_BTN_TIM_HIEU_THEM)

        # self.double_click_element(self.WARNING_BTN_LEARN)
        assert self.is_element_appeared(
            self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES1
        )
        assert self.is_element_appeared(
            self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES2
        )
        assert self.is_element_appeared(
            self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES3
        )
        if "vi" in lang:
            assert self.is_element_appeared(
                self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES4
            )

        assert self.is_element_appeared(self.BTN_COOKIES_AND_SITE_DATA)
        assert self.is_element_appeared(self.BTN_SITE_SETTINGS)

    def click_btn_connection_is_secure(self) -> None:
        self.move_to_element(self.BTN_CONNECTION_IS_SECURED)
        sleep(3)
        self.right_click_element(self.BTN_CONNECTION_IS_SECURED)

    def verify_connection_is_secure_ui(self) -> None:
        assert self.is_element_appeared(self.SECURITY_TITLE)
        assert self.is_element_appeared(self.CONNECTION_IS_SECURE)
        assert self.is_element_appeared(self.CONNECTION_SECURE_DES)
        assert self.is_element_appeared(self.BTN_LEARN_MORE)
        assert self.is_element_appeared(self.BTN_CERTIFICATE_IS_VALID)

    def verify_popup_unsecure_and_unsafe_page_ui(self) -> None:
        assert self.is_element_appeared(self.WARNING)
        assert self.is_element_appeared(self.WARNING_TITLE)
        assert self.is_element_appeared(self.WARNING_DES)
        assert self.is_element_appeared(self.WARNING_BTN_GOT_IT)
        assert self.is_element_appeared(self.WARNING_BTN_CLOSE_TAB)

    def verify_no_popup_and_warning_text_of_unsecure_and_unsafe_show(self) -> None:
        assert self.is_element_disappeared(self.WARNING)
        assert self.is_element_disappeared(self.WARNING_TITLE)
        assert self.is_element_disappeared(self.WARNING_DES)
        assert self.is_element_disappeared(self.WARNING_BTN_GOT_IT)
        assert self.is_element_disappeared(self.WARNING_BTN_CLOSE_TAB)

    def verify_popup_warning_hidden(self) -> None:
        assert self.is_element_disappeared(self.WARNING_TITLE)
        assert self.is_element_disappeared(self.WARNING_DES)
        assert self.is_element_disappeared(self.WARNING_BTN_GOT_IT)
        assert self.is_element_disappeared(self.WARNING_BTN_CLOSE_TAB)

    def verify_unsecure_and_unsafe_page_ui_after_click_warning(self) -> None:
        assert self.is_element_appeared(self.WARNING)
        assert self.is_element_appeared(self.WARNING_TITLE)
        assert self.is_element_appeared(self.WARNING_DES)
        assert self.is_element_appeared(self.BTN_COOKIES_AND_SITE_DATA)
        assert self.is_element_appeared(self.BTN_SITE_SETTINGS)
        assert self.is_element_appeared(self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE)
        if "en" in lang:
            assert self.is_element_appeared(self.WARNING_BTN_LEARN)
            assert self.is_element_appeared(self.WARNING_BTN_MORE)
        else:
            assert self.is_element_appeared(self.WARNING_BTN_TIM_HIEU_THEM)

        # self.double_click_element(self.WARNING_BTN_LEARN)
        assert self.is_element_appeared(
            self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES1
        )
        assert self.is_element_appeared(
            self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES2
        )
        assert self.is_element_appeared(
            self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES3
        )
        if "vi" in lang:
            assert self.is_element_appeared(
                self.YOUR_CONNECTION_TO_THIS_SITE_IS_NOT_SECURE_DES4
            )

    def click_btn_warning_learn_more(self) -> None:
        if "en" in lang:
            self.click_element(self.WARNING_BTN_LEARN)
        else:
            self.click_element(self.WARNING_BTN_TIM_HIEU_THEM)

    def click_btn_got_it(self) -> None:
        self.click_element(self.WARNING_BTN_GOT_IT)

    def click_btn_close_tab(self) -> None:
        self.click_element(self.WARNING_BTN_CLOSE_TAB)
