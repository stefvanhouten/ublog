#!/usr/bin/python
"""Database abstraction model for ublog."""

import binascii
import hashlib

# Custom modules
from uweb3 import model
from . import decorators

class Article(model.Record):
  """Abstraction class for the article table."""

  _PRIMARY_KEY = 'ID'

  @classmethod
  def ByUser(cls, connection, user):
    """Get articles by user."""
    with connection as cursor:
      articles = cursor.Execute("""
                            SELECT *
                            FROM article
                            WHERE user=%s""" % connection.EscapeValues(user))
    for article in articles:
      yield cls(connection, article)

  @classmethod
  def LastN(cls, connection, count=10, public=True):
    """A list of the last N posts that were made. (title and blurb).

    Arguments:
      count: int (opt), the number of posts to yield. Default 10.

    Yields:
      list that specifies the posts id, title and a blurb of content.
      indices: 0:'articleid' (int), 1:'title' (str), 2:'content' (str),
            3:'username' (str), 4:'userid' (int), 5:'date' (str),
            6:'commentcount' (int).
    """
    with connection as cursor:
      articles = cursor.Execute("""
          select
            article.ID,
            article.title,
            article.content,
            user.author,
            article.user,
            article.date,
            count(comment.ID) as comments,
            article.commentable,
            article.public
          from
            user,
            article
              left join comment on (comment.article = article.ID)
          where
            article.public = '%s' and
            article.user = user.ID
          group by article.ID
          order by article.ID desc
          limit %d
          """ % (str(public).lower(), count))
    for article in articles:
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      yield cls(connection, article)

  @classmethod
  def ActiveMonths(cls, connection):
    """Yields all months in which articles were created."""
    with connection as cursor:
      months = cursor.Execute("""
        select
          month(article.date) as month,
          year(article.date) as year,
          count(article.ID) as count
        from
          article
        where
          article.public = 'true'
        group by month, year
        order by month, year desc
        """)
    for month in months:
      yield month

  def Comments(self, connection, limit=10, offset=0):
    """Yield comments that belong to an article, with optional limit and offset.

    Arguments:
      limit:  int (opt), maximum amount of comments to grab.
      offset: int (opt), number of comments to skip before yielding.

    Yields:
      dictionary with the comments index, contents and user information.
      keys: 'index' (int), 'content' (unicode), 'date' (str, ISO-6801),
            'author' (str), 'email' (str), 'website' (str), 'userid' (int)
    """
    with connection as cursor:
      comments = cursor.Select(
        table=('comment', 'user'),
        fields=('comment.ID', 'content', 'author', 'user', 'date'),
        conditions=('comment.user=user.ID', 'comment.article=%i' % self['ID']),
        order=[('date', True)],
        limit=limit,
        offset=offset,
        escape=False)
    for comment in comments:
      yield Comment(connection, comment)

  def Tags(self):
    """Yield tags that belong to an article."""
    with self.connection as cursor:
      tags = cursor.Select(
        table=('articletags', 'tags'),
        fields='name',
        conditions=('articleid=%d' % self['ID'], 'articletags.tagid=tags.ID'))
    return tags

  @classmethod
  def Month(cls, connection, month, year):
    """A quick overview of the posts made in the given month (title and blurb).

    Arguments:
      month: int, number of the month (1-based).
      year:  int, year that the month is in.

    Yields:
      list that specifies the posts id, title and a blurb of content.
      indices: 0:'articleid' (int), 1:'title' (str), 2:'content' (str),
            3:'authorname' (str), 4:'authorid' (int), 5:'date' (str),
            6:'commentcount' (int).
    """
    with connection as cursor:
      articles = cursor.Execute("""
        select
          article.ID,
          article.title,
          article.content,
          user.author,
          article.user,
          article.date,
          count(comment.ID) as comments
        from
          user,
          article
            left join comment on (comment.article = article.ID)
        where
          article.public = 'true' and
          article.user = user.ID and
          month(article.date) = %i and
          year(article.date) = %i
        group by article.ID
        order by article.ID desc
        """ % (int(month), int(year)))
    for article in articles:
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      yield cls(connection, article)

  @classmethod
  def Year(cls, connection, year):
    """A quick overview of the posts made in a given year.

    Arguments:
      year: int, year to provide details of.

    Yields:
      list that specifies the posts id, title and a blurb of content.
      indices: 0:'articleid' (int), 1:'title' (str), 2:'content' (str),
            3:'authorname' (str), 4:'authorid' (int), 5:'date' (str),
            6:'commentcount' (int).
    """
    with connection as cursor:
      articles = cursor.Execute("""
        select
          article.ID,
          article.title,
          article.content,
          user.author,
          article.user,
          article.date,
          count(comment.ID) as comments
        from
          user,
          article
          left join comment on (comment.article = article.ID)
        where
          article.public = 'true' and
          article.user = user.ID and
          year(article.date) = %i
        group by article.ID
        order by article.ID desc
        """ % int(year))
    for article in articles:
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      yield cls(connection, article)

  @classmethod
  def Tag(cls, connection, tag):
    """A quick overview of the posts made in the given month (title and blurb).

    Arguments:
      month: int, number of the month (1-based).
      year:  int, year that the month is in.

    Yields:
      list that specifies the posts id, title and a blurb of content.
      indices: 0:'articleid' (int), 1:'title' (str), 2:'content' (str),
            3:'authorname' (str), 4:'authorid' (int), 5:'date' (str),
            6:'commentcount' (int).
    """
    with connection as cursor:
      articles = cursor.Execute("""
        select
          article.ID,
          article.title,
          article.content,
          user.author,
          article.user,
          article.date,
          count(comment.ID) as comments
        from
          articletags,
          tags,
          user,
          article
            left join comment on (comment.article = article.ID)
        where
          article.public = 'true' and
          article.user = user.ID and
          articletags.articleid = article.ID and
          articletags.tagid = tags.ID and
          tags.name = "%s"
        group by article.ID
        order by article.ID desc
        """ % (tag))
    for article in articles:
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      yield cls(connection, article)

  @classmethod
  def User(cls, connection, userid):
    """Yields all articles written by the given user."""
    with connection as cursor:
      articles = cursor.Execute("""
        select
          article.ID,
          article.title,
          article.content,
          user.author,
          article.user,
          article.date,
          count(comment.ID) as comments
        from
          user,
          article
            left join comment on (comment.article = article.ID)
        where
          article.public = 'true' and
          article.user = user.ID and
          article.user = %s
        group by article.ID
        order by article.ID desc
        """ % (userid))
    for article in articles:
      article['date'] = article['date'].strftime('%Y-%m-%d %H:%M:%S')
      yield cls(connection, article)

  def Delete(self, connection):
    """Deletes all the article's comments before deleting itself."""
    for comment in Comment.ByArticle(connection, self['ID']):
      comment.Delete()
    super(Article, self).Delete()


