-- MySQL dump 10.19  Distrib 10.3.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: fitjourney
-- ------------------------------------------------------
-- Server version	10.3.34-MariaDB-0ubuntu0.20.04.1

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
-- Table structure for table `COACHEDBY`
--

DROP TABLE IF EXISTS `COACHEDBY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `COACHEDBY` (
  `client_id` int(11) NOT NULL,
  `coach_id` int(11) NOT NULL,
  `starting_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`client_id`,`coach_id`,`starting_date`),
  KEY `coach_id` (`coach_id`),
  CONSTRAINT `COACHEDBY_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `USER` (`id`),
  CONSTRAINT `COACHEDBY_ibfk_2` FOREIGN KEY (`coach_id`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `COACHEDBY`
--

LOCK TABLES `COACHEDBY` WRITE;
/*!40000 ALTER TABLE `COACHEDBY` DISABLE KEYS */;
INSERT INTO `COACHEDBY` VALUES (11,2,'2022-05-31','2022-08-31'),(11,2,'2022-06-01','2022-12-01'),(11,2,'2022-06-02','2022-12-02'),(13,12,'2022-05-31','2022-08-31'),(16,14,'2022-06-09','2022-09-09'),(17,2,'2022-05-31','2022-08-31'),(21,2,'2022-06-02','2022-09-02');
/*!40000 ALTER TABLE `COACHEDBY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `COACHING_REVIEW`
--

