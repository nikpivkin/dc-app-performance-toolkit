from selenium_ui.bitbucket import modules
from extension.bitbucket import extension_ui  # noqa F401


def test_0_selenium_a_login(bitbucket_webdriver, bitbucket_datasets, bitbucket_screen_shots):
    modules.login(bitbucket_webdriver, bitbucket_datasets)


def test_1_code_search_load(bitbucket_webdriver, bitbucket_datasets, bitbucket_screen_shots):
    extension_ui.code_search_load(bitbucket_webdriver, bitbucket_datasets)


def test_1_open_target_link(bitbucket_webdriver, bitbucket_datasets, bitbucket_screen_shots):
    extension_ui.open_target_link(bitbucket_webdriver, bitbucket_datasets)


def test_2_selenium_logout(bitbucket_webdriver, bitbucket_datasets, bitbucket_screen_shots):
    modules.logout(bitbucket_webdriver, bitbucket_datasets)
