#!/usr/bin/python
"""A uBlog base project."""

# Standard modules
import os

# Third-party modules
import uweb3

# Application components
from . import pages

__author__ = 'Arjen Pander <arjen@underdark.nl>'
__version__ = '0.1'

def main():
  """Creates a uWeb3 application.

  The application is created from the following components:

  - The presenter class (PageMaker) which implements the request handlers.
  - The routes iterable, where each 2-tuple defines a url-pattern and the
    name of a presenter method which should handle it.
  - The configuration file (ini format) from which settings should be read.
  """
  path = os.path.dirname(os.path.abspath(__file__))
  routes = [('/', 'Index'),
            ('/page/(\d+)/?(\d+)?', 'Index'),
            ('/ULF-Login', 'ValidateLogin'),
            ('/home', 'Index'),
            ('/login', 'Login'),
            ('/signup', 'Signup'),
            ('/adduser', 'AddUser'),
            ('/addcomment', 'AddComment'),
            ('/logout', 'RequestLogout'),
            ('/comment/(\d+)', 'Comment'),
            ('/article/(\d+)/(.*)', 'Article'),
            ('/articles/(\d+)/(\d+)', 'ArticlesByDate'),
            ('/tags/(.*)', 'ArticlesByTag'),
            ('/author/(\d+)/(.*)', 'ArticlesByUser'),
            ('/alltags', 'alltags'),
            ('/allmonths', 'allmonths'),
            ('/allauthors', 'allauthors'),

            ('/admin/users', 'Users'),
            ('/admin/user/(\d+)/(.*)/?(\d+)?/?(\d+)?/?', 'User'),
            ('/admin/deleteuser', 'DeleteUser'),
            ('/admin/deletecomment', 'DeleteComment'),
            ('/admin/deletearticle', 'DeleteArticle'),
            ('/admin/updateuser', 'UpdateUser'),
            ('/admin/updateuserpassword', 'UpdateUserPassword'),
            ('/admin/updatearticle', 'UpdateArticle'),
            ('/admin/article/(\d+)/(.*)', 'AdminArticle'),
            ('/admin/newarticle', 'NewArticle'),
            ('/admin/addarticle', 'AddArticle'),
            ('/(.*)', 'FourOhFour')]
  return uweb3.uWeb(pages.PageMaker, routes, executing_path=path)