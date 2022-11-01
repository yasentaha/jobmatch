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
  `successful_matches` int(11) DEFAULT 0,
  PRIMARY KEY (`user_id`),
  KEY `fk_companies_users1_idx1` (`user_id`),
  CONSTRAINT `fk_companies_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (32,'Telerik Academy','Telerik Academy trains Bulgaria digital builders: school students, young professionals and career switchers. Connects companies with top tech talent.',0),(34,'Coca Cola Bulgaria','In 2018 Coca-Cola opens the second largest IT HUB in Sofia. The main areas of activity are related to the creation of innovative digital solutions, development of software products, IoT.',0),(35,'Schwarz IT Bulgaria','At Schwarz IT, we take care of the entire digital infrastructure and all software solutions for all users in our retail divisions Lidl and Kaufland, in Schwarz Produktion, and in our environmental services provider PreZero.',0),(36,'Childish - Software Development Company','Childish is a software development company. Our name comes from our values – we admire and preach honesty and creativity.',0),(37,'Strypes','We provide custom end-to-end software solutions that create business impact. Nearsurance is our way of outsourcing.',0),(39,'HedgeServ','HedgeServ is a top-ranked global, independent fund administrator. HedgeServ provides uniquely client-centric service and is the industry’s leader in technology.',0),(40,'Progress','Dedicated to propelling business forward in a technology-driven world, Progress (Nasdaq: PRGS) helps businesses drive faster cycles of innovation, fuel momentum and accelerate their path to success.',0),(42,'Accedia','Accedia is a professional IT services company, specializing in Technology Consulting, Software Development and IT Operations Management.',0),(43,'EnhanCV','Enhancv is a SaaS startup built around a web platform for creating modern resumes. Our tool helps you highlight your achievements, attitude, and personality, so you can tell your story with confidence.',0);
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
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
  `town_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `views` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `fk_job_ads_towns1_idx` (`town_id`),
  KEY `fk_job_ads_users1_idx` (`company_id`),
  CONSTRAINT `fk_job_ads_towns1` FOREIGN KEY (`town_id`) REFERENCES `towns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_users1` FOREIGN KEY (`company_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
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
  PRIMARY KEY (`user_id`),
  KEY `fk_professionals_users1_idx1` (`user_id`),
  CONSTRAINT `fk_professionals_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professionals`
--

LOCK TABLES `professionals` WRITE;
/*!40000 ALTER TABLE `professionals` DISABLE KEYS */;
INSERT INTO `professionals` VALUES (1,'Jeff','Weiner','Creator of LinkedIn, Entrepreneur',0),(2,'Yasen','Taha','Junior Software Developer with Python',0),(3,'Krasimir','Bozhilov','Junior Software Developer with Python',0),(4,'Dimityr','Vasilev','Junior Software Developer',0),(5,'Nikolay','Likyov','Junior Software Developer',0),(6,'Rossitsa','Racheva','Senior Software Developer',0),(7,'Evgeni','Vladimirov','Full-Stack Software Developer and Physicist',0),(8,'Nikol','Bratkova','Full-Stack Software Developer',0),(9,'Nora','Andonova','Senior Software Develor with Python, Java',0),(10,'Anastasiya','Valtcheva','Senior Software Develor with Python - Jango, FastApi',0),(11,'Grigor','Mironov','Junior Software Develor',0),(12,'Irena','Ruseva','Intermediate Software Develor and QA',0),(13,'Ivaylo','Penchev','Intermediate Software Developer',0),(14,'Ivo','Georgiev','Intermediate Software Developer',0),(15,'Konstantin','Valtchanov','Intermediate Data Scientist',0),(16,'Maria','Kamenarova','Senior Data Engineer',0),(17,'Mitko','Bochev','Intermediate Data Engineer',0),(18,'Nikolay','Vedzhov','Software developer, Team Leader',0),(19,'Nikolay','Angelov','Software Architect',0),(20,'Nikolay','Radoslavov','Intermediate Data Scientist',0),(21,'Pavel','Petkov','Senior C# Developer',0),(22,'Plamen','Gunchev','Senior Python Developer',0),(23,'Stamen','Konarchev','Senior JavaScript Developer',0),(24,'Svetoslav','Doychinov','Senior C++ Developer',0),(25,'Valeria','Nikolaeva','Senior C++ Developer',0),(26,'Ventsislav','Kostadinov','Senior Data Engineer',0),(27,'Yavor','Chobanov','Intermediate Kotlin Developer',0),(28,'Edward','Evlogiev','Javascript, C#, Python Developer, Software Trainer',0),(29,'Vladimir','Venkov','Java, C#, Python Developer, Software Trainer',0),(30,'Radko','Stanev','Senior C# Developer, Software Trainer',0),(31,'Boyan','Hadjiev','International Relations Expert, Soft Skills Trainer',0);
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
  `main` tinyint(2) DEFAULT 0,
  `status` varchar(50) DEFAULT 'hidden',
  `town_id` int(11) NOT NULL,
  `professional_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_resumes_towns1_idx` (`town_id`),
  KEY `fk_resumes_users1_idx` (`professional_id`),
  CONSTRAINT `fk_resumes_towns1` FOREIGN KEY (`town_id`) REFERENCES `towns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_resumes_users1` FOREIGN KEY (`professional_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
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
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `towns`
--

LOCK TABLES `towns` WRITE;
/*!40000 ALTER TABLE `towns` DISABLE KEYS */;
INSERT INTO `towns` VALUES (28,'Sofia'),(29,'Plovdiv'),(30,'Ruse'),(31,'Varna'),(32,'Burgas'),(33,'Vidin'),(34,'Montana'),(35,'Pernik'),(36,'Kiustendil'),(37,'Blagoevgrad'),(38,'Vratsa'),(39,'Pazardzhik'),(40,'Smolian'),(41,'Pleven'),(42,'Lovech'),(43,'Veliko Tarnovo'),(44,'Gabrovo'),(45,'Stara Zagora'),(46,'Haskovo'),(47,'Kardzhali'),(48,'Targovishte'),(49,'Sliven'),(50,'Yambol'),(51,'Silistra'),(52,'Razgrad'),(53,'Shumen'),(54,'Dobrich');
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
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `town_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name_UNIQUE` (`user_name`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `fk_users_towns1_idx` (`town_id`),
  CONSTRAINT `fk_users_towns1` FOREIGN KEY (`town_id`) REFERENCES `towns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','581ff982edcc0a85ec62e926e8686b8089a0c0c01db8695be337669d0cd34383','admin','bigboss@linkedin.com',NULL,NULL,32),(2,'yasen_taha','b7dbcbaf85904ef1fd13d38c53a4b8913c64c4e908d2557017b9b7f4bc54c3cd','professional','yasen.h.taha@gmail.com','+359882559590',NULL,28),(3,'krasi_boz','5fdedcdc2ab09242213d8db5efe3bedcb2a8906f193bc23b85896e5571bafcac','professional','krasimir.bozhilov@gmail.com','+359888123123',NULL,28),(4,'dimityr','d6d1c4395696116646785f6649fd3b0dc0cf8101871c1745f06d21ae324912b8','professional','dimityr931@gmail.com','+359888789789',NULL,45),(5,'nikolay_likyov','24fd39e7b2ee80c8b7ced78c883314969b2ad1a110a0f69c8ea614b8d704a0e3','professional','nikolay@nws.net',NULL,NULL,28),(6,'rossitsar','29bc8052cbd6dedd2246326c07a1a526edd12376b1fc6d2fadece9466833b487','professional','rossitsa_racheva@nws.net',NULL,NULL,28),(7,'evgeni_v','014b61061716932941a8ece0f154f784028215c89920bd020c3e7eb383c8f1c3','professional','evgeni_vladimirov@nws.net',NULL,NULL,28),(8,'nikol_bratkova','be5626d2af805b2edc542a26a7264e358ac07ac32ed6e5f9a0d590592fd3a684','professional','nikol_bratkova@nikolsoftware.bg',NULL,NULL,28),(9,'nora_and','df711bc3d18ca2f418f4828f3b5c2ec08a310b0f31419da35ee79d56cf2c73c1','professional','nora_and@nikolsoftware.bg',NULL,NULL,28),(10,'anastasiya','a943388192a57318029d0cc6fd374b8235ebfde9fc8ece91f02d8bb05cf9c8f9','professional','anastasiya@timepy.com',NULL,NULL,28),(11,'grishata','f9f23e2d1cc7d75dc06653d9862de01954ac5b6a7377bbf171ddc3f2a27365b5','professional','grigor@aol.com',NULL,NULL,43),(12,'irra_ruseva','e73b0c7961697b46396363888f3d40ac90fd9c602859034788ebfdcc0e1eea70','professional','irena_ruseva@nws.net',NULL,NULL,29),(13,'ivaylo','7f73bd475bd0c2a1d6c7893ff5a2ed2f1923e66319c49f49b6cf85ed75148bbc','professional','ivaylo_penchev@company.com',NULL,NULL,30),(14,'ivo_georgiev','7f73bd475bd0c2a1d6c7893ff5a2ed2f1923e66319c49f49b6cf85ed75148bbc','professional','ivo_georgiev@company.com',NULL,NULL,36),(15,'constantine','cdea84b2dd997cbfa9dcc62ac663bf3fc4c372e4111c4418c564f756918eeb02','professional','konstantin@nws.net',NULL,NULL,48),(16,'maria_db','4e60a973c29aa9ac41cd16549c1d15dffa698217de26423303efbd155f07c700','professional','maria@nws.net',NULL,NULL,39),(17,'mitko_bochev','62948e38020047b4de9bdeab88ba5fd43792dd106b53fe65a0982c758af2bd3f','professional','mitko_bochev@nws.net',NULL,NULL,50),(18,'nikolay_vedzhov','3546bd8eb66f3953edd9b8736d3dc0f8169a8686b56e287dfbb1fb0c765cf466','professional','vedzhov@nws.net',NULL,NULL,38),(19,'nikolay_angelov','3546bd8eb66f3953edd9b8736d3dc0f8169a8686b56e287dfbb1fb0c765cf466','professional','angelov@nws.net',NULL,NULL,32),(20,'nikolay_radoslavov','3546bd8eb66f3953edd9b8736d3dc0f8169a8686b56e287dfbb1fb0c765cf466','professional','radoslavov@nws.net',NULL,NULL,47),(21,'pavel_petkov','baeba2513fc2420af5b535e128122d9cbaefc27b7b196117bf716ce51397cb22','professional','pavel@nws.net',NULL,NULL,51),(22,'plamen','6d45da2245d3cc5d476468f97f73b629336264ae1da7f06da1f9ffdb67beb7fd','professional','plamen@nws.net',NULL,NULL,29),(23,'stamen','a6bef9bed07690a6fc3925a988bda6d2bf23b0f8a941780cf88d7a355256ad87','professional','stamen@nws.net',NULL,NULL,48),(24,'svetlyaka','96844e5bdbe9277a70b7a1dd19c770f63f3b3c7e2b1f73179f8ea2f5dd715a71','professional','svetoslav@nws.net',NULL,NULL,35),(25,'valeria','9ae835e4f586bf9266db5bb42d15c4457e5f9245831f457274fded5e5e487cc7','professional','valeria@nws.net',NULL,NULL,53),(26,'bat_ventsi','51d6c813116afa620b2cf1e9efce4b363e9d8c953d8bfc1fd76c6e14da64e48c','professional','ventsislav@nws.net',NULL,NULL,46),(27,'yavkata_dlg','32d988d7113e1070828225731738fd3d865c6d995c3aa75eb13d820f21cfda79','professional','yavor@nws.net',NULL,NULL,31),(28,'edward','029043336e62785117a9c9164ed2f980d852eff11b5fba6048ced4fe310ebfa4','professional','edward_trainer@nws.net',NULL,NULL,28),(29,'vladimir','0d099d81fcd7c85dce9606c426c022b11c2e149f46c555c8559d65b84ef1f369','professional','vladimir@nws.net',NULL,NULL,28),(30,'radko','91095657deb6dac17b2de1029a3ee825cdd593b2e5e3455aca768b9f4752bf32','professional','radko@progress.net',NULL,NULL,28),(31,'boyan','7a07a508a9396fe3f831aab3097c7e558cc3d79ab76e86e5988c00e3f112ef8d','professional','boyan@nws.net',NULL,NULL,28),(32,'telerikacademy','5c54c9329b395ca302d545c32a760b73428457878b89d813236b215d9e9512b7','company','jombatch@telerikacademy.com',NULL,'30, ul. Krastyu Rakovski str',28),(34,'coca_cola','ee9b7a34c1b7a5e8852bbccf2a24ea8979855e70dcc36f124108400700481434','company','jombatch@coca-cola.bg',NULL,'4 Racho Petrov Kazandzhiyata str',28),(35,'schwarz_it','efb839ffe76e666ff06dfa4920c44a50aeeca4d06b428682d450e9264ecc87ec','company','jombatch@schwarzit.bg',NULL,'Mladost 4, Business Park Sofia, building 15a, floor 2',28),(36,'childish','c2c77dd465a9e5e86309169dc942a134eda06429355285da2eb69c3fa18d7268','company','jombatch@childishbg.bg',NULL,'31 Alexander Malinov Blvd., 1729 Mladost 1A',28),(37,'strypes_bg','e4fb76708a24a0291a4801846befcc849c8223d163fc2fa2779dfc420f458907','company','jombatch@strypess.bg',NULL,'10 Maistor Alexi Rilets St.',28),(39,'hedgeserv','d303ec0b73b07bbe1583a5f899fc7df81256e265aaf767e514cf51939aea6f7c','company','jombatch@hedgeserv.bg',NULL,'1 Alabin str.',28),(40,'progress','db705da8cac1443c21a5fe5a7f5cbda82c19add214420d677344f70b4dbfa74e','company','jombatch@progresss.bg',NULL,'54B Tsarigradsko Tsarigradsko Shose Blvd.',28),(42,'accedia','91568e887db2a82c792df0561dd33ef904f33186ec6122e44a167e7a17f3ef46','company','jombatch@accediata.bg',NULL,'13 Henrik Ibsen St',28),(43,'enhancv','5937c8098d23bcd0a72f564b36a65348d13863af166049faa508ce54da99e711','company','jombatch@enhancvs.bg',NULL,'4 Chervena Stena St',28);
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

-- Dump completed on 2022-11-01 15:31:46
