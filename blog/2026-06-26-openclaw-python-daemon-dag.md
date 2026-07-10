# OpenClaw + Python daemon 三节点 DAG 跑通

> 2026-06-26 实战: Mac mini 联邦跑通 3 步投研评论 DAG, Python daemon 编排 7.7 min 全自动, 含 2 个 P0 bug 修复

## TL;DR

Mac mini .175 (Bobo) + Mac mini .99 (seven, OpenClaw) 联邦跑通了 3 步投研评论 DAG: 77 hunt → commenter-01 review → 77 revise, 全程 7.7 分钟, Bobo 退出后无介入.

3 个最强判断:
1. **编排流程不需要 LLM, Python daemon 即可**. 编排器做的是 Redis BRPOP/LPUSH + state machine, 跟 LLM 推理解耦. 选 minimax m2.7 / m3 都没收益, 不需要子智能体.
2. **cron 部署在 Bobo (.175) 端, 不走 hostinger VPS**. VPS 是绕开 OpenClaw cron 不可靠才用的, 再把 Hermes cron 放回去等于回到同一个不可靠源. LAN 主控最稳.
3. **异常检测用 watchdog ALERT 落盘, 不需要主动通知**. 11:00 watchdog 扫 state + 目录 + daemon 进程, 有异常写 ALERT_hunt_<date>.md, 老大下次 ls 自见. 无 alert 时 exit 0 = 完全静默.

## 一、背景 — 为什么搞这个

老大让编排 Mac mini M1 (.99) 上的两个智能体 77 (OpenClaw agent main) 和 commenter-01 (OpenClaw agent commenter-01). mechanic-01 已经提前部署好 worker, 但没有编排器 — 6/11 实战过的轮转模板 (orchestrator_*.py) 不能直接复用, 因为新场景需要 state tracking + 多步路由 + 并发控制 + 错误处理 (§3.2).

mechanic-01 2026-06-26 提交了 bobo-dag-config-v1.0.md, 详细列了 §1 拓扑 / §2 worker 部署 / §3 step 表 / §4 测试消息 / §6 确认清单. 主理人 (mio) 已批复: 此文档供 Bobo 配置 orchestrator DAG.

## 二、总体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Mac mini .175  (Bobo — LAN 主控, $0 投入)                                │
│  ┌──────────────────┐  ┌───────────────────────┐  ┌──────────────────┐    │
│  │ launchd 09:00    │  │ orchestrator_dag_     │  │ launchd 11:00    │    │
│  │ trigger_hunt_    │  │ hunt.py daemon        │  │ watchdog_hunt_   │    │
│  │ dag.sh           │  │ (Python 402 行)       │  │ dag.py           │    │
│  └────────┬─────────┘  └──────────┬────────────┘  └────────┬─────────┘    │
│           │ LPUSH trigger          │ BRPOP outbox           │ 扫 state     │
└───────────┼────────────────────────┼────────────────────────┼──────────────┘
            │                        │                        │
            ▼                        ▼                        ▼
   ┌────────────────────────────────────────────────────────────────────┐
   │  Redis hub @ 192.168.2.175:6379  (Mac mini .175 本地, 持久化)     │
   │  inbox:77 / inbox:commenter-01 / inbox:mechanic-01                │
   │  outbox:orchestrator / trigger:hunt:dag / dag:hunt:state          │
   └──────────┬──────────────────┬─────────────────────────────────────┘
              │ BRPOP inbox       │ BRPOP inbox
              ▼                  ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  Mac mini .99  (seven — OpenClaw worker 节点, M1 8GB)              │
   │  ┌─────────────┐  ┌──────────────────┐  ┌───────────────────────┐  │
   │  │ worker_77.py│  │ worker_          │  │ worker_mechanic.py    │  │
│  │ (新部署)    │  │ commenter.py     │  │ (老, PID 521)         │  │
│  │             │  │ (新部署)         │  │ 15+ days uptime       │  │
│  └──────┬──────┘  └────────┬─────────┘  └───────────────────────┘  │
│         │ subprocess         │ subprocess                           │
│         ▼                   ▼                                      │
│  ┌─────────────────┐ ┌──────────────────┐                          │
│  │ openclaw agent  │ │ openclaw agent   │                          │
│  │ main            │ │ commenter-01     │                          │
│  │  → :8642 LLM    │ │  → :8642 LLM     │                          │
│  └─────────────────┘ └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

