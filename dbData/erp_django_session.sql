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
INSERT INTO `django_session` VALUES ('19lb1f1uacjjavlsza8hkfnoof2ymrcv','ODM0YWUzOTQ1NzJmZDExMzhjZjNiNjRhMzM1ZThmNzE4Mjc2ODkxOTp7Il9jc3JmdG9rZW4iOiJHTlllMUI3aDhNQmE4SUxYdzliSHJDcWMxTUdkNmZramdHdzhxdGFNOGNIcExCSGp4dkVOTHRDaVpxR01iMllqIiwidXNlcm5hbWUiOiJsaW5pIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-05 08:12:12.280559'),('1w66laapo81euibckumsokampnjlrxjc','Mjk5MjEzZDg1M2UwYTJkYzdjY2M4Y2RiMDI3ODBkZmRiOGZjMjI2YTp7Il9jc3JmdG9rZW4iOiI3TXhKU05YR0wzemZBRWE0TkhhNDNFbkdoRmxpdkVBcGdsS0N0RkY0U3E1dExqRnN1OTVwOXJOOGlWZjdIcmQ2IiwidXNlcm5hbWUiOiJndXhpYW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-12 01:02:26.897076'),('2pgq4obedzuddwu632v7qsxz7eqzj9ok','MjI2YTgwNTVlYjNhZmU1YjdkMDAyYjc5Mzk3ZDU5NjAyNjhmYWFmMjp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6ImRlNGVxQksxekt0d0FueUhpNlJsU0FoTEV6MTdYSEkyYlhNRlprMW40a3JEaWVqRVRqNmRhdW5CWU1GeGpnY3YiLCJ1c2VybmFtZSI6ImxpdXhpYW9saSJ9','2018-01-22 08:17:23.513680'),('506b69j814q0olv71ceqbt8bs8zn5zzj','ZTkzYzA5YWRmZDY1MDhiYWNlYWNkMGJiZjEzMGJhZDMwNmNiODVkZjp7InVzZXJuYW1lIjoiZ3V4aWFuZyIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6Im11aEo0dm9VR01jQ1pNaDNEQmtCNlFzeXhSNG5xdTJTSlhEdXN2S2d2aXJRR2ZGYVRRMnJMWlBWWVNhbDZtcXMifQ==','2018-01-25 02:23:44.025742'),('573fsn6agjt1w5rmf349cfivyucyoe2k','YWE1OGYxMTFmZmVjOTBhMjliMmMxYzY4NGU3NGQxMWJlMWZjMjcwNjp7Il9jc3JmdG9rZW4iOiJzcjl1eFRxeDduYnRZOUJKb0tzSzJmRFVHY3A5cTQ5eE5SMnRlTTY1Z2RjMUFWYk92OFBtU1JSR2Zvc1UxalV2IiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6ImxpamlhbmxlIn0=','2018-01-05 03:36:41.067602'),('81rggsvzzvkfrpskgztucmnsjax5beah','YTEyNjc1NTBjNTBjN2Q3OGQ1Y2UwMzA0YTcxMDhkOGQ5YTJmZGRjMTp7Il9jc3JmdG9rZW4iOiJzRU9POE9aWFpUb3IyWG5YQ2tOQU1za0RRTDE5WDM1bGswMEZCRVdkenRSdjhDcGxzVXg2REFnMG5IOVo4bzhaIiwidXNlcm5hbWUiOiIiLCJfc2Vzc2lvbl9leHBpcnkiOjB9','2018-01-16 01:54:23.218001'),('953m7ridwapajtag7vm9l0okqzik7b8n','MmU4MGIxOWQ2ZmQ5MGZmNTM2OGNmMjhhOGFjNDE5M2QyOTQ4MTE4ZTp7InVzZXJuYW1lIjoibGluaSIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6IlFyd1pZaXZTZHRsTXljWEVaMWlSUEZ0T0dsTGFFakU5ZzB4RVlGNFpZWWUzOVc5MTBUZXRKMjlrbG9pQ3NFZUIifQ==','2018-01-25 02:40:56.319786'),('9dg6z3z5kduhbad5lz2ps6fi25hn2zwq','ZDE5OTViYTBlYjJkYmM3ZDQ4N2Q3NjkwZDYxMzAzZWY2ZDE1ODE4MDp7InVzZXJuYW1lIjoiZ3V4aWFuZyIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6ImZpemZJU2FtSHBIQjR1dE9rRW5mR2tMdGJIZm9xaEFtTmR6a21SZmtvaW1uUTNFb1NkcXZiaTZWSG5IbGFucWEifQ==','2018-01-25 02:26:31.101298'),('a7o328f90uhoks6c7mealg82nnplqfx5','YjM0NWMwZTY1OWVkMGRiMDcyYWNjNDAyNWMwOTg5ZDU4NGNlYjY4ZTp7Il9jc3JmdG9rZW4iOiJDaGIwZHhUQUlGQ29NY3UzQk9FRmV5OWRkZnNWVHY0aTR0UWFZV29kTGxxMWFNamlpeE4yR3BpWUdPN1lwaWJKIiwidXNlcm5hbWUiOiJndXhpYW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-16 02:54:20.102257'),('d74d8yr5eyh49uacrt0x5rdyybxoc6ll','ZDFhNTEwNjdkOTY1OGIzMmQ4MmVmMWY0ODc4NTVhMWI5YjY5YzY5MDp7Il9jc3JmdG9rZW4iOiJLWm9LQWJTUElwNGxZWE82QUJJdGhiOW9RUTZPNmh5ZTZCNGtBaHQ4VU5icG1qaGp3T3VmUlRDU3htdzlZaThxIiwidXNlcm5hbWUiOiJndXhpYW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-19 01:09:26.128789'),('gnfuvuxncjobo65znm1jzai8lh6lbhn5','ODQwNTQ3OGQyMzUzYWUyN2U5NjZlNmUxMWFjNTljMjQ4OGQ5OTE2ZTp7InVzZXJuYW1lIjoiZ3V4aWFuZyIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6InFDRVBrTVM4aE1IMEo0aFV6enlPR2E3TEd3VVk4SmFEUUdBRURTc1k3Q1ZxZUJPbzhrdXptWUwwZFB5bnBTcDcifQ==','2018-01-25 02:27:37.740110'),('hk5m5h4c1k5cllohhdb5tdjwfhma3m3l','NjljMTY2OWQwZGRmODMwZWE3NmFjMjczMjg4ZGU2NTE3NWY3NmIzMTp7Il9jc3JmdG9rZW4iOiJZdXg1MUxuUFQzZXQwUEpGVWpWU1d0ODBwNG9ZQ25xMmxnaU5OYkJibXlEMEFDemgyc2tMQ1dPSHNwZkM1U1BWIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6InJlbnl1bmZlaSJ9','2018-01-05 03:41:43.926534'),('igfy052dzxht8hz0e3ra0wsrmqk4ahaw','OTJlNzFlZjdlMWM2ODM0YWJkN2QyZDY5NzA2ZmNiNDMxMDkyZDYyOTp7Il9jc3JmdG9rZW4iOiJsZGN5ZjUxUXlrZ2Rsem5peVNGYnlsQngyTElFWmw2MWNlSmRIUWl3cUxQbWJjSWdydnlDV2FkcGxRWEsxaEtGIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6Imd1ZXN0In0=','2018-01-05 03:34:46.861473'),('k9pz6k2ol56u7t5xpoqeq8c5vapozry1','OTY4N2EyZTNhZTcxMjY2OGM4NGRlOWMzODMxN2E3MzUzYjNjOTU1Mzp7InVzZXJuYW1lIjoicmVueXVuZmVpIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJfY3NyZnRva2VuIjoiNUxtTVVkUUN3U1dkTnIxVmNpSWJkNFpCN0llZzBRckNuNVBnSnRmVWRCbjFpVHE3MmZsUWZDcWpwV2NERXZjSyJ9','2018-01-24 03:26:46.201273'),('mk4g3wrfr71l19r4mi3xwlan8p59340x','MTFiZWQ3ODg0MjNlOTFkZDlhNjhjYmI1ZWE2YzI5ZmJjNzE2NTViNTp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6IkVza29XVWphZDh4U3JOa2drYmx1Nm15dk9FQ0tWZGxWclkybDZyR0t5OVk1ME45OHpUOXdISncwT21wNlp1WjIiLCJ1c2VybmFtZSI6Imd1eGlhbmcifQ==','2018-01-19 05:32:11.511353'),('ofp0dkwmpcqz3c59hg0h6dtptxss8wes','NjYyYmUzYzE3ZjlkNTRlNjc3YmRiMjI3ZWU4NWMyMmVkMWYxMzU0Njp7Il9jc3JmdG9rZW4iOiJEQXJXanBodGtubVNwVU9GaVlpc05CVjIwd0ZOR1RBV3BQaHh4RmZXczRHM0tjcmFlU0pwTjhZSnBUUTZUeWRMIiwidXNlcm5hbWUiOiJndWVzdCIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2018-01-05 04:12:16.181534'),('pbsc6k9lnjefilhxtacuvev0mrfda467','ZWVkNTg4OWU1NTUwZDQ3YWNlYzcyMTdlMGY0YmQ5YmE0MzA5N2Q3NDp7Il9jc3JmdG9rZW4iOiJndmpWd1l6dGVLeks0NzBRaHdWR1JoREw3dnJqeVkwaEVOeUZmOFpTVVdNSFNnYllZZ2hlbGNGM3NqMTJEbzVVIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6IiJ9','2018-01-05 03:49:36.559768'),('qt9qo0usuzaap8scbm4qr5d5guqysmnt','ZTBhNTBlZThmZWEwOGE3ZDhiNDU5YmFlYzM3YzkzNDNkMGExNWY5ODp7InVzZXJuYW1lIjoibGl1eGlhb2xpIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJfY3NyZnRva2VuIjoiTVVkbmw2Z0Y3cHZVM0xVUWJ5WW5CcmpJUFZoZXg3dXIwbzBVOGhBVmRxSmtPbWdyZTB1allRSm5FSlk2STJ4WSJ9','2018-01-24 08:39:41.637166'),('rmoclcd265210m298ij97gafrfpuyn8j','MTY0ZjRlNDg2MWJmYzYyOTk5NTZhMDhjMTFiZjdmZWUyMDQyMDk0YTp7Il9jc3JmdG9rZW4iOiIyVVBaUGUxQnFrOTZ0SVhwd3RyZVhETkNqN0RKUlJnZVR6UUI3VUtEWmVsOW9vWVZ3NHhmSmNPV3VQak1CS0JKIiwidXNlcm5hbWUiOiJndWVzdCIsIl9zZXNzaW9uX2V4cGlyeSI6MH0=','2018-01-05 04:13:20.810848'),('rvjzj86bxgonzkkq2mt6b5l38he76mb9','OTcxMzAwZjMxZGU1ODNiYzk1MDc2NzEzMjc3NTViYjZkYTNkNDVkOTp7InVzZXJuYW1lIjoibGluaSIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6IjBnclRTWUVYNDd3VFVZQXduQWJ1WWtoTnBublVTUjl5b3VPMGdDcjBhT1BOY2xHZ3duSWt5OHp6NjMzSkM2aEoifQ==','2018-01-25 02:25:19.725216'),('sh250044dtx5vwq1a2rrk8jpchixr0u1','MTZiOGZlNDZjM2M2NDE5NjFjMzQwMmExNjk4MGE0MDA2ZDY2YjZjODp7InVzZXJuYW1lIjoiZ3V4aWFuZyIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6InhvMDAyb3h6NzdBSmtyRzJMOTBNMTJUV2oya0oxdXZ3MEdUMTJkUEpqdXQzTjVGV25PTVdFdm42ZEFvY0hyc2MifQ==','2018-02-05 00:57:50.738761'),('si4vr6nqkr8nz9o2szfml6w2ul07bm37','NjY5ZTQ4YWNlZTU2ODkwYmZiY2RiMjEyNjI4NDY5ZWFkMzY4NWRhNzp7InVzZXJuYW1lIjoiZ3Vlc3QiLCJfc2Vzc2lvbl9leHBpcnkiOjAsIl9jc3JmdG9rZW4iOiJVYkdmTko4bTRtZVBxdE1EaTdpRDhhb1ZOZ0txb0llYmtFVE1qbTlTNDBDREY5WDE2d3FTSmIwb0NqZ3ZyNEZZIn0=','2018-01-23 08:49:56.873558'),('t7oz6ftvf2e8e713rmwvwfu88146edtf','ZmVjYjliMWQxOGE1NmQwNjc1ODY0ZDk0ODQzZDQwZmE3MzhlMWUwYTp7Il9jc3JmdG9rZW4iOiJxb2hieHl1TmFoTUhLcFNHVkszcXVLaXlVem1yeWxESm5YTEdGOUQzY0pGdjRGNDVHa0ZSZk9zSnNSakNwRVhFIiwidXNlcm5hbWUiOiJndXhpYW5nIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==','2018-01-14 04:35:38.176843'),('uhx0df2ciz9oc6xswu6wf3ytq5v12h3f','MTk1ZGRjNDc1OWEzMThiNzFmMzk1NzkyZDM3ZDkzYzAxYjI0NGY3MDp7Il9zZXNzaW9uX2V4cGlyeSI6MCwiX2NzcmZ0b2tlbiI6IlNEZTJ4d0R5MWhSTGNUYXlWWU1hd2hxMlhaUzJPSk4yb2FPV01mbEdVS1VkR0o3T1U0dUdEMHkxYWtQRTlaWnEiLCJ1c2VybmFtZSI6ImxpbmkifQ==','2018-01-22 06:41:50.675780'),('x8fftqyruxahf90dv1glxmsbv4dgl2mg','MmE3MTNiMmIyYzc5YmQ3YzA2OGVjYjI5YmRjODc5YjgxMzk0NjAzMzp7Il9jc3JmdG9rZW4iOiJPZUYxbE1UbkF5WFBvMUloNE5hR1ZMNUVoTTJBN01ZMmQ0R0Rsc0FGUUp3SkJTemdRUWE5UzhhSEtua0x1MTZDIiwiX3Nlc3Npb25fZXhwaXJ5IjowLCJ1c2VybmFtZSI6Inh1ZmFuIn0=','2018-01-05 03:55:13.846387');
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

-- Dump completed on 2018-01-22  9:08:30
