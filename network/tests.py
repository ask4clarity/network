from sqlite3 import Timestamp
from xxlimited import foo
from django.test import Client, TestCase
from .models import Post, User
from selenium import webdriver
import os
import pathlib
import unittest 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome()

class PostTestCase(TestCase):

    def setUp(self):

        test_user = User.objects.create(username="test_user")
        Post.objects.create(Owner=test_user, Content="test_content")

    def test_content(self):
        test_user = User.objects.get(username="test_user")
        post = Post.objects.get(Owner=test_user)
        self.assertEqual(f'{post.Content}', 'test_content')

    def test_user(self):
        test_user = User.objects.get(username="test_user")
        self.assertEqual(f'{test_user.username}', "test_user")

    def test_not_empty(self):
        test_user = User.objects.get(username="test_user")
        post = Post.objects.get(Owner=test_user)
        self.assertTrue(post.not_empty())

    def test_index(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 1)

class WebpageTests(unittest.TestCase):

    def test_title(self):
        driver.get("http://127.0.0.1:8000/")
        open_form = driver.find_element_by_id("new-post")
        open_form.click()
        form = driver.find_element_by_id("post-view")
        self.assertTrue(form.is_displayed())
        
        if __name__ == "__main__":
            unittest.main()