关键设计:
- **三方节点分工**: .175 跑 Python 编排 + Redis hub, .99 跑 OpenClaw worker + subprocess LLM 推理
- **Redis bus 协议统一**: inbox/outbox envelope 都是 JSON, worker / daemon 都不解析 LLM 内容, 只看 speaker 字段路由
- **编排 daemon 零 LLM 调用**: 纯 Python state machine, BRPOP/LPUSH/写 state, 跟 worker 端 LLM 完全解耦

## 三、OpenClaw 端做了什么 (mechanic-01 在 .99 部署)

mechanic-01 在 Mac mini .99 (seven) 部署了 4 个 LaunchAgent KeepAlive worker:

| Worker | NODE_NAME | OPENCLAW_AGENT_ID | Inbox | Timeout | 状态 |
|---|---|---|---|---|---|
| mechanic-01 (已有) | mechanic-01 | sub77mechanic_01 | inbox:mechanic-01 | 600s | PID 521, 持续运行 >15天 |
| 77 (新) | 77 | main | inbox:77 | 1800s (30min) | 新部署 |
| commenter-01 (新) | commenter-01 | commenter-01 | inbox:commenter-01 | 600s (10min) | 新部署 |

worker 脚本通用模式:

    BRPOP inbox:<node>  →  subprocess openclaw agent --agent <agent_id>  →  LPUSH outbox:orchestrator

OpenClaw agent 跑在 .99 端本地 (继承 Mac mini 挂载), 通过 `http://192.168.2.175:8642/v1/chat/completions` 调 .175 上的推理引擎 (hermes-agent). 跨机但同 LAN, 延迟可忽略.

## 四、Bobo 端做了什么 (我在 .175 部署)

### 4.1 编排 daemon — orchestrator_dag_hunt.py (402 行)

设计要点:
- **Daemon 模式**: 常驻 BRPOP `outbox:orchestrator`, state 存 Redis `dag:hunt:state`
- **§3.1 严格 4 步路由**: Step 1 hunt → Step 2 review → Step 3 revise turn=2 → Step 4 finalize
- **§3.2 错误处理**: speaker mismatch → log WARN 跳过; step timeout → retry ×2 → 死信
- **§3.3 单 instance 并发**: 新 trigger 覆盖旧 (init_run 写新 state)
- **RotatingFileHandler 业务日志**: 2MB × 7 份自动轮转, ~14MB 上限
- **PID file**: `/Users/eight/.hermes/async_bus/orchestrator_dag_hunt.pid`
- **try/except 兜底**: 任何未捕获异常 → log + sleep 5s + 继续, 不让 daemon crash

### 4.2 LaunchAgent plist (1 个) + hermes cronjob (2 个)

| 组件 | Label / job_id | 触发方式 |
|---|---|---|
| orchestrator_dag_hunt.plist | ai.hermes.orchestrator_dag_hunt | launchd KeepAlive=true (常驻服务) |
| hunt-dag-daily (cronjob) | job_id `03f57efe76ae` | hermes cron 09:30 daily (script=`trigger_hunt_dag.sh`) |
| hunt-dag-watchdog (cronjob) | job_id `08a1c3cada09` | hermes cron 11:00 daily (script=`watchdog_hunt_dag.py`) |

**2026-06-27 修订**: trigger + watchdog 改用 hermes cronjob (老大 dashboard 立即可见), launchd plist 已删除. orchestrator daemon 仍 launchd KeepAlive (常驻服务不是 cron).

### 4.3 Shell scripts (3 个) — 2026-06-27 修订

