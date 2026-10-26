SELECT throwIf(count() != 1200, 'event count mismatch') FROM events;
SELECT throwIf(count() != 900, 'skew mismatch') FROM events WHERE customer_id = 1;
SELECT throwIf(count() != 1, 'precision mismatch') FROM exact_values
WHERE big_integer = 9223372036854775807 AND amount = toDecimal128('12345678901234567890123.12345678', 8);
SELECT throwIf(count() != 1, 'dataset marker mismatch') FROM demo_ready WHERE id=1 AND dataset_version='dblab-v1';
