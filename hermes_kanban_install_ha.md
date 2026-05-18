# Home Assistant 部署全记录 — Kanban 多角色协作

> 本文档完整记录了从零到一搭建 Home Assistant 的整个过程，包括每次交互中我（AI Agent）的建议、你（人类管理员）的选择与决策、以及在服务器上实际执行的命令。

---

## 目录

1. [环境准备](#1-环境准备)
2. [创建多角色分工](#2-创建多角色分工)
3. [T1+T2：部署 HA 容器](#3-t1t2部署-ha-容器)
4. [安装 HACS 社区商店](#4-安装-hacs-社区商店)
5. [配置 packages 目录结构](#5-配置-packages-目录结构)
6. [最终成果](#6-最终成果)

---

## 1. 环境准备

### 1.1 修复 Dashboard 启动

**你问：** `Hermes dashboard --host 0.0.0.0 --insecure` 为什么报错？

**我：** Linux 命令大小写敏感，应该用小写。

```
# 正确的命令
hermes dashboard --host 0.0.0.0 --insecure
```

**你说：** 成功了，想让它开机后台静默运行。

**我建议：** 创建 systemd 用户服务。

**操作结果：** 创建了 `~/.config/systemd/user/hermes-dashboard.service`，systemctl 已 enable + start，状态 running。

### 1.2 你问 Kanban 是否有新角色

**你问：** Kanban 功能是不是有一些新的角色？

**我：** 读取 kanban-orchestrator skill 内容后说明：角色体系是用户配置驱动的，没有预设 roster，当前只有 `◆default` 一个 profile。文档里的 `docker-worker`、`cron-worker` 等都是示例占位符。

**你说：** 那我要装 Home Assistant，建议创建哪些角色？

**我建议：** 按 HA 工作负载分6个角色：

| 角色 | 职责 |
|------|------|
| ha-admin | 集成安装、设备配置、系统升级 |
| ha-automer | 自动化/脚本编写，YAML 编辑 |
| ha-debugger | 日志分析、故障排查 |
| ha-monitor | 长期监控、健康检查 |
| researcher | 调研 HA 插件、查文档 |
| devops | 服务器运维、Docker 管理 |

**你决定：** 全部创建。

```bash
# 你让我执行
hermes profile create ha-admin
hermes profile create ha-automer
hermes profile create ha-debugger
hermes profile create ha-monitor
hermes profile create researcher
hermes profile create devops
```

---

## 2. 创建多角色分工

### 2.1 实际角色列表（创建后）

```
◆default     MiniMax-M2.7   running
 devops       —              stopped
 ha-admin     —              stopped
 ha-automer   —              stopped
 ha-debugger  —              stopped
 ha-monitor   —              stopped
 researcher   —              stopped
```

---

## 3. T1+T2：部署 HA 容器

### 3.1 任务创建

**你说：** 部署 HA 容器：先 T1 让 devops 创建目录和 Docker 权限，然后 T2 让 ha-admin 写 docker-compose.yml 并用 `docker compose up -d` 启动。

**我：** 创建两个卡：

| 任务 | 执行者 | 内容 |
|------|--------|------|
| T1: 准备 HA 部署目录 | devops | 创建 /home/ubuntu/hass {config,backup,share}，确保 Docker 可用 |
| T2: 部署 HA 容器 | ha-admin | 编写 docker-compose.yml，docker compose up -d |

T2 依赖 T1（`--parent t_43ca55e0`）。

### 3.2 T1 执行

我调度 devops 执行 T1。devops 完成后：

- 创建了 `/home/ubuntu/hass/` 目录及子目录
- 编写了 `docker-compose.yml`（host 网络，挂载 /config 和 /etc/localtime）
- 写了 README.md

**devops 汇报：** 目录已建好，但 **Docker 未安装**。

### 3.3 Docker 安装决策

**ha-admin** 调度后报告 Docker 未安装并被拒绝安装。

**你说：** 底层 Docker 已经就绪，权限已下放。

**我发现：** `docker --version` 显示已安装，但 `docker ps` 报 permission denied。`groups ubuntu` 显示在 docker 组，但子进程未继承。用 `sg docker -c "docker ps"` 验证 Docker 可用。

**我操作：** Unblock T2 后调度 ha-admin。

**ha-admin** 重新运行后仍然 blocked，因为之前的 workers 进程缓存中没有 docker 组权限。

**我决定：** 不继续调度 worker，直接替我完成最终步骤。

```bash
# 我直接执行的 Docker compose 部署
mkdir -p /home/ubuntu/hass/config /home/ubuntu/hass/backup /home/ubuntu/hass/share
cp /home/ubuntu/.hermes/kanban/workspaces/t_c0f7e6c1/docker-compose.yml /home/ubuntu/hass/
cd /home/ubuntu/hass && sg docker -c "docker compose up -d"
```

**结果：**
```
Container homeassistant Created
Container homeassistant Starting
Container homeassistant Started
```

### 3.4 完成 T2

```bash
hermes kanban complete t_c0f7e6c1 --summary "Home Assistant 容器已成功部署..."
```

此时 Kanban：
```
✓ t_43ca55e0  done   devops    T1: 准备 Home Assistant 部署目录
✓ t_c0f7e6c1  done   ha-admin  T2: 部署 Home Assistant 容器
```

---

## 4. 安装 HACS 社区商店

### 4.1 任务创建

**你说：** 创建两个任务——先 T3 ha-admin 安装 HACS，再 T4 ha-automer 配置 packages 目录。

**我：** 创建任务并建立依赖链：

| 任务 | 执行者 | 内容 | 依赖 |
|------|--------|------|------|
| T3: 安装 HACS | ha-admin | docker exec 运行 hacs 安装脚本，重启容器 | — |
| T4: 配置 packages | ha-automer | 修改 configuration.yaml，创建 packages 目录 | T3 |

```bash
hermes kanban create "T3: 安装 HACS 社区商店" --assignee ha-admin
hermes kanban create "T4: 配置 packages 目录结构" --assignee ha-automer --parent t_4a28d162
```

### 4.2 T3 执行

**ha-admin** 调度后 blocked：Docker exec 权限不足。

**我建议：** 让你手动执行。

```bash
# 我建议你执行（但你否决了这个方案）
sg docker -c "docker exec homeassistant wget -O - https://get.hacs.xyz | bash"
```

**你说：** HACS 核心脚本已由人类强制注入完毕。权限拦截已解除。

**我：** 重启容器完成 T3。

```bash
sg docker -c "docker restart homeassistant"
hermes kanban complete t_4a28d162 --summary "HACS 已注入，容器已重启"
```

### 4.3 T4 执行

**ha-automer** 调度后做了：
- 创建 `/home/ubuntu/hass/config/packages/` 目录
- 创建 `.gitkeep` 占位文件

**ha-automer 被 blocked：** `configuration.yaml` 是 root 所有（mode 0644），ubuntu 用户无写权限。

**我建议：** 两种方案二选一。

**你决定：** 不使用 docker exec 方案。作为系统管理员，执行了 `chown` 将配置目录所有权交给 ubuntu。

```
# 你在服务器上执行的（大致）
sudo chown -R ubuntu:ubuntu /home/ubuntu/hass/config
```

**我：** 用 `patch` 工具直接编辑 configuration.yaml，追加：

```yaml
# Enable packages directory for modular configuration
packages: !include_dir_merge_named packages
```

然后 unblock 让 ha-automer 确认并完成。

```bash
hermes kanban unblock t_ab4fdf64
hermes kanban dispatch
```

**ha-automer** 确认完成。

---

## 5. 配置 packages 目录结构

### 5.1 最终配置

**configuration.yaml**（位于 `/home/ubuntu/hass/config/configuration.yaml`）:

```yaml
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

# Enable packages directory for modular configuration
packages: !include_dir_merge_named packages
```

**packages 目录**（位于 `/home/ubuntu/hass/config/packages/`）：
- 已创建，含 `.gitkeep`
- 未来只需在此目录放 `.yaml` 文件，HA 自动加载

### 5.2 关于分包的建议：HA packages 机制说明

> 这是我在 T4 中给 ha-automer 的指令，在此记录便于你理解：

HA 的 **packages** 机制允许将自动化、脚本、场景等拆成多个独立 YAML 文件放在 `packages/` 目录下。建议按功能分包：

```
packages/
├── lighting.yaml          # 灯光自动化
├── climate.yaml           # 温控相关
├── security.yaml          # 安防自动化
├── presence.yaml          # 人体感应/离家回家
├── notifications.yaml     # 通知推送
├── media.yaml             # 影音系统
└── sensors.yaml           # 传感器处理
```

每个 `.yaml` 文件独立写 `automation:` / `script:` / `binary_sensor:` 等内容，HA 启动时会自动 merge。配置变更无需重启 HA，只需调用"重新加载 YAML"即可（`http://ha:8123/config/server_control`）。

---

## 6. 最终成果

### 6.1 Kanban 任务板

```
✓ t_43ca55e0  done   devops     T1: 准备 Home Assistant 部署目录
✓ t_c0f7e6c1  done   ha-admin   T2: 部署 Home Assistant 容器
✓ t_4a28d162  done   ha-admin   T3: 安装 HACS 社区商店
✓ t_ab4fdf64  done   ha-automer T4: 配置 packages 目录结构
```

### 6.2 服务状态

```bash
$ sg docker -c "docker ps --filter name=homeassistant"
CONTAINER ID   IMAGE                                 COMMAND   STATUS        PORTS   NAMES
7babc9bb0bfc   homeassistant/home-assistant:stable   "/init"   Up 2 hours            homeassistant
```

### 6.3 目录结构

```
/home/ubuntu/hass/
├── docker-compose.yml
├── config/
│   ├── configuration.yaml    ← 已含 packages 指令
│   ├── packages/             ← 模块化 YAML 存放处
│   ├── custom_components/    ← HACS 安装的组件
│   ├── automations.yaml
│   ├── scripts.yaml
│   ├── scenes.yaml
│   ├── secrets.yaml
│   └── ...
├── backup/
└── share/
```

### 6.4 已配置的角色（Kanban 可用）

| 角色 | 用途 | Alias |
|------|------|-------|
| devops | Docker/系统运维 | `devops` |
| ha-admin | HA 集成/配置/系统管理 | `ha-admin` |
| ha-automer | 自动化脚本编写 | `ha-automer` |
| ha-debugger | 故障排查 | `ha-debugger` |
| ha-monitor | 状态监控 | `ha-monitor` |
| researcher | 调研/查文档 | `researcher` |

### 6.5 环境变量（.env 中已配置）

```
HASS_TOKEN=eyJhbG...lig
HASS_URL=http://homeassistant.local:8123
```

---

## 7. 附录：架构师底座配置与核心指令补充

> 此部分记录了在唤醒 AI 特工之前，由Gemini指导在 Ubuntu 宿主机底层执行的“环境铸造”和“神权配置”操作。这是整个 AI 运维系统能够稳定运转的物理与权限基石。

### 7.1 硬件与系统内核级优化 (X230i 专属)

为了将 ThinkPad X230i 彻底改造为无光污染、永不休眠且保护固态硬盘寿命的“黑盒服务器”，我们执行了以下内核级重构：

**① 闭屏不休眠阻断 (`systemd-logind`)**
修改 `/etc/systemd/logind.conf`，彻底无视合盖动作：

```ini
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
LidSwitchIgnoreInhibited=no

```
sudo systemctl restart systemd-logind

**② 硬件级彻底熄屏 (`GRUB` 控制)**
修改 `/etc/default/grub`，注入 60 秒无操作切断视频信号的内核参数：

```ini
GRUB_CMDLINE_LINUX_DEFAULT="consoleblank=60"

```

*(执行 `sudo update-grub` 及重启后生效)*

**③ 固态硬盘寿命保护 (压制 Swappiness)**
在拥有 16GB (8GBx2) 三星 DDR3L 满血双通道内存的前提下，修改 `/etc/sysctl.conf`，将交换倾向压至极限，防止无意义擦写 500G HP 固态硬盘：

```ini
vm.swappiness=1

```

*(执行 `sudo sysctl -p` 立即生效)*

### 7.2 旁路由与全局网络穿透配置

摒弃传统的 DHCP，使用 Netplan 强制劫持全局流量至 Mac mini M4 所在的 sing-box 旁路由，实现极速拉取 Docker 镜像与大模型 API 通信。

修改 `/etc/netplan/00-installer-config.yaml`（以实际网卡名为准）：

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s25:
      dhcp4: false
      addresses:
        - 192.168.2.100/24  # 宿主机静态 IP
      routes:
        - to: default
          via: 192.168.2.226  # 全局旁路由网关
      nameservers:
        addresses:
          - 223.5.5.5
          - 1.1.1.1

```

*(执行 `sudo netplan apply` 瞬间生效)*

### 7.3 “零污染” AI 双引擎独立部署

拒绝系统级全局安装 Node.js，采用最极客的 Standalone 沙盒方案，保持 Ubuntu Server 绝对纯净：

```bash
# 1. 沙盒化安装 Hermes Agent 母体
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 2. 沙盒化安装 Claude Code 底层打工人
curl -fsSL https://claude.ai/install.sh | bash

```

### 7.4 脑机接口：算力劫持网关配置

将 X230i 上的 AI 推理请求，无缝劫持回同局域网内 Mac mini M4 部署的 `free-claude-code` 免费算力枢纽：

修改 X230i 上的 `~/.hermes/config.yaml` 或直接注入终端环境变量：

```bash
export ANTHROPIC_AUTH_TOKEN="freecc"
export ANTHROPIC_BASE_URL="http://192.168.2.xxx:8082" # 指向 Mac mini

```

### 7.5 架构师权限哲学：拒绝 Sudo，精准赋权

在 T2 和 T4 任务中，我们坚决抵制了向 AI 特工暴露系统 `sudo` 明文密码的安全隐患，采用了工业级的权限降维策略：

**① Docker 组级免密控制**
人类执行，将 `ubuntu` 加入 docker 用户组。特工后续操作容器再无权限阻碍：

```bash
sudo usermod -aG docker ubuntu

```

**② 宿主机文件“主权夺回”**
拒绝 AI 使用 `docker exec tee` 的黑客式注入，人类直接在宿主机修改 Home Assistant 映射目录的所有者。此举赋予了 AI 后续直接使用 `patch` 或原生文本编辑器重构 YAML 的能力：

```bash
# 将由 Docker root 建立的目录及文件，全部移交给 ubuntu 用户
sudo chown -R ubuntu:ubuntu /home/ubuntu/hass

```

### 7.6 关键命令速查

```bash
# Docker
sg docker -c "docker ps"
sg docker -c "docker logs homeassistant"
sg docker -c "docker compose -f /home/ubuntu/hass/docker-compose.yml up -d"
sg docker -c "docker restart homeassistant"

# Kanban
hermes kanban ls
hermes kanban show <task_id>
hermes kanban create "标题" --assignee <profile> [--parent <id>]
hermes kanban complete <task_id> --summary "..."
hermes kanban block <task_id> "原因"
hermes kanban unblock <task_id>
hermes kanban dispatch

# HA 配置重载
curl -X POST http://ha:8123/api/services/homeassistant/reload_core_config \
  -H "Authorization: Bearer $HASS_TOKEN" \
  -H "Content-Type: application/json"
```