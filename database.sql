-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.14-log - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for telemetry
CREATE DATABASE IF NOT EXISTS `telemetry` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `telemetry`;


-- Dumping structure for table telemetry.couple
CREATE TABLE IF NOT EXISTS `couple` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `device` int(10) NOT NULL,
  `sim` int(10) NOT NULL,
  `couple_date` date NOT NULL,
  `assigned_to` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device` (`device`),
  KEY `sim` (`sim`),
  CONSTRAINT `device` FOREIGN KEY (`device`) REFERENCES `device` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sim` FOREIGN KEY (`sim`) REFERENCES `sim` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table telemetry.device
CREATE TABLE IF NOT EXISTS `device` (
  `id` int(10) NOT NULL COMMENT 'auto increment?',
  `delivery_date` date NOT NULL,
  `provider` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL,
  `model` varchar(20) NOT NULL,
  `serial` int(14) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table telemetry.sim
CREATE TABLE IF NOT EXISTS `sim` (
  `id` int(10) NOT NULL COMMENT 'auto increment?',
  `delivery_date` date NOT NULL,
  `carrier` varchar(20) NOT NULL,
  `number` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
