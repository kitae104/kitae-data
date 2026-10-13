const crypto = require('crypto');
const { configured, pipeline, kstDate } = require('./_store');

const DAY_TTL = 60 * 60 * 24 * 120; // 일별 키는 120일 보관
const LOG_MAX = 500;

function normalizePath(raw) {
    if (typeof raw !== 'string') return null;
    let p = raw.split(/[?#]/)[0];
    try { p = decodeURIComponent(p); } catch { return null; }
    if (!p.startsWith('/') || p.length > 200) return null;
    p = p.replace(/\/index\.html$/i, '/');
    return p || '/';
}

module.exports = async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
    if (!configured()) return res.status(503).json({ error: 'storage not configured' });

    const body = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
    const page = normalizePath(body.path);
    if (!page) return res.status(400).json({ error: 'invalid path' });

    const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
    const ua = String(req.headers['user-agent'] || '');
    const today = kstDate();
    // 원본 IP는 저장하지 않고 일 단위 솔트 해시만 사용 → 하루 단위 순 방문자 집계
    const visitor = crypto.createHash('sha256')
        .update(`${process.env.STATS_SALT || 'kitae'}|${today}|${ip}|${ua}`)
        .digest('hex').slice(0, 24);

    let ref = '';
    try { ref = body.referrer ? new URL(String(body.referrer)).host : ''; } catch { /* ignore */ }

    const entry = JSON.stringify({
        t: new Date().toISOString(),
        p: page,
        c: req.headers['x-vercel-ip-country'] || '',
        r: ref.slice(0, 80),
        m: /mobile/i.test(ua) ? 'm' : 'd',
    });

    const dayKey = `v:day:${today}`;
    const pageDayKey = `v:page:${today}`;
    const uniqDayKey = `u:day:${today}`;
    try {
        await pipeline([
            ['INCR', 'v:total'],
            ['INCR', dayKey],
            ['EXPIRE', dayKey, DAY_TTL],
            ['HINCRBY', 'v:pages', page, 1],
            ['HINCRBY', pageDayKey, page, 1],
            ['EXPIRE', pageDayKey, DAY_TTL],
            ['PFADD', uniqDayKey, visitor],
            ['EXPIRE', uniqDayKey, DAY_TTL],
            ['LPUSH', 'v:log', entry],
            ['LTRIM', 'v:log', 0, LOG_MAX - 1],
        ]);
    } catch (err) {
        console.error('track failed', err);
        return res.status(500).json({ error: 'track failed' });
    }
    return res.status(204).end();
};

function safeParse(s) { try { return JSON.parse(s); } catch { return {}; } }