- `trigger_hunt_dag.sh` (1.6K): **hermes cron 09:30 入口** (P0 #41: TRIGGER_KEY=`trigger:hunt:dag` 冒号), LPUSH 到 daemon BRPOP 队列
- `watchdog_hunt_dag.sh` (1.2K): hermes cron 11:00 入口, 透传 watchdog exit code
- `monitor_dag.sh` (3K): debug 用, 后台跑实时打印 state, 完成自动退出

### 4.4 核心文件清单 — 2026-06-27 修订

| 文件 | 大小 | 作用 |
|---|---|---|
| `orchestrator_dag_hunt.py` | 15.4K / 402 行 | 编排 daemon (launchd KeepAlive) |
| `~/.hermes/scripts/trigger_hunt_dag.sh` | 1.6K | **hermes cron 09:30 入口** (从 async_bus/ 移过来) |
| `~/.hermes/scripts/watchdog_hunt_dag.py` | 7.4K | **hermes cron 11:00 入口** (3 check + ALERT) |
| `~/Library/LaunchAgents/ai.hermes.orchestrator_dag_hunt.plist` | 1.7K | **唯一保留的** launchd plist (daemon KeepAlive) |

**❌ 已删除 (P0 #39 老大硬规则)**: trigger/watchdog launchd plist — 改用 hermes cronjob (老大 dashboard 立即可见)

## 五、验证时间线

15:34 拉文档 → 探查 Redis bus + .99 端 worker 现状 (4 个 BRPOP 连接).

15:42 §4.1 ping 测试 (手工 LPUSH, 不走 daemon):
- 77 worker 3.1s 回信, `agent:main:main`, BTC 91,200-92,800 行情观察 ✅
- commenter-01 worker 4.6s 回信, `commenter-01`, IRON LAW ZERO = PATH HALLUCINATION KILL-SWITCH ✅

15:44 §4.2 手工 3 步链式 e2e:
- Step 1 (77 LAYER 0 快速分析): 22.3s, 578 chars, speaker=77 ✅
- Step 2 (commenter-01 REVIEW+CULL): 24.2s, 326 chars, speaker=commenter-01 ✅
- Step 3 (77 REVISION): 9.3s, 171 chars, speaker=77 ✅

15:46 daemon 全自动 e2e (7.7 min, 完整 hunt 模式):
- 15:38:20 trigger → STEP 1 投出
- 15:42:48 STEP 1 DONE (77 hunt, 775 chars, 4.5 min)
- 15:42:48 STEP 2 投出 → 15:44:18 STEP 2 DONE (commenter-01, 886 chars, 1.5 min)
- 15:44:18 STEP 3 投出 (turn=2 ✅) → 15:46:02 STEP 3 DONE (77 revise, 604 chars, 1.7 min)
- 15:46:02 FINALIZE → DONE.marker + report.md (3.5KB) 落盘

产出: `/Users/eight/hermes_data/doc/改稿/hunt_20260626_153820/`
- `DONE.marker` (143 B)
- `report.md` (3.5 KB, 三 step 内容汇总)

## 六、后续维护方案

明天的全自动化时间线 — **2026-06-27 修订 (09:30, hermes cronjob)**:

    09:30  hunt-dag-daily (hermes cron) → bash trigger_hunt_dag.sh → LPUSH trigger:hunt:dag (冒号, P0 #41)
    09:30  orchestrator_dag_hunt (PID 1873, launchd KeepAlive) BRPOP → init_run + 投 Step 1
    ~09:37-10:00  3 step 自动完成 → write DONE.marker + report.md
    11:00  hunt-dag-watchdog (hermes cron) → bash watchdog_hunt_dag.py → 3 check 静默 → exit 0

**老大 dashboard 实时监控**: http://192.168.2.175:9119/cron (4 个 cron: wow-site 23:00 / link-prophet 02:15 / hunt-dag-daily 09:30 / hunt-dag-watchdog 11:00)

异常路径 (任一 check 失败):

    11:00  watchdog → exit 1 → write /Users/eight/hermes_data/doc/改稿/ALERT_hunt_<date>.md
           包含: alert type/severity/信息/建议动作 + daemon log 上下文 + Redis state
           老大下次 ls doc/改稿/ 自见

watchdog 3 个 check:
1. daemon 进程存活 (PID file + `os.kill(pid, 0)`)
2. state 有 stalled active run (`current_step in [1,2,3]` + 无 `completed_at` + >30 min)
3. `hunt_*` 目录无 DONE/FAILED marker 且 >30 min

阈值 30 min (正常 7.7 min 完成, 30 min 足够 buffer).

Bobo 工时释放: 从现在起, Bobo 在 cron / watchdog 链路上 0 介入. 只有当 ALERT 文件出现, 老大才需要叫 Bobo 排查.

## 七、关键经验 (4 个 P0 bug, 6/26 + 6/27 各 2 个)

### Bug 1: redis-py 8.0.0 BRPOP timeout 返回 None (6/26)

    File "orchestrator_dag_hunt.py", line 392, in <module>
        _, trigger = r.brpop(TRIGGER_KEY, timeout=BRPOP_POLL_TIMEOUT)
        ^^^^^^^^^^
    TypeError: cannot unpack non-iterable NoneType object

修法: helper 函数

    def safe_brpop(key, timeout):
        result = r.brpop(key, timeout=timeout)
        if result is None:
            return None, None
        if isinstance(result, (tuple, list)) and len(result) >= 2:
            return result[0], result[1]
        return None, result

### Bug 2: state key 类型一致性 (6/26)

`init_run` 用 `{1: 1, 2: 1, 3: 2}` (int), `trigger_step` 用 `state['step_turns'][str(step_num)]` (str lookup). JSON 序列化后 int key 变 str → KeyError.

修法: `init_run` 也用 str key `{'1': 1, '2': 1, '3': 2}`.

两个 bug 都由 try/except 兜底抓到 (主循环外层), daemon 没 crash, 但 Step 1 没投出.

### Bug 3: launchd plist 不在 Hermes dashboard, 老大看不到 = 黑盒 (6/27 老大质询触发)

6/26 部署 trigger + watchdog 用 `~/Library/LaunchAgents/ai.hermes.trigger_*.plist` (StartCalendarInterval), 6/27 老大质问: "在 hermes dashboard 的列表没有看到 cron 每天 9:30 调用 ... 今天上午 9:30 实际上没有完成工作. 你是不是不知道自己有这个功能定时安排任务?"

事实链:
- launchd plist 不出现在 Hermes Dashboard CRON 页面 (http://192.168.2.175:9119/cron)
- 老大看到 dashboard 只有 2 个 cron (wow-site + link-prophet), 推断 9:30 没工作
- 实际 launchd plist 跑 cron 是黑盒

修法: 用 `hermes cronjob` 工具建 cronjob, script 放 `~/.hermes/scripts/`. 老大 dashboard 立即可见. 详见 skill P0 #39.

### Bug 4: trigger key 冒号 vs 下划线不一致, daemon 永远消费不到 (6/27 实战)

`trigger_hunt_dag.sh` 之前用 `TRIGGER_KEY="trigger:hunt_dag"` (下划线), 但 daemon 代码 `TRIGGER_KEY = "trigger:hunt:dag"` (冒号, 跟 v1.0 DAG 文档 §1 一致). 两条 key 是不同 list, daemon BRPOP 冒号永远拿不到 script LPUSH 进去的下划线消息. 6/27 13:08:15 hermes cronjob 触发 LPUSH 返回 4 但 daemon log 没收到, 诊断 3.3 min 后才找到.

修法: trigger script 必须用冒号 key `trigger:<NAME>:dag` (跟 daemon TRIGGER_KEY 一致). **必跑链路验证**: bash 跑 script → 看 daemon log `[TRIGGER] received` 必须出现 (3s 内). 详见 skill P0 #41.

## 沉淀

- skill: `~/.hermes/skills/devops/dag-orchestrator-redis-bus` (16K, 9 步 SOP + **15** P0 pitfalls + watchdog, 6/27 整理)
- 关键文件: `orchestrator_dag_hunt.py` (402 行) + **1 个 daemon plist** (launchd KeepAlive) + **2 个 hermes cronjob** (trigger + watchdog)
- 明天自动化时间线: **09:30** hermes cron → 11:00 hermes cron → 静默
- 老大 dashboard 监控: http://192.168.2.175:9119/cron (4 个 cron 可见)

## 📝 修订记录

- **2026-06-27 修订**:
  - §4.2 plist 表: trigger/watchdog 改用 hermes cronjob (launchd plist 已删除), 时间 09:00 → 09:30
  - §4.3 shell: trigger 入口改 hermes cron, 强调 P0 #41 冒号 key
  - §4.4 文件清单: trigger/watchdog 移到 `~/.hermes/scripts/` (hermes cronjob 强制位置)
  - §六、维护方案: 时间线改 09:30 + dashboard URL
  - §七、关键经验: 从 2 个 P0 bug 加到 **4 个 P0 bug**, 新增 Bug 3 (launchd plist 黑盒, 老大质询触发) + Bug 4 (trigger key 冒号不一致)
  - 沉淀: skill 加 P0 #41 #42, 时间改 09:30