const fs = require('fs');
const c = fs.readFileSync('./blog/generate-blog.js', 'utf8');
const lines = c.split('\n');
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('renderPosts')) {
        console.log('Line', i + 1, ':', lines[i].trim().substring(0, 80));
    }
}