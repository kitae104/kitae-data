// 페이지 방문 기록: 같은 탭에서 같은 페이지를 30분 안에 다시 열면 중복 집계하지 않음
(function () {
    try {
        var path = location.pathname;
        var key = 'tracked:' + path;
        var last = Number(sessionStorage.getItem(key) || 0);
        if (Date.now() - last < 30 * 60 * 1000) return;
        sessionStorage.setItem(key, String(Date.now()));
    } catch (e) { /* 저장소 사용 불가 시에도 기록은 진행 */ }
    var body = JSON.stringify({ path: location.pathname, referrer: document.referrer });
    if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/track', new Blob([body], { type: 'application/json' }));
    } else {
        fetch('/api/track', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body, keepalive: true });
    }
})();
