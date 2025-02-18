from enum import Enum
from tests import setting

lang = setting.coccoc_language


class ToggleStatus:
    # def __str__(self) -> str:
    #     return self.value

    ON = "ON"
    OFF = "OFF"


class CocCocTitles:
    NEW_TAB_TITLE_VI = "Thẻ mới - Cốc Cốc"
    NEW_TAB_TITLE_EN = "New Tab - Cốc Cốc"
    if "en" in lang:
        NEW_TAB = "New Tab"
    else:
        NEW_TAB = "Thẻ mới"
    if "en" in lang:
        NEW_TAB_TITLE = "New Tab - Cốc Cốc"
    else:
        NEW_TAB_TITLE = "Thẻ mới - Cốc Cốc"
    if "en" in lang:
        CLOCK_ERROR = r"Clock error - Network error - Cốc Cốc"
    else:
        CLOCK_ERROR = r"Lỗi đồng hồ - Lỗi mạng - Cốc Cốc"
    if "en" in lang:
        ADDRESS_BAR = r"Address and search bar"
    else:
        ADDRESS_BAR = r"Thanh địa chỉ và tìm kiếm"

    COCCOC_HISTOGRAMS_TITLE = r"Histograms - Cốc Cốc"

    if "en" in lang:
        WELCOME_PAGE_TITLE = "Welcome to Cốc Cốc browser - Cốc Cốc"
    else:
        WELCOME_PAGE_TITLE = "Chào mừng bạn đến với trình duyệt Cốc Cốc - Cốc Cốc"
    if "en" in lang:
        DEFAULT_TOR_WINDOW_TITLE: str = "New Incognito Tab - Cốc Cốc (Incognito)"
    else:
        DEFAULT_TOR_WINDOW_TITLE: str = "Thẻ ẩn danh mới - Cốc Cốc (Ẩn danh)"

    if "en" in lang:
        VERSION_PAGE_TITLE = r"About Version - Cốc Cốc"
    else:
        VERSION_PAGE_TITLE = r"Giới thiệu Phiên bản - Cốc Cốc"
    if "en" in setting.coccoc_language:
        TOR_WINDOW_TITLE = "New Incognito Tab - Cốc Cốc"
    else:
        TOR_WINDOW_TITLE = "Thẻ ẩn danh mới - Cốc Cốc"

    COCCOC_HOMEPAGE_TITLE_INCOGNITO_TOR = "Trình duyệt Cốc Cốc | Trình duyệt web dành cho người Việt - Cốc Cốc (Incognito)"
    COCCOC_HOMEPAGE_TITLE_TOR = (
        "Trình duyệt Cốc Cốc | Trình duyệt web dành cho người Việt - Cốc Cốc"
    )
    if "en" in lang:
        UNTITLED_INCOGNITO_COCCOC = "Untitled - Cốc Cốc (Incognito)"
    else:
        UNTITLED_INCOGNITO_COCCOC = "Untitled - Cốc Cốc (Ẩn danh)"

    if "en" in lang:
        UNTITLED_COCCOC = "Untitled - Cốc Cốc"
    else:
        UNTITLED_COCCOC = "Untitled - Cốc Cốc"

    if "en" in lang:
        ABOUT_BLANK_COCCOC = "about:blank - Cốc Cốc"
    else:
        ABOUT_BLANK_COCCOC = "about:blank - Cốc Cốc"

    if "en" in lang:
        DOWNLOADS_PAGE_TITLE = r"Downloads - Cốc Cốc"
    else:
        DOWNLOADS_PAGE_TITLE = r"Tệp đã tải về - Cốc Cốc"

    if "en" in lang:
        COCCOC_TASK_MANAGER_TITLE = r"Task Manager - Cốc Cốc"
    else:
        COCCOC_TASK_MANAGER_TITLE = r"Trình quản lý tác vụ - Cốc Cốc"

    if "en" in lang:
        REPORT_ISSUE = r"Report an issue"
    else:
        REPORT_ISSUE = r"Báo cáo sự cố"
    EXPERIMENTS_TITLE: str = "Experiments - Cốc Cốc"


