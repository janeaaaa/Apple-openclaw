const fs = require('fs');
const html = fs.readFileSync('./blog/index.html', 'utf8');

// Check click functionality
const hasOnclick = html.includes('onclick');
const hasShowPost = html.includes('function showPost');

console.log('=== Blog Click Check ===');
console.log('Has onclick:', hasOnclick);
console.log('Has showPost function:', hasShowPost);

// Find onclick patterns
const regex = /onclick="showPost[^"]+"/g;
const matches = html.match(regex);
console.log('onclick count:', matches ? matches.length : 0);
if (matches && matches.length > 0) {
    console.log('First 3:', matches.slice(0, 3));
}