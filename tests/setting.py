# Contains setting
implicit_wait = 30
timeout_pywinauto = 60
timeout = 30
timeout_selenium = 30
timeout_for_tor = 180
timeout_for_installing = 300
timeout_for_tor_loadpage_playwright = 60000  # milisecond
timeout_for_waiting_browser_update = 1200
timeout_for_update_components = 1200
timeout_waiting_for_network_up = 30
timeout_waiting_for_network_down = 10
timeout_for_waiting_download_small_file_size = 1200
timeout_for_waiting_download_medium_file_size = 3600
timeout_for_waiting_download_big_file_size = 36000
timeout_for_waiting_the_download_is_started = (
    30  # The crdownload extension appears at the download folder
)
sleep_n_seconds_for_testing_performance_tor = 600
coccoc_language = "en"  # 'vi' or 'en' only
platform = "64bit"  # 64bit or '32bit'
is_skip_test_update_download_cases: bool = False  # True --> Dont test update/upgrade cases, False --> test update/upgrade cases
coccoc_test_version = "116.0.5845.190"  # '105.0.5195.142'
old_coccoc_version = ["113.0.5672.174", "114.0.5735.210", "115.0.5790.188"]
very_old_coccoc_version = [
    "85.0.4183.146",
    "86.0.4240.198",
    "87.0.4280.148",
    "88.0.4324.202",
]
windows_version = "win11"  # win7, win8, win8.1, win11
coccoc_binary_64bit = "C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe"
coccoc_binary_64bit_debug = "C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe --remote-debugging-port=9222"
coccoc_binary_32bit = (
    "C:\\Program Files (x86)\\CocCoc\\Browser\\Application\\browser.exe"
)
coccoc_binary_32bit_debug = "C:\\Program Files (x86)\\CocCoc\\Browser\\Application\\browser.exe --remote-debugging-port=9222"
coccoc_default_profile = (
    "C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default"
)
notepad_plus_plus_64_bit = r"C:\Program Files\Notepad++\notepad++.exe"
notepad_plus_plus_32_bit = r"C:\Program Files (x86)\Notepad++\notepad++.exe"
coccoc_settings_page = "coccoc://settings"
coccoc_settings_default_browser_page = "coccoc://settings/defaultBrowser"
coccoc_histograms = "coccoc://histograms/"
coccoc_components = "coccoc://components/"
coccoc_extensions = "coccoc://extensions/"
coccoc_version_page = "coccoc://version/"
coccoc_settings_about = "coccoc://settings/help"
# coccoc_build_name = 'STANDALONE_VERSION_MACHINE'
coccoc_build_name = "STANDALONE_COCCOC_EN_MACHINE"
# coccoc_build_name = 'STANDALONE_COCCOC_VI_MACHINE'
coccoc_about = "coccoc://settings/help"
cashback_extension_json = "afaljjbleihmahhpckngondmgohleljb.json"
savior_extension_json = "jdfkmiabjpfjacifcmihfdjhpnjpiick.json"
dictionary_extension_json = "gfgbmghkdjckppeomloefmbphdfmokgd.json"
adblock_extension_json = "jeoooddfnfogpngdoijplcijdcoeckgm.json"
dictionary_extension_id = "gfgbmghkdjckppeomloefmbphdfmokgd"
savior_extension_id = "jdfkmiabjpfjacifcmihfdjhpnjpiick"
cashback_extension_id = "afaljjbleihmahhpckngondmgohleljb"
list_default_coccoc_extension_id = [
    "gfgbmghkdjckppeomloefmbphdfmokgd",
    "jdfkmiabjpfjacifcmihfdjhpnjpiick",
    "afaljjbleihmahhpckngondmgohleljb",
]
chrome_binary_64bit = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_binary_64bit_debug = r"C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222"
chrome_binary_32bit = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_binary_32bit_debug = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222"

brave_binary_64bit = (
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
)
brave_binary_64bit_debug = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe --remote-debugging-port=9223"
brave_binary_32bit = (
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
)
brave_binary_32bit_debug = r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe --remote-debugging-port=9223"

alluredir = "reports"
serve_allure_report = True
generate_allure_report = "allure generate"
url_download_setup_file = [
    "https://coccoc.com/en/download/thanks?ref=coccoc.com&plat=win&arch=x32",
    "https://coccoc.com/en/download/thanks?ref=coccoc.com&plat=win&arch=x64",
    "https://coccoc.com/vi/download/thanks?ref=coccoc.com&plat=win&arch=x32",
    "https://coccoc.com/vi/download/thanks?ref=coccoc.com&plat=win&arch=x64",
]
cc_account_user = "jevolih361@hekarro.com"
cc_account_password = "123456X@x"
coccoc_homepage_url = "https://coccoc.com"
coccoc_homepage_newtab = "https://coccoc.com/webhp"
cc_account_url = (
    "https://accounts.coccoc.com/?signin=sync&continue=https%3A%2F%2Fcoccoc.com"
)
coccoc_folder_64bit = "C:\\Program Files\\CocCoc\\"
coccoc_folder_32bit = "C:\\Program Files (x86)\\CocCoc"
# ftp_host = 'browser3v.dev.itim.vn'
ftp_server_remote = "browser3v.dev.itim.vn"
ftp_server_local = "10.193.8.18"
max_current_omaha_version = "2.9.1.10"
fiddler_title = "Progress Telerik Fiddler"
sleep_n_seconds_after_each_test = 3