class Tags(model.Record):
  """Abstraction class for the tags table."""

  @classmethod
  def Tagcloud(cls, connection):
    """Lists all active tags.

    Returns a tuple: (tagid, name, count)

    Count is the number of articles related to the tag.
    """
    with connection as cursor:
      tags = cursor.Select(
        table=('articletags', 'tags', 'article'),
        fields=('tagid', 'name', 'count(tagid) as count'),
        conditions=('articletags.tagid=tags.ID',
                    'articletags.articleid=article.ID',
                    'article.public="true"'),
        group='tagid',
        order=[('count', True)],
        escape=False)
    return (tag for tag in tags)

  @classmethod
  def FromName(cls, connection, name):
    """Get tag by name."""
    with connection as cursor:
      tag = cursor.Execute("""
                            SELECT *
                            FROM tags
                            WHERE name=%s""" % connection.EscapeValues(name))
    if tag:
      return cls(connection, tag)
    raise model.NotExistError(f"There was no tag with name {name}")

  @classmethod
  def removeFromArticle(cls, connection, id):
    """Remove all tags from article with id."""
    with connection as cursor:
      result = cursor.Execute("""
                              DELETE
                              FROM articletags
                              where articleid=%s""" %
                              id)
    return result


class Comment(model.Record):
  """Abstraction class for the comment table."""

  @classmethod
  def ByUser(cls, connection, user):
    """Get comments by user."""
    with connection as cursor:
      comments = cursor.Execute("""
                            SELECT *
                            FROM comment
                            WHERE user=%s""" % connection.EscapeValues(user))
    for comment in comments:
      yield cls(connection, comment)

  @classmethod
  def ByArticle(cls, connection, article):
    """Get comments by article."""
    with connection as cursor:
      comments = cursor.Execute("""
                            SELECT *
                            FROM comment
                            WHERE article=%s"""
                                % connection.EscapeValues(article))
    for comment in comments:
      yield cls(connection, comment)


