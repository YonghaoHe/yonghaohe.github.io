# 个人主页

## 用 JSON 维护内容

站点内容由根目录的 **`content.json`** 驱动。修改文案、时间线、论文列表等，请只编辑该文件。

生成静态页面：

```bash
python build.py
```

会覆盖生成 **`index.html`**。然后提交并推送：

```bash
git add content.json index.html
git commit -m "Update content"
git push
```

GitHub Pages 会按仓库中的 `index.html` 部署，无需在服务器上运行 Python。

### `content.json` 结构说明

| 区块 | 说明 |
|------|------|
| `site` | `lang`、`page_title`（浏览器标题） |
| `nav` | 导航链接：`label`、`href` |
| `hero` | 姓名、副标题（`subtitle_prefix` + 可选 `subtitle_link`）、简介段落、头像路径、Core Insights、社交链接 |
| `education` / `experience` | `section_title` 与 `items` 列表 |
| `publications` | 每项可设 `thumbnail_image`（有则显示图，无则显示占位）、`authors` 数组（第一项会加粗）、`links`、`tags` |
| `footer` | `copyright` |

社交图标通过 `hero.social[].icon` 指定：`wechat`、`xiaohongshu`、`x`。
