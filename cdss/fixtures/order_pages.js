var data = require('../fixtures/pages.json');

function compare_pks(a, b) {
  if (a.pk < b.pk) return -1;
  if (a.pk > b.pk) return 1;
}

data.sort(function comparator(a, b) {
  return compare_pks(a, b);
});

var json_write = JSON.stringify(data);

console.log(json_write);

var fs = require('fs');
fs.writeFile(
  '../fixtures/pages_fixture.json',
  json_write,
  'utf8',
  function (err) {
    if (err) throw err;
    console.log('complete');
  },
);
