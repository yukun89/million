CREATE TABLE if not exists `kline` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `exchange_name` char(20) DEFAULT 'okx' COMMENT '交易所名称',
  `symbol` char(20) NOT NULL,
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `interval` enum('1H','4H','1D','1W') NOT NULL,
  `o_price` decimal(20,10) DEFAULT NULL,
  `h_price` decimal(20,10) DEFAULT NULL,
  `l_price` decimal(20,10) DEFAULT NULL,
  `c_price` decimal(20,10) DEFAULT NULL,
  `vol` decimal(20,4) DEFAULT NULL COMMENT '成交量:交易量，以张为单位',
  `volCcy` decimal(20,4) DEFAULT NULL COMMENT '成交量:交易量，以币为单位',
  `volCcyQuote` decimal(20,4) DEFAULT NULL COMMENT '成交量:交易量，以计价货币为单位',
  PRIMARY KEY (`ts`,`symbol`, `interval`, `exchange_name`)
);

CREATE TABLE if not exists `funding_rate` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `symbol` char(10) NOT NULL COMMENT 'like:BTC-USDT-SWAP',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `exchange_name` char(20) DEFAULT 'okx' COMMENT '交易所名称',
  PRIMARY KEY (`ts`,`symbol`, `exchange_name`)
);

CREATE TABLE if not exists `coin_list` (
  `id` char(100) NOT NULL COMMENT 'id',
  `symbol` char(40) NOT NULL COMMENT 'symbol',
  `name` char(100) NOT NULL COMMENT 'name',
  PRIMARY KEY (`id`, `symbol`)
);

CREATE TABLE if not exists `coin_markets` (
  `id` char(100) COLLATE utf8_bin NOT NULL COMMENT 'id',
  `symbol` char(40) COLLATE utf8_bin NOT NULL COMMENT 'symbol',
  `total_supply` int(20) NOT NULL COMMENT '总市值',
  `max_supply` int(20) NOT NULL COMMENT '流通市值',
  `max_supply_updated_hour_ts` int(11) NOT NULL COMMENT '流通市值更新小时时间戳',
  PRIMARY KEY (`id`, `symbol`, `max_supply_updated_hour_ts`)
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

CREATE TABLE if not exists `daily_greedy_fear_index` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `greedy_fear_index` int(10) DEFAULT 50,
  PRIMARY KEY (`ts`)
);

CREATE TABLE if not exists `test_orm` (
  `ts` int(11) NOT NULL COMMENT '时间戳',
  `mtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `uniq_id` int(10) DEFAULT 50,
  `name` char(10) NOT NULL,
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
