--
-- Table structure for table `article`
--

CREATE TABLE IF NOT EXISTS `article` (
  `ID` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `user` smallint(5) unsigned NOT NULL,
  `date` datetime NOT NULL,
  `lastchange` datetime NOT NULL,
  `content` text COLLATE utf8_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `public` enum('true','false') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'false',
  `commentable` enum('true','false') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'false',
  PRIMARY KEY (`ID`),
  KEY `author` (`user`),
  KEY `public` (`public`,`commentable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `articletags`
--

CREATE TABLE IF NOT EXISTS `articletags` (
   `articleid` mediumint(8) unsigned NOT NULL,
   `tagid` smallint(5) unsigned NOT NULL,
   PRIMARY KEY (`articleid`,`tagid`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
   `ID` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
   `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
   `name` varchar(45) NOT NULL,
   `admin` enum('true','false') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
   `password` varbinary(255),
   `salt` varbinary(45),
   `active` enum('true','false') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
   PRIMARY KEY (`ID`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE IF NOT EXISTS `comment` (
   `ID` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
   `article` smallint(5) unsigned NOT NULL,
   `user` smallint(5) unsigned NOT NULL,
   `date` datetime NOT NULL,
   `content` text COLLATE utf8_unicode_ci NOT NULL,
   PRIMARY KEY (`ID`),
   KEY `article` (`article`,`user`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- --------------------------------------------------------

--
-- Table structure for table `tags`
--

CREATE TABLE IF NOT EXISTS `tags` (
   `ID` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
   `name` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
   PRIMARY KEY (`ID`),
   KEY `name` (`name`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- --------------------------------------------------------

--
-- Table structure for table `challenge`
--

CREATE TABLE IF NOT EXISTS `challenge` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `user` smallint(5) unsigned NOT NULL,
  `remote` varchar(45) NOT NULL,
  `challenge` varbinary(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `userloginnumber_idx` (`user`),
  CONSTRAINT `userloginnumber` FOREIGN KEY (`user`) REFERENCES `user` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `session`
--

CREATE TABLE IF NOT EXISTS `session` (
  `session` binary(16) NOT NULL,
  `remote` varchar(39) COLLATE utf8_unicode_ci NOT NULL,
  `user` smallint(5) unsigned NOT NULL,
  `expiry` datetime NOT NULL,
  `iplocked` tinyint(1) NOT NULL,
  PRIMARY KEY (`session`,`remote`),
  KEY `client` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- ------------------------------------------------
