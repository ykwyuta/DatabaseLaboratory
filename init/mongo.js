// Standalone MongoDB: nested documents, arrays, NULL, Unicode, exact BSON types.
db = db.getSiblingDB('rava');
db.customers.insertMany([
  {_id: 1, code: 'C0001', name: '東京の顧客', tags: ['法人', '優先'], note: null},
  {_id: 2, code: 'C0002', name: '大阪の顧客', tags: [], note: ''},
  {_id: 3, code: 'C0003', name: '名古屋の顧客', address: {city: '名古屋', zip: '460-0001'}}
]);
db.customers.createIndex({code: 1}, {unique: true});
db.orders.insertMany(Array.from({length: 1200}, (_, i) => ({
  _id: i + 1, customer_id: i < 900 ? 1 : i % 2 + 2,
  ordered_at: ISODate('2026-10-01T00:00:00Z'),
  amount: Decimal128('1234.50'), items: [{sku: 'P0001', quantity: 2}]
})));
db.orders.createIndex({customer_id: 1, ordered_at: 1});
db.exact_values.insertOne({_id: 1, big_integer: Long('9223372036854775807'),
  amount: Decimal128('12345678901234567890123.12345678')});
db.demo_ready.insertOne({_id: 1, dataset_version: 'rava-v1'});
