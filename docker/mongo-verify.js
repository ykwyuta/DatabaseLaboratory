const assert = {eq: (actual, expected) => {if (actual !== expected) throw new Error(`${actual} != ${expected}`);}};
db = db.getSiblingDB('dblab');
assert.eq(db.demo_ready.findOne({_id: 1}).dataset_version, 'dblab-v1');
assert.eq(db.customers.countDocuments({}), 3);
assert.eq(db.orders.countDocuments({}), 1200);
assert.eq(db.orders.countDocuments({customer_id: 1}), 900);
assert.eq(db.exact_values.findOne({_id: 1}).big_integer.toString(), '9223372036854775807');
assert.eq(db.exact_values.findOne({_id: 1}).amount.toString(), '12345678901234567890123.12345678');
print('dblab-mongo-ok');