DROP TABLE IF EXISTS `COACHING_REVIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `COACHING_REVIEW` (
  `id` int(11) NOT NULL,
  `satisfaction` int(11) NOT NULL,
  `support` int(11) NOT NULL,
  `disponibility` int(11) NOT NULL,
  `advice` int(11) NOT NULL,
  `target_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `target_id` (`target_id`),
  CONSTRAINT `COACHING_REVIEW_ibfk_1` FOREIGN KEY (`id`) REFERENCES `REVIEW` (`id`),
  CONSTRAINT `COACHING_REVIEW_ibfk_2` FOREIGN KEY (`target_id`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `COACHING_REVIEW`
--

LOCK TABLES `COACHING_REVIEW` WRITE;
/*!40000 ALTER TABLE `COACHING_REVIEW` DISABLE KEYS */;
INSERT INTO `COACHING_REVIEW` VALUES (1,9,10,8,6,2),(2,10,7,8,9,2),(3,7,6,6,10,2);
/*!40000 ALTER TABLE `COACHING_REVIEW` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PHYSICAL_INFO`
--

DROP TABLE IF EXISTS `PHYSICAL_INFO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PHYSICAL_INFO` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `height` int(11) NOT NULL,
  `weight` decimal(4,1) NOT NULL,
  `age` int(11) NOT NULL,
  `bmi` decimal(3,1) NOT NULL,
  `bmr` decimal(5,1) NOT NULL,
  `bodyfat_percentage` decimal(3,1) NOT NULL,
  `muscle_mass_percentage` decimal(3,1) NOT NULL,
  `bone_mass_percentage` decimal(3,1) NOT NULL,
  `water_percentage` decimal(3,1) NOT NULL,
  `protein_percentage` decimal(3,1) NOT NULL,
  `bone_mass` decimal(3,1) NOT NULL,
  `muscle_mass` decimal(4,1) NOT NULL,
  `bodyfat_mass` decimal(4,1) NOT NULL,
  `leanbody_mass` decimal(4,1) NOT NULL,
  `fat_visceral` decimal(4,1) NOT NULL,
  `body_age` int(11) NOT NULL,
  `date` date NOT NULL,
  `front_photo` varchar(250) DEFAULT NULL,
  `right_side_photo` varchar(250) DEFAULT NULL,
  `left_side_photo` varchar(250) DEFAULT NULL,
  `back_photo` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `PHYSICAL_INFO_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PHYSICAL_INFO`
--

LOCK TABLES `PHYSICAL_INFO` WRITE;
/*!40000 ALTER TABLE `PHYSICAL_INFO` DISABLE KEYS */;
INSERT INTO `PHYSICAL_INFO` VALUES (1,11,184,96.9,21,28.6,2019.0,26.4,67.9,3.7,49.1,14.9,3.5,65.8,25.6,71.3,10.0,24,'2022-05-30',NULL,NULL,NULL,NULL),(2,11,184,97.8,21,28.9,2045.0,27.2,68.1,3.6,50.1,15.0,3.6,66.0,26.1,71.5,10.0,24,'2022-04-30',NULL,NULL,NULL,NULL),(3,11,184,99.3,20,29.3,2054.0,27.3,67.0,3.6,50.4,12.6,3.6,66.6,27.1,72.2,10.0,24,'2022-03-30',NULL,NULL,NULL,NULL),(4,11,184,100.1,20,29.5,2065.0,27.5,66.8,3.6,50.3,12.5,3.6,66.8,27.5,72.5,10.0,24,'2022-02-28',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `PHYSICAL_INFO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PROGRAM`
--

DROP TABLE IF EXISTS `PROGRAM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PROGRAM` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL,
  `pdf` longblob DEFAULT NULL,
  `date` date DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `coach_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `coach_id` (`coach_id`),
  CONSTRAINT `PROGRAM_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `USER` (`id`),
  CONSTRAINT `PROGRAM_ibfk_2` FOREIGN KEY (`coach_id`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PROGRAM`
--

LOCK TABLES `PROGRAM` WRITE;
/*!40000 ALTER TABLE `PROGRAM` DISABLE KEYS */;
/*!40000 ALTER TABLE `PROGRAM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PURCHASE`
--

DROP TABLE IF EXISTS `PURCHASE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PURCHASE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `subscription_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `PURCHASE_ibfk_1` (`client_id`),
  KEY `PURCHASE_ibfk_2` (`subscription_id`),
  CONSTRAINT `PURCHASE_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `USER` (`id`),
  CONSTRAINT `PURCHASE_ibfk_2` FOREIGN KEY (`subscription_id`) REFERENCES `SUBSCRIPTION` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PURCHASE`
--

LOCK TABLES `PURCHASE` WRITE;
/*!40000 ALTER TABLE `PURCHASE` DISABLE KEYS */;
INSERT INTO `PURCHASE` VALUES (1,11,'2022-05-31',2),(2,13,'2022-05-31',2),(3,16,'2022-06-09',2),(5,17,'2022-05-31',2),(7,21,'2022-06-02',2);
/*!40000 ALTER TABLE `PURCHASE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REVIEW`
--

DROP TABLE IF EXISTS `REVIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `REVIEW` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(250) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `type` varchar(15) NOT NULL,
  `id_client` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_client` (`id_client`),
  CONSTRAINT `REVIEW_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REVIEW`
--

LOCK TABLES `REVIEW` WRITE;
/*!40000 ALTER TABLE `REVIEW` DISABLE KEYS */;
INSERT INTO `REVIEW` VALUES (1,'Love this coach','2022-05-30 09:49:40','COACHING',11),(2,'yes','2022-05-30 10:30:14','COACHING',11),(3,'','2022-06-01 14:33:56','COACHING',11),(4,'This was good','2022-06-01 14:34:59','WORKOUT',11),(5,'It was amazing :)','2022-06-03 15:06:48','WORKOUT',11);
/*!40000 ALTER TABLE `REVIEW` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ROLE`
--

DROP TABLE IF EXISTS `ROLE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ROLE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ROLE`
--

LOCK TABLES `ROLE` WRITE;
/*!40000 ALTER TABLE `ROLE` DISABLE KEYS */;
INSERT INTO `ROLE` VALUES (1,'Client'),(2,'Coach');
/*!40000 ALTER TABLE `ROLE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SESSION`
--

DROP TABLE IF EXISTS `SESSION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SESSION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `duration` time NOT NULL,
  `workout_type` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `coach_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `workout_type` (`workout_type`),
  KEY `client_id` (`client_id`),
  KEY `coach_id` (`coach_id`),
  CONSTRAINT `SESSION_ibfk_1` FOREIGN KEY (`workout_type`) REFERENCES `WORKOUT_TYPE` (`id`),
  CONSTRAINT `SESSION_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `USER` (`id`),
  CONSTRAINT `SESSION_ibfk_3` FOREIGN KEY (`coach_id`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SESSION`
--

LOCK TABLES `SESSION` WRITE;
/*!40000 ALTER TABLE `SESSION` DISABLE KEYS */;
INSERT INTO `SESSION` VALUES (1,'2022-05-31 10:30:00','2022-05-31 12:30:00','02:00:00',1,11,2),(2,'2022-05-31 14:30:00','2022-05-31 15:30:00','01:00:00',1,13,12),(3,'2022-06-11 13:00:00','2022-06-11 14:00:00','01:00:00',3,16,14),(4,'2022-06-01 11:30:00','2022-06-01 12:30:00','01:00:00',1,16,14),(5,'2022-05-31 12:00:00','2022-05-31 13:00:00','01:00:00',1,11,2),(6,'2022-06-02 18:15:00','2022-06-02 20:15:00','02:00:00',3,11,2),(7,'2022-06-15 18:00:00','2022-06-15 20:00:00','02:00:00',1,11,2);
/*!40000 ALTER TABLE `SESSION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUBSCRIPTION`
--

DROP TABLE IF EXISTS `SUBSCRIPTION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SUBSCRIPTION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) DEFAULT NULL,
  `cost` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `duration` (`duration`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUBSCRIPTION`
--

LOCK TABLES `SUBSCRIPTION` WRITE;
/*!40000 ALTER TABLE `SUBSCRIPTION` DISABLE KEYS */;
INSERT INTO `SUBSCRIPTION` VALUES (1,'1 Month',100,1),(2,'3 Months',280,3),(3,'6 Months',500,6);
/*!40000 ALTER TABLE `SUBSCRIPTION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USER` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `surname` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` blob NOT NULL,
  `birthdate` date NOT NULL,
  `card_id` varchar(32) DEFAULT NULL,
  `profile_pic` varchar(250) DEFAULT NULL,
  `city` varchar(64) DEFAULT NULL,
  `country` varchar(64) DEFAULT NULL,
  `address` varchar(64) DEFAULT NULL,
  `npa` varchar(32) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `card_id` (`card_id`),
  KEY `role` (`role`),
  CONSTRAINT `USER_ibfk_1` FOREIGN KEY (`role`) REFERENCES `ROLE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES (2,'John','Doe','john.doe@gmail.com','84fa858c2fbb74e2a6d92b4044f6561485afd30973391c8077e8cf38cda1a3b99701331284a53f8c77d4d84e85524728bdb6b15a345ff476eec5e2976871d17c96db2a2d6727f97dcc38eeeec5288dfb454e68789ef9f51efa29414c69f480ee','1995-06-10',NULL,'7c622d4d-e0d3-11ec-898e-2c4d544bcd7d_image.png','Bernex','Suisse','Chemin des Curiades 43','1233','2022-05-30 07:25:48',2),(11,'Thomas','Fujise','thomasf1536@gmail.com','f618c79853d52abbc17a20fd6fed09f69f9609a2ef14156f6095a74023458c5eeadcb73719b709669795e4d36f0966a59e5f8b5f201b6b4912f38bf7bdafc6ef9999e5f5eb043336cd442852e4bc44799884920acd050271da88d61bfc2eff69','2001-04-13','243 94 173 12','8551e31c-e183-11ec-b8d0-2c4d544bcd7d_tatum.jpg','Bernex','','Chemin des Curiades 35','','2022-05-30 07:45:12',1),(12,'David','Fernandez','david.fr@gmail.com','c3869ccd87b3f3d6340e6667d695ec6a9ffd122cad2658f87e592249af4e2175d8b473efafcd5a165eb0d11a791e624e3efa6a4a4709a115f59d47f17194e90deb35d57d711c11862eb778273c6ea3107c51f23c7b7eae86a57b9e63c219633d','1998-08-10',NULL,NULL,NULL,NULL,NULL,NULL,'2022-05-30 08:09:31',2),(13,'Diogo','Almeida','diogo.ogoid@gmail.com','49718d3fb7a6d2f34c71cad53c1424af2cdc2d6ccbcebd6b98d223d1691351e26ed9e14ec8e00a7afeb369a3129cd826859c4a296099a6fd0e4d243a931058a318ea9d3933b9794bc4e1ed5f4783f5ec211fdaaed8c10db8bd7616f795f0d601','2001-09-18',NULL,'default_profile_pic.png',NULL,NULL,NULL,NULL,'2022-05-30 08:10:24',1),(14,'Diogo','Canas','diogo@gmail.com','c17751940558348f90b14a8bd23be7177e585156f04f5d8c3a228318b05cba6bf9592c9212aa66d1d8ed6c1a7a90edd953be0d61fb055e159059e5160e08922e31eaabf60adf38b9e10497f88f6553d0ac6e0a3a3365d705d6818c5a271b7f91','2001-04-13',NULL,NULL,NULL,NULL,NULL,NULL,'2022-05-30 08:25:22',2),(15,'David','Fuji','test@gmail.com','8b4ca35ab80f2d0595a07e6ba1c66ba0a6c3bcc2c44bdb39b63d86efd1562dda5d31eeeeac0f306d5ecc77d0ca003efb291d093f01d32e197a5b61def0137e4f54c40e8594fcc69817f18f9c22fc8a978b255747587300de2ec8590590748255','2001-09-18',NULL,NULL,NULL,NULL,NULL,NULL,'2022-05-30 08:41:53',2),(16,'Francis','Oliv','franco.oliv@gmail.com','f3479b3f36a7e2e8960cd6fdf9807058bcb182480238a1a92fb8ed97245be23dfec0c332527a2d4ea79a15ce46ccf87c08220eac40a710a6faf18d08aff1eafe5b6c4d10e7c6ee751fd04f0b16976552c2d1abd137a6236697a51d9de63ea2ba','2000-04-19',NULL,'default_profile_pic.png',NULL,NULL,NULL,NULL,'2022-05-30 09:00:45',1),(17,'Tom','Ford','thomas.fjs@eduge.ch','908c1dace646c7d70601787adf158765889aeee842d078c092009b2f840a62c601b0cda90a0c3ce85777725752674d371892e8df08931f31a3e51656a53372558ad615fe2d01a7323a164720b64b69a38aa37c897c4af52084b2e28a7352b81e','2001-04-13',NULL,'default_profile_pic.png',NULL,NULL,NULL,NULL,'2022-05-31 13:20:49',1),(18,'Josh','Dobo','dobo@gmail.com','79a80f78fb635e7e723143907901435bc6e4e07858b047c42a8959860334fd871eef57d553543438723b82562a71ec933c516451932c3ae7df2e0a4261b24cb1b18f2725be18b252c3c9dd17a4a3df9917a54e7d77f4f5a7d56af63626aff851','2002-09-21',NULL,NULL,NULL,NULL,NULL,NULL,'2022-06-01 09:21:39',2),(19,'Josh','Dobo','adobo@gmail.com','9fdf3865e70edfc545b76ed71f0f26622ced7e47d9622d6f323017ec580c8935ec029b280181a510acc52e2f27ce6e59f49b5f35b9a57f46626f0ccca38a3e55dc1b2f51c4860f3c7f83f7ec16c2404bde9ce092af2425453f5ae8757267c472','2002-09-21',NULL,NULL,NULL,NULL,NULL,NULL,'2022-06-01 09:22:30',2),(20,'Tom','Test','test2@gmail.com','894d51ba59189f6e875795be46fe0c8158d03074577ee9f673cee5828b009e8ad96f8178d1d032c9f90249c197b26c364047eae99ac0517cceedc347485feac6b04878b7ac4b24ff5b11425dc6d4ebc586137b76750d062abc199ce47096c554','2000-07-19',NULL,NULL,NULL,NULL,NULL,NULL,'2022-06-01 12:21:41',2),(21,'Diogo','Fuji','test3@gmail.com','20e28eb847b95f7c0327fe4fa7aa73649730b25edf4a44d66502ee3e8d660d3bbbd2206f93113fad0e2c8ce2608a5029fcdc49dd57e5403e22b74123dd6c73d9b34cec31977b5fba7bd143ed9e759ae65ee83df80749feae4a21e185df0f1a70','2001-08-17',NULL,'default_profile_pic.png',NULL,NULL,NULL,NULL,'2022-06-01 12:29:31',1);
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WORKOUT`
--

DROP TABLE IF EXISTS `WORKOUT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WORKOUT` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workout_type` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `heart_rate_max` decimal(10,0) DEFAULT NULL,
  `heart_rate_min` decimal(10,0) DEFAULT NULL,
  `heart_rate_avg` decimal(10,0) DEFAULT NULL,
  `calories` decimal(10,0) DEFAULT NULL,
  `active_calories` decimal(10,0) DEFAULT NULL,
  `distance` decimal(10,0) DEFAULT NULL,
  `pace_avg` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `workout_type` (`workout_type`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `WORKOUT_ibfk_1` FOREIGN KEY (`workout_type`) REFERENCES `WORKOUT_TYPE` (`id`),
  CONSTRAINT `WORKOUT_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `USER` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WORKOUT`
--

LOCK TABLES `WORKOUT` WRITE;
/*!40000 ALTER TABLE `WORKOUT` DISABLE KEYS */;
INSERT INTO `WORKOUT` VALUES (1,1,11,'2022-05-29 00:00:00','01:30:00',163,67,103,698,603,NULL,NULL),(2,3,11,'2022-05-27 19:00:00','01:00:00',160,69,113,980,873,10,'00:06:00'),(3,2,11,'2022-05-26 17:30:00','01:00:00',167,72,109,673,606,6,'00:10:00'),(4,1,11,'2022-02-21 16:00:00','01:00:00',143,69,102,623,589,NULL,NULL),(6,1,11,'2022-06-03 11:24:50','00:01:31',66,NULL,56,3,NULL,0,NULL),(7,1,11,'2022-06-03 15:03:23','00:01:09',105,NULL,100,6,NULL,0,NULL);
/*!40000 ALTER TABLE `WORKOUT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WORKOUT_REVIEW`
--

DROP TABLE IF EXISTS `WORKOUT_REVIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WORKOUT_REVIEW` (
  `id` int(11) NOT NULL,
  `difficulty` int(11) NOT NULL,
  `feel` int(11) NOT NULL,
  `fatigue` int(11) NOT NULL,
  `energy` int(11) NOT NULL,
  `target_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `target_id` (`target_id`),
  CONSTRAINT `WORKOUT_REVIEW_ibfk_1` FOREIGN KEY (`id`) REFERENCES `REVIEW` (`id`),
  CONSTRAINT `WORKOUT_REVIEW_ibfk_2` FOREIGN KEY (`target_id`) REFERENCES `WORKOUT` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WORKOUT_REVIEW`
--

LOCK TABLES `WORKOUT_REVIEW` WRITE;
/*!40000 ALTER TABLE `WORKOUT_REVIEW` DISABLE KEYS */;
INSERT INTO `WORKOUT_REVIEW` VALUES (4,5,9,5,9,1),(5,10,10,1,10,7);
/*!40000 ALTER TABLE `WORKOUT_REVIEW` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WORKOUT_TYPE`
--

DROP TABLE IF EXISTS `WORKOUT_TYPE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WORKOUT_TYPE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `logo` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WORKOUT_TYPE`
--

LOCK TABLES `WORKOUT_TYPE` WRITE;
/*!40000 ALTER TABLE `WORKOUT_TYPE` DISABLE KEYS */;
INSERT INTO `WORKOUT_TYPE` VALUES (1,'Weightlifting','Weight','weightlifting.svg'),(2,'Cycling','Cardio cycling','cycling.svg'),(3,'Running','Cardio running','running.svg');
/*!40000 ALTER TABLE `WORKOUT_TYPE` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-03 16:11:05