class CocCocSettingTitle:
    START_UP_LABEL_VI = r"Khởi động cùng hệ thống"
    START_UP_LABEL_EN = r"Run automatically on system startup"
    SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI = r"Cài đặt - Trình duyệt mặc định - Cốc Cốc"
    SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN = r"Settings - Default browser - Cốc Cốc"
    SETTINGS = "Settings"
    COCCOC_FLAGS = r"Experiments - Cốc Cốc"
    if "en" in lang:
        SETTINGS_TOR_OPTION = r"Settings - Tor options - Cốc Cốc"
    else:
        SETTINGS_TOR_OPTION = r"Cài đặt - Tùy chọn Tor - Cốc Cốc"
    if "en" in lang:
        SETTINGS_COOKIES_AND_OTHER_SITE_DATA = (
            "Settings - Cookies and other site data - Cốc Cốc"
        )
    else:
        SETTINGS_COOKIES_AND_OTHER_SITE_DATA = (
            "Cài đặt - Cookie và các dữ liệu khác của trang web - Cốc Cốc"
        )
    if "en" in lang:
        # SETTINGS_DOWNLOADS_TITLE = r"Settings - Downloads - Cốc Cốc"
        SETTINGS_DOWNLOADS_TITLE = r"Settings - Downloads and torrent - Cốc Cốc"
    else:
        # SETTINGS_DOWNLOADS_TITLE = r"Cài đặt - Tệp đã tải về - Cốc Cốc"
        SETTINGS_DOWNLOADS_TITLE = r"Cài đặt - Tải về và torrent - Cốc Cốc"

    if "en" in lang:
        SETTINGS_DOWNLOADS_PATH_DIALOG_TITLE = r"Location"
    else:
        SETTINGS_DOWNLOADS_PATH_DIALOG_TITLE = r"Vị trí"
    if "en" in lang:
        ABOUT_COCCOC_TITLE = "Settings - About Cốc Cốc - Cốc Cốc"
    else:
        ABOUT_COCCOC_TITLE = "Cài đặt - Giới thiệu về Cốc Cốc - Cốc Cốc"
    if "en" in lang:
        SETTING_COCCOC = "Settings - Cốc Cốc"
    else:
        SETTING_COCCOC = "Cài đặt - Cốc Cốc"

    if "en" in lang:
        DICTIONARY_TITLE = "Dictionary options"
    else:
        DICTIONARY_TITLE = "Tùy chọn từ điển"
    if "en" in lang:
        SETTINGS_ADBLOCK_TITLE = "Settings - Adblock - Cốc Cốc"
    else:
        SETTINGS_ADBLOCK_TITLE = "Cài đặt - Chặn quảng cáo - Cốc Cốc"


class CocCocFolder:
    pass


class CocCocDialog:
    if "en" in lang:
        BTN_EXIT = "Exit"
    else:
        BTN_EXIT = "Thoát"

    if "en" in lang:
        BTN_CONTINUE_DOWNLOADING = "Continue downloading"
    else:
        BTN_CONTINUE_DOWNLOADING = "Tiếp tục tải xuống"


class ChromeTitles:
    NEW_TAB_GOOGLE_CHROME = "New Tab - Google Chrome"


class TestingSiteTittles:
    if "en" in lang:
        BBC_INCOGNITO_COCCOC_WINDOW_TITLE = "BBC - Homepage - Cốc Cốc (Incognito)"
    else:
        BBC_INCOGNITO_COCCOC_WINDOW_TITLE = "BBC - Homepage - Cốc Cốc (Ẩn danh)"

    UNLOADED_BBC_INCOGNITO_COCCOC_WINDOW_TITLE = "bbc.com - Cốc Cốc"

    if "en" in lang:
        BBC_COCCOC_WINDOW_TITLE = "BBC - Homepage - Cốc Cốc"
    else:
        BBC_COCCOC_WINDOW_TITLE = "BBC - Homepage - Cốc Cốc"

    if "en" in lang:
        ONION_SITE_SHARE_DOCUMENT_WINDOW_TITLE = (
            "Share and accept documents securely - Cốc Cốc (Incognito)"
        )
    else:
        ONION_SITE_SHARE_DOCUMENT_WINDOW_TITLE = (
            "Share and accept documents securely - Cốc Cốc (Ẩn danh)"
        )


