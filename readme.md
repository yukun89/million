ds: data structure
store: handle data base.

Transaction:
- status: created(0), finished(1)
- start_order_id: 12345
- end_order_id: 23456
- currency_type:
- low_price:
- up_price:
- profilt:?

Order:
- order_id: 12345
- transaction_type: +1 means 开仓， -1 means 平仓
- transaction_id:
- status: marken, taken
- currency_type:
- deal_type: +1 means buy, -1 means sell
- expected_price: 挂单价格
- deal_price: 成交价格
- deal_amount: 成交额（usdt）计价
- deal_volume: 成交量
- mark_timestamp: 挂单时间
- deal_timestamp: 成交时间
