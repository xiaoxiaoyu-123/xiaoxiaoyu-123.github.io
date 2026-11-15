// Umami Cloud 统计脚本注入（Hexo injector，主题无关、升级安全）
hexo.extend.injector.register(
  'head_end',
  '<script defer src="https://cloud.umami.is/script.js" data-website-id="215130f2-7efc-4218-b160-8df1a92d1906" data-domains="xiaoxiaoyu-123.github.io"></script>',
  'default'
);
