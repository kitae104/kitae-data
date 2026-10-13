// Upstash Redis REST 래퍼 (Vercel Marketplace의 Upstash/KV 연동이 주입하는 환경변수 사용)
const URL_ = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

function configured() {
    return Boolean(URL_ && TOKEN);
}

// commands: [['INCR','k'], ['HINCRBY','h','f',1], ...] → 각 명령의 결과 배열
async function pipeline(commands) {
    const res = await fetch(`${URL_}/pipeline`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(commands),
    });
    if (!res.ok) throw new Error(`redis ${res.status}`);
    const out = await res.json();
    return out.map(r => {
        if (r.error) throw new Error(r.error);
        return r.result;
    });
}

// 한국 시간(KST) 기준 날짜 YYYY-MM-DD
function kstDate(offsetDays = 0, now = Date.now()) {
    const d = new Date(now + 9 * 3600 * 1000 + offsetDays * 86400 * 1000);
    return d.toISOString().slice(0, 10);
}

module.exports = { configured, pipeline, kstDate };
