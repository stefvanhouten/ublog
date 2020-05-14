#!/usr/bin/python
"""Html generators for the base uweb3 server."""

import datetime
import time
import binascii
import os
import uweb3
from creole import creole2html
from . import admin
from . import model
from . import decorators
from uweb3.response import Redirect


def indexText(blogpost):
  """Cuts down a string to a maximum of 50 words.

  to be used in the admin index
  """
  blogpost = blogpost.split()
  blogpost = blogpost[:50]

  if len(blogpost) >= 50:
    output = " ".join(blogpost) + " ..."
  else:
    output = " ".join(blogpost)

  return output


def slashfilter(text):
  """Filters slashes from a string."""
  return text.replace('/', '&-#')


# ##############################################################################
# Actual Pagemaker mixin class
#
class LoginMixin(uweb3.model.SecureCookie):
  """Provides the Login Framework for uWeb3."""
  USER = model.User

  class NoSessionError(Exception):
    """Custom exception for user not having a (unexpired) session cookie."""

  @decorators.checkxsrf
  def ValidateLogin(self):
    try:
      user = self.USER.FromName(
          self.connection, self.post.getfirst('username'))
      if user.VerifyPlaintext(str(self.post.getfirst('password', ''))):
        return self._Login_Success(user)
      return self._Login_Failure()
    except uweb3.model.NotExistError:
      return self._Login_Failure()

  def _Login_Success(self, user):
    """Renders the response to the user upon authentication failure."""
    raise NotImplementedError

  def _ULF_Success(self, secure):
    """Renders the response to the user upon authentication success."""
    raise NotImplementedError


