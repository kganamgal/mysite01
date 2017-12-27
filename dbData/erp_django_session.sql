CREATE DATABASE  IF NOT EXISTS `erp` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `erp`;
-- MySQL dump 10.13  Distrib 5.7.20, for Linux (i686)
--
-- Host: 172.17.22.176    Database: erp
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('19lb1f1uacjjavlsza8hkfnoof2ymrcv','ODM0YWUzOTQ1NzJmZDExMzhjZjNiNjRhMzM1ZThmNzE4Mjc2ODkxOTp7Il9jc3JmdG9rZW4iOiJHTlllMUI3aDhNQmE4SUxYdzliSHJDcWMxTUdkNmZramdHdzhxdGFNOGNIcExCSGp4dkVOTHRDaVpxR01iMllqIiwidXNlcm5hbWUiOiJsaW5pIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-05 08:12:12.280559'),('573fsn6agjt1w5rmf349cfivyucyoe2k','YWE1OGYxMTFmZmVjOTBhMjliMmMxYzY4NGU3NGQxMWJlMWZjMjcwNjp7Il9jc3JmdG9rZW4iOiJzcjl1eFRxeDduYnRZOUJKb0tzSzJmRFVHY3A5cTQ5eE5SMnRlTTY1Z2RjMUFWYk92OFBtU1JSR2Zvc1UxalV2IiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6ImxpamlhbmxlIn0=','2018-01-05 03:36:41.067602'),('hk5m5h4c1k5cllohhdb5tdjwfhma3m3l','NjljMTY2OWQwZGRmODMwZWE3NmFjMjczMjg4ZGU2NTE3NWY3NmIzMTp7Il9jc3JmdG9rZW4iOiJZdXg1MUxuUFQzZXQwUEpGVWpWU1d0ODBwNG9ZQ25xMmxnaU5OYkJibXlEMEFDemgyc2tMQ1dPSHNwZkM1U1BWIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6InJlbnl1bmZlaSJ9','2018-01-05 03:41:43.926534'),('igfy052dzxht8hz0e3ra0wsrmqk4ahaw','OTJlNzFlZjdlMWM2ODM0YWJkN2QyZDY5NzA2ZmNiNDMxMDkyZDYyOTp7Il9jc3JmdG9rZW4iOiJsZGN5ZjUxUXlrZ2Rsem5peVNGYnlsQngyTElFWmw2MWNlSmRIUWl3cUxQbWJjSWdydnlDV2FkcGxRWEsxaEtGIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6Imd1ZXN0In0=','2018-01-05 03:34:46.861473'),('k9pz6k2ol56u7t5xpoqeq8c5vapozry1','MzIxNzc0YTMzYTI0OTIxMWRiZmJjZDI3NzhlNWE4OGUyZDYwNDIxOTp7Il9jc3JmdG9rZW4iOiI1TG1NVWRRQ3dTV2ROcjFWY2lJYmQ0WkI3SWVnMFFyQ241UGdKdGZVZEJuMWlUcTcyZmxRZkNxanBXY0RFdmNLIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6InJlbnl1bmZlaSJ9','2018-01-05 03:42:44.532641'),('ofp0dkwmpcqz3c59hg0h6dtptxss8wes','NjYyYmUzYzE3ZjlkNTRlNjc3YmRiMjI3ZWU4NWMyMmVkMWYxMzU0Njp7Il9jc3JmdG9rZW4iOiJEQXJXanBodGtubVNwVU9GaVlpc05CVjIwd0ZOR1RBV3BQaHh4RmZXczRHM0tjcmFlU0pwTjhZSnBUUTZUeWRMIiwidXNlcm5hbWUiOiJndWVzdCIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2018-01-05 04:12:16.181534'),('pbsc6k9lnjefilhxtacuvev0mrfda467','ZWVkNTg4OWU1NTUwZDQ3YWNlYzcyMTdlMGY0YmQ5YmE0MzA5N2Q3NDp7Il9jc3JmdG9rZW4iOiJndmpWd1l6dGVLeks0NzBRaHdWR1JoREw3dnJqeVkwaEVOeUZmOFpTVVdNSFNnYllZZ2hlbGNGM3NqMTJEbzVVIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6IiJ9','2018-01-05 03:49:36.559768'),('rmoclcd265210m298ij97gafrfpuyn8j','MTY0ZjRlNDg2MWJmYzYyOTk5NTZhMDhjMTFiZjdmZWUyMDQyMDk0YTp7Il9jc3JmdG9rZW4iOiIyVVBaUGUxQnFrOTZ0SVhwd3RyZVhETkNqN0RKUlJnZVR6UUI3VUtEWmVsOW9vWVZ3NHhmSmNPV3VQak1CS0JKIiwidXNlcm5hbWUiOiJndWVzdCIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2018-01-05 04:13:20.810848'),('sh250044dtx5vwq1a2rrk8jpchixr0u1','ODJmYTc1MTlhZmJjNWQ5ODY1ZjQyMjcyMDRlOTM2MTk4ZTljZTIwZDp7Il9jc3JmdG9rZW4iOiJ4bzAwMm94ejc3QUprckcyTDkwTTEyVFdqMmtKMXV2dzBHVDEyZFBKanV0M041RlduT01XRXZuNmRBb2NIcnNjIiwidXNlcm5hbWUiOiJndXhpYW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-08 02:12:13.644155'),('si4vr6nqkr8nz9o2szfml6w2ul07bm37','MWM4NWY5MTM2MDM2NDc4MWNjM2NkMmRhNDMwNmU1OWE2MGJiMTFjNDp7Il9jc3JmdG9rZW4iOiJVYkdmTko4bTRtZVBxdE1EaTdpRDhhb1ZOZ0txb0llYmtFVE1qbTlTNDBDREY5WDE2d3FTSmIwb0NqZ3ZyNEZZIiwidXNlcm5hbWUiOiIiLCJfc2Vzc2lvbl9leHBpcnkiOjB9','2018-01-05 04:09:54.217069'),('x8fftqyruxahf90dv1glxmsbv4dgl2mg','MmE3MTNiMmIyYzc5YmQ3YzA2OGVjYjI5YmRjODc5YjgxMzk0NjAzMzp7Il9jc3JmdG9rZW4iOiJPZUYxbE1UbkF5WFBvMUloNE5hR1ZMNUVoTTJBN01ZMmQ0R0Rsc0FGUUp3SkJTemdRUWE5UzhhSEtua0x1MTZDIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6Inh1ZmFuIn0=','2018-01-05 03:55:13.846387');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-26 10:15:49