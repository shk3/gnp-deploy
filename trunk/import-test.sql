-- phpMyAdmin SQL Dump
-- version 3.5.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 26, 2013 at 10:55 PM
-- Server version: 5.00.15
-- PHP Version: 5.3.13

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cdnlab`
--
USE `cdnlab`;
-- --------------------------------------------------------

--
-- Table structure for table `roundtrip`
--

DROP TABLE IF EXISTS `roundtrip`;
CREATE TABLE IF NOT EXISTS `roundtrip` (
  `id` bigint(33) NOT NULL auto_increment,
  `ip` bigint(32) NOT NULL default '0',
  `done` tinyint(1) NOT NULL default '0',
  `online` tinyint(1) NOT NULL default '1',
  `min_roundtrip` int(11) NOT NULL default '-1',
  `trails` int(11) NOT NULL default '0',
  `last_change` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`),
  KEY `ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=25601 ;

--
-- Dumping data for table `roundtrip`
--

INSERT INTO `roundtrip` (`id`, `ip`, `done`, `online`, `min_roundtrip`, `trails`, `last_change`) VALUES
(1, 134744072, 0, 1, -1, 0, '2013-07-26 09:24:42'),
(2, 134744073, 0, 1, -1, 0, '2013-07-26 09:24:42'),
(3, 134743044, 0, 1, -1, 0, '2013-07-26 09:24:42');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
