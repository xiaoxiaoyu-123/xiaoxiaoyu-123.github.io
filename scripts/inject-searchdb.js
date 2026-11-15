// searchdb 前端搜索脚本注入（async 主题依赖它处理搜索结果；本地化避免 unpkg 依赖）
hexo.extend.injector.register(
  'head_end',
  '<script src="/js/searchdb.js"></script>',
  'default'
);
