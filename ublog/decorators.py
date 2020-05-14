"""This file holds all the decorators we use in this project"""
import uweb3
from uweb3.response import Redirect


def adminonly(f):
    """Decorator that checks if the user requesting the page is in fact an
    admin"""
    def wrapper(*args, **kwargs):
      try:
        user = args[0]._GetUserLoggedIn()
        args[0].user = user
      except (uweb3.model.NotExistError, args[0].NoSessionError):
        return Redirect('/login')
      if user['admin'] != 'true':
          return Redirect('/', httpcode=303)
      return f(*args, **kwargs)
    return wrapper


def loggedin(f):
    """Decorator that checks if the user requesting the page is in fact logged
    in"""
    def wrapper(*args, **kwargs):
      try:
        user = args[0]._GetUserLoggedIn()
        args[0].user = user
      except (uweb3.model.NotExistError, args[0].NoSessionError):
        return Redirect('/login')
      return f(*args, **kwargs)
    return wrapper


def checkxsrf(f):
    """Decorator that checks if the xsrf in the user's cookie matches that from
    the (post) request"""
    def wrapper(*args, **kwargs):
      if args[0].incorrect_xsrf_token:
        return args[0].XSRFInvalidToken('Your XSRF token was incorrect, please try again.')
      return f(*args, **kwargs)
    return wrapper


import sys
PYTHON_VERSION = 2
if (sys.version_info > (3, 0)):
  PYTHON_VERSION = 3

def TemplateParser(template, *t_args, **t_kwargs):
    """Decorator that wraps the output in a templateparser call if its not
    already something that we prepared for direct output to the client"""
    def template_decorator(f):
      def wrapper(*args, **kwargs):
        pageresult = f(*args, **kwargs) or {}
        if (
          (PYTHON_VERSION == 3 and not isinstance(pageresult, (str, uweb3.Response, Redirect))) or
          (PYTHON_VERSION == 2 and not isinstance(pageresult, (str, unicode, uweb3.Response, Redirect)))):
          pageresult.update(args[0].CommonBlocks(*t_args, **t_kwargs))
          return args[0].parser.Parse(template, **pageresult)
        return pageresult
      return wrapper
    return template_decorator