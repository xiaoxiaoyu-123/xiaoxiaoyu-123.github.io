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

<div id="music-player"><meting-js api="https://api.injahow.cn/meting/?server=:server&type=:type&id=:id&r=:r" server="netease" type="playlist" id="18532675254" theme="#ff7c9c" loop="all" order="random" preload="auto" list-max-height="400px"></meting-js></div>

<div id="music-tools"><button id="music-theater-btn" type="button">🎬 大屏歌词模式</button></div>

> 💡 小提示：点左下角的 📂 可以展开完整歌单；个别 VIP 歌曲只能试听，是网易云的版权限制～
>
> 🎶 想给我推荐歌？去 [关于我](/about/) 页面找到我！

<style>
/* ---------- 普通模式 ---------- */
#music-player { margin: 18px 0 6px; }
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
/* 歌词墙：默认隐藏的 30px 歌词条在大屏模式展开 */
#music-player.theater .aplayer-lrc {
  display: block !important;
  position: relative !important; bottom: auto !important; left: auto !important; right: auto !important;
  width: min(620px, 90vw) !important;
  height: 240px !important; margin: 4px 0 2px !important;
  text-align: center; overflow: hidden;
  -webkit-mask-image: linear-gradient(180deg, transparent, #000 16%, #000 84%, transparent);
  mask-image: linear-gradient(180deg, transparent, #000 16%, #000 84%, transparent);
  pointer-events: none;
}
#music-player.theater .aplayer-lrc p {
  font-size: 17px !important; color: rgba(255,255,255,.5) !important;
  line-height: 34px !important; height: 34px !important;
  text-shadow: none !important; opacity: 1 !important;
}
#music-player.theater .aplayer-lrc p.aplayer-lrc-current {
  color: #fff !important; font-weight: 700; font-size: 19px !important;
}
#music-player.theater .aplayer-list { display: none !important; }
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
})();
</script>
