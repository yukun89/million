CREATE TABLE if not exists `order_base` (
  `oid` bigint(20) NOT NULL,
  `currency_type` char(10) DEFAULT NULL,
  `buy` int(11) DEFAULT NULL,
  `usdt_amout` decimal(20,8) DEFAULT NULL,
  `amout` decimal(20,8) DEFAULT NULL,
  `fee_amout` decimal(20,8) DEFAULT NULL,
  `stat` int(11) DEFAULT NULL,
  `tm` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`oid`)
);

CREATE TABLE if not exists `daily_price` (
  `id` int(11) NOT NULL,
  `currency_type` char(10) NOT NULL,
  `open` decimal(20,8) DEFAULT NULL,
  `high` decimal(20,8) DEFAULT NULL,
  `low` decimal(20,8) DEFAULT NULL,
  `close` decimal(20,8) DEFAULT NULL,
  `amount` decimal(20,8) DEFAULT NULL,
  `price_date` date NOT NULL,
  PRIMARY KEY (`id`,`currency_type`,`price_date`),
  KEY `width` (`price_date`)
);
