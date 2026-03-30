const fs = require('fs');
const h = fs.readFileSync('./blog/index.html', 'utf8');
const ids = h.match(/"id": \d+/g);
console.log('id数量:', ids ? ids.length : 0);
console.log('ids:', ids);