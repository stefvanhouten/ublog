#!/usr/bin/python
"""Html generators for the ublog's admin pages."""

import datetime
import pymysql

import uweb3
# from underdark.libs.sqltalk import sqlresult
from uweb3.ext_lib.libs.sqltalk import sqlresult

from . import decorators, model
from uweb3.response import Redirect



class PageMaker(object):
  """Holds all the html generators for the admin pages of the webapp.

  Each page as a separate method.
  """

  @decorators.adminonly
  @decorators.TemplateParser('admin/users.html', 'Users')
  def Users(self):
    """Returns the users.html template."""
    return {'loggedinuser': self._GetUserLoggedIn(),
            'userlist': list(model.User.List(self.connection))}

  @decorators.adminonly
  def User(self, userid, name, commentsPage=1, articlesPage=1):
    """Returns the edituser.html template."""
    try:
      user = model.User.FromPrimary(self.connection, userid)
    except uweb3.model.NotExistError:
      return Redirect('/users', httpcode=303)
    commentslist = list(user.Comments(self.connection))
    commentpagination = None
    if commentslist:
      if commentsPage is None:
        commentsPage = 1
      commentpagination = self.MakePagination(int(commentsPage),
                                              len(commentslist))
      if commentpagination:
        commentslist = commentslist[10*(commentpagination['currentpage']-1):
                                    10*commentpagination['currentpage']]
      rowtype = True
      for comment in commentslist:
        rowtype = not rowtype
        comment['date'] = comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        comment['rowtype'] = rowtype and 'Even' or 'Odd'
        comment['user'] = user
        comment['article'] = model.Article.FromPrimary(self.connection,
                                                       comment['article'])
        comment['check'] = True
    try:
      articles = list(model.Article.User(self.connection, userid))
    except (uweb3.model.NotExistError, ValueError, TypeError):
      return Redirect('/', httpcode=303)
    articlesPage = articlesPage if articlesPage else 1
    articlePagination = None
    articlePagination = self.MakePagination(int(articlesPage),
                                            len(articles))
    if articlePagination:
      articles = articles[10*(articlePagination['currentpage']-1):
                          10*articlePagination['currentpage']]
    loggedinuser = self._GetUserLoggedIn()
    return self.parser.Parse('admin/edituser.html', user=user,
                             commentslist=commentslist, commentform="",
                             articles=articles,
                             loggedinuser=loggedinuser,
                             commentpagination=commentpagination,
                             articlePagination=articlePagination,
                             **self.CommonBlocks('Edit author: %s'
                                                 % user['author']))

  @decorators.adminonly
  @decorators.checkxsrf
  def UpdateUser(self):
    """Updates a user's information."""
    if not self.post:
      return Redirect('/admin/users', httpcode=303)
    try:
      user = model.User.FromPrimary(self.connection,
                                    self.post.getfirst('user'))
    except uweb3.model.NotExistError:
      return Redirect('/admin/users', httpcode=303)
    if self.post.getfirst('name'):
      if len(self.post.getfirst('name')) > 30:
        message = 'The username is too long.'
        return self.RequestMessage(message, 'Error', '/signup')
      check = model.User.FromAuthor(self.connection,
                                    self.post.getfirst('name'))
      if check and check['ID'] != user['ID']:
        message = 'The username is already in use.'
        return self.RequestMessage(message, 'Error', '/signup')
      user['author'] = self.post.getfirst('name')
    email = self.post.getfirst('email')
    if len(email) > 200:
        message = 'The email is too long.'
        return self.RequestMessage(message, 'Error', '/login')
    elif email:
      user['name'] = email
    user['admin'] = 'true' if self.post.getfirst('admin') == 'on' else 'false'
    user['active'] = 'true'if self.post.getfirst('active') == 'on' else 'false'
    try:
        user.Save()
    except pymysql.IntegrityError:
        message = 'The email has already been created.'
        return self.RequestMessage(message, 'Error', '/login')
    message = 'The changes have been saved.'
    return self.RequestMessage(message, 'Success', '/admin/users')

  @decorators.adminonly
  @decorators.checkxsrf
  def UpdateUserPassword(self):
    """Updates a user's password."""
    if not self.post:
      return Redirect('/admin/users', httpcode=303)
    try:
      user = model.User.FromPrimary(self.connection,
                                    self.post.getfirst('user'))
    except uweb3.model.NotExistError:
      return Redirect('/admin/users', httpcode=303)
    password = self.post.getfirst('password')
    if not password or len(password) <= 5:
      message = 'The Password is too short.'
      return self.RequestMessage(message, 'Error', '/admin/users')
    if password != self.post.getfirst('repassword'):
      message = 'The Passwords are not the same.'
      return self.RequestMessage(message, 'Error', '/admin/users')
    user.UpdatePassword(password)
    message = 'The new password has been saved.'
    return self.RequestMessage(message, 'Success', '/admin/users')

  @decorators.adminonly
  @decorators.checkxsrf
  @decorators.TemplateParser('message.html', 'Success')
  def DeleteUser(self):
    """Deletes a user."""
    if not self.post:
      return Redirect('/', httpcode=303)
    userid = self.post.getfirst('id')
    try:
      user = model.User.FromPrimary(self.connection, userid)
    except uweb3.model.NotExistError:
      return Redirect('/admin/users', httpcode=303)
    user.Delete(self.connection)
    message = 'The user has been deleted.'
    refresh = '/admin/users'
    return {'message': message, 'refresh': refresh, 'article': None}
    loggedinuser = self._GetUserLoggedIn()

  @decorators.adminonly
  @decorators.checkxsrf
  @decorators.TemplateParser('message.html', 'Success')
  def DeleteComment(self):
    """Deletes a comment."""
    if not self.post:
      return Redirect('/', httpcode=303)
    commentid = self.post.getfirst('id')
    try:
      comment = model.Comment.FromPrimary(self.connection, commentid)
    except uweb3.model.NotExistError:
      return Redirect('/admin/users', httpcode=303)
    comment.Delete()
    message = 'The comment has been deleted.'
    refresh = '/home'
    return {'message': message, 'refresh': refresh, 'article': None}

  @decorators.adminonly
  @decorators.checkxsrf
  @decorators.TemplateParser('message.html', 'Success')
  def DeleteArticle(self):
    """Deletes an article."""
    if not self.post:
      return Redirect('/', httpcode=303)
    articleid = self.post.getfirst('id')
    try:
      article = model.Article.FromPrimary(self.connection, articleid)
    except uweb3.model.NotExistError:
      return Redirect('/', httpcode=303)
    article.Delete(self.connection)
    message = 'The Article has been deleted.'
    refresh = '/home'
    return {'message': message, 'refresh': refresh, 'article': article}

  @decorators.adminonly
  def AdminArticle(self, number, title):
    """Returns the editarticle.html template."""
    try:
      article = model.Article.FromPrimary(self.connection, int(number))
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      javascripts = ['validate.js']
      tags = []
      for tag in article.Tags():
        tags.append(tag['name'])
      tags = ', '.join(tags)
    except (uweb3.model.NotExistError, ValueError):
      return Redirect('/', httpcode=303)
    try:
      commentslist = list(article.Comments(self.connection))
      rowtype = True
      for comment in commentslist:
        comment['check'] = False
        rowtype = not rowtype
        comment['date'] = comment['date'].strftime('%Y-%m-%d %H:%M:%S')
        comment['rowtype'] = rowtype and 'Even' or 'Odd'
    except uweb3.model.NotExistError:
      commentslist = None
    return self.parser.Parse('admin/editarticle.html', article=article,
                             tags=tags, commentslist=commentslist,
                             commentform=True, user=self.user,
                             **self.CommonBlocks('Edit article: "%s"'
                                                 % article['title'],
                                                 javascripts=javascripts))

  def SaveTags(self, tags, article):
    """Saves all the given tags, and adds them to the article."""
    notification = ""
    for tag in tags:
      tag = tag.strip()
      if len(tag) > 0 and len(tag) < 25:
        try:
          tag = model.Tags.FromName(self.connection, tag)
        except (uweb3.model.NotExistError, sqlresult.FieldError):
          tag = model.Tags.Create(self.connection, {'name': tag[:25]})
        try:
          model.Articletags.FromPrimary(self.connection, (tag['ID'],
                                                          article['ID']))
        except uweb3.model.NotExistError:
          model.Articletags.Create(self.connection,
                                   {'tagid': tag['ID'],
                                    'articleid': article['ID']})
      elif len(tag) >= 25:
          notification += (
                   "tag '%s' has been skipped because it was too long" % tag)
    return notification

  @decorators.adminonly
  @decorators.checkxsrf
  @decorators.TemplateParser('message.html', 'Success')
  def UpdateArticle(self):
    """Updates an article's information."""
    if not self.post:
      return Redirect('/', httpcode=303)
    try:
      article = model.Article.FromPrimary(self.connection,
                                          self.post.getfirst('article'))
    except uweb3.model.NotExistError:
      return Redirect('/', httpcode=303)
    if self.post.getfirst('title'):
      article['title'] = self.post.getfirst('title')
    if self.post.getfirst('content'):
      article['content'] = self.post.getfirst('content')
    publicstate = self.post.getfirst('public')
    comstate = self.post.getfirst('commentable')
    article['public'] = 'true' if publicstate == 'on' else 'false'
    article['commentable'] = 'true' if comstate == 'on' else 'false'
    now = datetime.datetime.now()
    article['lastchange'] = now.strftime("%Y-%m-%d %H:%M:%S")
    article.Save()
    model.Tags.removeFromArticle(self.connection, article['ID'])
    notification = ''
    if self.post.getfirst('tags'):
      notification = self.SaveTags(self.post.getfirst('tags').split(','),
                                   article)
    message = 'The changes have been saved. %s' % notification
    refresh = '/home'
    return {'message': message, 'refresh': refresh, 'article': article}

  @decorators.adminonly
  @decorators.checkxsrf
  @decorators.TemplateParser('admin/newarticle.html', 'New article')
  def NewArticle(self):
    """Returns the newarticle.html template."""
    article = {}
    article['title'] = self.post.getfirst("title")
    article['tags'] = self.post.getfirst("tags")
    article['content'] = self.post.getfirst("content")
    if article:
      if article['title'] == 'None':
        article['title'] = ''
      if article['content'] == 'None':
         article['content'] = ''
      if article['tags'] == 'None':
         article['tags'] = ''
    return {'article': article}

  @decorators.adminonly
  @decorators.checkxsrf
  @decorators.TemplateParser('message.html', 'Error')
  def AddArticle(self):
    """Adds a new article to the blog."""
    if not self.post:
      return Redirect('/', httpcode=303)
    for item in ['title', 'content', 'public', 'commentable']:
      if not item:
        message = 'The following item needs to be filled out: %s' % item
        refresh = '/admin/newarticle'
        return {'message': message, 'refresh': refresh, 'article': None}
    article = {}
    article['title'] = self.post.getfirst('title')
    if len(article['title']) > 250:
      message = "The provided title is too long."
      return self.RequestMessage(message, 'Error', '/home')
    article['content'] = self.post.getfirst('content')
    publicstate = self.post.getfirst('public')
    comstate = self.post.getfirst('commentable')
    article['public'] = 'true' if publicstate == 'on' else 'false'
    article['commentable'] = 'true' if comstate == 'on' else 'false'
    if article['title'] and article["content"]:
      article['user'] = self.user['ID']
      now = datetime.datetime.now()
      article['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
      article['lastchange'] = article['date']
      article = model.Article.Create(self.connection, article)
      notification = ''
      if self.post.getfirst('tags'):
        notification = self.SaveTags(self.post.getfirst('tags').split(','),
                                     article)
      message = 'The article has been created. %s' % notification
      return self.RequestMessage(message, 'Success', '/home')
    else:
      article['tags'] = self.post.getfirst('tags')
      message = 'Please fill in a title and text'
      refresh = '/admin/newarticle'
      return {'message': message, 'refresh': refresh, 'article': None}
