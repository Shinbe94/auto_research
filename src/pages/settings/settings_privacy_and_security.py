from time import sleep
from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright, BaseSelenium

from src.pages.constant import LocatorJSPath
from tests import setting

lang = setting.coccoc_language


class SettingsPrivacyAndSecuritySel(BaseSelenium):
    # Locators:
    BTN_CHECKNOW = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckParentButton")'
    DES_TEXT = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckParent div.flex.cr-padded-text")'
    BTN_RERUN_CHECK = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckParent > cr-icon-button")'

    UPDATE_LABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-updates-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#label")'
    UPDATE_SUBLABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-updates-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#subLabel")'

    PASSWORD_MANAGER_LABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-passwords-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#label")'
    PASSWORD_MANAGER_SUBLABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-passwords-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#subLabel")'

    SAFE_BROWSING_LABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-safe-browsing-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#label")'
    SAFE_BROWSING_SUBLABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-safe-browsing-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#subLabel")'

    EXTENSIONS_LABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-extensions-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#label")'
    EXTENSIONS_SUBLABEL = f'{LocatorJSPath.SETTINGS_SAFETY_CHECK}.shadowRoot.querySelector("#safetyCheckCollapse > settings-safety-check-extensions-child").shadowRoot.querySelector("#safetyCheckChild").shadowRoot.querySelector("#subLabel")'

    AGE_VERIFICATION_LABEL = f'{LocatorJSPath.SETTINGS_PRIVACY_PAGE}.shadowRoot.querySelector("#labelWrapper > div")'
    AGE_VERIFICATION_SUBLABEL = (
        f'{LocatorJSPath.SETTINGS_PRIVACY_PAGE}.shadowRoot.querySelector("#subLabel")'
    )
    AGE_VERIFICATION_DROPDOWN = f"{LocatorJSPath.SETTINGS_PRIVACY_PAGE_AGE_DROPDOWN}"
    DROPDOWN_BLANK = f"{LocatorJSPath.SETTINGS_PRIVACY_PAGE_AGE_DROPDOWN}.querySelector(\"option[value='0']\")"
    DROPDOWN_IM_UNDER_18 = f"{LocatorJSPath.SETTINGS_PRIVACY_PAGE_AGE_DROPDOWN}.querySelector(\"option[value='1']\")"
    DROPDOWN_IM_18_OR_OLDER = f"{LocatorJSPath.SETTINGS_PRIVACY_PAGE_AGE_DROPDOWN}.querySelector(\"option[value='2']\")"
    LOCATION_RATIO_ICON_DISABLE = f'{LocatorJSPath.SETTINGS_PRIVACY_PAGE_LOCATION_RAIO}.shadowRoot.querySelector("#disabledRadioOption").shadowRoot.querySelector("#buttonIcon").shadowRoot.querySelector("svg")'
    LOCATION_RATIO_ICON_ENABLE = f'{LocatorJSPath.SETTINGS_PRIVACY_PAGE_LOCATION_RAIO}.shadowRoot.querySelector("#enabledRadioOption").shadowRoot.querySelector("#buttonIcon").shadowRoot.querySelector("svg")'

    # Interaction methods
    def open_privacy_security_page(self):
        self.open_page(url="coccoc://settings/privacy")

    def open_safety_check(self):
        self.open_page(url="coccoc://settings/safetyCheck")

    def click_btn_checknow(self):
        self.open_safety_check()
        self.click_shadow_element(self.BTN_CHECKNOW)

    def verify_after_checknow(self):
        if "en" in lang:
            assert self.wait_for_text_is_present_shadow_element(
                self.DES_TEXT, text="Safety check ran a moment ago"
            )
            assert self.wait_for_text_is_present_shadow_element(
                self.UPDATE_LABEL, text="Updates"
            )
            assert self.wait_for_text_is_present_shadow_element(
                self.UPDATE_SUBLABEL, text="Cốc Cốc is up to date."
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.PASSWORD_MANAGER_LABEL, text="Password Manager"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.PASSWORD_MANAGER_SUBLABEL, text="weak passwords"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.SAFE_BROWSING_LABEL, text="Safe Browsing"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.SAFE_BROWSING_SUBLABEL,
                text="Standard protection is on. For even more security, use enhanced protection.",
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.EXTENSIONS_LABEL, text="Extensions"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.EXTENSIONS_SUBLABEL,
                text="You're protected from potentially harmful extensions",
            )
        else:
            assert self.wait_for_text_is_present_shadow_element(
                self.DES_TEXT,
                text="Tính năng kiểm tra an toàn đã hoạt động vài phút trước",
            )
            assert self.wait_for_text_is_present_shadow_element(
                self.UPDATE_LABEL, text="Bản cập nhật"
            )
            assert self.wait_for_text_is_present_shadow_element(
                self.UPDATE_SUBLABEL, text="Cốc Cốc đã được cập nhật."
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.PASSWORD_MANAGER_LABEL, text="Trình quản lý mật khẩu"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.PASSWORD_MANAGER_SUBLABEL, text="mật khẩu yếu"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.SAFE_BROWSING_LABEL, text="Duyệt web an toàn"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.SAFE_BROWSING_SUBLABEL,
                text="Tính năng Bảo vệ thông thường đang bật. Để tăng cường khả năng bảo mật, hãy sử dụng chế độ bảo vệ nâng cao.",
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.EXTENSIONS_LABEL, text="Tiện ích mở rộng"
            )

            assert self.wait_for_text_is_present_shadow_element(
                self.EXTENSIONS_SUBLABEL,
                text="Đã tắt 1 tiện ích có thể gây hại. Bạn cũng có thể xóa tiện ích này.",
            )

    def get_age_verification_value(self, is_need_open_privacy_security=True) -> str:
        if is_need_open_privacy_security:
            self.open_privacy_security_page()
        return self.get_attribute_value_of_shadow_element(
            self.AGE_VERIFICATION_DROPDOWN, "value"
        )

    def verify_ui_age_confirmation(self, is_need_open_privacy_security=True) -> None:
        if is_need_open_privacy_security:
            self.open_privacy_security_page()
        if "en" in lang:
            assert (
                self.get_text_shadow_element(self.AGE_VERIFICATION_LABEL)
                == "Age verification"
            )
            assert (
                self.get_text_shadow_element(self.AGE_VERIFICATION_SUBLABEL)
                == "We need to verify your age to show appropriate content"
            )
            assert self.get_text_shadow_element(self.DROPDOWN_BLANK) == ""
            assert (
                self.get_text_shadow_element(self.DROPDOWN_IM_UNDER_18)
                == "I'm under 18"
            )
            assert (
                self.get_text_shadow_element(self.DROPDOWN_IM_18_OR_OLDER)
                == "I'm 18 or older"
            )
        else:
            assert (
                self.get_text_shadow_element(self.AGE_VERIFICATION_LABEL)
                == "Xác nhận tuổi"
            )
            assert (
                self.get_text_shadow_element(self.AGE_VERIFICATION_SUBLABEL)
                == "Chúng tôi cần xác nhận tuổi của bạn nhằm mục đích hiển thị các nội dung phù hợp"
            )
            assert self.get_text_shadow_element(self.DROPDOWN_BLANK) == ""
            assert (
                self.get_text_shadow_element(self.DROPDOWN_IM_UNDER_18)
                == "Tôi dưới 18 tuổi"
            )
            assert (
                self.get_text_shadow_element(self.DROPDOWN_IM_18_OR_OLDER)
                == "Tôi 18 tuổi trở lên"
            )

    def verify_default_value_of_age_confirmation(self) -> None:
        assert self.get_age_verification_value() == "0"

    def select_default_option_age_confirmation(self) -> None:
        if self.get_age_verification_value() != "0":
            self.click_shadow_element(self.AGE_VERIFICATION_DROPDOWN)
            self.click_shadow_element(self.DROPDOWN_BLANK)
            assert self.get_age_verification_value() == "0"

    def select_im_under_18_option_age_confirmation(self) -> None:
        if self.get_age_verification_value() != "1":
            self.click_shadow_element(self.AGE_VERIFICATION_DROPDOWN)
            self.click_shadow_element(self.DROPDOWN_IM_UNDER_18)
            assert self.get_age_verification_value() == "1"

    def select_im_18_or_older_option_age_confirmation(self) -> None:
        if self.get_age_verification_value() != "2":
            self.click_shadow_element(self.AGE_VERIFICATION_DROPDOWN)
            self.click_shadow_element(self.DROPDOWN_IM_18_OR_OLDER)
            assert self.get_age_verification_value() == "2"

    def verify_location_icon_appeared(self) -> None:
        self.open_page("coccoc://settings/content/location")
        assert self.is_shadow_element_appeared(self.LOCATION_RATIO_ICON_DISABLE)
        assert self.is_shadow_element_appeared(self.LOCATION_RATIO_ICON_ENABLE)


class SettingsPrivacyAndSecurityPlay(BasePlaywright):
    # Locators:
    @property
    def age_verify(self) -> Locator:
        return self.page.locator("#ageVerify")

    @property
    def dropdown_blank(self) -> Locator:
        return self.page.locator("#dropdownMenu option[value='0']")

    @property
    def dropdown_im_under_18(self) -> Locator:
        return self.page.locator("#dropdownMenu option[value='1']")

    @property
    def dropdown_im_18_or_older(self) -> Locator:
        return self.page.locator("#dropdownMenu option[value='2']")

    # Interaction methods
    def open_privacy_security_page(self):
        self.open_page(url="coccoc://settings/privacy")

    def open_safety_check(self):
        self.open_page(url="coccoc://settings/safetyCheck")

    def click_age_verify_dropdown(self):
        self.age_verify.click()

    def select_im_18_or_older_option_age_confirmation(self) -> None:
        self.open_privacy_security_page()
        self.click_age_verify_dropdown()
        # self.dropdown_im_18_or_older.click()
        self.page.select_option("select#dropdownMenu", "2")