NEW_TAB_TITLE_VI = r"Thẻ mới - Cốc Cốc"
NEW_TAB_TITLE_EN = r"New Tab - Cốc Cốc"
ADDRESS_BAR_VI = r"Thanh địa chỉ và tìm kiếm"
ADDRESS_BAR_EN = r"Address and search bar"
WELCOME_TITLE_VI = r"Chào mừng bạn đến với trình duyệt Cốc Cốc - Cốc Cốc"
WELCOME_TITLE_EN = r"Welcome to Cốc Cốc browser - Cốc Cốc"
performance_browsers_test = ["CocCoc", "Chrome", "Brave"]
# performance_browsers_test = ['CocCoc']
enable_browser_adblock = False
PAID_ICONS_API = "https://coccoc.com/webhp/icons.json"
list_possible_default_custom_icons = ["Youtube", "Facebook"]
list_recommended_custom_icons = {
    "Cốc Cốc Search": "https://search.coccoc.com/",
    "Youtube": "https://www.youtube.com/",
    "Facebook": "https://m.facebook.com/",
    "Google Translate": "https://translate.google.com.vn/",
    "Google": "https://www.google.com.vn/",
    "Spotify": "https://open.spotify.com/",
    "Instagram": "https://www.instagram.com/",
    "TikTok": "https://www.tiktok.com/",
    "VnExpress": "https://vnexpress.net/",
    "Zing": "https://zing.vn/",
    "24h": "https://24h.com.vn/",
    "ChatGPT": "https://chat.openai.com/",
}

list_on_boarding_feature_icons = {
    "Skype": "https://web.skype.com/",
    "Telegram": "https://web.telegram.org/",
    "Facebook Messenger": "https://www.messenger.com/",
    "Zalo": "https://id.zalo.me/",
}

list_sidebar_feature_icons = [
    "Settings",
    "History",
    "Reading List",
    "Cốc Cốc Points",
    "Facebook Messenger",
    "Telegram",
    "Skype",
    "Zalo",
    "Cốc Cốc Games",
]
list_default_search_engine_vendor = {
    "Cốc Cốc": "coccoc.com/search",
    "Google": "google.com/search",
    "Bing": "bing.com/search",
    "Yahoo!": "search.yahoo.com/search",
    "DuckDuckGo": "duckduckgo.com",
    "Ecosia": "ecosia.org/search",
}

list_testing_sites = [
    "https://search.coccoc.com/",
    "https://www.youtube.com/",
    "https://m.facebook.com/",
    "https://translate.google.com.vn/",
    "https://www.google.com.vn/",
    "https://open.spotify.com/",
    "https://www.instagram.com/",
    "https://www.tiktok.com/",
    "https://vnexpress.net/",
    "https://zing.vn/",
    "https://24h.com.vn/",
    "https://chat.openai.com/",
    "https://tinhte.vn/",
    "https://genk.vn/",
    "https://tiki.vn",
    "https://game24h.vn",
    "https://thegioididong.com",
    "https://twitter.com",
]
list_sites_for_tor = [
    "https://xvideos.com/",
    "https://bbc.co.uk/",
    "https://medium.com/",
]
list_onion_sites = [
    "http://keybase5wmilwokqirssclfnsqrjdsi7jdir5wy7y7iu3tanwmtp6oid.onion/",
    "http://zerobinftagjpeeebbvyzjcqyjpmjvynj5qlexwyxe7l3vqejxnqv5qd.onion/",
    "http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
]
fixed_custom_user_dir = (
    rf"C:\browsers"  # a Custom location for custom user profile(user-dir)
)
MAGNET_SINTEL = r"magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10&dn=Sintel&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fsintel.torrent"
MAGNET_BIG_BUCK_BUNNY = r"magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c&dn=Big+Buck+Bunny&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fbig-buck-bunny.torrent"
list_vast_videos = [
    "https://coccoc.com/webhp?type=2&show=43381349",
    "https://coccoc.com/webhp?type=2&show=43388621",
    "https://coccoc.com/webhp?type=2&show=43154738",
]

list_cc_sites = [
    "https://coccoc.com/",
    "https://points.coccoc.com/",
    "https://rungrinh.vn/",
    "https://quizz.coccoc.com/",
]
list_non_cc_sites = ["https://google.com", "https://tinhte.vn"]
list_internal_sites = [
    "coccoc://settings",
    "coccoc://bookmarks",
    "coccoc://downloads",
    "coccoc://version/",
    "coccoc://newtab/",
    "coccoc://history/",
    "coccoc://extensions",
    "coccoc://flags",
    "coccoc://components",
    "coccoc://apps/",
]

list_sites_for_adblock_testing = ["https://www.24h.com.vn", "https://kenh14.vn"]
keep_reports_during_n_days = 7
