const fs = require('fs');
let h = fs.readFileSync('./blog/index.html', 'utf8');

// Fix the broken regex: **(text)** should be **text** in markdown
// Current broken: .replace(/**(.*?)**/g, '<strong>$1</strong>')
// Fix: remove the broken line or comment it out

h = h.replace(/\.replace\(\/\*\*\(.*?\)\*\*\/g, '<strong>\$1<\/strong>'\)/g, '');

fs.writeFileSync('./blog/index.html', h);
console.log('Fixed regex issue');
