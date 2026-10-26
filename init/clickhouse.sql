CREATE TABLE dblab.events (
  event_id UInt64,
  customer_id UInt32,
  occurred_at DateTime64(3, 'UTC'),
  category LowCardinality(String),
  amount Decimal(31,8),
  note Nullable(String)
) ENGINE = MergeTree ORDER BY (customer_id, occurred_at, event_id);
INSERT INTO dblab.events SELECT number + 1, if(number < 900, 1, 2 + number % 23),
  toDateTime64('2026-10-01 00:00:00', 3, 'UTC') + toIntervalSecond(number),
  if(number % 2 = 0, '購入', '閲覧'), toDecimal128('1234.50000000', 8),
  if(number % 2 = 0, NULL, '') FROM numbers(1200);
CREATE TABLE dblab.exact_values (id UInt8, big_integer Int64, amount Decimal(31,8))
ENGINE = MergeTree ORDER BY id;
INSERT INTO dblab.exact_values VALUES (1, 9223372036854775807, '12345678901234567890123.12345678');
CREATE TABLE dblab.demo_ready (id UInt8, dataset_version String) ENGINE = TinyLog;
INSERT INTO dblab.demo_ready VALUES (1, 'dblab-v1');
