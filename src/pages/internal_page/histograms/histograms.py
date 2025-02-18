import time

from playwright.sync_api import Locator, expect, sync_playwright
from selenium.webdriver.common.by import By

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser
from src.pages.coccoc_common.open_browser import get_executable_path
from src.utilities import string_number_utils, os_utils, file_utils
from tests import setting


class Histograms(BasePlaywright):
    # Locators
    @property
    def metric_locator(self) -> Locator:
        return self.page.locator(
            'div[id="histograms"] span[class="histogram-header-text"]'
        )

    @property
    def sidebar_enabled(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.Enabled"]')

    @property
    def sidebar_show(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.Show"]')

    @property
    def sidebar_setting_open_clicked(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.SidebarSettings.OpenClicks"]'
        )

    @property
    def sidebar_feature_icons_clicked(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.FeatureIcons.Clicked"]')

    @property
    def sidebar_custom_icon_clicked(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.CustomIcons.Clicked"]')

    @property
    def sidebar_paid_icon_clicked(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.PaidIcons.Clicked"]')

    @property
    def sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.CustomIcons.EditIconWithOpenInWebPanelCheckboxChanged"]'
        )

    @property
    def sidebar_custom_icons_fetching_response_code(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.CustomIcons.FetchingResponseCode"]'
        )

    @property
    def sidebar_custom_icons_read_result(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.CustomIcons.ReadResult"]')

    @property
    def sidebar_paid_icons_read_result(self) -> Locator:
        return self.page.locator('div[histogram-name="Sidebar.PaidIcons.ReadResult"]')

    @property
    def sidebar_add_web_panel_autocomplete_matches(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.AddWebPanel.AutocompleteMatches"]'
        )

    @property
    def sidebar_add_web_panel_autocomplete_selected(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.AddWebPanel.AutocompleteSelected"]'
        )

    @property
    def sidebar_custom_icon_decode_image_time(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.CustomIcons.DecodeImageTime"]'
        )

    @property
    def sidebar_custom_icon_fetching_response_code(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.CustomIcons.FetchingResponseCode"]'
        )

    @property
    def sidebar_custom_icon_fetching_time(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Sidebar.CustomIcons.FetchingTime"]'
        )

    @property
    def savior_onboard_shown(self) -> Locator:
        # https://coccoc.atlassian.net/browse/PE-8573
        return self.page.locator('div[histogram-name="Savior.featureOnboadShown"]')

    @property
    def savior_onboard_try_now_click(self) -> Locator:
        # https://coccoc.atlassian.net/browse/PE-8573
        return self.page.locator(
            'div[histogram-name="Savior.featureOnboardingTryNowClick"]'
        )

    @property
    def savior_close_onboard_popup(self) -> Locator:
        # https://coccoc.atlassian.net/browse/PE-8573
        return self.page.locator('div[histogram-name="Savior.featureOnboardingClosed"]')

    @property
    def tor_open_new_tor_window(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Tor.AppMenuModel.OpenNewTorWindow"]'
        )

    @property
    def tor_new_tor_connection_for_this_site(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Tor.AppMenuModel.NewTorConnectionForThisSite"]'
        )

    @property
    def tor_new_tor_window_count(self) -> Locator:
        return self.page.locator('div[histogram-name="Tor.Browser.WindowCount"]')

    @property
    def tor_error_page_retry_with_tor(self) -> Locator:
        return self.page.locator('div[histogram-name="Tor.ErrorPage.RetryWithTor"]')

    @property
    def tor_tab_count(self) -> Locator:
        return self.page.locator('div[histogram-name="Tor.Tab.Count"]')

    @property
    def tor_open_link_with_tor(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Tor.RenderViewContextMenu.OpenLinkWithTor"]'
        )

    @property
    def tor_show_retry_with_tor_button(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="Tor.ErrorPage.ShowRetryWithTorButton"]'
        )

    @property
    def in_product_help_notify_event_ready_state(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="InProductHelp.NotifyEventReadyState.IPH_CocCocScrollToTop"]'
        )

    @property
    def in_product_help_should_trigger_help_ui(self) -> Locator:
        return self.page.locator(
            'div[histogram-name="InProductHelp.ShouldTriggerHelpUI.IPH_CocCocScrollToTop"]'
        )

    @property
    def coccoc_newtab_search_action(self) -> Locator:
        return self.page.locator('div[histogram-name="Coccoc.NewTab.SearchAction"]')

    @property
    def page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocRemoteNTP.PaintTiming.NavigationToFirstContentfulPaint"]'
        )

    @property
    def page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocRemoteNTP.PaintTiming.NavigationToLargestContentfulPaint"]'
        )

    @property
    def page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocRemoteNTP.ParseTiming.NavigationToParseStart"]'
        )

    @property
    def page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocSearch.PaintTiming.NavigationToFirstContentfulPaint"]'
        )

    @property
    def page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocSearch.ParseTiming.NavigationToParseStart"]'
        )

    @property
    def page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocOthers.PaintTiming.NavigationToFirstContentfulPaint"]'
        )

    @property
    def page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="PageLoad.Clients.CocCocOthers.ParseTiming.NavigationToParseStart"]'
        )

    @property
    def coccoc_adblock_metric(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="InProductHelp.ShouldTriggerHelpUI.IPH_CocCocAdBlock"]'
        )

    @property
    def coccoc_safety_tips_unsafe_URLData_domain_size(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="CocCocSafetyTips.UnsafeURLData.DomainSize"]'
        )

    @property
    def coccoc_safety_tips_unsafe_URLData_url_size(
        self,
    ) -> Locator:
        return self.page.locator(
            'div[histogram-name="CocCocSafetyTips.UnsafeURLData.UrlSize"]'
        )

    # ------------------------------------------------------------------------------------------------------------------
    # Interaction methods
    # ------------------------------------------------------------------------------------------------------------------
    def open_histograms_page(self):
        self.page.goto("coccoc://histograms/", timeout=30000)
        time.sleep(1)

    def check_paid_icons_read(self):
        self.page.goto("coccoc://histograms/#Sidebar.PaidIcons.ReadResult")
        expect(self.metric_locator).to_contain_text(
            "Histogram: Sidebar.PaidIcons.ReadResult recorded 1 samples"
        )

    def check_paid_icon_clicked(self, no_of_clicked: int):
        self.page.goto("coccoc://histograms/#Sidebar.PaidIcons.Clicked")
        expect(self.metric_locator).to_contain_text(
            rf"Histogram: Sidebar.PaidIcons.Clicked recorded {str(no_of_clicked)} samples"
        )

    def check_sidebar_activated(self):
        self.page.goto("coccoc://histograms/#Sidebar.Activated")
        expect(self.metric_locator).to_contain_text(
            "Histogram: Sidebar.Activated recorded 1 samples, mean = 1.0 (flags = 0x41)"
        )

    def check_sidebar_enable_metric(self, count: int = 0):
        """
        this is for checking metric Sidebar.Enabled is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_enabled).to_have_count(count)

    def get_total_samples_of_metric_sidebar_enable(self) -> int:
        # text_metric = self.sidebar_enabled.text_content()
        # no_of_sample = string_number_utils.find_text_between_2_string(text_metric, 'recorded ', ' samples')
        # return int(no_of_sample)
        return self.get_no_of_metric_sample(self.sidebar_enabled)

    def get_total_samples_of_metric_sidebar_show(self) -> int:
        return self.get_no_of_metric_sample(self.sidebar_show)

    def check_sidebar_metric_setting_open_clicked(self, count: int = 0):
        """
        this is for checking metric Sidebar.SidebarSettings.OpenClicks is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_setting_open_clicked).to_have_count(count)

    def get_total_samples_of_metric_setting_open_clicked(self) -> int:
        return self.get_no_of_metric_sample(self.sidebar_setting_open_clicked)

    def check_sidebar_feature_icons_clicked(self, count: int = 0):
        """
        this is for checking metric Sidebar.FeatureIcons.Clicked is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_feature_icons_clicked).to_have_count(count)

    def get_total_samples_of_metric_feature_icons_clicked(self) -> int:
        return self.get_no_of_metric_sample(self.sidebar_feature_icons_clicked)

    def check_sidebar_custom_icons_clicked(self, count: int = 0):
        """
        this is for checking metric Sidebar.CustomIcons.Clicked is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_custom_icon_clicked).to_have_count(count)

    def get_total_samples_of_metric_custom_icons_clicked(self) -> int:
        return self.get_no_of_metric_sample(self.sidebar_custom_icon_clicked)

    def check_sidebar_paid_icons_clicked(self, count: int = 0):
        """
        this is for checking metric Sidebar.PaidIcons.Clicked is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_paid_icon_clicked).to_have_count(count)

    def get_total_samples_of_metric_paid_icons_clicked(self) -> int:
        return self.get_no_of_metric_sample(self.sidebar_paid_icon_clicked)

    def check_sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked(
        self, count: int = 0
    ):
        """
        this is for checking metric Sidebar.CustomIcons.EditIconWithOpenInWebPanelCheckboxChanged is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked
        ).to_have_count(count)

    def get_total_samples_of_metric_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked
        )

    def check_sidebar_custom_icons_fetching_response_code(self, count: int = 0):
        """
        this is for checking metric Sidebar.CustomIcons.FetchingResponseCode is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_custom_icons_fetching_response_code).to_have_count(count)

    def get_total_samples_of_metric_custom_icons_fetching_response_code(self) -> int:
        return self.get_no_of_metric_sample(
            self.sidebar_custom_icons_fetching_response_code
        )

    def check_sidebar_add_web_panel_autocomplete_matches(self, count: int = 0):
        """
        this is for checking metric Sidebar.AddWebPanel.AutocompleteMatches is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_add_web_panel_autocomplete_matches).to_have_count(count)

    def get_total_samples_of_metric_sidebar_add_web_panel_autocomplete_matches(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.sidebar_add_web_panel_autocomplete_matches
        )

    def check_sidebar_add_web_panel_autocomplete_selected(self, count: int = 0):
        """
        this is for checking metric Sidebar.AddWebPanel.AutocompleteSelected is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_add_web_panel_autocomplete_selected).to_have_count(count)

    def get_total_samples_of_metric_sidebar_add_web_panel_autocomplete_selected(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.sidebar_add_web_panel_autocomplete_selected
        )

    def check_sidebar_custom_icon_decode_image_time(self, count: int = 0):
        """
        this is for checking metric Sidebar.CustomIcons.DecodeImageTime is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_custom_icon_decode_image_time).to_have_count(count)

    def get_total_samples_of_metric_sidebar_custom_icon_decode_image_time(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(self.sidebar_custom_icon_decode_image_time)

    def check_sidebar_custom_icon_fetching_time(self, count: int = 0):
        """
        this is for checking metric Sidebar.CustomIcons.FetchingTime is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.sidebar_custom_icon_fetching_time).to_have_count(count)

    def get_total_samples_of_metric_sidebar_custom_icon_fetching_time(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(self.sidebar_custom_icon_fetching_time)

    def check_metric_savior_onboard_shown(self, count: int = 0):
        """
        this is for checking metric Savior.onboardShown is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.savior_onboard_shown).to_have_count(count)

    def get_total_samples_of_metric_savior_onboard_shown(self) -> int:
        return self.get_no_of_metric_sample(self.savior_onboard_shown)

    def check_metric_savior_onboard_try_now_click(self, count: int = 0):
        """
        this is for checking metric Savior.onboardTryNowClick is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.savior_onboard_try_now_click).to_have_count(count)

    def get_total_samples_of_metric_savior_onboard_try_now_click(self) -> int:
        return self.get_no_of_metric_sample(self.savior_onboard_try_now_click)

    def check_metric_savior_close_onboard_popup(self, count: int = 0):
        """
        this is for checking metric Savior.closeOnboardPopup is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.savior_close_onboard_popup).to_have_count(count)

    def get_total_samples_of_metric_savior_close_onboard_popup(self) -> int:
        return self.get_no_of_metric_sample(self.savior_close_onboard_popup)

    def get_metric_details(self, locator_text: str) -> str:
        """
        This method return the metrics detail of each metric
        Args:
            locator_text: Relative locator e.g: "div:below(div[histogram-name='Sidebar.CustomIcons.FetchingResponseCode'])"
            get get element by below div tag
        Returns: str
        """
        return self.page.locator(locator_text).first.text_content()

    # Tor metrics
    def check_metric_open_new_tor_window(self, count: int = 0):
        """
        this is for checking metric Tor.AppMenuModel.OpenNewTorWindow is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_open_new_tor_window).to_have_count(count)

    def get_total_samples_of_metric_open_new_tor_window(self) -> int:
        return self.get_no_of_metric_sample(self.tor_open_new_tor_window)

    def check_metric_new_tor_connection_for_this_site(self, count: int = 0):
        """
        this is for checking metric Tor.AppMenuModel.NewTorConnectionForThisSite is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_new_tor_connection_for_this_site).to_have_count(count)

    def get_total_samples_of_metric_new_tor_connection_for_this_site(self) -> int:
        return self.get_no_of_metric_sample(self.tor_new_tor_connection_for_this_site)

    def check_metric_new_tor_window_count(self, count: int = 0):
        """
        this is for checking metric Tor.Browser.WindowCount is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_new_tor_window_count).to_have_count(count)

    def get_total_samples_of_metric_tor_window_count(self) -> int:
        return self.get_no_of_metric_sample(self.tor_new_tor_window_count)

    def check_metric_tor_error_page_retry_with_tor(self, count: int = 0):
        """
        this is for checking metric Tor.ErrorPage.RetryWithTor is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_error_page_retry_with_tor).to_have_count(count)

    def get_total_samples_of_metric_tor_error_page_retry_with_tor(self) -> int:
        return self.get_no_of_metric_sample(self.tor_error_page_retry_with_tor)

    def check_metric_tor_tab_count(self, count: int = 0):
        """
        this is for checking metric Tor.Tab.Count is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_tab_count).to_have_count(count)

    def get_total_samples_of_metric_tor_tab_count(self) -> int:
        return self.get_no_of_metric_sample(self.tor_tab_count)

    def check_metric_tor_open_link_with_tor(self, count: int = 0):
        """
        this is for checking metric Tor.RenderViewContextMenu.OpenLinkWithTor is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_open_link_with_tor).to_have_count(count)

    def get_total_samples_of_metric_open_link_with_tor(self) -> int:
        return self.get_no_of_metric_sample(self.tor_open_link_with_tor)

    def check_metric_show_retry_with_tor_button(self, count: int = 0):
        """
        this is for checking metric Tor.ErrorPage.ShowRetryWithTorButton is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.tor_show_retry_with_tor_button).to_have_count(count)

    def get_total_samples_of_metric_show_retry_with_tor_button(self) -> int:
        return self.get_no_of_metric_sample(self.tor_show_retry_with_tor_button)

    def check_in_product_help_notify_event_ready_state(self, count: int = 0):
        """
        this is for checking metric InProductHelp.NotifyEventReadyState.IPH_CocCocScrollToTop is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.in_product_help_notify_event_ready_state).to_have_count(count)

    def get_total_samples_of_metric_in_product_help_notify_event_ready_state(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.in_product_help_notify_event_ready_state
        )

    def check_in_product_help_should_trigger_help_ui(self, count: int = 0):
        """
        this is for checking metric InProductHelp.ShouldTriggerHelpUI.IPH_CocCocScrollToTop is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.in_product_help_should_trigger_help_ui).to_have_count(count)

    def get_total_samples_of_metric_in_product_help_should_trigger_help_ui(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(self.in_product_help_should_trigger_help_ui)

    def check_coccoc_newtab_search_action(self, count: int = 0):
        """
        this is for checking metric Coccoc.NewTab.SearchAction is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.coccoc_newtab_search_action).to_have_count(count)

    def get_total_samples_of_metric_coccoc_newtab_search_action(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(self.coccoc_newtab_search_action)

    def check_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocRemoteNTP.PaintTiming.NavigationToFirstContentfulPaint is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint
        )

    def check_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocRemoteNTP.PaintTiming.NavigationToLargestContentfulPaint is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint
        )

    def check_page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocRemoteNTP.ParseTiming.NavigationToParseStart is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start
        )

    def check_page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocSearch.PaintTiming.NavigationToFirstContentfulPaint is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint
        )

    def check_page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocSearch.ParseTiming.NavigationToParseStart is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start
        )

    def check_page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocOthers.PaintTiming.NavigationToFirstContentfulPaint is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint
        )

    def check_page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start(
        self, count: int = 0
    ):
        """
        this is for checking metric PageLoad.Clients.CocCocOthers.ParseTiming.NavigationToParseStart is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(
            self.page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start
        ).to_have_count(count)

    def get_total_samples_of_metric_page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(
            self.page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start
        )

    def check_coccoc_adblock_metric(self, count: int = 0):
        """
        this is for checking metric InProductHelp.ShouldTriggerHelpUI.IPH_CocCocAdBlock is appeared or not
        Args:
            count: 0: mean disappeared, 1 mean appeared
        Returns:
        """
        self.page.goto("coccoc://histograms/")
        expect(self.coccoc_adblock_metric).to_have_count(count)

    def get_total_samples_of_metric_coccoc_adblock(
        self,
    ) -> int:
        return self.get_no_of_metric_sample(self.coccoc_adblock_metric)

    @staticmethod
    def get_no_of_metric_sample(locator: Locator) -> int:
        try:
            text_metric = locator.text_content()
        except Exception as e:
            raise e
        else:
            no_of_sample = string_number_utils.find_text_between_2_string(
                text_metric, "recorded ", " samples"
            )
            return int(no_of_sample)

    @staticmethod
    def get_value_of_mean(locator: Locator) -> str:
        try:
            text_metric = locator.text_content()
        except Exception as e:
            raise e
        else:
            no_of_sample = string_number_utils.find_text_between_2_string(
                text_metric, "mean = ", " (flags"
            )
            return no_of_sample

    def get_value_of_domain_size_mean(self) -> int:
        self.open_histograms_page()
        try:
            value_text = self.get_value_of_mean(
                self.coccoc_safety_tips_unsafe_URLData_domain_size
            )
        except Exception as e:
            raise e
        else:
            return int(value_text.split(".")[0])

    def get_value_of_url_size_mean(self) -> int:
        self.open_histograms_page()
        try:
            value_text = self.get_value_of_mean(
                self.coccoc_safety_tips_unsafe_URLData_url_size
            )
        except Exception as e:
            raise e
        else:
            return int(value_text.split(".")[0])


"""Outside class"""


def open_new_history_window():
    driver = open_browser.open_coccoc_by_selenium()
    try:
        driver.get("coccoc://histograms/#Sidebar.Activated")
        metric_locator = (
            By.CSS_SELECTOR,
            'div[id="histograms"] span[class="histogram-header-text"]',
        )
        assert (
            driver.find_element(*metric_locator).text
            == "Histogram: Sidebar.Activated recorded 1 samples, mean = 1.0 (flags = 0x41)"
        )
    finally:
        driver.quit()


# Open a coccoc then reload repeatedly and wait for the metrics sent
def wait_for_paid_icon_metric_is_sent(timeout=120) -> bool:
    max_delay = timeout
    interval_delay = 10
    total_delay = 0
    metrics_json = (
        rf"C:\Users\{os_utils.get_username()}\Documents\paid_icon_metrics_log.json"
    )
    while total_delay < max_delay:
        try:
            if file_utils.check_file_is_exists(metrics_json):
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if file_utils.check_file_is_exists(metrics_json):
        return True
    else:
        print(rf"Time out after {timeout} seconds of waiting for the metrics sent")
        return False
