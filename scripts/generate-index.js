const fs = require('fs').promises;
const path = require('path');

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

(async () => {
    try {
        const webDir = path.resolve(__dirname, '..', 'Web');
        const entries = await fs.readdir(webDir, { withFileTypes: true });
        const htmlFiles = entries
            .filter(e => e.isFile() && e.name.endsWith('.html') && e.name.toLowerCase() !== 'index.html')
            .map(e => e.name)
            .sort((a, b) => a.localeCompare(b, 'ko'));

        const listItems = htmlFiles.map(f => `<li><a href="./${encodeURIComponent(f)}">${escapeHtml(f)}</a></li>`).join('\n');

        const html = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>자료 인덱스</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,'Noto Sans KR',Arial,sans-serif;padding:32px;max-width:900px;margin:auto}
    ul{line-height:1.6}
    li{margin:6px 0}
    a{color:#0366d6;text-decoration:none}
  </style>
</head>
<body>
  <h1>웹 자료 인덱스</h1>
  <p>아래는 Web 폴더에 있는 HTML 파일 목록입니다.</p>
  <ul>
    ${listItems || '<li>아직 등록된 HTML 파일이 없습니다.</li>'}
  </ul>
  <hr/>
  <p>※ 이 파일은 <strong>npm run build</strong> 또는 Vercel 빌드 과정에서 자동 생성됩니다.</p>
</body>
</html>`;

        await fs.writeFile(path.join(webDir, 'index.html'), html, 'utf8');
        console.log('Web/index.html 생성됨. 항목:', htmlFiles);
    } catch (err) {
        console.error('인덱스 생성 중 오류:', err);
        process.exitCode = 1;
    }
})();
