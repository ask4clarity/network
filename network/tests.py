from sqlite3 import Timestamp
from xxlimited import foo
from django.test import Client, TestCase
from .models import Post, User, Follow
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

class ModelTestCase(TestCase):

    def setUp(self):

        test_user = User.objects.create(username="test_user")
        test_user2 = User.objects.create(username="test_user2")
        Post.objects.create(Owner=test_user, Content="test_content")
        Follow.objects.create(Owner=test_user, Target=test_user2)

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

    def test_not_same(self):
        test_user = User.objects.get(username="test_user")
        follow = Follow.objects.get(Owner=test_user)
        self.assertTrue(follow.not_same())

    def test_index(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 1)

class WebpageTests(unittest.TestCase):

    def test_new_post(self):
        #login
        driver.get ("http://127.0.0.1:8000/login")
        email = driver.find_element_by_id("user_n")
        email.send_keys("josh")
        password = driver.find_element_by_id("pw")
        password.send_keys("hello")
        driver.find_element_by_id("login").click()
        #open form 
        open_form = driver.find_element_by_id("new-post")
        open_form.click()
        form = driver.find_element_by_id("post-view")
        self.assertTrue(form.is_displayed())
        
        if __name__ == "__main__":
            unittest.main()

    def test_user_link(self):
        #login
        driver.get ("http://127.0.0.1:8000/login")
        email = driver.find_element_by_id("user_n")
        email.send_keys("josh")
        password = driver.find_element_by_id("pw")
        password.send_keys("hello")
        driver.find_element_by_id("login").click()
        #page redirect works
        user_direct = driver.find_element_by_id("user-link")
        link = user_direct.get_attribute("href")
        user_direct.click()
        url = driver.current_url
        self.assertEquals(link, url)
        #Build LiveServerTestCase test for follow button

      
        


        


        

    