class AWADL:
    """
    AWADL: stands for Appium Win App Driver Locator
    Support 3 type: automation_id, class_name, and name
    """

    # def __str__(self) -> str:
    #     return self.value

    AUTOMATION_ID = "AUTOMATION_ID"
    CLASS_NAME = "CLASS_NAME"
    NAME = "NAME"


class ChromeType(object):
    GOOGLE = "google-chrome"
    CHROMIUM = "chromium"
    BRAVE = "brave-browser"
    MSEDGE = "edge"
    COCCOC = "CocCoc"


class LocatorJSPath:
    """
    Set the prefix for js_path
    """

    SETTINGS_DOWNLOAD_PRE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#advancedPage settings-section settings-downloads-page")'
    SETTINGS_DEFAULT_BROWSER_PRE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("settings-section[section=\"defaultBrowser\"]").querySelector("settings-default-browser-page")'
    EXTENTIONS_PRE = r'document.querySelector("body extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#'
    EXTENTIONS_DETAIL_PRE = r'document.querySelector("body extensions-manager").shadowRoot.querySelector("#viewManager > extensions-detail-view").shadowRoot'
    EXTENTIONS_ITEM_LIST = r'document.querySelector("body extensions-manager").shadowRoot.querySelector("#items-list")'
    DICT_PRE = r'document.querySelector("html > div.corom-element").shadowRoot'
    UNIT_EX_PRE = r'document.querySelector("html > div.corom-element").shadowRoot'
    SETTINGS_ABOUT_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-about-page")'
    SETTINGS_STARTUP_RATIO = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-on-startup-page").shadowRoot.querySelectorAll("#onStartupRadioGroup controlled-radio-button")'
    SETTINGS_STARTUP_BUTTON_ADD_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-on-startup-page").shadowRoot.querySelector("settings-startup-urls-page").shadowRoot.querySelector("#addPage")'
    SETTINGS_STARTUP_BUTTON_USE_CURRENT_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-on-startup-page").shadowRoot.querySelector("settings-startup-urls-page").shadowRoot.querySelector("#useCurrentPages")'
    SETTINGS_STARTUP_DIALOG = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-on-startup-page").shadowRoot.querySelector("settings-startup-urls-page").shadowRoot.querySelector("settings-startup-url-dialog")'
    SETTINGS_STARTUP_URL_ENTRY_ALL = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-on-startup-page").shadowRoot.querySelector("settings-startup-urls-page").shadowRoot.querySelectorAll("settings-startup-url-entry")'
    SETTINGS_STARTUP_URL_ENTRY = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-on-startup-page").shadowRoot.querySelector("settings-startup-urls-page").shadowRoot.querySelector("settings-startup-url-entry")'
    SETTINGS_STARTUP_URL_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section  settings-on-startup-page").shadowRoot.querySelector("settings-startup-urls-page")'
    SETTINGS_LANGUAGE_TRANSLATE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#advancedPage settings-section settings-translate-page")'
    SETTINGS_APPEAREANCE_TOGGLE_ALL = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-appearance-page").shadowRoot.querySelectorAll("#pages settings-toggle-button")'
    SETTINGS_APPEAREANCE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-appearance-page")'
    SETTINGS_SAFETY_CHECK = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#safetyCheckSettingsSection > settings-safety-check-page")'
    SETTINGS_PRIVACY_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-privacy-page")'
    SETTINGS_PRIVACY_PAGE_AGE_DROPDOWN = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-privacy-page").shadowRoot.querySelector("#ageVerify").shadowRoot.querySelector("#dropdownMenu")'
    SETTINGS_PRIVACY_PAGE_LOCATION_RAIO = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section.expanded settings-privacy-page").shadowRoot.querySelector("#pages settings-subpage.iron-selected settings-category-default-radio-group")'
    SETTINGS_RESET_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#advancedPage settings-section settings-reset-page")'
    SETTINGS_RESET_PAGE_DIALOG = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#advancedPage settings-section  settings-reset-page").shadowRoot.querySelector("#reset-pages settings-reset-profile-dialog")'
    SETTINGS_SYSTEM_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#advancedPage settings-section settings-system-page")'
    SETTINGS_ADSBLOCK_PAGE = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-adblock-page")'
    SETTINGS_ADSBLOCK_SECTION = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section[section=\'adblock\']")'
    SETTINGS_ADSBLOCK_WHITE_LIST = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-section settings-adblock-page").shadowRoot.querySelector("adblock-white-list-list")'


class CocCocText:
    if "en" in lang:
        OPEN_NEWTAB_PAGE = "Open the New Tab page"
    else:
        OPEN_NEWTAB_PAGE = "Mở trang thẻ mới"
    if "en" in lang:
        CONTINUE_WHERE_YOU_LEFT_OFF = "Continue where you left off"
    else:
        CONTINUE_WHERE_YOU_LEFT_OFF = "Tiếp tục từ nơi bạn đã dừng lại"

    if "en" in lang:
        OPEN_SPECIFIC_OR_SET_OF_PAGES = "Open a specific page or set of pages"
    else:
        OPEN_SPECIFIC_OR_SET_OF_PAGES = "Mở một trang cụ thể hoặc tập hợp các trang"
    if "en" in lang:
        WARN_YOU_WHEN_CLOSING_MULTIPLE_TABS = "Warn you when closing multiple tabs"
    else:
        WARN_YOU_WHEN_CLOSING_MULTIPLE_TABS = "Cảnh báo bạn khi đóng nhiều thẻ một lúc"

    if "en" in lang:
        OPEN_CHROME_STORE_TEXT = "Open Chrome Web Store"
    else:
        OPEN_CHROME_STORE_TEXT = "Mở cửa hàng Chrome trực tuyến"
    if "en" in lang:
        HOME_NEWTAB_PAGE = "New Tab page"
    else:
        HOME_NEWTAB_PAGE = "Trang thẻ mới"

    if "en" in lang:
        SHOW_BOOKMARK_BAR = "Show bookmarks bar"
    else:
        SHOW_BOOKMARK_BAR = "Hiển thị thanh dấu trang"

    if "en" in lang:
        SHOW_HOME_BTN = "Show home button"
    else:
        SHOW_HOME_BTN = "Hiển thị nút trang chủ"

    if "en" in lang:
        RUNNING_IN_BG_AFTER_CLOSING = (
            "Continue running background apps when Cốc Cốc is closed"
        )
    else:
        RUNNING_IN_BG_AFTER_CLOSING = (
            "Tiếp tục chạy các ứng dụng dưới nền khi Cốc Cốc bị đóng"
        )
    if "en" in lang:
        TEXT_NEALY_UPDATE = r"Nearly up to date! Relaunch Cốc Cốc to finish updating."
    else:
        TEXT_NEALY_UPDATE = (
            r"Gần được cập nhật! Hãy khởi chạy lại Cốc Cốc để hoàn tất cập nhật."
        )


class TaskManagerText:
    if "en" in lang:
        TASK_MANAGER_TITLE = "Task Manager - Cốc Cốc"
    else:
        TASK_MANAGER_TITLE = "Trình quản lý tác vụ - Cốc Cốc"

    if "en" in lang:
        TASK = "Task"
    else:
        TASK = "Tác vụ"
    if "en" in lang:
        MEMORY_FOOTPRINT = "Memory footprint"
    else:
        MEMORY_FOOTPRINT = "Mức sử dụng bộ nhớ"
    if "en" in lang:
        CPU = "CPU"
    else:
        CPU = "CPU"
    if "en" in lang:
        NETWORK = "Network"
    else:
        NETWORK = "Mạng"
    if "en" in lang:
        PROCESS_ID = "Process ID"
    else:
        PROCESS_ID = "ID Tiến trình"

    if "en" in lang:
        BTN_END_PROCESS = "End process"
    else:
        BTN_END_PROCESS = "Kết thúc quá trình"


# text = AWADL()
# print(text.CLASS_NAME)