class PageMaker(uweb3.DebuggingPageMaker,
                LoginMixin,
                admin.PageMaker):
  """Holds all the html generators for the webapp.

  Each page as a separate method.
  """

  ULF_SESSION_NAME = 'ulf_session_id'
  incorrect_xsrf_token = False

  def __init__(self, *args, **kwds):
    """Overwrites the default init to add extra templateparser functions."""
    super(PageMaker, self).__init__(*args, **kwds)
    LoginMixin.__init__(self)
    self.parser.RegisterFunction("creole", creole2html)
    self.parser.RegisterFunction("indextext", indexText)
    self.parser.RegisterFunction("slashfilter", slashfilter)
    if 'xsrf' in self.cookies:
      self.req.AddCookie('xsrf', self.cookies['xsrf'], path='/',
                         max_age=108000)
    else:
      self.req.AddCookie('xsrf', binascii.hexlify(os.urandom(16)),
                         max_age=108000)
      self.incorrect_xsrf_token = True

    if self.post:
      try:
        if self.post.getfirst('xsrf') != self.cookies['xsrf']:
          self.incorrect_xsrf_token = True
      except Exception:
        self.incorrect_xsrf_token = True

    if self.incorrect_xsrf_token is True:
      self.post.list = []

  def Index(self, page=1, unpubpage=1):
    """Returns the index.html template."""
    articles = list(model.Article.LastN(self.connection, count=1000))
    pagination = self.MakePagination(int(page), len(articles))
    if articles:
      articles = articles[10*(pagination['currentpage']-1):
                          10*pagination['currentpage']]

    try:
      user = self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError, TypeError):
      pass
    else:
      if user['admin'] == 'true':
        unpubarticles = list(model.Article.LastN(self.connection, public=False,
                                                 count=1000))
        if unpubpage is None:
          unpubpage = 1
        unpubpagination = self.MakePagination(int(unpubpage), len(unpubarticles))
        if unpubpagination:
          unpubarticles = unpubarticles[10*(unpubpagination['currentpage']-1):
                                        10*unpubpagination['currentpage']]
        return self.parser.Parse('admin/adminindex.html', articles=articles,
                                 unpubarticles=unpubarticles,
                                 pagination=pagination,
                                 unpubpagination=unpubpagination,
                                 **self.CommonBlocks('Index'))

    return self.parser.Parse('index.html', articles=articles,
                             blogname=self.options['blog']['name'],
                             pagination=pagination,
                             unpubpagination=None,
                             **self.CommonBlocks('Index'))

  @decorators.TemplateParser('login.html', 'Login')
  def Login(self):
    """Returns the login.html template."""
    try:
      self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError, TypeError):
      pass
    else:
      return Redirect('/', httpcode=303)

  @decorators.TemplateParser('signup.html', 'Signup')
  def Signup(self):
    """Returns the signup.html template."""
    try:
      self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError, TypeError):
      pass
    else:
      return Redirect('/', httpcode=303)

  def RequestMessage(self, message, status, refresh, article=None):
    """Returns the message.html template."""
    return self.parser.Parse('message.html', message=message,
                             refresh=refresh, article=article,
                             **self.CommonBlocks(status))

  @decorators.checkxsrf
  def AddUser(self):
    """Adds a new user based on the given input."""
    email = self.post.getfirst('email')
    if not email:
      return Redirect('/signup', httpcode=303)
    if len(email) > 200:
        message = 'The email is too long.'
        return self.RequestMessage(message, 'Error', '/home')
    user = model.User.FromEmail(self.connection, email)
    if len(self.post.getfirst('name')) > 30:
      message = 'The username is too long.'
      return self.RequestMessage(message, 'Error', '/home')
    if model.User.FromAuthor(self.connection, self.post.getfirst('name')):
      message = 'The username is already in use.'
      return self.RequestMessage(message, 'Error', '/signup')
    if (not self.post.getfirst('password')
       or len(self.post.getfirst('password')) <= 5):
      message = 'The Password is too short.'
      return self.RequestMessage(message, 'Error', '/signup')
    if not user:
      hashed = model.User.HashPassword(self.post.getfirst('password'))
      user = model.User.Create(self.connection, {
          'name': self.post.getfirst('email'),
          'password': hashed['password'],
          'salt': hashed['salt'].decode('utf-8'),
          'author': self.post.getfirst('name'),
          'active': 'true',
          'admin': 'false'})
    elif user['active'] == 'false':
      user['author'] = self.post.getfirst('name')
      user['active'] = 'true'
      user['admin'] = 'false'
    else:
      message = 'The provided email has already been used.'
      return self.RequestMessage(message, 'Error', '/signup')
    message = 'Your account has successfully been created.'
    return self.RequestMessage(message, 'Success', '/home')

  def Article(self, number, title):
    """Returns the singlepost.html template."""
    try:
      user = self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError, TypeError):
      user = None
    try:
      article = model.Article.FromPrimary(self.connection, int(number))
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      javascripts = ['validate.js', 'newcomment.js']
      tags = article.Tags()
    except (uweb3.model.NotExistError, ValueError):
      return Redirect('/', httpcode=303)

    first = article['content'].find("{{")
    if first > 0:
      last = article['content'].find("|", first)
      article["image"] = article['content'][first+2:last]
    else:
      article["image"] = ""
    try:
      commentslist = list(article.Comments(self.connection))
      rowtype = True
      for comment in commentslist:
        rowtype = not rowtype
        comment['date'] = comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        comment['rowtype'] = rowtype and 'Even' or 'Odd'
    except uweb3.model.NotExistError:
      commentslist = False
    return self.parser.Parse('singlepost.html', article=article, tags=tags,
                             commentslist=commentslist, user=user,
                             **self.CommonBlocks(article['title'],
                                                 javascripts=javascripts,
                                                 OGdata=article))

  def ArticlesByDate(self, year, month=None):
    """Returns the articles.html template by date."""
    try:
      if month:
        articles = list(model.Article.Month(self.connection, month, year))
      else:
        articles = list(model.Article.Year(self.connection, year))
    except (uweb3.model.NotExistError, ValueError, TypeError):
      return Redirect('/', httpcode=303)
    title = 'Month: %s %s' % (year, month)
    return self.parser.Parse('articles.html', articles=articles, title=title,
                             **self.CommonBlocks('Month: %s %s' % (month,
                                                                   year)))

  def ArticlesByTag(self, tag):
    """Returns the articles.html template by tag."""
    tag = tag.replace('&-#', '/')
    try:
      articles = list(model.Article.Tag(self.connection, tag))
    except (uweb3.model.NotExistError, ValueError, TypeError):
      return Redirect('/', httpcode=303)
    title = 'Tag: %s' % tag
    return self.parser.Parse('articles.html', articles=articles, title=title,
                             **self.CommonBlocks('Tag: %s' % tag))

  def ArticlesByUser(self, user, title):
    """Returns the articles.html template by user."""
    author = model.User.FromID(self.connection, user)
    try:
      articles = list(model.Article.User(self.connection, user))
    except (uweb3.model.NotExistError, ValueError, TypeError):
      return Redirect('/', httpcode=303)
    if author:
      title = 'Author: %s' % author["author"]
      return self.parser.Parse('articles.html', articles=articles, title=title,
                               **self.CommonBlocks(title))
    else:
      title = 'no user found'
      return uweb3.Response(self.parser.Parse('articles.html',
                           articles=articles, title=title,
                           **self.CommonBlocks(title)), httpcode=404)

  def Comment(self, comment):
    """Returns the singlecomment.html template."""
    try:
      user = self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError, TypeError):
      user = None
    try:
      comment = model.Comment.FromPrimary(self.connection, comment)
      comment['date'] = comment['date'].strftime('%Y-%m-%d %H:%M:%S')
    except (uweb3.model.NotExistError, TypeError):
      return Redirect('/', httpcode=303)
    return self.parser.Parse('singlecomment.html', comment=comment, user=user,
                             **self.CommonBlocks('Comment # %s'
                                                 % comment['ID']))

  @decorators.TemplateParser('alltags.html', 'alltags')
  def alltags(self):
    """Returns the alltags.html template."""
    tags = list(model.Tags.Tagcloud(self.connection))
    return {'tags': tags}

  @decorators.TemplateParser('allauthors.html', 'allauthors')
  def allauthors(self):
    """Returns the allauthors.html template."""
    users = list(model.User.authors(self.connection))
    return {'users': users}

  @decorators.TemplateParser('allmonths.html', 'allmonths')
  def allmonths(self):
    """Returns the allmonths.html template."""
    menuitems = list(model.Article.ActiveMonths(self.connection))
    return {'menuitems': menuitems}

  @decorators.checkxsrf
  @decorators.TemplateParser('message.html', 'Success')
  def AddComment(self):
    """Adds a new comment to an article."""
    if not self.post.getfirst('comment'):
      return Redirect('/', httpcode=303)
    try:
      article = model.Article.FromPrimary(self.connection,
                                          self.post.getfirst('article'))
    except uweb3.model.NotExistError:
      return Redirect('/', httpcode=303)
    try:
      user = self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError, TypeError):
      user = model.User.FromEmail(self.connection, self.post.getfirst('email'))
      if not user:
        if len(self.post.getfirst('user')) > 30:
          message = 'The username is too long.'
          return self.RequestMessage(message, 'Error', '/signup')
        if model.User.FromAuthor(self.connection, self.post.getfirst('user')):
          message = 'The username is already in use.'
          return self.RequestMessage(message, 'Error', '/signup')
        user = model.User.Create(self.connection, {
            'name': self.post.getfirst('email'),
            'author': self.post.getfirst('user'),
            'active': 'false',
            'admin': 'false'})
      else:
        if user['active'] == 'true':
          return Redirect('/login', httpcode=303)
    if article['commentable'] != 'true' and user['admin'] != 'true':
      return Redirect('/', httpcode=303)
    comment = {}
    now = datetime.datetime.now()
    comment['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
    comment['user'] = user['ID']
    comment['article'] = self.post.getfirst('article')
    comment['content'] = self.post.getfirst('comment')
    if len(comment['content']) > 65535:
        message = 'The comment is too long.'
        return self.RequestMessage(message, 'Error', '/home')
    model.Comment.Create(self.connection, comment)
    message = 'Your message has successfully been added.'
    refresh = '/home'
    return {'message': message, 'refresh': refresh, 'article': None}

  def RequestLogout(self):
    """Logs the user out and returns them to the homepage."""
    try:
      self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError):
      print("Redirect")
      return Redirect('/login')
    self.Delete('login')
    return self.Index()

  @decorators.TemplateParser('message.html', 'Error')
  def _Login_Failure(self):
    message = 'Incorrect username or password combination.'
    refresh = '/login'
    return {'message': message, 'refresh': refresh, 'article': None}

  @decorators.checkxsrf
  def _Login_Success(self, user):
    secure_user = { key : value for key, value in user.items() if key not in ('password', 'salt')}

    self.Create('login',
                secure_user,
                max_age='172800')
    message = 'You have been logged in.'
    return self.RequestMessage(message, 'Success', '/home')

  def _GetUserLoggedIn(self):
    """Gets the user that is logged in from the current session."""
    self.user = self.cookiejar.get('login')
    print(self.cookiejar)
    if self.user:
      return self.user
    raise self.NoSessionError("security error for session")

  def _GetXSRF(self):
    if 'xsrf' in self.cookies:
      return self.cookies['xsrf']

  def XSRFInvalidToken(self, command):
    """Returns an error message regarding an incorrect XSRF token."""
    page_data = self.parser.Parse('403.html', error=command,
                                  **self.CommonBlocks('Invalid XSRF token'))
    return uweb3.Response(content=page_data, httpcode=403)

  def FourOhFour(self, path):
    """The request could not be fulfilled, self returns a 404."""
    return uweb3.Response(self.parser.Parse('404.html', path=path,
                         **self.CommonBlocks('404')), httpcode=404)

  def CommonBlocks(self, page, javascripts=None, OGdata=None):
    """Returns a dictionary with the header and footer in it."""
    xsrftoken = self._GetXSRF()
    blogOptions = self.options['blog']
    blogcopyright = time.strftime('%Y')
    blogpoweredby = uweb3.__version__
    tags = list(model.Tags.Tagcloud(self.connection))[:10]
    users = list(model.User.authors(self.connection))[:10]
    menuitems = list(model.Article.ActiveMonths(self.connection))[:10]
    try:
      user = self._GetUserLoggedIn()
    except (uweb3.model.NotExistError, self.NoSessionError):
      user = None
    return {
        'header': self.parser.Parse('header.html',
                                    blogname=blogOptions['name'],
                                    blogtitle=blogOptions['title'],
                                    blogsubtitle=blogOptions['subtitle'],
                                    blogurl=blogOptions['url'], page=page,
                                    javascripts=javascripts,
                                    menuitems=menuitems, tags=tags, user=user,
                                    xsrftoken=xsrftoken,
                                    users=users, OGdata=OGdata),
        'footer': self.parser.Parse('footer.html', blogcopyright=blogcopyright,
                                    blogtitle=blogOptions['title'], user=user,
                                    blogpoweredby=blogpoweredby),
        'xsrftoken': xsrftoken}

  def MakePagination(self, currentpage, totalcount, pageposts=10, maxlinks=10):
    """Returns a dictionary with pages and page information.

    Takes:
      currentpage: int
      totalcount: int of total amount of posts
      pageposts: int of how many posts per page, default 10
      maxlinks: int of the maximum amount of linked pages, default 10

    Returns:
      currentpage: int with the current page
      totalpages: int of the total amount of pages
      pagenumbers: list of integers of pages that should be linked
      next: int of next page, if possible
      previous: int of previous page, if possible
      first: int of first page, if necessary
      last: int of last page, if necessary
      """
    totalpages = int(((totalcount + (pageposts - 1)) / pageposts))
    if totalpages < 1:
      return None
    currentpage = min(max(currentpage, 1), totalpages)
    pagination = {}
    pagination['currentpage'] = currentpage
    pagination['totalpages'] = totalpages
    pagination['previous'] = currentpage-1 if currentpage-1 >= 1 else None
    pagination['next'] = currentpage+1 if currentpage+1 <= totalpages else None
    pagination['first'] = 1 if currentpage != 1 else None
    pagination['last'] = totalpages if currentpage != totalpages else None
    pagination['pagenumbers'] = []
    if totalpages <= maxlinks + 1:
      pagination['pagenumbers'] = range(1, totalpages + 1)
    else:
      for x in xrange(currentpage - (maxlinks / 2), currentpage):
        if x > 0:
          pagination['pagenumbers'].append(x)
      pagination['pagenumbers'].append(currentpage)
      for x in xrange(currentpage + 1, currentpage + (maxlinks / 2) + 1):
        if x <= totalpages:
          pagination['pagenumbers'].append(x)
    return pagination
