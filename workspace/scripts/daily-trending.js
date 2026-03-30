// 每日热点抓取脚本
// 用于定时推送到飞书

const https = require('https');

function fetchTrending() {
  return new Promise((resolve, reject) => {
    https.get('https://tophub.today/n/KqndgxeLl9', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function main() {
  console.log('开始抓取热点...');
  const html = await fetchTrending();
  console.log('抓取完成，长度:', html.length);
  // TODO: 解析HTML，提取热点
  console.log('热点数据已获取');
}

main().catch(console.error);
