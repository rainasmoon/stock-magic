-- MySQL dump 10.17  Distrib 10.3.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: stocks
-- ------------------------------------------------------
-- Server version	10.3.25-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `calender`
--

DROP TABLE IF EXISTS `calender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calender` (
  `cal_date` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`cal_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `model_ev_mid`
--

DROP TABLE IF EXISTS `model_ev_mid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_ev_mid` (
  `state_dt` varchar(50) NOT NULL,
  `stock_code` varchar(45) NOT NULL,
  `resu_predict` decimal(20,2) DEFAULT NULL,
  `resu_real` decimal(20,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `model_ev_resu`
--

DROP TABLE IF EXISTS `model_ev_resu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_ev_resu` (
  `state_dt` varchar(50) NOT NULL DEFAULT '',
  `stock_code` varchar(45) NOT NULL DEFAULT '',
  `acc` decimal(20,4) DEFAULT NULL,
  `recall` decimal(20,4) DEFAULT NULL,
  `f1` decimal(20,4) DEFAULT NULL,
  `acc_neg` decimal(20,4) DEFAULT NULL,
  `bz` varchar(45) DEFAULT NULL,
  `predict` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`state_dt`,`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_capital`
--

DROP TABLE IF EXISTS `my_capital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `my_capital` (
  `capital` decimal(30,2) NOT NULL,
  `money_lock` decimal(30,2) DEFAULT NULL,
  `money_rest` decimal(30,2) DEFAULT NULL,
  `deal_action` varchar(45) DEFAULT NULL,
  `stock_code` varchar(45) DEFAULT NULL,
  `deal_price` decimal(30,2) DEFAULT NULL,
  `stock_vol` int(20) DEFAULT NULL,
  `profit` decimal(30,2) DEFAULT NULL,
  `profit_rate` decimal(20,2) DEFAULT NULL,
  `bz` varchar(45) DEFAULT NULL,
  `state_dt` varchar(45) DEFAULT NULL,
  `seq` int(11) NOT NULL AUTO_INCREMENT,
  `score` decimal(20,6) DEFAULT NULL,
  PRIMARY KEY (`seq`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_stock_pool`
--

DROP TABLE IF EXISTS `my_stock_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `my_stock_pool` (
  `stock_code` varchar(50) NOT NULL,
  `buy_price` decimal(20,2) DEFAULT NULL,
  `hold_vol` int(11) DEFAULT NULL,
  `hold_days` int(11) DEFAULT 1,
  PRIMARY KEY (`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_all`
--

DROP TABLE IF EXISTS `stock_all`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_all` (
  `state_dt` varchar(45) NOT NULL,
  `stock_code` varchar(45) NOT NULL,
  `open` decimal(20,2) DEFAULT NULL,
  `close` decimal(20,2) DEFAULT NULL,
  `high` decimal(20,2) DEFAULT NULL,
  `low` decimal(20,2) DEFAULT NULL,
  `vol` int(20) DEFAULT NULL,
  `amount` decimal(30,2) DEFAULT NULL,
  `pre_close` decimal(20,2) DEFAULT NULL,
  `amt_change` decimal(20,2) DEFAULT NULL,
  `pct_change` decimal(20,2) DEFAULT NULL,
  `big_order_cntro` decimal(20,2) DEFAULT NULL,
  `big_order_delt` decimal(20,2) DEFAULT NULL,
  PRIMARY KEY (`state_dt`,`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_index`
--

DROP TABLE IF EXISTS `stock_index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_index` (
  `date` char(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `open` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `code` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_info`
--

DROP TABLE IF EXISTS `stock_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_info` (
  `state_dt` varchar(45) NOT NULL,
  `stock_code` varchar(45) NOT NULL,
  `open` decimal(20,2) DEFAULT NULL,
  `close` decimal(20,2) DEFAULT NULL,
  `high` decimal(20,2) DEFAULT NULL,
  `low` decimal(20,2) DEFAULT NULL,
  `vol` int(20) DEFAULT NULL,
  `amount` decimal(30,2) DEFAULT NULL,
  `pre_close` decimal(20,2) DEFAULT NULL,
  `amt_change` decimal(20,2) DEFAULT NULL,
  `pct_change` decimal(20,2) DEFAULT NULL,
  `big_order_cntro` decimal(20,2) DEFAULT NULL,
  `big_order_delt` decimal(20,2) DEFAULT NULL,
  PRIMARY KEY (`state_dt`,`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-19 20:33:33
