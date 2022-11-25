import os
import random
from PIL import Image
from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import ProjectFolderPage, PopupManager

get_random_project_key = lambda data: random.choice(data['projects'])[0]

def project_page_load(webdriver, datasets):
    page = ProjectFolderPage(webdriver, get_random_project_key(datasets))
    @print_timing("selenium_s3_project_page_load")
    def measure():
        page.go_to()
        page.wait_for_page_loaded()
    measure()
    PopupManager(webdriver).dismiss_default_popup()

def project_page_create_folder(webdriver, datasets):
    page = ProjectFolderPage(webdriver, get_random_project_key(datasets))

    @print_timing("project_page_create_folder")
    def measure():
        PopupManager(webdriver).dismiss_default_popup()

        @print_timing('project_page_create_folder:load_page')
        def sub_measure():
            page.go_to()
            page.wait_for_page_loaded()

        sub_measure()

        @print_timing('project_page_create_folder:folder_creating')
        def sub_measure():
            page.create_folder()

        sub_measure()
    measure()
    PopupManager(webdriver).dismiss_default_popup()

def _create_and_save_img(size: int):
    temp_file = Image.new(mode='RGB', size=(size, size), color='red')
    base_path = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    temp_file_path = os.path.join(base_path, BasePage.generate_random_string(10) + '.jpg')
    temp_file.save(temp_file_path)

    return temp_file_path

def project_page_upload(webdriver, datasets):
    page = ProjectFolderPage(webdriver, get_random_project_key(datasets))
    img_path = _create_and_save_img(64)

    @print_timing("project_page_upload")
    def measure():
        PopupManager(webdriver).dismiss_default_popup()

        @print_timing('project_page_upload:load_page')
        def sub_measure():
            page.go_to()
            page.wait_for_page_loaded()

        sub_measure()

        @print_timing('project_page_upload:uploading')
        def sub_measure():
            page.upload_file(img_path)

        sub_measure()
    measure()
    os.remove(img_path)
    PopupManager(webdriver).dismiss_default_popup()

def project_page_upload_and_delete_file(webdriver, datasets):
    page = ProjectFolderPage(webdriver, get_random_project_key(datasets))
    img_path = _create_and_save_img(64)

    @print_timing("project_page_upload_and_delete_file")
    def measure():
        PopupManager(webdriver).dismiss_default_popup()

        @print_timing('project_page_upload_and_delete_file:load_page')
        def sub_measure():
            page.go_to()
            page.wait_for_page_loaded()

        sub_measure()

        @print_timing('project_page_upload_and_delete_file:upload_and_delete')
        def sub_measure():
            page.upload_and_delete_file(img_path, webdriver)
        sub_measure()

    measure()
    os.remove(img_path)
    PopupManager(webdriver).dismiss_default_popup()

def project_page_upload_and_rename_file(webdriver, datasets):
    page = ProjectFolderPage(webdriver, get_random_project_key(datasets))
    img_path = _create_and_save_img(64)

    @print_timing("project_page_upload_and_rename_file")
    def measure():
        PopupManager(webdriver).dismiss_default_popup()

        @print_timing('project_page_upload_and_rename_file:load_page')
        def sub_measure():
            page.go_to()
            page.wait_for_page_loaded()

        sub_measure()

        @print_timing('project_page_upload_and_rename_file:upload_and_delete')
        def sub_measure():
            page.upload_and_rename_file(img_path, webdriver)
        sub_measure()

    measure()
    os.remove(img_path)
    PopupManager(webdriver).dismiss_default_popup()
