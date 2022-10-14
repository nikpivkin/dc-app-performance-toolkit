import random

from selenium_ui.conftest import print_timing
from selenium_ui.bitbucket.pages.pages import CodeSearch, PopupManager


def code_search_load(webdriver, datasets):
    rnd_repo = random.choice(datasets["repos"])

    project_key = rnd_repo[1]
    repo_slug = rnd_repo[0]
    page = CodeSearch(webdriver, project_key, repo_slug)

    @print_timing("selenium_code_search_load")
    def measure():
        page.go_to()
        page.open_search()
        page.wait_for_page_loaded()

    measure()
    PopupManager(webdriver).dismiss_default_popup()


def open_target_link(webdriver, datasets):

    project_key = "PROJECT_2"
    repo_slug = "js-examples"
    page = CodeSearch(webdriver, project_key, repo_slug)

    @print_timing("selenium_code_search_load")
    def measure():
        page.go_to()
        page.find_links()

    measure()
    PopupManager(webdriver).dismiss_default_popup()
