---
title: 🎵 欢迎来到我的音乐小窝
description: 这里收藏了小🐟一些爱听的歌曲
cover: ../img/Weather-Children13.jpg
top_img: ../img/Weather-Children13.jpg
---

# 🎵 欢迎来到小🐟的音乐小窝

学习敲代码的时候，音乐是标配 BGM～下面这个歌单会**实时同步我的网易云**，我加了什么歌这里就能听到什么 🎧

<link rel="stylesheet" href="/aplayer/APlayer.min.css">
<script src="/aplayer/APlayer.min.js"></script>
<script src="/aplayer/Meting.min.js"></script>

<div id="music-player"><meting-js api="https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r" server="netease" type="playlist" id="18532675254" theme="#ff7c9c" loop="all" order="random" preload="auto" list-max-height="400px"></meting-js><div id="music-lrc"><div id="music-lrc-contents"></div></div></div>

<div id="music-tools"><button id="music-theater-btn" type="button">🎬 大屏歌词模式</button></div>

> 💡 小提示：点左下角的 📂 可以展开完整歌单；个别 VIP 歌曲只能试听，是网易云的版权限制～
>
> 🎶 想给我推荐歌？去 [关于我](/about/) 页面找到我！

<style>
/* ---------- 普通模式 ---------- */
#music-player { margin: 18px 0 6px; position: relative; }
#music-lrc { display: none; }
#music-tools { text-align: center; margin: 6px 0 4px; }
#music-theater-btn {
  background: linear-gradient(135deg, #ff7c9c, #ff5f8f);
  color: #fff; border: none; cursor: pointer;
  font-size: 15px; font-weight: 600; letter-spacing: 1px;
  padding: 10px 26px; border-radius: 999px;
  box-shadow: 0 6px 18px rgba(255, 124, 156, .35);
  transition: transform .2s ease, box-shadow .2s ease;
}
#music-theater-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(255, 124, 156, .45); }
#music-theater-close { display: none; }

/* ---------- 大屏歌词模式 ---------- */
#music-player.theater {
  position: fixed; inset: 0; z-index: 99999; margin: 0;
  background: radial-gradient(130% 130% at 28% 18%, #43303f 0%, #191219 58%, #0d0a0f 100%);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
#music-player.theater .aplayer {
  width: min(660px, 94vw); background: transparent; box-shadow: none; margin: 0;
  height: auto !important;
}
#music-player.theater .aplayer-body {
  flex-direction: column; align-items: center;
  height: auto !important; position: static !important;
  display: flex; gap: 12px; width: 100%;
}
#music-player.theater .aplayer-info {
  padding-left: 0 !important; text-align: center; width: 100%;
  position: static !important; height: auto !important;
}
#music-player.theater .aplayer-music, #music-player.theater .aplayer-controller { width: 100% !important; }
#music-player.theater .aplayer-music .aplayer-title,
#music-player.theater .aplayer-music .aplayer-author { color: rgba(255,255,255,.92) !important; }
#music-player.theater .aplayer-icon path { fill: rgba(255,255,255,.85) !important; }
#music-player.theater .aplayer-time { color: rgba(255,255,255,.7) !important; }
#music-player.theater .aplayer-bar-wrap { margin: 0 !important; }
/* 唱片封面：大圆盘，播放时旋转 */
#music-player.theater .aplayer-pic {
  width: 250px !important; height: 250px !important;
  border-radius: 50% !important;
  box-shadow: 0 0 0 12px rgba(255,255,255,.05), 0 0 0 26px rgba(255,255,255,.03), 0 24px 70px rgba(0,0,0,.55);
}
#music-player.theater .aplayer-playing .aplayer-pic {
  animation: music-disc-spin 16s linear infinite;
}
@keyframes music-disc-spin { to { transform: rotate(360deg); } }
/* 隐藏 APlayer 自带歌词（其滚动步长写死 16px，改用下方自定义歌词墙） */
#music-player.theater .aplayer-lrc { display: none !important; }
#music-player.theater .aplayer-list { display: none !important; }
/* 自定义歌词墙 */
#music-player.theater #music-lrc {
  display: block;
  width: min(640px, 90vw); height: 264px; overflow: hidden;
  text-align: center;
  -webkit-mask-image: linear-gradient(180deg, transparent, #000 18%, #000 82%, transparent);
  mask-image: linear-gradient(180deg, transparent, #000 18%, #000 82%, transparent);
}
#music-lrc-contents { transition: transform .35s ease-out; }
#music-lrc-contents p {
  font-size: 17px; color: rgba(255,255,255,.5);
  line-height: 40px; height: 40px; margin: 0;
  transition: color .3s ease, font-size .3s ease;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
#music-lrc-contents p.current {
  color: #fff; font-weight: 700; font-size: 19px;
  text-shadow: 0 0 18px rgba(255, 124, 156, .45);
}
#music-player.theater #music-theater-close {
  display: block; position: absolute; top: 20px; right: 28px;
  background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.25);
  color: rgba(255,255,255,.85); font-size: 18px; line-height: 1;
  width: 44px; height: 44px; border-radius: 50%; cursor: pointer;
}
#music-player.theater #music-theater-close:hover { background: rgba(255,255,255,.18); }
</style>

