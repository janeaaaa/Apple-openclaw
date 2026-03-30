const fs = require('fs');
const p = JSON.parse(fs.readFileSync('./blog/posts.json', 'utf8'));
const small = p.slice(0, 2).map(x => ({
    id: x.id,
    title: x.title,
    category: x.category,
    date: x.date,
    tags: x.tags,
    content: x.content.substring(0, 100)
}));
const json = JSON.stringify(small);
const h = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Test Small</title></head><body><h1>Test Small</h1><div id="postList"></div><script>var allPosts=' + json + ';document.getElementById("postList").innerHTML="<p>共"+allPosts.length+"篇</p>"+allPosts.map(function(p){return"<div>"+p.title+"</div>"}).join("");</script></body></html>';
fs.writeFileSync('./blog/test-small.html', h);
console.log('创建完成');