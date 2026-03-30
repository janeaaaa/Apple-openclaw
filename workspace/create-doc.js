const { Client } = require('@openclaw/openclaw');
const client = new Client();

async function createReport() {
  try {
    const result = await client.callTool('feishu_doc', {
      action: 'create',
      title: '小苹果下班汇报 - 2026年3月28日',
      owner_open_id: 'ou_a9c7b81a2b296cec5faa9df7ed96a8c0'
    });
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error(e);
  }
}

createReport();