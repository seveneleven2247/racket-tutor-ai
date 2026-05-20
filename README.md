# Racket Tutor AI

一个面向有 C++ 基础学习者的 56 天 Racket 学习网站。

功能：

- 56 天每日课程计划，每天一个独立 category
- 每天详细讲解、C++ 对照、Racket 示例、练习和 checklist
- 本地保存每日 checklist 进度
- 上传作业文件或粘贴代码
- AI 批改作业，指出正确性、风格、Racket 思维和下一步改进
- 没有 `OPENAI_API_KEY` 时，自动使用本地规则反馈，方便离线体验

## 运行

```bash
cd ~/Public/racket-tutor-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py --port 5055
```

浏览器打开：

```text
http://127.0.0.1:5055
```

## 配置 AI 批改

编辑 `.env`：

```bash
OPENAI_API_KEY=你的 OpenAI API key
OPENAI_MODEL=gpt-5.4-mini
```

然后重启：

```bash
python app.py --port 5055
```

## 公开访问

### 临时分享

如果只想临时给别人打开，可以用隧道工具：

```bash
cloudflared tunnel --url http://127.0.0.1:5055
```

它会打印一个 `https://...trycloudflare.com` 地址，可以直接分享。

当前这次运行生成的临时地址：

```text
https://municipal-packets-ticket-believes.trycloudflare.com
```

当前本机测试访问码：

```text
share123
```

这个地址只有在本机 Flask 服务和 cloudflared 进程都保持运行时有效。

### 局域网分享

```bash
python app.py --host 0.0.0.0 --port 5055
```

然后用同一 Wi-Fi 下的其他设备访问：

```text
http://你的电脑局域网IP:5055
```

### 部署到真正公网

推荐 Render、Railway、Fly.io 或 VPS。这个项目已经包含：

```text
Procfile
render.yaml
```

云平台环境变量建议：

```bash
OPENAI_API_KEY=你的 OpenAI API key
OPENAI_MODEL=gpt-5.4-mini
FLASK_SECRET_KEY=随机长字符串
ACCESS_CODE=你想设置的访问码
```

`ACCESS_CODE` 建议一定设置。公开网站会开放作业上传和 AI 批改，如果不加访问码，陌生人可能上传文件或消耗你的 API key。

## 目录

```text
app.py              Flask 后端
course_data.py      56 天课程生成逻辑
static/index.html   前端页面
static/styles.css   样式
static/app.js       前端交互
data/uploads/       上传作业保存目录
data/submissions.json 自动生成的提交记录
```