<script>
(function () {
  const wrap = document.getElementById('music-player');
  if (!wrap) return;
  const close = document.createElement('button');
  close.id = 'music-theater-close';
  close.type = 'button';
  close.textContent = '✕';
  close.title = '退出大屏模式 (Esc)';
  wrap.appendChild(close);
  const open = () => { wrap.classList.add('theater'); document.documentElement.style.overflow = 'hidden'; };
  const shut = () => {
    if (!wrap.classList.contains('theater')) return;
    wrap.classList.remove('theater');
    document.documentElement.style.overflow = '';
  };
  close.addEventListener('click', shut);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') shut(); });
  const btn = document.getElementById('music-theater-btn');
  if (btn) btn.addEventListener('click', open);

  /* ---------- 自定义歌词墙：数据源 = 歌单自带 lrc → LRCLIB 同步歌词 → 静态兜底 ---------- */
  const lrcBox = document.getElementById('music-lrc');
  const lrcContent = document.getElementById('music-lrc-contents');
  const LINE_H = 40;
  let lrcLines = [], curLine = -1, curSongKey = null;
  const lrcCache = {};
  let lastFailKey = null, lastFailTime = 0;

  function getAplayer() {
    const mjs = document.querySelector('meting-js');
    return mjs && mjs.aplayer ? mjs.aplayer : null;
  }
  function parseLrc(text) {
    const out = [];
    (text || '').split('\n').forEach((line) => {
      const m = line.match(/\[(\d{1,2}):(\d{1,2})(?:[.:](\d{1,3}))?\](.*)$/);
      if (m) {
        out.push({ t: (+m[1]) * 60 + (+m[2]) + (+('0.' + (m[3] || '0'))), text: m[4].trim() });
      } else if (line.trim()) {
        out.push({ t: out.length ? out[out.length - 1].t : 0, text: line.trim().replace(/^\[[^\]]*\]/, '').trim() });
      }
    });
    return out.sort((a, b) => a.t - b.t);
  }
  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  async function loadLrc() {
    const p = getAplayer();
    if (!p || !p.options || !p.options.audio) return;
    const au = p.options.audio[p.index] || {};
    const key = p.index + '|' + (au.name || '');
    if (key === curSongKey) return;
    // 加载失败后 8 秒退避，避免频繁重试；到点自动重拉
    if (key === lastFailKey && Date.now() - lastFailTime < 8000) return;
    curSongKey = key;
    lrcLines = [];
    curLine = -1;
    lrcContent.innerHTML = '<p class="current">歌词加载中…</p>';
    lrcContent.style.transform = 'translateY(0)';
    const hasTs = (s) => /\[\d{1,2}:\d{1,2}/.test(s || '');
    let synced = [], plain = '';
    // ① 音源自带带时间轴的 lrc 直接用
    if (hasTs(au.lrc)) synced = parseLrc(au.lrc);
    // ② 网易云官方歌词（injahow 代理 type=lrc，歌曲 ID 从 url 字段提取）
    const idm = (au.url || '').match(/[?&]id=(\d+)/);
    if (!synced.length && idm) {
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 6000);
        const r = await fetch('https://api.injahow.cn/meting/?server=netease&type=lrc&id=' + idm[1], { signal: ctrl.signal });
        clearTimeout(timer);
        if (r.ok) {
          const text = await r.text();
          if (hasTs(text)) synced = parseLrc(text);
          else plain = text;
        } else { lastFailKey = key; lastFailTime = Date.now(); curSongKey = null; return; }
      } catch (e) {
        lastFailKey = key; lastFailTime = Date.now(); curSongKey = null; return;
      }
    }
    // ③ LRCLIB 开源歌词库（带时间轴）
    if (!synced.length && au.name) {
      try {
        const cacheKey = au.name + '|' + (au.artist || '');
        let cached = lrcCache[cacheKey];
        if (cached === undefined) {
          const q = new URLSearchParams({ track_name: au.name, artist_name: au.artist || '' });
          const ctrl = new AbortController();
          const timer = setTimeout(() => ctrl.abort(), 6000);
          const r = await fetch('https://lrclib.net/api/get?' + q.toString(), { signal: ctrl.signal });
          clearTimeout(timer);
          cached = r.ok ? await r.json() : null;
          lrcCache[cacheKey] = cached;
        }
        if (cached && cached.syncedLyrics) synced = parseLrc(cached.syncedLyrics);
        else if (cached && cached.plainLyrics) plain = cached.plainLyrics;
      } catch (e) { /* 网络失败静默降级 */ }
    }
    if (!synced.length && !plain) {
      lrcContent.innerHTML = '<p class="current">暂无歌词，请好好听歌 🎧</p>';
      return;
    }
    if (synced.length) {
      // ④ 时间轴歌词正常建墙
      lrcLines = synced;
      lrcContent.innerHTML = lrcLines.map((l) => '<p>' + (escapeHtml(l.text) || '&nbsp;') + '</p>').join('');
      curLine = -1;
      return;
    }
    // ⑤ 静态纯文本歌词（无时间轴，不滚动）
    lrcLines = plain.split('\n').filter((l) => l.trim()).map((l) => ({ t: -1, text: l.trim() }));
    lrcContent.innerHTML = lrcLines.map((l) => '<p>' + (escapeHtml(l.text) || '&nbsp;') + '</p>').join('');
  }
  function syncLrc() {
    if (!wrap.classList.contains('theater')) return;
    loadLrc();
    const p = getAplayer();
    if (!p || !lrcLines.length || lrcLines[0].t < 0) return;
    const t = p.audio ? p.audio.currentTime : 0;
    let idx = 0;
    for (let i = 0; i < lrcLines.length; i++) {
      if (lrcLines[i].t <= t + 0.3) idx = i;
    }
    if (idx === curLine) return;
    curLine = idx;
    lrcContent.style.transform = 'translateY(' + (-idx * LINE_H) + 'px)';
    [...lrcContent.children].forEach((c, i) => c.classList.toggle('current', i === idx));
  }
  setInterval(syncLrc, 200);
})();
</script>
