CREATE TABLE if not exists `kline` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `currency_type` char(10) NOT NULL,
  `trade_type` char(20) DEFAULT '' COMMENT '现货/U合约/B合约',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `unit` enum('min','hour','day','week') NOT NULL,
  `open` decimal(20,8) DEFAULT NULL,
  `high` decimal(20,8) DEFAULT NULL,
  `low` decimal(20,8) DEFAULT NULL,
  `close` decimal(20,8) DEFAULT NULL,
  `amount` decimal(20,8) DEFAULT NULL,
  PRIMARY KEY (`ts`,`currency_type`, `trade_type`, `unit`)
);

CREATE TABLE if not exists `cme_info` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `user` enum('huge','small','company','week') NOT NULL,
);
