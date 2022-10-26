-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: job_match_db
-- ------------------------------------------------------
-- Server version	5.5.5-10.9.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `companies` (
  `user_id` int(11) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `description` varchar(10000) NOT NULL,
  `logo_url` varchar(1000) DEFAULT NULL,
  `contact_id` int(11) NOT NULL,
  `sucessful_matches` int(11) DEFAULT 0,
  PRIMARY KEY (`user_id`),
  KEY `fk_companies_contacts1_idx` (`contact_id`),
  KEY `fk_companies_users1_idx` (`user_id`),
  CONSTRAINT `fk_companies_contacts1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_companies_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `contacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `address` varchar(1000) NOT NULL,
  `town_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `fk_contacts_towns1_idx` (`town_id`),
  CONSTRAINT `fk_contacts_towns1` FOREIGN KEY (`town_id`) REFERENCES `towns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_ads`
--

DROP TABLE IF EXISTS `job_ads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `job_ads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(10000) NOT NULL,
  `min_salary` int(11) NOT NULL,
  `max_salary` int(11) NOT NULL,
  `work_place` varchar(50) NOT NULL,
  `status` varchar(50) DEFAULT 'active',
  `company_id` int(11) NOT NULL,
  `town_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_job_ads_towns1_idx` (`town_id`),
  CONSTRAINT `fk_job_ads_towns1` FOREIGN KEY (`town_id`) REFERENCES `towns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_ads`
--

LOCK TABLES `job_ads` WRITE;
/*!40000 ALTER TABLE `job_ads` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_ads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_ads_skills`
--

DROP TABLE IF EXISTS `job_ads_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `job_ads_skills` (
  `job_ad_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  `stars` tinyint(2) NOT NULL,
  PRIMARY KEY (`job_ad_id`,`skill_id`),
  KEY `fk_job_ads_has_skills_skills1_idx` (`skill_id`),
  KEY `fk_job_ads_has_skills_job_ads1_idx` (`job_ad_id`),
  CONSTRAINT `fk_job_ads_has_skills_job_ads1` FOREIGN KEY (`job_ad_id`) REFERENCES `job_ads` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_has_skills_skills1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_ads_skills`
--

LOCK TABLES `job_ads_skills` WRITE;
/*!40000 ALTER TABLE `job_ads_skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_ads_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `match_requests`
--

DROP TABLE IF EXISTS `match_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `match_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resume_id` int(11) NOT NULL,
  `job_ad_id` int(11) NOT NULL,
  `match` tinyint(2) NOT NULL DEFAULT 0,
  `request_from` varchar(45) NOT NULL,
  PRIMARY KEY (`id`,`resume_id`,`job_ad_id`),
  KEY `fk_resumes_has_job_ads_job_ads1_idx` (`job_ad_id`),
  KEY `fk_resumes_has_job_ads_resumes1_idx` (`resume_id`),
  CONSTRAINT `fk_resumes_has_job_ads_job_ads1` FOREIGN KEY (`job_ad_id`) REFERENCES `job_ads` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_resumes_has_job_ads_resumes1` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match_requests`
--

LOCK TABLES `match_requests` WRITE;
/*!40000 ALTER TABLE `match_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `match_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professionals`
--

DROP TABLE IF EXISTS `professionals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `professionals` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `summary` varchar(10000) DEFAULT NULL,
  `busy` tinyint(2) DEFAULT 0,
  `image_url` varchar(1000) DEFAULT NULL,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `fk_professionals_contacts1_idx` (`contact_id`),
  KEY `fk_professionals_users1_idx` (`user_id`),
  CONSTRAINT `fk_professionals_contacts1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_professionals_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professionals`
--

LOCK TABLES `professionals` WRITE;
/*!40000 ALTER TABLE `professionals` DISABLE KEYS */;
/*!40000 ALTER TABLE `professionals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumes`
--

DROP TABLE IF EXISTS `resumes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `resumes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(10000) NOT NULL,
  `min_salary` int(11) NOT NULL,
  `max_salary` int(11) NOT NULL,
  `work_place` varchar(50) NOT NULL,
  `status` varchar(50) DEFAULT 'hidden',
  `professional_id` int(11) NOT NULL,
  `town_id` int(11) NOT NULL,
  `main` tinyint(2) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `fk_resumes_towns1_idx` (`town_id`),
  CONSTRAINT `fk_resumes_towns1` FOREIGN KEY (`town_id`) REFERENCES `towns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumes`
--

LOCK TABLES `resumes` WRITE;
/*!40000 ALTER TABLE `resumes` DISABLE KEYS */;
/*!40000 ALTER TABLE `resumes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumes_skills`
--

DROP TABLE IF EXISTS `resumes_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `resumes_skills` (
  `resume_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  `stars` tinyint(2) NOT NULL,
  PRIMARY KEY (`resume_id`,`skill_id`),
  KEY `fk_resumes_has_skills_skills1_idx` (`skill_id`),
  KEY `fk_resumes_has_skills_resumes1_idx` (`resume_id`),
  CONSTRAINT `fk_resumes_has_skills_resumes1` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_resumes_has_skills_skills1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumes_skills`
--

LOCK TABLES `resumes_skills` WRITE;
/*!40000 ALTER TABLE `resumes_skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `resumes_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `towns`
--

DROP TABLE IF EXISTS `towns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `towns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `towns`
--

LOCK TABLES `towns` WRITE;
/*!40000 ALTER TABLE `towns` DISABLE KEYS */;
INSERT INTO `towns` VALUES (1,'Sofia'),(2,'Plovdiv'),(3,'Ruse'),(4,'Varna'),(5,'Burgas'),(6,'Vidin'),(7,'Montana'),(8,'Pernik'),(9,'Kiustendil'),(10,'Blagoevgrad'),(11,'Vratsa'),(12,'Pazardzhik'),(13,'Smolian'),(14,'Pleven'),(15,'Lovech'),(16,'Veliko Tarnovo'),(17,'Gabrovo'),(18,'Stara Zagora'),(19,'Haskovo'),(20,'Kardzhali'),(21,'Targovishte'),(22,'Sliven'),(23,'Yambol'),(24,'Silistra'),(25,'Razgrad'),(26,'Shumen'),(27,'Dobrich');
/*!40000 ALTER TABLE `towns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name_UNIQUE` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-26 14:45:06
