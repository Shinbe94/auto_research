from pytest_pytestrail import pytestrail

from src.pages.internal_page.downloads.download_page import (
    DownloadPageSel,
)
from src.pages.settings.settings_downloads import SettingsDownloadsSel
from src.pages.support_pages.support_pages import WebTorrentSel


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54216")
def test_donot_seed_for_all_torrents(
    settings_downloads_sel: SettingsDownloadsSel,
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        settings_downloads_sel.turn_on_toggle_automatically_stop_seeding_completed_torrents(
            is_need_to_open_downloads_setting=True
        )
        web_torrent_sel.download_sintel_torrent_file()
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file()
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=2, timeout=1800, is_need_open_download_page=True
            )
            is True
        )
        download_page_sel.click_items_seeding()
        assert download_page_sel.get_total_items_seeding(timeout=5) == 0
        assert download_page_sel.is_element_appeared(download_page_sel.DESCRIPTION_TEXT)
    finally:
        download_page_sel.clear_all_downloads_data()
        settings_downloads_sel.turn_off_toggle_automatically_stop_seeding_completed_torrents(
            is_need_to_open_downloads_setting=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54217")
def test_stop_seeding_a_torrent(
    settings_downloads_sel: SettingsDownloadsSel,
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    settings_downloads_sel.turn_off_toggle_automatically_stop_seeding_completed_torrents(
        is_need_to_open_downloads_setting=True
    )
    try:
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        download_page_sel.open_download_page()
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1800
            )
            is True
        )
        assert download_page_sel.get_total_items_seeding() == 1
        download_page_sel.click_to_stop_seeding_an_item()
        download_page_sel.check_donot_seed_is_checked()
    finally:
        download_page_sel.clear_all_downloads_data()
