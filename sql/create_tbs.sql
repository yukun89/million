CREATE TABLE if not exists `kline` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `symbol` char(10) NOT NULL,
  `trade_type` char(20) DEFAULT '' COMMENT '现货/U合约/B合约',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `duration` enum('min','hour','day','week') NOT NULL,
  `o_price` decimal(20,8) DEFAULT NULL,
  `h_price` decimal(20,8) DEFAULT NULL,
  `l_price` decimal(20,8) DEFAULT NULL,
  `c_price` decimal(20,8) DEFAULT NULL,
  `amount` decimal(20,8) DEFAULT NULL COMMENT '成交额',
  `volume` decimal(20,8) DEFAULT NULL COMMENT '成交量',
  PRIMARY KEY (`ts`,`symbol`, `trade_type`, `duration`)
);

CREATE TABLE if not exists `exchange_info` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `symbol` char(10) NOT NULL,
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `exchange_name` char(20) DEFAULT '' COMMENT '交易所名称',
  `open_interest` decimal(20,2) DEFAULT NULL COMMENT '合约持仓',
  `user_long_ratio` float NOT NULL DEFAULT 0.5,
  `user_short_ratio` float NOT NULL DEFAULT 0.5,
  `amount_long_ratio` float NOT NULL DEFAULT 0.5,
  `amount_short_ratio` float NOT NULL DEFAULT 0.5,
  `fee_rate` decimal(20,8) NOT NULL DEFAULT 0.0 COMMENT '资金费率',
  `boom_amont` decimal(20,2) NOT NULL DEFAULT 0.0 COMMENT '爆仓数据',
  PRIMARY KEY (`ts`,`symbol`, `exchange_name`)
) COMMENT '交易所相关信息：合约';

CREATE TABLE if not exists `bitfinex_info` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `symbol` char(10) NOT NULL,
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `long_volume` decimal(20,8) DEFAULT NULL COMMENT 'long',
  `short_volume` decimal(20,8) DEFAULT NULL COMMENT 'short',
  `long_ratio` decimal(20,8) DEFAULT NULL COMMENT '多单占比',
  PRIMARY KEY (`ts`,`symbol`)
);


CREATE TABLE if not exists `cme_info` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `symbol` char(10) NOT NULL,
  `big_user_long_units` decimal(20,4) DEFAULT NULL,
  `big_user_short_units` decimal(20,4) DEFAULT NULL,
  `small_user_long_units` decimal(20,4) DEFAULT NULL,
  `small_user_short_units` decimal(20,4) DEFAULT NULL,
  `fund_user_long_units` decimal(20,4) DEFAULT NULL,
  `fund_user_short_units` decimal(20,4) DEFAULT NULL,
  PRIMARY KEY (`ts`,`symbol`)
);

CREATE TABLE if not exists `daily_greedy_index` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `greedy_index` int(10) DEFAULT 50,
  PRIMARY KEY (`ts`)
);

CREATE TABLE if not exists `block_info` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `symbol` char(10) NOT NULL,
  `transactions` decimal(20,4) DEFAULT NULL,
  `active_addresss` decimal(20,4) DEFAULT NULL,
  `new_address` decimal(20,4) DEFAULT NULL,
  `adjusten_on_chain_volume` decimal(20,4) DEFAULT NULL,
  `miner_revenue` decimal(20,4) DEFAULT NULL,
  `addresss_with_balance_over_x` decimal(20,4) DEFAULT NULL,
  PRIMARY KEY (`ts`,`symbol`)
);
