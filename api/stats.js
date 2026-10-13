const { configured, pipeline, kstDate } = require('./_store');

function hashToObject(arr) {
    const o = {};
    for (let i = 0; i < (arr || []).length; i += 2) o[arr[i]] = Number(arr[i + 1]);
    return o;
}

module.exports = async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    if (!configured()) return res.status(503).json({ error: 'storage not configured' });

    const days = Array.from({ length: 7 }, (_, i) => kstDate(-(6 - i)));
    const today = days[days.length - 1];
    // 최근 접속 기록은 STATS_KEY 를 설정하고 ?key= 로 일치할 때만 공개
    const wantLog = process.env.STATS_KEY && req.query && req.query.key === process.env.STATS_KEY;

    const cmds = [
        ['GET', 'v:total'],
        ['HGETALL', 'v:pages'],
        ['HGETALL', `v:page:${today}`],
        ...days.map(d => ['GET', `v:day:${d}`]),
        ...days.map(d => ['PFCOUNT', `u:day:${d}`]),
    ];
    if (wantLog) cmds.push(['LRANGE', 'v:log', 0, 99]);

    try {
        const r = await pipeline(cmds);
        const totalPages = hashToObject(r[1]);
        const todayPages = hashToObject(r[2]);
        const views = r.slice(3, 3 + days.length).map(Number);
        const uniques = r.slice(3 + days.length, 3 + 2 * days.length).map(Number);

        const pages = Object.keys({ ...totalPages, ...todayPages })
            .map(path => ({ path, total: totalPages[path] || 0, today: todayPages[path] || 0 }))
            .sort((a, b) => b.total - a.total);

        const out = {
            total: Number(r[0] || 0),
            today: views[views.length - 1],
            todayVisitors: uniques[uniques.length - 1],
            date: today,
            daily: days.map((date, i) => ({ date, views: views[i], visitors: uniques[i] })),
            pages,
        };
        if (wantLog) out.recent = r[r.length - 1].map(s => JSON.parse(s));
        return res.status(200).json(out);
    } catch (err) {
        console.error('stats failed', err);
        return res.status(500).json({ error: 'stats failed' });
    }
};