class User(model.Record):
  """Abstraction class for the user table."""
  SALT_BYTES = 8

  @classmethod
  def FromName(cls, connection, username):
    """Returns a User object based on the given username."""
    with connection as cursor:
      safe_name = connection.EscapeValues(username)
      user = cursor.Select(
          table=cls.TableName(),
          conditions='name=%s' % safe_name)
    if not user:
      raise cls.NotExistError('No user with name %r' % username)
    return cls(connection, user[0])

  @classmethod
  def HashPassword(cls, password, salt=None):
    if not salt:
      salt = cls.SaltBytes()
    if (len(salt) * 3) / 4 - salt.decode('utf-8').count('=', -2) != cls.SALT_BYTES:
      raise ValueError('Salt is of incorrect length. Expected %d, got: %d' % (
          cls.SALT_BYTES, len(salt)))
    m = hashlib.sha256()
    m.update(password.encode("utf-8") + binascii.hexlify(salt))
    password = m.hexdigest()
    return { 'password': password, 'salt': salt }

  @classmethod
  def SaltBytes(cls):
    """Returns the configured number of random bytes for the salt."""
    random_bytes = os.urandom(cls.SALT_BYTES)
    return base64.b64encode(random_bytes).decode('utf-8').encode('utf-8') #we do this to cast this byte to utf-8

  def UpdatePassword(self, plaintext):
    """Stores a new password hash and salt, from the given plaintext."""
    self.update(self.HashPassword(plaintext))
    self.Save()

  def VerifyChallenge(self, attempt, challenge):
    """Verifies the password hash against the stored hash.
    Both the password hash (attempt) and the challenge should be provided
    as raw bytes.
    """
    password = binascii.hexlify(self['password'])
    actual_pass = hashlib.sha256(password + binascii.hexlify(challenge)).digest()
    return attempt == actual_pass

  def VerifyPlaintext(self, plaintext):
    """Verifies a given plaintext password."""
    salted = self.HashPassword(plaintext, self['salt'].encode('utf-8'))['password']
    return salted == self['password']


  @classmethod
  def FromEmail(cls, connection, email):
    """Get user by email."""
    with connection as cursor:
      userquery = cursor.Execute("""
                            SELECT *
                            FROM user
                            WHERE name=%s"""
                                 % connection.EscapeValues(email))
    if userquery:
      return cls(connection, userquery[0])
    else:
      return False

  @classmethod
  def FromAuthor(cls, connection, name):
    """Get user by id."""
    with connection as cursor:
      userquery = cursor.Execute("""
                            SELECT *
                            FROM user
                            WHERE author=%s"""
                                 % connection.EscapeValues(name))
    if userquery:
      return cls(connection, userquery[0])
    else:
      return False

  @classmethod
  def FromID(cls, connection, id):
    """Get user by id."""
    with connection as cursor:
      userquery = cursor.Execute("""
                            SELECT *
                            FROM user
                            WHERE ID=%s"""
                                 % connection.EscapeValues(id))
    if userquery:
      return cls(connection, userquery[0])
    else:
      return False

  def Comments(self, connection, limit=10, offset=0):
    """Yield comments that belong to a user, with optional limit and offset.

    Arguments:
      limit:  int (opt), maximum amount of comments to grab.
      offset: int (opt), number of comments to skip before yielding.

    Yields:
      dictionary with the comments index, contents and author information.
      keys: 'index' (int), 'content' (unicode), 'date' (str, ISO-6801),
            'name' (str), 'email' (str), 'website' (str), 'authorid' (int)
    """
    with connection as cursor:
      comments = cursor.Select(
        table=('comment', 'article'),
        fields=('comment.ID', 'comment.content', 'comment.date',
                'comment.user', 'comment.article'),
        conditions=('comment.user=%i' % self['ID'],
                    'article.ID=comment.article'),
        order=[('article.ID', True), ('date', True)],
        limit=limit,
        offset=offset,
        escape=False)
    for comment in comments:
      yield comment

  @classmethod
  def authors(self, connection):
    """Returns all authors."""
    with connection as cursor:
      users = cursor.Execute("""
        select
        user.ID, author,
        count(article.user) as count
        FROM user, article
        WHERE user.admin = true
        AND user.active = true
        AND user.ID = article.user
        AND article.public = true
        GROUP BY user.ID
        """)
    for user in users:
      yield user

  def Delete(self, connection):
    """Deletes all articles and comments before deleting itself."""
    for comment in Comment.ByUser(connection, self['ID']):
      comment.Delete()
    for article in Article.ByUser(connection, self['ID']):
      article.Delete(self.connection)
    super(User, self).Delete()


class Articletags(model.Record):
  """Abstraction class for the articletags table."""

  _PRIMARY_KEY = 'tagid', 'articleid'
"""Abstraction for the `user` table."""
