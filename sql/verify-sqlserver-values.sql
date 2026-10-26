-- SQL Server requires the N prefix to retain Unicode string literals.
SELECT 'unicode' AS check_name, 1 AS expected_value, COUNT(*) AS actual_value FROM departments WHERE name=N'営業部'
UNION ALL
SELECT 'bigint', 1, COUNT(*) FROM exact_values WHERE big_integer=9223372036854775807
UNION ALL
SELECT 'decimal_precision', 1, COUNT(*) FROM exact_values WHERE amount=12345678901234567890123.12345678
UNION ALL
SELECT 'skew', 900, COUNT(*) FROM orders WHERE customer_id=1
UNION ALL
SELECT 'null_text', 1, COUNT(*) FROM exact_values WHERE value_id=1 AND optional_text IS NULL
UNION ALL
SELECT 'view_rows', 24, COUNT(*) FROM customer_sales;
