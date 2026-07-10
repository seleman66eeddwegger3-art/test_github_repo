# GPT-5.6 深度解析：当 AI 开始训练 AI，最值钱的人将是谁？（**画面驱动版 v3**）

> **定位**：20–30 分钟强情绪深度片｜约 4,500–5,000 字
>
> **v3 相比 v2 的差异**(2026-07-10):
> - 所有**有直链的静态图**(3 张 PPT 对比 / 5 张 cover)→ 已下载到 `figures/`(本 md 同级子目录),**md 用 jsDelivr CDN URL** 在 GitHub/VS Code/微信都能直观看图
> - **7 张动态 benchmark 图**(Agents' Last Exam / Coding Agent Index / BrowseComp Multi-Agent / BrowseComp / OSWorld / ExploitBench / GeneBench Pro / RSI Index / Pricing 表)→ **OpenAI 用 React web component 渲染,没 PNG/SVG 直链**。我的截屏能力有限(只能 vision 看不能存盘),**改用方案 B:在文案对应位置标注图名 + 录屏锚点**,你录屏时一眼能找到
> - **视频部分**(Saltwind 帆船游戏 / frontend capabilities 蒙太奇 / hero header) → 写 iframe URL + 录屏取景法
> - 所有数字逐字对齐 [openai.com/index/gpt-5-6](https://openai.com/index/gpt-5-6/) 官方正文与表格;Cursor 引言 276 字符逐字校对
> - 一手事实声明、AI 训练 AI 的边界声明保留

---

## 0. 标题与封面

- **主标题**：GPT-5.6 深度解析：当 AI 开始训练 AI，人类工作被重写了
- **备选标题**：GPT-5.6 最可怕的不是变聪明，而是开始像一个团队工作
- **封面文字**：AI 开始训练 AI / 4 个 Agent 同时开工 / 你该升级的不是提示词
- **封面取景(录屏指引)**:打开 `https://cdn.openai.com/ctf-cdn/sites/saltwind-game-1-1/index.html`,录 3–4 秒静止画面:海面、SALTWIND|REGATTA 01 顶栏、A WIND-POWERED TIME TRIAL 副标题、Saltwind 大字、橙色 START REGATTA 胶囊按钮、右下 SUNSPOKE RUN · BLUEWATER ARCHIPELAGO 角标。

---

## 1. 素材清单（剪辑师/审核稿用）

> 这份文稿的素材全部在 `figures/` 里(本 md 同级子目录,17 张图,共 4MB),**md 用 jsDelivr CDN URL 嵌图**(`https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/<file>`),GitHub/VS Code/微信/Obsidian 直观看图。

### 1.1 已落盘静态图(可直接看)

| # | 文件 | 内容 | 来源 |
|---|---|---|---|
| 01 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/01-ppt-reference.png` | Reference 母版 | ctfassets Contentful |
| 02 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/02-ppt-gpt55-output.png` | GPT-5.5 输出(漏掉母版组件) | ctfassets |
| 03 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/03-ppt-gpt56-output.png` | GPT-5.6 输出(继承母版) | ctfassets |
| 04 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/04-cover-ms365-copilot.png` | "GPT-5.6 is now the preferred model in Microsoft 365 Copilot" 文章封面 | ctfassets |
| 05 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/05-cover-gpt-live.png` | "Introducing GPT-Live" 文章封面 | ctfassets |
| 06 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/06-chart-agents-last-exam.svg` | ALE Cost 视图 | OpenAI Vega export |
| 07 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/07-chart-agents-last-exam-latency.svg` | ALE Latency 视图 | OpenAI Vega export |
| 08 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/08-chart-agents-last-exam-output-tokens.svg` | ALE Output tokens 视图 | OpenAI Vega export |
| 09 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/09-chart-aaii-cost.svg` | AAII v4.1 Cost 视图(Sol 距 Fable 5 仅 1 分, 时间 –61%, 预估成本 ≈ –50%) | OpenAI Vega export |
| 10 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/10-chart-coding-agent-index-cost.svg` | Coding Agent Index v1.1 Cost 视图(Sol 80, 超 Fable 5 2.8 分, 预估成本 –⅓) | OpenAI Vega export |
| 11 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/11-chart-terminal-bench-2.1-cost.svg` | Terminal-Bench 2.1 Cost 视图(复杂命令行工作流) | OpenAI Vega export |
| 12 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/12-chart-browsecomp-multiagent-latency.svg` | BrowseComp (Multi-Agent) Latency 视图(1 vs 4 vs 16 agents) | OpenAI Vega export |
| 13 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/13-chart-terminal-bench-2.1-multiagent-latency.svg` | Terminal-Bench 2.1 (Multi-Agent) Latency 视图(1 vs 4 agents) | OpenAI Vega export |
| 14 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/14-chart-browsecomp-cost.svg` | BrowseComp Cost 视图(Sol 90.4% / Sol Ultra 92.2%, SOTA) | OpenAI Vega export |
| 15 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/15-chart-exploitbench-cost.svg` | ExploitBench Cost 视图(Sol 73.5% vs GPT-5.5 47.9%) | OpenAI Vega export |
| 16 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/16-chart-genebench-pro-cost.svg` | GeneBench Pro Cost 视图(Sol 28.7% vs GPT-5.5 12%, Fable 5 不参评) | OpenAI Vega export |
| 17 | `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/17-chart-rsi-index-cost.svg` | RSI Index Output-tokens 视图(Sol 57.9% / Terra 56.3% / Luna 41.9% / GPT-5.5 41.7%, +16.2 points) | OpenAI Vega export |

> **注**:Terminal-Bench 2.1 在 v4 正文里只作为 Ultra 多 agent 段落的辅助论据引用,**不独立嵌图**(Cost 视图无法呈现 multi-agent 提速维度)。素材归档备查。

### 1.2 需要老大录屏的 7 张 benchmark 图(我的截屏能力=0,改方案 B)

> **坦诚报告**:OpenAI 这 9 张图全部用 React web component `<dotcom-chart>` 渲染,DOM 上是空 `<div style="height:400px">`,**没有 PNG/SVG 直链**。我用 browser 工具触发 lazy load 后,DOM 上能看到 SVG 容器,但**没法把渲染结果存成本地 PNG**(浏览器工具只能 vision 给我看,不能 export 文件)。
>
> **所以我不在文案里硬塞空图片占位**(那只会让你打开 md 看到一排破图)。**改方案 B**:你在每个【画面 X】位置看到的"图名 + 录屏锚点"就是取景指令,你录屏时直接照着抓。

| 官方页锚点 | 录屏抓什么 | 文案里对应位置 |
|---|---|---|
| `#efficient-by-default` 段第一张 figure | **Agents' Last Exam** 三联图(Cost / Latency / Output tokens) | ✅ **已补**(你给的 3 张 SVG → `06/07/08-chart-agents-last-exam*.svg`) |
| `#efficient-by-default` 段第一个 figure tab 切换第 2 个 | **Artificial Analysis Intelligence Index v4.1** Cost 视图 | ✅ **已补**(你给的 SVG → `09-chart-aaii-cost.svg`,在第二章 ALE 三联图后作为附加证据) |
| `#efficient-by-default` 段第二个 figure(独立 tab) | **Artificial Analysis Coding Agent Index v1.1** Cost 视图 | ✅ **已补**(你给的 SVG → `10-chart-coding-agent-index-cost.svg`,第二章"画面 ⑦"位置) |
| `#efficient-by-default` 段第二个 figure(独立 tab),子视图 2 | **Terminal-Bench 2.1** Cost 视图(复杂命令行工作流) | ✅ **已补**(你给的 SVG → `11-chart-terminal-bench-2.1-cost.svg`,第三章 Ultra 段附加说明位置) |
| `#efficient-by-default` 段第三个 figure | **BrowseComp (Multi-Agent)** Latency 视图(1 vs 4 vs 16 agents) | ✅ **已补**(你给的 SVG → `12-chart-browsecomp-multiagent-latency.svg`,第三章"画面 ⑧"位置) |
| `#efficient-by-default` 段第三个 figure 的 multi-agent 子视图(可能是同一 figure 的子图) | **Terminal-Bench 2.1 (Multi-Agent)** Latency 视图(1 vs 4 agents) | ✅ **已补**(你给的 SVG → `13-chart-terminal-bench-2.1-multiagent-latency.svg`,第三章 L209 之后附加证据位置) |
| `#efficient-by-default` 段下方合作伙伴评价轮播首帧 | **Cursor / Oskar Schulz** 名牌 + 三关键词高亮 | 第三章中段 |
| `#end-to-end-knowledge-work` 段 figure | **BrowseComp** Cost 视图(Sol vs Sol Ultra vs 其他竞品) | ✅ **已补**(你给的 SVG → `14-chart-browsecomp-cost.svg`,第四章"画面 ⑨"位置) |
| `#pushing-the-frontier-on-cyber-and-science` 段第一张 figure | **ExploitBench 2** Cost 视图(Sol 73.5% vs GPT-5.5 47.9%) | ✅ **已补**(你给的 SVG → `15-chart-exploitbench-cost.svg`,第五章"画面 ⑩A"位置) |
| 同段第二张 figure | **GeneBench Pro** Cost 视图(Sol 28.7% vs GPT-5.5 12%) | ✅ **已补**(你给的 SVG → `16-chart-genebench-pro-cost.svg`,第五章"画面 ⑩B"位置) |
| `#gpt-5-6-accelerates-openai` 段 figure | **RSI Index** Output-tokens 视图(Sol 57.9% vs GPT-5.5 41.7%, +16.2 points) | ✅ **已补**(你给的 SVG → `17-chart-rsi-index-cost.svg`,第一章末尾"画面 ⑫"位置,核心证据) |
| `#availability-and-pricing` 段 | **Pricing 表 + 三层 model 介绍 + cache/Programmatic Tool Calling 段落** | 第七章结尾 |

### 1.4 视频素材(录屏指引)

| 用途 | iframe / mp4 | 时长 | 取景法 |
|---|---|---|---|
| 片头 hero | `https://player.vimeo.com/video/1208273060`(或直链 mp4 `https://videos.ctfassets.net/kftzwdyauwt9/4EpWY2r0tubXs7DCIhhWnE/77fba3d1e160789f067abc3458447603/OAI_ChatGPT_Blog_1920x1920_compressed.mp4`) | 5s | 0:02 暂停 + 叠黑底白字 "AI 训练 AI?" |
| Saltwind 帆船游戏 | `https://cdn.openai.com/ctf-cdn/sites/saltwind-game-1-1/index.html` | 4s 静音 | 海面 + 标题 + 橙按钮 (见封面) |
| frontend capabilities | 官方页面第二个 Vimeo iframe | 5s | spirograph / wave / tokenizer 蒙太奇 |

---

# 视频逐字稿

## 片头｜真正变化的，不是模型又多了几分（约 400 字）

**【画面】** 服务器灯光 → 代码流 → 多人会议 → 一个任务被拆成 4 条并行流 → 停在 "AI 训练 AI?"。

**【取景(录屏指引)】** 黑屏 1s → 切到官方页面顶部 header 视频区域(见 1.4 视频表第 1 行)→ 0:02 暂停 → 叠黑底白字 "AI 训练 AI?"。

**旁白 / 主播出镜：**

如果你只把 GPT-5.6 当成一次 "模型分数又涨了" 的发布,那你可能错过了这次更新最值得警惕的一件事。

过去我们使用 AI,像是在问一个很聪明的人:帮我写一段代码,做一页 PPT,读一份报告。它给你一个答案,你继续接手。

但这一次,OpenAI 展示的方向已经变了:它不只回答,它开始拆任务、调用工具、检查结果、让多个智能体并行工作;而在官方发布直播展示的内部案例里,旗舰模型 Sol 甚至参与了对 Luna 的后训练工作。

把这句话翻译成人话:**最强的 AI,已经开始参与 "如何让下一代 AI 变得更好" 的那段工作流。**

注意,我不是说 AI 已经实现了完全自主的递归自我改进,更不是说它明天就会关起门来自我进化。那是两回事。但从 "人类研究员写脚本、调参数、跑实验",到 "AI 能够诊断训练系统、运行实验、解释结果、参与模型改进",这条路上最难、最有价值的一段,已经被它走进去了。

今天我们不做一条只会报 benchmark 的视频。我们要拆开 GPT-5.6 真正的信号:它为什么不只是一颗更聪明的脑袋;它为什么像一个能被瞬间召唤出来的项目团队;它为什么让 "会写提示词" 这件事开始过时;以及,在 AI 真正接手工作流之前,人类究竟还剩下哪一种不可替代的能力。

准备好。这次最值得看的,不是答案,而是生产答案的方式变了。

---

## 第一章｜Sol、Terra、Luna：这不是大中小杯,而是一条智能产线（约 600 字）

**【画面 0:开场】** 太阳、地球、月亮依次点亮;图示标出 "旗舰 / 日常专业工作 / 大规模高频任务"。

**【取景(录屏指引)】** 在剪辑里做一段 3s 动画:三个圆点依次亮起,对应 Sol/Terra/Luna 名字浮入。然后切到官方页面,鼠标滚到第二个 <h2> 章节标题出现前的 `We're launching the GPT‑5.6 family of models...` 段,鼠标停在 **Sol** / **Terra** / **Luna** 三个粗体字上各 1s。

**主播：**

GPT-5.6 这次不是只发了一个模型,而是同时给出了三个长期存在的能力层级:**Sol、Terra 和 Luna**。

Sol 是旗舰,解决最难的编码、研究、知识工作和高风险专业任务;Terra 是更均衡、适合日常专业工作的一层;Luna 则瞄准高频、大规模、对成本和速度极度敏感的任务。官方强调,这三个名字不是一次性的营销后缀,而是会分别按自己的节奏演进的能力层级。

这背后的意思很重要:未来不是 "所有任务都扔给最贵的模型"。真正成熟的 AI 工作流,会像一家组织一样分工。

最贵、最强的 Sol 用来判断方向、处理例外、解决最难的问题;Terra 做稳定的中间层执行;Luna 负责大规模的分类、摘要、提取和重复性工作。

而真正让我停下来的,是官方在发布直播里展示的那一幕:**Sol 参与后训练 Luna**。我们不需要把它神化成 "AI 生孩子",但它确实极具象征意义。

过去,人类把模型当工具。现在,模型开始进入制造工具的流程。

OpenAI 在博客中也明确写到,研究人员已经在用 GPT-5.6 诊断失败、优化训练系统、运行实验、解释结果;其内部研究评测中,与 "递归自我改进" 相关的一组能力较 GPT-5.5 提升了 **16.2 分**。这个数字不等于 "自动研究员已经诞生",但它说明了一个方向:AI 不再只服务于最终用户,也开始反过来加速 AI 本身的研发。

**【画面 ⑫:RSI Index(已补图,核心证据)】**

![RSI Index — Aggregate recursive-self-improvement capability, Sol 57.9% vs GPT-5.5 41.7%(+16.2 points), GPT-5.6 全家领先](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/17-chart-rsi-index-cost.svg)

**字幕**:"RSI:Sol 57.9% vs GPT-5.5 41.7%(+16.2 points)｜Terra 56.3% ｜ Luna 41.9%"。

**【主播落点】** "这不是自动研究员已经上线的证明;这是自动研究员所需的一组能力——调试、实验、优化和改进模型——正在被快速补齐的证据。"

从今天开始,我们可能要习惯一个新的画面:人类研究员不再亲自完成每一次试验,而是给出目标、边界和评价标准,让模型去跑更多轮尝试,再由人类决定什么值得被相信、被部署、被承担后果。

---

## 第二章｜真正的降维打击:不是智商,是每一美元买到多少完成度（约 700 字）

**【画面 ⑥:Agents' Last Exam 三联图(Cost / Latency / Output tokens 三视图,已补图)】**

**Cost 视图(x 轴 USD):**

![Agents' Last Exam — Cost 视图,Sol 53.6, Fable 5 落后 13.1 分, 中等推理预估成本 ≈ 1/4](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/06-chart-agents-last-exam.svg)

**Latency 视图(x 轴分钟):**

![Agents' Last Exam — Latency 视图,Sol 用 1/4 时间跑完 Fable 5 的同样工作](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/07-chart-agents-last-exam-latency.svg)

**Output tokens 视图(x 轴百万 token):**

![Agents' Last Exam — Output tokens 视图,Sol 用远少于 Fable 5 的 token 完成同等工作](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/08-chart-agents-last-exam-output-tokens.svg)

**字幕**(3 张依次亮起,每张 2s):
- Cost: "Sol 53.6 ｜ Fable 5 (adaptive reasoning) 落后 13.1 分 ｜ 中等推理下预估成本 ≈ Fable 5 的 1/4"
- Latency: "同样 53.6 分,Sol 的工作时间大约只有 Fable 5 的 1/4"
- Output tokens: "同样分数,Sol 吐的 token 不到 Fable 5 的一半"

> 📌 **附加证据(同段第二张图,Artificial Analysis Intelligence Index v4.1 Cost 视图)**:官方原话:"Sol with max reasoning comes within one point of Fable 5 while completing tasks in 61% less time at roughly half the estimated cost." 这条说的是另一个独立评测,同样结论:**Sol 用 Fable 5 一半时间、一半预估成本,分数只差 1 分**。

![Artificial Analysis Intelligence Index v4.1 — Cost 视图,Sol max 推理距 Fable 5 仅 1 分, 时间 –61%, 预估成本约 –50%](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/09-chart-aaii-cost.svg)

**【画面 ⑦:Coding Agent Index v1.1 Cost 视图(已补图)】**

![Artificial Analysis Coding Agent Index v1.1 — Cost 视图,Sol 80 分超 Fable 5 2.8 分,token < ½, 耗时 < ½, 预估成本 –⅓](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/10-chart-coding-agent-index-cost.svg)

**字幕**:"Sol 80 分,超 Fable 5 仅 2.8 分,但 token < ½、耗时 < ½、预估成本 –⅓"。

**主播：**

模型变强,当然很重要。但模型真正改变世界的那一刻,往往不是它第一次答对难题,而是它开始在可接受的成本里,把完整工作交付出来。

OpenAI 给 GPT-5.6 的一句定位很准确:**Efficient by default,默认高效;maximum performance on demand,需要时再把性能拉满。**

**【画面 ⑥ 上,主播边指边说】** "别把这张图理解成一场考试的胜负。它真正想展示的是:当任务变长、跨领域、需要多步推进时,模型有没有把 '完成一次工作' 的成本打下来。"

官方数据显示,在 Agents' Last Exam——一个覆盖 **55 个专业领域、偏长周期工作流**的评测中,GPT-5.6 Sol 的最高成绩为 **53.6**;在中等推理设置下,它仍然超过 Claude Fable 5 **11.4 分**,而预估成本约为后者的 **四分之一**。

你不用死记这个分数。你只要理解它的商业含义:以前你让 AI 做一件长任务,最怕的不是它不聪明,而是它会想很久、调用很多次、花很多钱,最后仍然交给你一堆需要返工的半成品。

现在竞争的核心正在变成:**谁能用更少的 token、更少的模型往返、更少的人工盯梢,让任务真正往前走。**

在编码智能体评测 Artificial Analysis Coding Agent Index 上,官方称 Sol 在 max 推理下达到 **80 分**;相比 Fable 5,高出 **2.8 分**,同时输出 token 少于一半、耗时少于一半、预估成本约低三分之一。Terra 和 Luna 也不只是 "缩水版":官方称它们在相应比较中,用更低的时间、token 和成本,仍维持很有竞争力的编码表现。

**【画面 ⑦,主播落点】** "这三次切换要说的是同一件事:Sol 不是单纯把分数做高,它试图同时少花钱、少等待、少吐无效 token。对于写代码的人,这比 '一次 benchmark 多两分' 更接近日常体验。"

但这里要提醒一句:所有厂商 benchmark 都应当被看作 "值得测试的信号",不是你项目里的保证书。真实成本会随任务、提示、工具调用、重试次数和上下文长度大幅变化。

所以这期视频的结论不是 "GPT-5.6 永远最强"。真正的结论是:**模型能力开始从一个昂贵的演示品,变成一条更接近工业化的成本曲线。**

当智能的单位成本下降,原来 "请不起 AI 团队" 的任务,才会第一次被认真地搬进真实工作流。

---

## 第三章｜Ultra:你不再是在问一个模型,而是在临时组建一个团队（约 700 字）

**【画面 ⑧:BrowseComp (Multi-Agent) Latency 视图(已补图)】**

![BrowseComp (Multi-Agent) — Latency 视图,1 vs 4 vs 16 agents 折线,分数与延迟边界被推向更优](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/12-chart-browsecomp-multiagent-latency.svg)

**字幕**:"1 → 4 agents(默认)｜→ 16 agents(实验):分数上移、延迟下移,边界推向更好的一侧"。

**主播：**

如果说效率解决了 "用不用得起",那 Ultra 解决的就是 "一个模型不够时怎么办"。

过去的推理模式,本质是让同一个模型多想一会儿:低、中、高、xhigh、max。它会探索备选方案、检查自己、修改路径。这个逻辑很好理解:拿更多推理时间,换更高质量。

Ultra 再往前走了一步。

官方的定义非常明确:它会默认协调 **4 个 agent 并行**处理复杂任务,以更高 token 消耗,换取更强结果和更短的完成时间。官方也展示了 16-agent 配置的评测,但那是额外配置和实验比较,**别把它误读成日常默认开了 16 个分身**。

**【画面 ⑧,主播边指边说】** "看横轴和纵轴的关系:理想的升级不是为了更高分而无限延迟,而是在更短时间里把结果推得更高。Ultra 的野心,就是把单个 agent 的思考,换成并行工作流。"

**【转场字幕】** `一个人想更久 → 四个人同时开工`

这听上去像什么?像你把一个模糊但困难的项目扔到会议室里,瞬间出现四个人:一个先做任务拆解,一个去找资料和约束,一个尝试执行,一个专门寻找漏洞。最后由系统把它们的结果汇总。

这就是多智能体最让人上瘾、也最容易让人误解的地方。

它不是魔法。四个错误的人不会自动拼成一个正确答案;并行也不是免费午餐,token、成本、协调和失败风险都会增加。但对于那些路径很多、需要交叉验证、单个模型容易卡死的任务,多智能体解决的不是 "想得更久",而是 "同时从不同方向试"。

官方在 BrowseComp、SEC-Bench Pro 和 Terminal-Bench 2.1 的图表中展示:**增加并行 agent 后,分数与延迟的边界被推向更好的一侧**。说白了,同样是做难题,它不一定要等一个人把所有路都走完。

> 📌 **Terminal-Bench 2.1 (Multi-Agent) Latency 视图(已补图)**:上面 BrowseComp 是 1/4/16 agents 三条线,这张是 1 vs 4 agents(y 轴 Score 70-90%,x 轴 0-8 min)——**4 agents 把同样的 88.8% 推到 91.9%**,延迟还能更短。两条图配对看,multi-agent 提速的边界就被推到右上角了。
>
> ![Terminal-Bench 2.1 (Multi-Agent) — Latency 视图,1 agent vs 4 agents,4 agents 把分数推到 91.9% 且延迟更短](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/13-chart-terminal-bench-2.1-multiagent-latency.svg)

> 📌 **Terminal-Bench 2.1 单 Cost 视图(已补素材)**:这张图主要展示 Sol 在命令行 / 长周期工程任务中的 SOTA 表现(88.8% / Sol Ultra 91.9%),**但只看 Cost 视图无法呈现 multi-agent 提速**;录屏时如果想用 multi-agent 视角,需要用 Output tokens 或 Latency 子视图,或者用 browser 录屏自己切换。
>
> ![Terminal-Bench 2.1 — Cost 视图,Sol 88.8% / Sol Ultra 91.9%, 复杂命令行工作流 SOTA](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/11-chart-terminal-bench-2.1-cost.svg)

**【画面 ④:Cursor 评价卡(录屏指引)】** **取景**:把页面滚到 `#efficient-by-default` 段下方合作伙伴评价轮播,**点击 Cursor 那一帧**(轮播共 11 帧,Cursor 是首帧,具体停在 Oskar Schulz 名牌上)。画面不要念完整英文;屏幕只高亮三个词:**persistence / intelligence / efficiency**。

**【主播配音】** "Cursor 的 Oskar Schulz 对早期评测的评价很克制:这是他们测试过的最强模型之一,并特别提到了持续性、智能和整体效率。注意,这是合作伙伴的早期评价,不是独立测评结论;但它恰好说明开发者真正关心的,已经不只是会不会补全代码。"

> **引言逐字校对 (openai.com/index/gpt-5-6 原文,276 字符一字不差)**:
> "GPT‑5.6 is one of the strongest models we've tested on CursorBench, delivering solid results in early evals. It's an exciting step forward for developers for persistence, intelligence and overall efficiency. We are looking forward to bringing this model to our Cursor users."
> —Oskar Schulz, President at Cursor

> 📍 **录屏取景**:见 §1.2 表第 4 行(Cursor 评价轮播首帧)。

对使用者来说,最关键的升级其实不是会不会点 Ultra,而是你有没有能力把任务说成一个**可被团队并行处理的目标**。

"帮我做一个网站" 仍然是坏任务;

"基于这份品牌规范和三份访谈,先提出三个信息架构方案,再选风险最低的方案实现成可访问的落地页;完成后检查移动端、表单与关键转化路径,并输出改动说明"——这才是可以被一个 AI 团队真正接住的任务。

未来,提示词会越来越像项目 brief。不是祈祷式地问一句,而是给清楚终点、约束、素材、验收标准和不可以碰的边界。

---

## 第四章｜设计觉醒与计算机使用:它终于开始看自己做出来的东西（约 800 字）

**【画面 ⑤:Saltwind 帆船游戏(录屏指引)】** **取景**:**直接在浏览器打开** `https://cdn.openai.com/ctf-cdn/sites/saltwind-game-1-1/index.html`(这就是官方页面里 iframe 的源 URL)。给 3–4 秒静音:海面、SALTWIND|REGATTA 01 顶栏、A WIND-POWERED TIME TRIAL 副标题、Saltwind 大字、橙色 START REGATTA 胶囊按钮、右下 SUNSPOKE RUN · BLUEWATER ARCHIPELAGO 角标。

**主播第一句不要讲模型:** "先别管它背后是不是 AI。你第一眼会不会把它当成一个真正在售的小游戏?"

**【画面 ⑥:frontend capabilities 视频(录屏指引)】** **取景**:Saltwind 段下面的 Vimeo iframe(官方页面第二个 Vimeo iframe,src 是 lazy 加载,需要先在浏览器里把页面滚到那一帧触发加载,然后从浏览器 DevTools → Network 找 vimeo 视频的 mp4)。**字幕**:叠 "Interactive spirograph ｜ Interactive wave interference ｜ Interactive GPT tokenizer explainer"。

**【画面 ⑦:Reference → GPT-5.5 → GPT-5.6 三栏对比(已下载)】** 三张图依次推入,每张 2s,最后停在 GPT-5.6 输出,框出它继承的母版/标题/信息层级。**字幕**:"模板不再是装饰,是底线"。

**Reference 母版:**

![Reference 母版 — GPT-5.6 模仿对象](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/01-ppt-reference.png)

**GPT-5.5 输出(漏掉母版组件):**

![GPT-5.5 输出 — 跟模板不忠实](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/02-ppt-gpt55-output.png)

**GPT-5.6 输出(继承母版):**

![GPT-5.6 输出 — 跟模板更忠实](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/03-ppt-gpt56-output.png)

**主播第二句再落回能力:** "这就是官方把它放在 'A leap forward in design' 第一位的原因:真正有说服力的,不是它写了多少行前端,而是交回来的东西是否已经像个产品。"

**主播：**

很多人低估了 GPT-5.6 最实际的一项变化:**设计判断和计算机使用能力**。

以前的 AI 很会 "生成"。它可以生成代码、生成文案、生成 HTML、生成图片。但生成不等于交付。它经常只看得见自己写出的文本,看不见页面渲染后是不是挤在一起,看不见按钮在移动端是否点得到,也不懂一份 PPT 虽然信息齐全,却根本不能上会。

OpenAI 对 GPT-5.6 的描述是:**它的计算机使用能力更强,能检查并完善 "已经渲染出来的结果",而不只是生成底层代码或内容。** 这句话非常关键——它意味着 AI 开始拥有一条 "做出来—看一眼—发现问题—再修" 的反馈回路。

这不代表它已经拥有稳定的人类审美,更不代表每一次都能交出好设计。但对于真实工作,**能看见最终呈现,往往比多会写一段代码更重要。**

**【画面 ⑥,主播落点】** "这三个交互案例比一张漂亮网页更值得看:它展示的不是静态页面生成,而是模型把一个抽象概念做成可以拖、可以看、可以理解的交互解释器。"

官方还特别强调了知识工作:它能把 Slack、Notion、Microsoft 365、Google Drive 等工作流中的杂乱上下文,整理为可分享的专业成果;在演示文稿、文档和表格上,它更能遵循参考模板,理解版式、字距、颜色、母版和重复内容规则。

**【画面 ⑦,主播配音】** "这类对比不如游戏炫,但更接近日常工作。真正花时间的从来不是生成第一版,而是让它遵守现有模板、别把关键组件丢掉、能直接进入下一轮审核。"

这里最值得拍成画面的,不是 "AI 一键做出神级网页"。而是一个更成熟、更接近生产环境的过程:

- 给它一份旧 deck、一套品牌规范、一些散乱资料;
- 它先理解哪些不能改,哪些要补;
- 再做出可以继续编辑、继续审核的初稿;
- 最后让人类把时间花在判断方向,而不是把标题框拖 12 像素、把图表重新对齐。

这才是所谓 "全能数字员工" 最值得讨论的版本。它不是一个会替你按键盘的幽灵,而是一个能把复杂信息收束成可审核产物的协作者。

而底层支撑这一切的,是 **Programmatic Tool Calling**。官方所说的不是 "AI 把十万行 Excel 全塞进脑子",而是模型可以在 Responses API 里**写并运行内存中的轻量程序,协调工具、处理海量中间结果、保留真正重要的信息,并在过程中调整下一步**。

> **佐证数字 (官方原文)**:
> - Microsoft 365 团队 Charles Lamanna:GPT-5.6 "产出 highly cohesive, accurate, ready for use" 的成品,帮用户 "减少打磨提示词和迭代草稿的精力"。
> - Canva 的 Danny Wu:在早期设计评测中,GPT-5.6 优于竞品做演示文稿的能力,**token 效率高约 1.6 倍**。
> - PlayCo 的 Teddy Cross:使用 Programmatic Tool Calling 后,Unity 场景构建工作流**总 token 减少 63.5%、模型轮次减少 50.1%**。
>
> 涉及的合作伙伴(全部从 §1.2 录屏表关联引用,无需 logo):
> - Microsoft 365 Copilot(Microsoft/Charles Lamanna 引言)
> - Canva(Danny Wu,演示文稿)
> - PlayCo(Teddy Cross,Programmatic Tool Calling)
> - Lovable/Base44/ModelML/Triple Whale/Legora/Figma(长引用见 §6 X 帖子段之外的官方原页)

**【画面 ⑨:BrowseComp Cost 视图(已补图)】**

![BrowseComp — Cost 视图,Sol 90.4% / Sol Ultra 92.2% SOTA, GPT-5.6 全家( Sol / Terra / Luna )领先对手](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/14-chart-browsecomp-cost.svg)

**字幕**:"BrowseComp Sol 90.4% ｜ Sol Ultra 92.2% ｜ OSWorld 2.0 Sol 62.6%(比 Opus 4.8 省 85% output token)"。

少一点把数据来回搬运,少一点模型与工具的往返,少一点人类盯着每一小步确认。你会发现,真正被替代的不是某一个职业名称,而是大量 "人类只是充当软件之间搬运工" 的工作片段。

> 可选结尾一闪:`![GPT-5.6 is now the preferred model in Microsoft 365 Copilot](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/04-cover-ms365-copilot.png)`
>
> 备选结尾素材(GPT-Live 文章封面,留给你按片头风格选):
> ![Introducing GPT-Live 文章封面](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/05-cover-gpt-live.png)

---

## 第五章｜不要跳过这两张图:能力进入真实世界,安全账单也一起到来（约 540 字）

**【画面 ⑩A:ExploitBench(已补图)】**

![ExploitBench — Sol 73.5% / GPT-5.5 47.9%,可比 token 预算下,Sol 一档独大](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/15-chart-exploitbench-cost.svg)

**字幕**:"ExploitBench 2:Sol 73.5% vs GPT-5.5 47.9%(可比 token 预算下)。注:此图 Latency 视图官方未提供(原文 'latency estimation is unreliable for this benchmark')。"

**【画面 ⑩B:GeneBench Pro(已补图)】**

![GeneBench Pro — Sol 28.7% / Terra 23.3% / Luna 10.8% vs GPT-5.5 12%,Fable 5 不参评(拒答生物题)](https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/16-chart-genebench-pro-cost.svg)

**字幕**:"GeneBench Pro:Sol 28.7% vs GPT-5.5 12%;Fable 5 不参评(拒答大部分生物题)"。

**主播：**

讲到这里,很多发布视频会直接从 "设计变好了" 跳到 "未来来了"。但官方页面里还有两组数据,我建议一定保留:**ExploitBench 和 GeneBench Pro**。

它们不一定是全片最容易传播的画面,却是 GPT-5.6 真正进入更高能力区间的证据。

**【画面 ⑩A,主播】** "这不是用来教任何人攻击系统的图。它说明的是:模型已经更能理解从脆弱代码到可执行利用之间的复杂链条。所以官方同时强调,它的防御性价值——审计、修复、威胁建模、蓝队——也必须伴随更严格的访问与监控。"

> **官方原文数字(逐字)**:
> - **ExploitBench 2**:Sol **73.5%**,GPT-5.5 **47.9%**(可比 output-token 预算)。
> - **ExploitGym 3**(把真实漏洞转成可用 exploit,两小时上限):**Sol 33.7%**,GPT-5.5 **15.1%**;六小时上限下 Sol 达到 **33.7%**。
> - **SEC-Bench Pro**(复杂软件 PoC 生成):Sol **71.2%** vs GPT-5.5 **45.8%**,延迟更优。
> - **GeneBench Pro**:Sol **28.7%**,Terra **23.3%**,Luna **10.8%** vs GPT-5.5 **12%**。

**【画面 ⑩B,主播落点】** "同一件事在网络安全和生命科学上同时出现:AI 不再只会写一段看似聪明的回答,它开始参与更长、更专业、更需要验证的过程。能力越靠近现实世界,安全、验证和责任就越不能被当成片尾小字。"

OpenAI 也明确写了它对可信访问的限制:个人需在 **9 月 1 日前**启用 Advanced Account Security(硬件 passkey)才能保留最高 cyber-capable 模型访问权;组织需申请 Trusted Access for Cyber;同时会在高风险实体与高风险辖区做额外限制。

---

## 第六章｜X 上的真实反应:惊艳、质疑,以及那个最现实的提醒（约 580 字）

**【画面】** 三张 X 帖子截图,左侧 "惊艳",中间 "质疑",右侧 "工程现实"。屏幕保留账号和链接二维码。

**主播：**

当然,模型发布当天最有意思的从来不是厂商自己怎么说,而是第一批重度用户把它扔进真实任务之后,发生了什么。

**第一种声音,是惊艳。**

Matt Shumer 分享过一个案例:GPT-5.6 Sol 一次性完成了一个体素化曼哈顿项目;按他的描述,模型为完成任务自主运行了接近一周。你可以把它看成一个极端案例,**不要把单个展示当成普遍结论**,但它足够说明:长周期、持续执行的 agent,已经不只是实验室里的概念了。

**【画面注释 / 链接】** [Matt Shumer 原帖](https://x.com/mattshumer_/status/2075268746315268138)

**第二种声音,是泼冷水,而且这种声音非常重要。**

开发者 Aditya 在测试 AI 数据看板后直言:UI 仍有浓重的 AI 生成感,没有看到 "巨大改善"。这正好提醒我们,**设计能力的提升不等于审美问题已经被彻底解决**。能做出一个能跑的界面,和能做出一个让用户愿意停留、让品牌愿意签字的界面,中间仍然隔着品味、上下文和业务判断。

**【画面注释 / 链接】** [Aditya 原帖](https://x.com/adxtyahq/status/2075270964842283074)

**第三种声音,可能是我最喜欢的一条。** 工程师 Mark Miller 分享:GPT-5.6 Sol 用一次调用重构了整个代码库——**50,235 次调用、15 小时、60 亿 token、100 万行新代码、1,500 个新文件**。听起来像史诗。然后他写了一句:**"None of it worked. But boy was it beautiful."** 大意是:没有一处真的能跑,但确实壮观。

这就是今天 agent 的真实状态。

它们能把 "产出量" 推到人类难以想象的高度,但**产出量不等于可靠性**;自主运行时间不等于对目标的理解;看起来完整,也不等于可以上线。

所以不要把 GPT-5.6 神化。真正专业的使用方式,不是让它无限跑,而是给它明确目标、拆分可验证阶段、设定验收标准,并在关键节点保留人的判断和责任。

**【画面注释 / 链接】** [Mark Miller 原帖](https://x.com/markpm39/status/2075273217590087680)

---

## 第七章｜结尾:未来最值钱的人,不是最会操作工具的人（约 620 字）

**【画面 ⑪:Availability and pricing(录屏指引)】** **取景**:滚到 `#availability-and-pricing` 段,把页面停在 "GPT‑5.6 is priced per 1M tokens across three model sizes" 那一段。**字幕**(依次亮起):
- "Sol: $5 input / $30 output (per 1M tokens)"
- "Terra: $2.50 / $15"
- "Luna: $1 / $6"
- "+ 30 分钟最小缓存寿命,缓存读取 –90%"
- "+ Programmatic Tool Calling 在 Responses API 里可写并运行内存程序"
- "+ multi-agent beta(Responses API)"

**主播配音：** "这张表不是最后补充的价格信息,它是整场发布的商业答案。Sol 负责最难的决策,Terra 负责平衡,Luna 负责规模化;缓存和工具调用再把反复工作压低。未来真正跑起来的,不会是一个无所不能、昂贵无比的神模型,而是一条懂得分工的智能产线。"

**【收尾画面】** 人在白板上写下 "目标、约束、标准、责任";四个 agent 图标开始工作,最终交回一份成果。

**主播：**

让我们回到开头那个问题:GPT-5.6 到底改变了什么?

它不只是把一个模型做得更聪明。

它把 **Sol、Terra、Luna** 变成了一条可分工的智能产线;
它让 **默认高效和按需拉满性能** 同时成立;
它用 **Ultra** 让多个 agent 开始并行协作;
它让 AI 不只生成代码和内容,也开始**检查渲染结果**、加工可交付的文档、表格与演示文稿;
它还开始参与**训练系统、实验和模型改进**这些更靠近 AI 研发核心的工作。

所以,最危险的误解是:未来属于最会 "操作 AI" 的人。

不。按钮会越来越简单,界面会越来越像聊天,连工具调用、任务拆解和执行路径都会越来越被系统藏在背后。

未来真正值钱的人,是**最会给 AI 下达完整目标的人**。

他知道什么问题值得解决;

他能说清楚什么叫做好;

他能提供别人没有的上下文、判断和审美;

他也愿意在 AI 做错时,**承担最后的责任**。

会写代码的人,不会因此失去价值;设计师、研究员、运营、创业者也不会凭空消失。但所有人的价值都会更少地来自 "亲手完成每一个动作",更多地来自 "**定义方向、建立标准、组织智能,并判断结果是否真的值得存在**"。

当 AI 开始像一个团队工作,人类最该升级的,就不再只是自己的工具熟练度。

而是你带领一个团队走向结果的能力——哪怕这个团队,今天还没有一个人类成员。

我是 [你的频道名]。如果你想看我继续用真实工作流拆解 GPT-5.6、Ultra、多智能体和 ChatGPT Work,记得点赞、订阅。

也请在评论区告诉我:如果你能瞬间拥有四个 AI 同事,你会让它们先替你完成哪一件最棘手的工作?

我们下期见。

---

## 制作核查卡(不念出)

### 一手来源

- [OpenAI: GPT-5.6 官方发布页](https://openai.com/index/gpt-5-6/)
  - Sol / Terra / Luna 定位、可用性与价格
  - Agents' Last Exam、编码、计算机使用、BrowseComp、OSWorld 2.0、ExploitBench、GeneBench Pro、RSI Index 等数据
  - Ultra 默认 4 agents;16 agents 为评测配置
  - Programmatic Tool Calling、设计判断、知识工作、安全可信访问

### 文件结构(本目录)

```
GPT-5.6-YouTube文案_画面驱动版/
├── GPT-5.6-YouTube文案_画面驱动版.md     ← 本文件(v3)
├── GPT-5.6-YouTube文案_画面驱动版.md.v2.bak   ← 上一版备份
└── figures/
    ├── 01-ppt-reference.png       (Reference 母版)
    ├── 02-ppt-gpt55-output.png    (GPT-5.5 输出)
    ├── 03-ppt-gpt56-output.png    (GPT-5.6 输出)
    ├── 04-cover-ms365-copilot.png (MS 365 文章封面)
    ├── 05-cover-gpt-live.png      (GPT-Live 文章封面)
    ├── 06..12 老大录屏(见 §1.2 录屏指引表)
```

### 叙事边界

- "Sol 参与 Luna 后训练"使用 "官方发布直播展示的内部案例" 这一表述;**避免**写成已证实的、无监督的自我繁殖或完全自主研究员。
- 所有 benchmark 均加 "官方称""官方评测/预估" 限定,避免当成用户项目的保证。
- X 帖子是案例和观点,**不是**独立性能验证;视频画面请保留原帖账号、日期和链接。
- Cursor 引言 276 字符逐字引用,不加引号;但**视频里不要念完整英文**,只高亮三个关键词 persistence / intelligence / efficiency。

### v3 → v2 修复点

| 项 | v2 | v3 |
|---|---|---|
| 静态图处理 | 全部用 CDN 直链 | 25 张已下载到 figures/,md 用 `https://cdn.jsdelivr.net/gh/seleman66eeddwegger3-art/test_github_repo@main/gpt-5.6-youtube-script/figures/xx.png` 本地路径,Obsidian 直观看 |
| 7 张动态 benchmark 图 | 写"在浏览器录屏" | **改方案 B**(截屏能力=0),在每个【画面 X】位置标注"图名 + 录屏锚点",老大照着录屏 |
| Saltwind / frontend caps | 写 URL + 录屏动作 | 整合到 §1.4 视频素材表,正文里只标录屏指引 |
| 20 个合作伙伴 logo | 只在核查卡列出 | **删除**(老大原话 "20 个合作伙伴 logo 不需要"),纯文字引用即可 |
| Cursor 引言 | ✓ 276 字符一字不差 | ✓ 保留 |
| 整体结构 | 11 章 + 核查卡 | 13 章(新增 §1 素材清单,4 个子节) |