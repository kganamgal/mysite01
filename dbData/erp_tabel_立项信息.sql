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
-- Table structure for table `tabel_立项信息`
--

DROP TABLE IF EXISTS `tabel_立项信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_立项信息` (
  `立项识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `项目名称` varchar(255) DEFAULT NULL,
  `分项名称` varchar(255) DEFAULT NULL,
  `父项立项识别码` bigint(20) DEFAULT NULL,
  `建设单位识别码` bigint(20) DEFAULT NULL,
  `代建单位识别码` bigint(20) DEFAULT NULL,
  `立项文件名称` varchar(255) DEFAULT NULL,
  `立项时间` date DEFAULT NULL,
  `项目概算` decimal(12,2) DEFAULT NULL,
  `立项备注` text,
  PRIMARY KEY (`立项识别码`),
  UNIQUE KEY `项目名称` (`项目名称`,`分项名称`)
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_立项信息`
--

LOCK TABLES `tabel_立项信息` WRITE;
/*!40000 ALTER TABLE `tabel_立项信息` DISABLE KEYS */;
INSERT INTO `tabel_立项信息` VALUES (42,'北王安置房',NULL,NULL,18,1,'关于李沧区北王家上流社区安置房项目备案的通知（李沧发改[2015]107号）','2015-05-20',812970000.00,NULL),(43,'北王安置房','工程费用',42,18,1,NULL,NULL,550889400.00,NULL),(44,'北王安置房','工程建设其他费用',42,18,1,NULL,NULL,177656800.00,NULL),(45,'北王安置房','预备费',42,18,1,NULL,NULL,36427300.00,NULL),(46,'北王安置房','建设期利息',42,18,1,NULL,NULL,47996500.00,NULL),(47,'北王安置房','施工总承包（多层区）',43,18,1,NULL,NULL,200000000.00,NULL),(48,'北王安置房','施工总承包（高层区）',43,18,1,NULL,NULL,220000000.00,NULL),(49,'北王安置房','建设用地费用',44,18,1,NULL,NULL,92053100.00,NULL),(50,'北王安置房','土地划拨费用',49,18,1,NULL,NULL,19895900.00,NULL),(51,'北王安置房','土地相关契税等',49,18,1,NULL,NULL,596900.00,NULL),(52,'北王安置房','拆迁补偿及奖励费合计',49,18,1,NULL,NULL,71560300.00,NULL),(53,'北王安置房','技术咨询费',44,18,1,NULL,NULL,10634500.00,NULL),(54,'北王安置房','报告编制',53,18,1,NULL,NULL,360000.00,NULL),(55,'北王安置房','项目论证费',53,18,1,NULL,NULL,100000.00,NULL),(56,'北王安置房','环境评价评估费 ',53,18,1,NULL,NULL,155300.00,NULL),(57,'北王安置房','节能评估审查费',53,18,1,NULL,NULL,155300.00,NULL),(58,'北王安置房','劳动安全卫生评价费',53,18,1,NULL,NULL,80000.00,NULL),(59,'北王安置房','规划建筑设计费、施工图设计费',53,18,1,NULL,NULL,9318000.00,NULL),(60,'北王安置房','勘察、方案设计费',53,18,1,NULL,NULL,465900.00,NULL),(61,'北王安置房','项目配套费',44,18,1,NULL,NULL,48955300.00,NULL),(62,'北王安置房','城市基础设施配套费',61,18,1,NULL,NULL,42707500.00,NULL),(63,'北王安置房','防空地下室易地建设费',61,18,1,NULL,NULL,4037800.00,NULL),(64,'北王安置房','白蚁预防工程费',61,18,1,NULL,NULL,310600.00,NULL),(65,'北王安置房','水土流失防治费',61,18,1,NULL,NULL,35800.00,NULL),(66,'北王安置房','建筑企业养老保障金',61,18,1,NULL,NULL,0.00,NULL),(67,'北王安置房','墙体建筑材料节能费',61,18,1,NULL,NULL,1553000.00,NULL),(68,'北王安置房','散装水泥专项资金',61,18,1,NULL,NULL,310600.00,NULL),(69,'北王安置房','项目建设管理费',44,18,1,NULL,NULL,20578400.00,NULL),(70,'北王安置房','项目代建费',69,18,1,NULL,NULL,8263300.00,NULL),(71,'北王安置房','规划技术服务费',69,18,1,NULL,NULL,326100.00,NULL),(72,'北王安置房','图纸审核费',69,18,1,NULL,NULL,745400.00,NULL),(73,'北王安置房','规划指标审核费',69,18,1,NULL,NULL,465900.00,NULL),(74,'北王安置房','规划测绘费',69,18,1,NULL,NULL,28000.00,NULL),(75,'北王安置房','零星测绘费',69,18,1,NULL,NULL,129500.00,NULL),(76,'北王安置房','竣工测量费',69,18,1,NULL,NULL,38800.00,NULL),(77,'北王安置房','工程建设监理费',69,18,1,NULL,NULL,5508900.00,NULL),(78,'北王安置房','工程造价咨询等编制费',69,18,1,NULL,NULL,2269200.00,NULL),(79,'北王安置房','招标代理费',69,18,1,NULL,NULL,0.00,NULL),(80,'北王安置房','工程质量监督费',69,18,1,NULL,NULL,275400.00,NULL),(81,'北王安置房','临设、防雷测试费',69,18,1,NULL,NULL,776500.00,NULL),(82,'北王安置房','抗震评比费',69,18,1,NULL,NULL,310600.00,NULL),(83,'北王安置房','主体结构检测费',69,18,1,NULL,NULL,233000.00,NULL),(84,'北王安置房','消防检测费',69,18,1,NULL,NULL,233000.00,NULL),(85,'北王安置房','设备抽检费（宽带与通风）',69,18,1,NULL,NULL,186400.00,NULL),(86,'北王安置房','空气检测',69,18,1,NULL,NULL,96100.00,NULL),(87,'北王安置房','电气检测',69,18,1,NULL,NULL,233000.00,NULL),(88,'北王安置房','基坑检测费',69,18,1,NULL,NULL,150000.00,NULL),(89,'北王安置房','沉降观测检测费',69,18,1,NULL,NULL,100000.00,NULL),(90,'北王安置房','外墙（窗）淋水试验',69,18,1,NULL,NULL,155300.00,NULL),(91,'北王安置房','保温系数检测',69,18,1,NULL,NULL,54000.00,NULL),(92,'北王安置房','与未来经营有关的其他费用',44,18,1,NULL,NULL,5435500.00,NULL),(93,'北王安置房','物业管理公共基金',92,18,1,NULL,NULL,5435500.00,NULL),(94,'北王安置房','优化设计',53,18,1,NULL,NULL,0.00,NULL),(95,'北王安置房','施工图优化设计',94,18,1,NULL,NULL,0.00,NULL),(96,'北王安置房','优化设计设计咨询结构专业概算计算',94,18,1,NULL,NULL,0.00,NULL),(98,'北王安置房','水土保持方案编制费',53,18,1,NULL,NULL,0.00,'从<北王安置房-工程建设其他费用-技术咨询费-报告编制>中移来55000元概算'),(99,'北王安置房','清单、控制价编制',78,18,1,NULL,NULL,978240.00,NULL),(100,'北王安置房','临时给水',43,18,1,'关于北王安置房项目相关问题专题会议纪要','2016-10-12',205000.00,NULL),(101,'北王安置房','临时供电',43,18,1,'关于北王安置房项目相关问题专题会议纪要（青世园字[2016]98号）','2016-10-12',480000.00,NULL),(102,'北王安置房','第三方担保',69,18,1,NULL,NULL,0.00,NULL),(105,'北王其他费用',NULL,NULL,18,1,NULL,NULL,150000000.00,NULL),(106,'北王其他费用','复印费等报销',105,18,1,NULL,NULL,100000.00,NULL),(107,'北王安置房','规划技术服务费（规划许可证）',71,18,1,NULL,NULL,32365.00,NULL),(108,'北王安置房','规划技术服务费（临建）',71,18,1,NULL,NULL,1034.00,NULL),(109,'北王其他费用','软件费用',105,18,1,NULL,NULL,100000.00,NULL),(110,'北王其他费用','安全劳保',105,18,1,NULL,NULL,4438.00,NULL),(111,'北王安置房','施工图审查费',72,18,1,NULL,NULL,283100.00,NULL),(112,'北王安置房','人防施工图审查费',72,18,1,NULL,NULL,99902.00,NULL),(113,'北王安置房','项目拆迁成本评估费',53,18,1,NULL,NULL,0.00,NULL),(114,'北王其他费用','南北王补亏地规划',105,18,1,NULL,NULL,1515000.00,NULL),(115,'北王安置房','建筑废弃物处置费',61,18,1,NULL,NULL,0.00,'办理施工许可证用'),(116,'北王安置房','北王安置房项目临时用电接电保证金',43,18,1,NULL,NULL,302400.00,NULL),(117,'北王其他费用','北王安置地块地上附着物拆除工程',105,18,1,NULL,NULL,150000.00,NULL),(118,'北王其他费用','北王补亏地地上附着物拆除工程',105,18,1,NULL,NULL,2664787.00,NULL),(119,'北王其他费用','各种土地费用',105,18,1,NULL,NULL,72173395.08,NULL),(120,'北王其他费用','青岛市2014年第一批、第二批城市建设用地社会保障补贴资金',119,18,1,NULL,NULL,390870.00,NULL),(121,'北王其他费用','青岛市第一批保障性安居工程、第二批建设用地实施方案征地预存款',119,18,1,NULL,NULL,16526160.00,NULL),(122,'北王其他费用','北王第一批建设用地社会保障补贴资金',119,18,1,NULL,NULL,1836240.00,NULL),(123,'北王其他费用','拆除北王C-07-02地块内两栋违法建筑',119,18,1,NULL,NULL,40000000.00,NULL),(124,'北王其他费用','北王补亏地项目征地预存款（地块：D-01-03）',119,18,1,NULL,NULL,7772990.90,NULL),(125,'北王其他费用','北王补亏地项目社保基金（地块：D-01-03）',119,18,1,NULL,NULL,800580.00,NULL),(126,'北王其他费用','北王补亏地项目征地预存款（地块：C-03-02b）北王：4437562.27、南王：4363632.23',119,18,1,NULL,NULL,4437562.27,NULL),(127,'北王其他费用','北王补亏地项目社保基金（地块：C-03-02b）北王：408991.91、南王：402178.09',119,18,1,NULL,NULL,408991.91,NULL),(128,'1609工程',NULL,NULL,63,65,NULL,NULL,137611190.80,NULL),(129,'1609工程','工程费用',128,63,65,NULL,NULL,113361569.30,'下含：\n土石方及地基处理工程871.16万\n地下部分6923.62万\n室外配套工程352.80万\n附属工程430万\n专用设备及系统费用2721.32万'),(130,'1609工程','工程建设其他费用',128,63,65,NULL,NULL,11739513.27,NULL),(131,'1609工程','预备费用',128,63,65,NULL,NULL,12510108.26,NULL),(132,'1609工程','建设单位管理费',130,63,65,NULL,NULL,1800000.00,NULL),(133,'1609工程','招标代理费',130,63,65,NULL,NULL,449600.00,NULL),(134,'1609工程','工程造价咨询费',130,63,65,NULL,NULL,864400.00,NULL),(135,'1609工程','勘察测绘费',139,63,65,NULL,NULL,600000.00,NULL),(136,'1609工程','工程设计费',130,63,65,NULL,NULL,3757070.90,NULL),(137,'1609工程','工程监理费',130,63,65,NULL,NULL,1949758.00,NULL),(138,'1609工程','环境影响评价费',130,63,65,NULL,NULL,22207.06,NULL),(139,'1609工程','前期工作费',130,63,65,NULL,NULL,1009160.29,NULL),(140,'1609工程','水土保持设施费',161,63,65,NULL,NULL,11874.00,NULL),(141,'1609工程','新型墙体材料专项基金',161,63,65,NULL,NULL,0.00,NULL),(142,'1609工程','白蚁预防工程费',161,63,65,NULL,NULL,0.00,NULL),(144,'1609工程','工程保险费',161,63,65,NULL,NULL,0.00,NULL),(145,'1609工程','苗木清点评估费',139,63,65,NULL,NULL,100000.00,NULL),(146,'1609工程','办公家具及器具购置费',130,63,65,NULL,NULL,700000.00,NULL),(147,'1609工程','工程岩土勘察',135,63,65,NULL,NULL,343518.24,NULL),(148,'1609工程','可行性研究报告编制费',139,63,65,NULL,NULL,159780.00,NULL),(149,'1609工程','基坑支护设计费',136,63,65,NULL,NULL,149400.00,NULL),(150,'1609工程','信息化工程设计费',136,63,65,NULL,NULL,985000.00,NULL),(151,'1609工程','概算、预算编制',134,63,65,NULL,NULL,350500.00,NULL),(153,'1609工程','全过程造价',134,63,65,NULL,NULL,497000.00,NULL),(157,'1609工程','声像档案管理费',161,63,65,NULL,NULL,1955.25,NULL),(159,'1609工程','总包内工程',129,63,65,NULL,NULL,107861569.30,NULL),(160,'1609工程','场地清理、苗木迁移及地上附着物补偿费用',129,63,65,NULL,NULL,5500000.00,NULL),(161,'1609工程','其他费用',130,63,65,NULL,NULL,1209524.07,NULL),(162,'1609工程','项目建议书编制费',139,63,65,NULL,NULL,79620.00,NULL),(163,'1609工程','人防审图',139,63,65,NULL,NULL,47553.24,NULL),(164,'1609工程','高可靠性供电费',161,63,65,NULL,NULL,120000.00,NULL),(165,'1609工程','消防维保费',161,63,65,NULL,NULL,15642.00,NULL),(166,'1609工程','消防检测费',161,63,65,NULL,NULL,39105.00,NULL),(167,'1609工程','废弃物处置费',161,63,65,NULL,NULL,260000.00,NULL),(168,'1609工程','空气质量检测费',161,63,65,NULL,NULL,15000.00,NULL),(169,'1609工程','房屋测绘费',161,63,65,NULL,NULL,21273.12,NULL),(170,'1609工程','主体结构抽检费',161,63,65,NULL,NULL,19200.00,NULL),(171,'1609工程','其他咨询',161,63,65,NULL,NULL,400000.00,NULL),(172,'1609工程','临时工程费',161,63,65,NULL,NULL,300000.00,NULL),(173,'1609工程','档案保管费',161,63,65,NULL,NULL,5474.70,NULL),(174,'1609工程','建筑设计含人防',136,63,65,NULL,NULL,2622670.00,NULL),(175,'1609工程','工程测绘',135,63,65,NULL,NULL,250000.00,NULL),(176,'1609工程其他','地面附着物拆除、树木迁移包活工程',177,70,NULL,'《中国馆人防项目苗木迁移专题会纪要》','2017-11-27',2280000.00,NULL),(177,'1609工程其他',NULL,NULL,70,NULL,'《中国馆人防项目苗木迁移专题会纪要》',NULL,4993068.00,NULL);
/*!40000 ALTER TABLE `tabel_立项信息` ENABLE KEYS */;
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
