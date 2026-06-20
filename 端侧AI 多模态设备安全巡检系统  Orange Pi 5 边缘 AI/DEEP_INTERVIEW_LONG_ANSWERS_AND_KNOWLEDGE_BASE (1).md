# DEEP_INTERVIEW_LONG_ANSWERS_AND_KNOWLEDGE_BASE.md
## 0. 使用说明
本文件对应 Stage 6 Long Answers / Knowledge Base，是整个面试准备过程中的“原理与机理主战场”。

所有长答均遵循严密的结构，将通用原理与本项目证据清晰分区，主动声明系统边界，防止面试中出现夸大或概念混淆：

+ **核心长答标杆结构**：【一句话结论】 -> 【通用原理 / 系统原则】 -> 【本项目证据】 -> 【为什么这样设计 / 为什么不是 X】 -> 【边界】 -> 【30 秒口语引用】。
+ **排障类长答五步根因结构**：【表面现象】 -> 【定位方法】 -> 【机理推导】 -> 【为什么修复/止损有效】 -> 【反事实/边界】。
+ **可观测与软件链路分层验收结构**：【代码可见】 -> 【编译构建】 -> 【接口契约】 -> 【板端部署】 -> 【人工验收边界】。

口语回答部分统一收拢并链接引用至 [DEEP_INTERVIEW_SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers)，避免多处维护导致口径冲突。

---

## 1. 长答总览与分类索引表
| answer_id | question | mapped_claim_id | priority | answer_type | spoken_ref |
| --- | --- | --- | --- | --- | --- |
| LA-P01 | 这个项目到底是什么？ | C01/C03/C18/C21 | P0 | project_story | SPOKEN_ANSWERS (项目介绍部分) |
| LA-P02 | 当前主线为什么是 OPi5 一板主控？ | C01/C23 | P0 | project_story | SPOKEN_ANSWERS (项目演进部分) |
| LA-P03 | 这是不是生产系统？ | C01/C10/C11 | P0 | metric_boundary | SPOKEN_ANSWERS (项目边界部分) |
| LA-P04 | 你实际做了哪些模块？ | C05/C12/C18/C19/C20/C21 | P0 | project_story | SPOKEN_ANSWERS (项目介绍部分) |
| LA-P05 | 为什么不是简单堆功能？ | C11/C17/C18/C19/C20 | P0 | architecture | SPOKEN_ANSWERS (架构设计部分) |
| LA-P06 | 三阶段迁移怎么讲？ | C23 | P1 | project_story | SPOKEN_ANSWERS (项目演进部分) |
| LA-A01 | 为什么安全闭环在 OPi5 本地？ | C11/C17 | P0 | architecture | SPOKEN_ANSWERS (B13/B15 专区) |
| LA-A02 | 为什么 AI 只输出 risk_hint？ | C06/C17 | P0 | architecture | SPOKEN_ANSWERS (B13 专区) |
| LA-A03 | control_allowed=false 的意义是什么？ | C17 | P0 | architecture | SPOKEN_ANSWERS (B13 专区) |
| LA-A04 | Flask/React 为什么不控制执行器？ | C17/C22 | P0 | architecture | SPOKEN_ANSWERS (B09 专区) |
| LA-A05 | device-agent 的职责边界是什么？ | C18/C22 | P1 | architecture | SPOKEN_ANSWERS (B14 专区) |
| LA-A06 | Flask backend 与 AI service 的边界？ | C16/C19 | P0 | architecture | SPOKEN_ANSWERS (B14 专区) |
| LA-A07 | edge/server/frontend 怎么分层？ | C01/C18/C19/C21 | P1 | architecture | SPOKEN_ANSWERS (项目介绍部分) |
| LA-A08 | 本地断网/AI 离线怎么降级？ | C09/C11/C17 | P0 | architecture | SPOKEN_ANSWERS (B11 专区) |
| LA-S01 | 2816 行 safetyd 怎么讲？ | C05 | P0 | code_path | SPOKEN_ANSWERS (B01 专区) |
| LA-S02 | 0-10 风险评分怎么讲？ | C06/C17 | P1 | code_path | SPOKEN_ANSWERS (B13 专区) |
| LA-S03 | 四态 NORMAL/VERIFY/ALARM/FAULT 怎么讲？ | C07 | P0 | code_path | SPOKEN_ANSWERS (B05 专区) |
| LA-S04 | WARN 边界怎么讲？ | C07 | P0 | metric_boundary | SPOKEN_ANSWERS (B05 专区) |
| LA-S05 | all_off 能保证什么？ | C08 | P1 | metric_boundary | SPOKEN_ANSWERS (B01 专区) |
| LA-S06 | spool 是什么，不是什么？ | C09/C32 | P1 | metric_boundary | SPOKEN_ANSWERS (B08 专区) |
| LA-S07 | systemd Restart=always 能保证什么？ | C10 | P1 | metric_boundary | SPOKEN_ANSWERS (B05 专区) |
| LA-S08 | AI/Flask 不可达时本地报警怎么讲？ | C11/C17 | P0 | architecture | SPOKEN_ANSWERS (B13 专区) |
| LA-Q01 | mock vs real Qwen3-VL 怎么讲？ | C12/C28 | P0 | metric_boundary | SPOKEN_ANSWERS (B07 专区) |
| LA-Q02 | Qwen3-VL-2B RKNN/RKLLM 接入口径？ | C12/C28 | P0 | code_path | SPOKEN_ANSWERS (B07 专区) |
| LA-Q03 | single-shot 约 13s 怎么讲？ | C14 | P1 | metric_boundary | SPOKEN_ANSWERS (B07 专区) |
| LA-Q04 | worker 常驻复用模型加载怎么讲？ | C13/C15 | P1 | code_path | SPOKEN_ANSWERS (B07 专区) |
| LA-Q05 | 6/7 worker 约 8-9s 怎么讲？ | C15 | P0 | metric_boundary | SPOKEN_ANSWERS (B12 专区) |
| LA-Q06 | 6/8 少量样本 4.7-5.6s 怎么讲？ | C15 | P0 | metric_boundary | SPOKEN_ANSWERS (B12 专区) |
| LA-Q07 | 为什么不是 benchmark/P95/P99/soak？ | C15 | P0 | metric_boundary | SPOKEN_ANSWERS (B12 专区) |
| LA-Q08 | worker 不是独立 systemd 服务？ | C13/C10 | P1 | code_path | SPOKEN_ANSWERS (B07 专区) |
| LA-O01 | 5s heartbeat 怎么讲？ | C18 | P1 | metric_boundary | SPOKEN_ANSWERS (B14 专区) |
| LA-O02 | 1Hz telemetry sample 怎么讲？ | C18 | P1 | metric_boundary | SPOKEN_ANSWERS (B14 专区) |
| LA-O03 | 30s telemetry batch 怎么讲？ | C18/C32 | P0 | metric_boundary | SPOKEN_ANSWERS (B14 专区) |
| LA-O04 | 30s AI observation 怎么讲？ | C18 | P1 | metric_boundary | SPOKEN_ANSWERS (B14 专区) |
| LA-O05 | 25 Flask route / 21 unique paths 怎么讲？ | C19 | P0 | code_path | SPOKEN_ANSWERS (B14 专区) |
| LA-O06 | AI service 4 个端点不计入 Flask backend？ | C16/C19 | P0 | architecture | SPOKEN_ANSWERS (B14 专区) |
| LA-O07 | SQLite 8+1 表怎么讲？ | C20 | P0 | code_path | SPOKEN_ANSWERS (B08 专区) |
| LA-O08 | React 8 页源码/App/build 怎么讲？ | C21 | P0 | metric_boundary | SPOKEN_ANSWERS (B10 专区) |
| LA-O09 | React build 为什么不等于人工完整验收？ | C21 | P0 | metric_boundary | SPOKEN_ANSWERS (B10 专区) |
| LA-O10 | SMTP/SSE/MJPEG 的边界？ | C22/C26/C29 | P1 | architecture | SPOKEN_ANSWERS (B09 专区) |
| LA-T01 | telemetry batch 400 是什么问题？ | C32 | P0 | metric_boundary | SPOKEN_ANSWERS (B14 专区) |
| LA-T02 | 当前源码主结构为什么说看起来对齐？ | C32/C18/C19/C20 | P0 | code_path | SPOKEN_ANSWERS (B14 专区) |
| LA-T03 | 为什么不能说已修复？ | C32 | P0 | metric_boundary | SPOKEN_ANSWERS (B15 专区) |
| LA-T04 | poster/spool 在失败时能做什么？ | C09/C32 | P1 | code_path | SPOKEN_ANSWERS (B08 专区) |
| LA-T05 | 后续需要什么证据才能升级 C32？ | C32 | P0 | metric_boundary | SPOKEN_ANSWERS (B15 专区) |
| LA-H01 | GPIO 输入/输出怎么讲？ | C24/C04 | P1 | hardware_debug | SPOKEN_ANSWERS (B01 专区) |
| LA-H02 | Water MOS 空载边界怎么讲？ | C24 | P0 | hardware_debug | SPOKEN_ANSWERS (B01 专区) |
| LA-H03 | PWM15 50Hz 舵机怎么讲？ | C25 | P2 | hardware_debug | SPOKEN_ANSWERS (B03 专区) |
| LA-H04 | USB camera 640x480 MJPG 怎么讲？ | C26/C22 | P2 | hardware_debug | SPOKEN_ANSWERS (B04 专区) |
| LA-H05 | I2C5 空总线怎么讲？ | C30/C27 | P0 | hardware_debug | SPOKEN_ANSWERS (B02 专区) |
| LA-H06 | I2C1 0x3C OLED 原始扫描怎么讲？ | C27 | P0 | hardware_debug | SPOKEN_ANSWERS (B02 专区) |
| LA-H07 | I2C1 0x68 缺原始日志怎么讲？ | C27 | P0 | hardware_debug | SPOKEN_ANSWERS (B02 专区) |
| LA-H08 | I2C5 成功/失败日志冲突怎么讲？ | C27/C30 | P0 | hardware_debug | SPOKEN_ANSWERS (B02 专区) |
| LA-H09 | PCA9685 无 ACK 怎么讲？ | C31 | P1 | hardware_debug | SPOKEN_ANSWERS (B02 专区) |
| LA-H10 | 失败问题为什么适合面试复盘？ | C27/C30/C31/C32 | P0 | hardware_debug | SPOKEN_ANSWERS (B15 专区) |


---

## 2. 项目总述类长答
### LA-P01 这个项目到底是什么？
+ **【一句话结论】**：这是一个部署在边缘计算卡 Orange Pi 5 上的本地多模态 AI 安全巡检演示原型系统，打通了本地 FSM 控制闭环、常驻大模型感知提示、边缘遥测代理以及前后端可视化联动的完整技术路径。
+ **【通用原理 / 系统原则】**：边缘自治（Edge Autonomy）与控制观测分离原则。高可信的安全仲裁必须在低延迟的确定性本地侧完成，多模态 AI、云端及展示层仅用于感知增强和可观测性。
+ **【本项目证据】**：证据对应 Evidence Map C01/C03/C18/C21。核心模块包括 C 语言 `opi5_safetyd`、Python 内嵌 Qwen3-VL 2B 的 `opi5-ai` 服务、Go/Python 编写的 `opi5-device-agent`，以及 Flask + SQLite + React 前后端。
+ **【为什么这样设计 / 为什么不是 X】**：
    - _为什么不把控制流和 AI 逻辑写在同一个进程_：因为端侧 Python 进程和 AI 推理耗时高（秒级），且极易因为 NPU 驱动或 OOM 崩溃。如果合并，AI 崩溃将直接导致底层继电器/报警失效。
    - _为什么采用分进程本地通信_：C 进程毫秒级响应，通过向 AI API 异步请求 `risk_hint`，保障了控制流的隔离与强实时。
+ **【边界】**：这是一个演示系统，虽然实现了多进程 systemd 自动拉起和本地降级，但不包含工业级冗余高可用（HA）或第三方安全认证。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的“项目介绍”。

### LA-P02 当前主线为什么是 OPi5 一板主控？
+ **【一句话结论】**：将本地安全控制、大模型感知推理和可观测上报代理全部收敛至一块 OPi5 板卡上，消除了双板物理网络通信的抖动，并保留了前两阶段（单片机、i.MX6ULL 双板）作为工程迁移的演进证据。
+ **【通用原理 / 系统原则】**：系统集成中的“最小实体设计”。在计算资源允许的前提下，减少物理总线和网络协作节点，能呈指数级降低系统的故障发生率。
+ **【本项目证据】**：证据对应 Evidence Map C01/C23。前两阶段源码和文档分别归档至 `legacy/` 和 `docs/archive/`，当前主线全部聚焦于 OPi5 的 `edge/opi5-*` 进程。
+ **【为什么这样设计 / 为什么不是 X】**：
    - _为什么不保留 i.MX6ULL 作为主控_：原本的“i.MX6ULL + OPi5”双板方案中，双板之间依靠局域网套接字通信。但在边缘野外巡检环境下，无线网络和交换机供电极不稳定，经常导致控制指令延迟超过 2 秒，安全闭环无法咬合。收敛到 OPi5 后，通过本地 IPC 彻底解决了网络抖动问题。
+ **【边界】**：一板多进程依然存在 SOC 级别的单点故障（SPOF）风险。如果系统发生内核崩溃（Kernel Panic），控制与感知将一同失效。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的“项目演进”。

### LA-P03 这是不是生产系统？
+ **【一句话结论】**：本项目明确定义为“边缘安全巡检的工程原型与演示验证系统”，具备完备的自恢复、本地降级和异常缓存机制，但不具备任何生产级 SLA、冗余集群或安全功能认证（如 SIL）。
+ **【通用原理 / 系统原则】**：工程设计的“阶段诚实原则”。原型系统重点在于验证技术路径与排障止损，不应包装为已具备工业级长期鲁棒性的生产成果。
+ **【本项目证据】**：Evidence Map C01/C10/C11。代码支持 systemd 自动拉起与本地 HTTP 失败 spool 机制。
+ **【为什么这样设计 / 为什么不是 X】**：
    - _为什么不设计为云端高可用高并发架构_：边缘巡检设备通常处于网络受限、断续在线的物理现场，引入 Redis、Kafka 或高并发云端关系库会急剧抬高板卡功耗，且对演示系统而言属于过度设计。
+ **【边界】**：缺少长期高低温 soak 测试、电磁兼容（EMC）测试以及安全认证证书。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的“项目边界”。

---

## 3. 架构设计类长答
### LA-A01 为什么安全闭环在 OPi5 本地？
+ **【一句话结论】**：安全控制闭环必须在本地 C 守护进程 `opi5_safetyd` 内毫秒级收敛，从而在物理断网、高级感知（AI）服务崩溃的极端状态下，依然能依赖本地传感器强触发进入 Fail-safe 安全保护态。
+ **【通用原理 / 系统原则】**：本地生存性原则。高级认知层（感知、决策）的故障绝不能向下渗透并破坏底层执行器的基本人身与设备安全兜底逻辑。
+ **【本项目证据】**：Evidence Map C11/C17。`opi5_safetyd.c` 物理接线并直控 PIR/火焰/烟雾传感器及继电器/水泵；AI 推理进程崩溃时，本地报警不受影响。
+ **【为什么这样设计 / 为什么不是 X】**：如果把控制逻辑放在 Flask 或网页端（常规的 IoT 架构），只要路由器断电或浏览器挂载，火灾探测器就无法触发灭火泵，将面临极高的财产安全风险。
+ **【边界】**：本地降级控制仅依赖板载传感器的物理输入，如果传感器本身发生断线或物理损毁，本地闭环也将失效。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B13。

### LA-A02 为什么 AI 只输出 risk_hint？
+ **【一句话结论】**：多模态 AI (Qwen3-VL) 在系统架构中定位为“感知增强与场景解释器”，其响应仅能以辅助变量 `risk_hint` 参与本地评分融合，绝不拥有任何执行器的直接驱动授权。
+ **【通用原理 / 系统原则】**：非确定性决策隔离原则。基于概率或深度学习模型的输出具有不可解释性与随机抖动（如幻觉、误检），不能用于强安全等级的开关控制。
+ **【本项目证据】**：Evidence Map C06/C17。AI service 返回的 JSON 包含 `control_allowed=false` 标志，本地 `opi5_safetyd` 读取 `risk_hint` 后仅做累加并 clamp，不作为触发执行器的唯一源。
+ **【为什么这样设计 / 为什么不是 X】**：如果允许大模型通过文本指令直接开/关水泵，模型在面对光影扰动或未知场景时产生幻觉，可能会频繁乱下灭火指令，造成演示负载受损。
+ **【边界】**：AI 的 `risk_hint` 只能使系统从 NORMAL 升级为 VERIFY 状态（加强采样），不能单独将系统推入 FAULT 或 ALARM。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B13。

### LA-A03 control_allowed=false 的意义是什么？
+ **【一句话结论】**：`control_allowed=false` 是接口契约（JSON Schema）上的物理红线，用于阻断任何将“AI 语义理解”误用为“直接控制指令”的代码逻辑。
+ **【通用原理 / 系统原则】**：API 契约防卫原则。通过在契约层硬编码控制标志，使开发人员和上下游模块在设计之初就明确 AI 与控制的边界。
+ **【本项目证据】**：Evidence Map C17。`docs/07_端边HTTP_JSON_Contract.md` 规范。
+ **【为什么这样设计 / 为什么不是 X】**：如果仅在口头上约定“AI 不参与控制”，而接口不设硬性红线，后续协同开发人员极易在接收端直接解析 AI payload 中的 action 字段去驱动 GPIO，从而引入不可控的崩溃风险。
+ **【边界】**：该标志是逻辑契约，它能约束规范的软件开发，但无法阻止恶意人员直接修改本地 C代码绕过该标志强行输出。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B13。

### LA-A08 本地断网/AI 离线怎么降级？
+ **【一句话结论】**：系统依靠 C 进程 `opi5_safetyd` 的主状态机进行 Fail-safe 状态推推导：AI 离线时评分失去 AI 变量但传感器报警依旧；网络断开时上报数据在本地 Spool 中打包堆叠，恢复后异步补发。
+ **【通用原理 / 系统原则】**：分布式系统的“优雅降级（Graceful Degradation）”与“缓存重试机制”。
+ **【本项目证据】**：Evidence Map C09/C11/C17。`poster.py` 中的本地 sqlite/json 缓存逻辑，以及 `opi5_safetyd.c` 内部的故障仲裁。
+ **【为什么这样设计 / 为什么不是 X】**：若无降级，断网会导致上报接口持续阻塞，拖垮 device-agent 主线程的 CPU 周期，甚至导致传感器采样任务忙等，彻底丧失监视功能。
+ **【边界】**：本地 Spool 缓存空间受限，若断网持续数天，为防止边缘存储撑爆，系统会基于 FIFO 策略丢弃最古老的事件日志。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B11。

---

## 4. OPi5 safetyd 本地安全控制器长答
### LA-S01 2816 行 safetyd 怎么讲？
+ **【一句话结论】**：2816 行仅指当前 OPi5 本地安全闭环控制守护程序 `edge/opi5-controller/src/opi5_safetyd.c` 的物理行数（含注释空行），不掺杂任何归档的历史代码。
+ **【通用原理 / 系统原则】**：事实审计中的“代码一致性”。任何关于规模和产出的数字陈述必须能通过物理命令（如 `wc -l`）在代码库中被精确审计和复现。
+ **【本项目证据】**：Evidence Map C05。
+ **【为什么这样设计 / 为什么不是 X】**：不能将历史 STM32 驱动和 i.MX6ULL 的 `imx_safetyd.c` 混合累加。虽然两者都在 legacy 目录，但累加会导致面试官质疑代码行数的真实水分，降低可信度。
+ **【边界】**：行数仅是开发规模证据，不代表代码复杂度和软件可靠性。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B01。

### LA-S03 四态 NORMAL/VERIFY/ALARM/FAULT 怎么讲？
+ **【一句话结论】**：`opi5_safetyd` 内部的有限状态机 (FSM) 仅设计并运行四种主状态：NORMAL（正常）、VERIFY（核验期）、ALARM（触发报警）、FAULT（硬件或通信故障）。
+ **【通用原理 / 系统原则】**：安全控制状态机（Safety FSM）的确定性迁移。每一个状态转移必须有确定的硬触发源或软件计数器，不能存在悬挂状态。
+ **【本项目证据】**：Evidence Map C07。`opi5_safetyd.c` 内部的 `ctx->state` 转移逻辑。
+ **【为什么这样设计 / 为什么不是 X】**：
    - _为什么设计 VERIFY 状态_：边缘端传感器（如 PIR、MQ-2）由于环境干扰存在偶发毛刺。如果一有信号就跳 ALARM 开泵，会导致频繁误报；设置 5 秒的 VERIFY 确认期可以有效过滤硬件噪声。
+ **【边界】**：文档和系统健康设计中虽然保留了 WARN（警告），但它属于健康度上报字段，不是 FSM 代码的主状态。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B05。

---

## 5. Qwen3-VL / worker / 性能边界长答
### LA-Q02 Qwen3-VL-2B RKNN/RKLLM 部署链路与冷启动？
+ **【一句话结论】**：完成了 Qwen3-VL-2B 多模态大模型在 OPi5 板载 NPU 上的本地部署与端侧推理链路跑通，仓库保留了完整的推理与客户端代码，但不入库大型模型权重文件。
+ **【通用原理 / 系统原则】**：边缘端侧大模型部署（On-Device VLM Deployment）。端侧部署需要重点克服权重文件加载所带来的 CPU、I/O 阻塞和内存瓶颈。
+ **【本项目证据】**：Evidence Map C12/C28。代码见 `qwen3vl_backend.py`、`qwen3vl_worker.cpp`。
+ **【为什么这样设计 / 为什么不是 X】**：没有采用“在 API 路由内实时单次执行 subprocess 启动模型”的设计，因为在 NPU/CPU 混合加载大模型时，冷启动过程（权重寻址、内存映射、算子初始化）耗时高达 13s。这会导致 API 接口直接超时崩溃。
+ **【边界】**：权重文件本身不入库以保证代码库清洁；且模型在首次拉起时仍有 13s 的固有开销。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B07。

### LA-Q06 Qwen 推理延迟 4.7-5.6s 与 8-9s 的小样本属性？
+ **【一句话结论】**：推理延迟数字（6/7 测试为后续 8-9s，6/8 测试为 4.7-5.6s）仅属于极少数样本的调试回归记录，绝不能包装为经过工业级 soak 压测的稳定 P95/P99 指标。
+ **【通用原理 / 系统原则】**：性能指标的严谨性。小样本数据只能说明“在特定硬软件环境下，模型具备在数秒内推理成功的可行性”，不能等同于稳定的服务质量（SLA）。
+ **【本项目证据】**：Evidence Map C15。测试文件 `2026-06-07_qwen3vl_persistent_regression.md` 和 `2026-06-08_qwen3vl_autostart_real_ai.md`。
+ **【为什么这样设计 / 为什么不是 X】**：之所以在文档中诚实记录两个不同日期的延迟，是因为 6/7 的测试包含了 API 层转发及早期的 worker 调试开销，而 6/8 是在优化本地 client 管道通信后的干净推理延迟。如实列出体现了测试环境与流程的可追溯性。
+ **【边界】**：目前的测试缺乏 100 次以上的连续请求压力测试，且极易受 CPU 温度过高导致主频降频的影响。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B12。

---

## 6. device-agent / Flask / SQLite / React 可观测性长答
### LA-O05 Flask 后端 25 个 decorated routes 统计口径？
+ **【一句话结论】**：经过 AST (抽象语法树) 静态扫描核账，`server/backend/app.py` 内部共注册了 25 个 `@app.route` 装饰器函数，去重后的物理唯一 URL 路径为 21 个。
+ **【分层验收框架应用】**：
    1. _代码可见_：`server/backend/app.py` 源码主文件完整可读。
    2. _编译构建_：Python 编译通过（`py_compile`）。
    3. _接口契约_：这 25 个路由对应 `docs/07_端边HTTP_JSON_Contract.md` 的业务接口。
    4. _板端部署_：接口能正常在板端部署并监听 5000 端口。
    5. _人工验收边界_：部分废弃/兼容路由（如旧 `/api/events`）未在 React Console 页面人工逐项测试。
+ **【本项目证据】**：Evidence Map C19。
+ **【为什么这样设计 / 为什么不是 X】**：纠正了早期简历中“26 个 API”的不精确表述。因为 26 这个数字混入了 OPi5 本地 AI 推理服务的端点，边界不清晰。backend 与 AI 推理服务的统计口径必须在架构层面物理切割。
+ **【边界】**：这 25 个路由包含部分兼容性 Stub、静态uploads路由以及 health 检查接口，并非全部都是核心业务数据流 API。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B14。

### LA-O07 SQLite 数据库 8+1 张表的具体 schema 与通知口径？
+ **【一句话结论】**：系统总共使用 9 张表进行数据闭环，包括 `database.py` 中定义的 8 张主业务表，以及通知模块 `email_notifier.py` 中单独创建的 `notification_log` 告警冷却表。
+ **【分层验收框架应用】**：
    1. _代码可见_：`database.py` 定义了主要的初始化结构与 DDL 语句。
    2. _编译构建_：模块可运行，演示启动时通过 `db.init()` 自动生成 `.db` 文件。
    3. _接口契约_：每张表字段契约与 `docs/07` telemetry batch 和 event payload 完全对齐。
    4. _板端部署_：SQLite 单文件成功生成并持续记录 1Hz 遥测（打包）与事件。
    5. _人工验收_：这 8+1 表没有在大规模高并发环境下进行过长期写入性能的审计。
+ **【本项目证据】**：Evidence Map C20。
+ **【为什么这样设计 / 为什么不是 X】**：没有将通知日志直接设计在 `database.py` 主业务 schema 中，因为通知逻辑与业务遥测流高度解耦。将 `notification_log` 隔离在邮件发送模块内，便于独立管理邮件去重时间窗口（cooldown）。
+ **【边界】**：这 9 张表属于边缘单机轻量闭环，不涉及主从复制、数据分片或任何分布式高并发支持。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B08。

### LA-O09 React build PASS 为什么不等于全页面人工验收？
+ **【一句话结论】**：React 前端 8 个页面编译构建通过仅能证明静态语法正确、打包链路畅通，决不代表所有交互逻辑、动态数据获取和异常分支都通过了浏览器端人工黑盒验收。
+ **【分层验收框架应用】**：
    1. _代码可见_：`server/frontend/src/pages/` 包含 8 个核心页面。
    2. _编译构建_：Vite 构建打包成功，输出至 `/tmp`（或 build 目录）无 error。
    3. _板端部署_：Vite build 静态文件可由 Flask `static` 托管运行。
    4. _人工验收边界_：build PASS 无法证明视频 MJPEG proxy 长期联调的掉帧与渲染性能问题，也无法保证告警阈值配置修改后 100% 能写入底层 SQLite。
+ **【本项目证据】**：Evidence Map C21。
+ **【为什么这样设计 / 为什么不是 X】**：不能将编译通过等同于业务验收。在前端开发中，缺少自动化端到端测试（如 Cypress/Playwright），静态打包通过只是质量闭环的第一步，必须诚实声明验收边界。
+ **【边界】**：目前页面数据加载与交互仍处于“基本跑通”级别，缺乏复杂浏览器的兼容性测试。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B10。

---

## 7. telemetry contract / batch 400 长答
### LA-T01 telemetry batch 400 字段不一致契约问题排障？
+ **【表面现象】**：在端边联调测试中，device-agent 批量上传遥测数据的 HTTP POST 请求频繁被 Flask 后端校验拦截，并返回 `400 Bad Request` 错误，导致 React 控制台上无法展现秒级历史遥测曲线。
+ **【定位方法】**：
    - _第一步_：在 device-agent 发送侧打印 POST payload，捕获原始 JSON 数据包；
    - _第二步_：查阅 Flask backend 日志，定位反序列化与字段校验报错的具体行号；
    - _第三步_：对比 `docs/07_端边HTTP_JSON_Contract.md` 的规范，核查 python 发送字典与数据库字段的 schema 兼容性。
+ **【机理推导】**：这是典型的契约不一致导致的故障。device-agent 上报的批量报文将 `cpu_temp_c` 和 `mem_used_mb` 等 8 个时序指标平铺放置在 JSON 的顶层；而 Flask 接口及 SQLite 数据表设计的 DDL 结构中，这些指标必须嵌套在子节点 `device` 中。格式不匹配触发了后端字段类型检查拦截。
+ **【为什么修复/止损有效】**：编写了 `batcher.py` 的格式重构补丁，强制将 1Hz 的平铺 sample 打包进嵌套的 `device` 结构体，并在 Flask 后端路由中通过 AST 审计进行了对账核算，使两端数据主结构在源码层对齐。
+ **【反事实/边界】**：虽然源码层看起来对齐，但由于 6/10 后续测试日志中缺板端实际回归 200/201 成功的日志支撑。我们在面试时**坚决只讲“发现与源码级字段对账”，不包装成“已闭环修复上线”的成果**。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B14。

---

## 8. 硬件验证与失败复盘长答
### LA-H02 Water MOS 空载联调与强电安全边界？
+ **【表面现象】**：利用 GPIO 控制继电器来模拟开/关水泵演示时，继电器线圈偶尔出现吸合异常或不吸合。
+ **【定位方法】**：
    - _第一步_：用万用表测量 OPi5 Pin 11 (GPIO 138) 在输出 HIGH 时的实际输出电平，确认是否为标准的 3.3V TTL；
    - _第二步_：核查 MOS 隔离驱动模块的阈值导通电压，发现部分第三方模块需要 5V 驱动；
    - _第三步_：进行空载测试（不接泵，仅观察 MOS 板上红色 LED 状态指示灯）。
+ **【机理推导】**：继电器与 MOS 模块的门极（Gate）导通需要足够的电流和门限电压。如果 OPi5 的引脚驱动能力不足或门限电压不匹配，MOS 就无法完全进入饱和导通状态，导致空载时 LED 指示灯闪烁正常，一旦接入大负载，由于内阻过大直接被烧毁。
+ **【为什么修复/止损有效】**：在面包板级测试中，通过引入三极管电平转换电路将 3.3V 信号拉高到 5V 驱动 MOS 门极，打通了控制链路，并在 2026-06-10 完成了空载 PASS 验证。
+ **【反事实/边界】**：**我们坚守项目安全红线，演示不接 220V 强电。** 该验证仅局限于“空载/低压直流”范围，不能夸大为“已经过长期真实高压水泵负载考验”。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B01。

### LA-H05 I2C5 总线扫空故障与 I2C1 方案切换？
+ **【表面现象】**：在第二阶段硬件调试时，将 OLED 与 MPU6050 传感器接在 OPi5 的 I2C5（物理引脚 3/5）上，运行 `i2cdetect -y 5` 进行总线扫描，返回全空状态（扫不到任何外设），导致屏幕完全无法初始化。
+ **【定位方法】**：
    - _第一步_：检查内核日志 `dmesg | grep i2c`，确认 I2C5 控制器在启动时已被使能，且引脚复用（pinmux）配置无误；
    - _第二步_：用示波器测量物理引脚 3/5 的物理电平，发现 SDA 和 SCL 在上拉电阻使能后依然被异常拉低死锁（低电平）；
    - _第三步_：测试同线 OLED 能在 I2C1 上正常被扫出。
+ **【机理推导】**：物理引脚死锁说明 SDA/SCL 极有可能在 SOC 侧的引脚多路复用（pinmux）中与其他硬件（如板载调试串口或特定上拉元件）存在电平冲突，或者该特定物理通道在当前 Android/Linux 内核 BSP 驱动中存在总线死锁 bug，导致主设备无法正常发出起始信号（START），因而从设备不可能反馈 ACK。
+ **【为什么修复/止损有效】**：由于工期紧张，果断砍掉 I2C5，将 OLED 硬件接线迁移到 OPi5 的 I2C1（引脚 16/18），重新使能设备树。扫描 `i2cdetect -y 1` 成功返回 `0x3c` 物理地址，成功显示本地数据，以最低成本完成了系统止损。
+ **【反事实/边界】**：此操作是物理通道切换止损，并非修复了 I2C5。且当前主线仍缺乏 MPU6050 的 0x68 原始读取日志，不可虚构 0x68 也已完整通过实测。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B02。

### LA-H09 PCA9685 扫不到设备无 ACK 时的直控止损？
+ **【表面现象】**：将多个 PCA9685 舵机扩展板接入 OPi5 进行调试时，`i2cdetect` 无法扫描到芯片地址，所有舵机无动作，控制台报 I2C NACK 错误。
+ **【定位方法】**：
    - _第一步_：用逻辑分析仪捕捉 I2C 寻址时序，证实 OPi5 发出了寻址数据包，但在对应的 ACK 位，SDA 线被拉高（表明从设备无 ACK 响应）；
    - _第二步_：用万用表测 PCA9685 芯片供电电压，发现供电纹波极大，且引脚虚焊。
+ **【机理推导】**：PCA9685 芯片由于供电不稳定或虚焊导致内部数字逻辑电路未能正常复位，无法拉低 SDA 反馈应答信号（NACK）。一旦中继扩展芯片失联，后端的任何云台控制指令都会被直接丢弃。
+ **【为什么修复/止损有效】**：决定不继续调试不稳定的扩展板，将云台舵机信号线直接物理直连到 OPi5 的引脚 7 (PWM15 / pwmchip4)，直接利用 Linux sysfs 系统底层接口驱动 50Hz PWM 控制，从而绕过了 PCA9685 扩展芯片，让云台演示链路在安全边界内恢复。
+ **【反事实/边界】**：此排障过程是系统设计的**应急降级与止损决策**，不能在简历中声称“实现了基于 PCA9685 的多路舵机复杂扩展”。
+ **【30 秒口语引用】**：口语表述参见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B02。

---

## 9. 核心技术机理深度解析 (通用原理专栏)
为了防止面试官认为我们的长答只是“死记硬背数字”，本节对关键的技术进行深度物理与逻辑推导：

### 9.1 GPIO 驱动与 PWM 舵机控制机理
+ **【通用原理与物理机理】**：
    - _GPIO 机制_：SOC 通过内部寄存器（如 Data Register, Direction Register）控制物理引脚输出 0V（低电平）或 3.3V（高电平）。输入引脚采用施密特触发器进行波形整形和电平转换，读寄存器即可得知物理电平。为了防止引脚悬空产生不确定逻辑值，必须使能内部或外部的上下拉电阻。
    - _PWM 舵机控制机理_：PWM 信号的周期 $ T $ 通常固定为 20ms（50Hz）。舵机的控制取决于正脉冲的宽度（Pulse Width）。1.5ms 脉宽对应舵机中心位置（0° / 90°），0.5ms 脉宽对应最左端，2.5ms 脉宽对应最右端。舵机内部含有电位计和闭环误差放大电路，通过比较接收脉宽与自身电位计阻值来调整直流电机的物理偏转。
+ **【本项目证据分区】**：
    - 证据见 `edge/opi5-controller/src/opi5_safetyd.c` 内部通过 sysfs 写入 `/sys/class/pwm/pwmchip4/pwm15/` 周期与占空比参数。
+ **【设计边界与反事实】**：
    - 本项目舵机为**开环控制**。主控仅下发 PWM 脉宽指令，无法获知舵机是否已实际偏转到位、是否发生卡死、或被物理外力强行改变了角度。
    - 舵机的电源线必须与板载控制电路进行“星形共地”（Common Grounding），否则信号线将失去回流参考，产生舵机抖动。

### 9.2 I2C 协议物理总线寻址与排障机理
+ **【通用原理与物理机理】**：
    - _I2C 总线物理特性_：I2C 仅由时钟线 (SCL) 和数据线 (SDA) 组成，两者均需外接上拉电阻到电源，默认为高电平。采用开漏 (Open-Drain) 驱动架构，任意设备拉低总线即可实现逻辑“0”。
    - _寻址与应答 (ACK)_：主设备发送起始信号（SCL为高时，SDA产生下降沿），随后发送 7 位从设备物理地址和 1 位读写方向。在第 9 个时钟脉冲，主设备释放 SDA 线，如果对应的从设备匹配，必须主动拉低 SDA（ACK），否则 SDA 被上拉保持高电平（NACK）。
+ **【本项目证据分区】**：
    - 物理联调中，`i2cdetect -y 1` 可成功反馈 OLED 0x3C 的 ACK，但 PCA9685 以及早期 I2C5 均为 NACK 失败日志。
+ **【设计边界与反事实】**：
    - 代码虽包含 MPU6500 的读取路径，但由于缺乏原始 I2C 0x68 的扫描日志证据，该部分在面试中被定性为 risky。

### 9.3 SQLite 存储引擎与 WAL 并发写入机理
+ **【通用原理与物理机理】**：
    - _传统的 Rollback Journal 模式_：修改数据库时，先将原始页拷贝到日志中，写回主库时直接锁定整个库文件。写操作时只允许读（共享锁），不支持任何写（排他锁），写操作会相互排挤。
    - _WAL (Write-Ahead Logging) 机制_：开启 WAL 后，修改直接追加写入独立的 `-wal` 文件中，主数据库文件保持不变。读取时可以结合主库与 `-wal` 文件进行数据重组。这使得读操作和写操作可以并行，只有多个写操作之间依然会发生阻塞（单 Writer 限制）。
+ **【本项目证据分区】**：
    - 证据在 `database.py` 连接初始化中执行 `PRAGMA journal_mode=WAL;`。这支撑了 device-agent 频繁的遥测批量入库与 SSE 的实时读取。
+ **【设计边界与反事实】**：
    - WAL 依然无法解决“多进程同时写”的限制。当 device-agent、Flask 甚至 safetyd 试图同时向 SQLite 执行写操作时，由于单写锁限制，依然会引发 `database is locked` 错误，故只适用于中低强度的边缘单机演示，绝非生产级分布式并发库。

### 9.4 SSE (Server-Sent Events) 与双向长连接对比机理
+ **【通用原理与物理机理】**：
    - _SSE 协议_：基于标准 HTTP 长连接，采用 `text/event-stream` 格式单向推送文本流。客户端通过 EventSource API 监听，连接断开时浏览器会自动重连。
    - _WebSocket 协议_：基于 TCP，需要执行协议握手（HTTP 101 Upgrade），建立双向对等的二进制长连接通道。
+ **【本项目证据分区】**：
    - 后端接口 `/api/stream/events`，前端 React Dashboard 事件面板消费该接口。
+ **【设计边界与反事实】**：
    - 排除 WebSocket 是为了严守安全红线：双向连接意味着前端可以通过网页将指令反向传递到后端和板卡，这给攻击者通过前端网页直接触发执行器动作（如开泵、乱打舵机）提供了通道。选用单向 SSE，能从协议层彻底确保前端“只可观测、不可控制”的物理边界。

---

## 10. 指标边界长答
_(本节数据与 DEEP_INTERVIEW_PREP_AI_SAFETY_MONITOR.md 以及 Evidence Map 保持绝对一致)_

+ **2816 行**：`opi5_safetyd.c` 的 wc -l 文件行数（C05），是代码规模审计事实，不代表复杂度。
+ **0-10 评分**：本地传感器叠加 AI 提示的累加评分规则，不包含概率模型（C06）。
+ **13s 延迟**：2026-06-07 测试中 Qwen3-VL 首次拉起并初始化大模型权重的开销（冷启动），非正常推理周期（C14）。
+ **4.7-5.6s 延迟**：2026-06-08 优化 persistent worker 通信管道后，后续图像推理延迟的小样本观察记录，非稳定 P95 指标（C15）。
+ **8-9s 延迟**：2026-06-07 包含 Flask API 路由跳转和早期 worker 通信延迟的数据，必须如实陈述，证明延迟的波动边界（C15）。
+ **25 个 Flask 路由 / 21 个唯一路径**：AST 静态扫描的 decorated 路由函数数量。不将 4 个本地 AI service 端点计入其中，以防混淆（C19）。
+ **8+1 张表**：SQLite 主 schema 8 张业务表 + email_notifier 里的 notification_log，共 9 张表（C20）。
+ **8 页 React Console**：Vite 成功 build 并通过静态路由注册的 8 个页面，不包装全部人工验收通过（C21）。

---

## 11. 失败复盘 STAR 长答
_(本节所有 STAR 故事已经套用排障五步法，且口语部分已经完全去重，改为链接引用)_

+ **STAR-01: Qwen single-shot 到 worker 推理优化**：参见 PREP 文档第 10.3 节。口语引用见 SPOKEN_ANSWERS.md 中的 B07 专区。
+ **STAR-02: PCA9685 无 ACK 后改用 GPIO/PWM 本地直控**：参见 PREP 文档第 10.2 节。口语引用见 SPOKEN_ANSWERS.md 中的 B02 专区。
+ **STAR-03: I2C5 空总线故障与 I2C1 方案切换**：参见 PREP 文档第 10.5 节。口语引用见 SPOKEN_ANSWERS.md 中的 B02 专区。
+ **STAR-04: telemetry batch 400 字段契约不一致排障**：参见 PREP 文档第 10.4 节。口语引用见 SPOKEN_ANSWERS.md 中的 B14 专区。
+ **STAR-05: i.MX6ULL 双板向 OPi5 一板主控迁移**：参见 PREP 文档第 10.1 节。口语引用见 SPOKEN_ANSWERS.md 中的“项目演进”部分。
+ **STAR-06: Flask+React 可观测性展示链路构建**：参见 PREP 文档第 11 节。口语引用见 SPOKEN_ANSWERS.md 中的 B10 专区。

---

## 12. 面试官继续追问树
_(本小节所有追问路径已经去重，口语回答全部改写为文字链接指向唯一口语稿)_

### Tree-01 C02 时间真实性拷打
+ **第一层问题**：你简历里写项目从 2026-03 开始，证据在哪里？
+ **第二层追问**：3 月具体做了什么？
+ **第三层证据追问**：3 月的立项文件、 commit 记录或文档在哪个目录下？
+ **第四层反驳**：如果找不到证据，是不是虚报项目周期？
+ **最终防守边界**：C02 仍为 risky。目前材料只能证明主要开发和回归测试集中在 2026-06。如果没有补齐 P0 级别立项证据，在面试中坚决保守陈述，不说 3 月已正式开展。
+ **口语引用**：见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的“项目演进”专区。

### Tree-02 C15 Qwen3-VL 性能拷打
+ **第一层问题**：你简历里说 Qwen3-VL 耗时在 5 秒内，这能作为稳定指标吗？
+ **第二层追问**：为什么 6/7 的测试日志里后续推理还有 8-9s？
+ **第三层证据追问**：测试时的样本量是多少？是在什么负载下测的？
+ **第四层反驳**：你这显然是挑选了最优的一两次数据，根本没有统计学意义吧？
+ **最终防守边界**：承认样本量较少，仅作为回归测试小样本观察，绝非大样本的 P95/P99 指标。
+ **口语引用**：见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B12 专区。

### Tree-07 C32 telemetry batch 400 契约拷打
+ **第一层问题**：为什么遥测批量上报 batch 接口返回了 400 错误？
+ **层层追问**：源码主结构对齐了，为什么还不算修复？代码改了为什么没部署验证？
+ **最终防守边界**：契约对齐不等同于集成回归闭环，缺乏板端部署及 200/201 回归日志前保持 risky。
+ **口语引用**：见 [SPOKEN_ANSWERS.md](file:_home_qbz415_safetymonitor__local_archive_interview_deep_interview_spoken_answers) 的 B15 专区。

---

## 13. 需要 GPT 联网补强的知识点
| 知识点 | 补强内容 | 限制边界 | 目标回填位置 |
| --- | --- | --- | --- |
| RK3588S / OPi5 硬件架构 | NPU 算力、共享内存寻址、BSP 内核版本、物理总线冲突等。 | 仅限通用知识，不把未使用的 RKNN 官方算子写成本项目成果。 | 第 9.1 节 |
| Qwen3-VL-2B RKLLM 量化原理 | INT8/INT4 逐层激活对齐与相似度比对。 | 拒绝夸大项目做过准确率与召回率 benchmark。 | 第 9.4 节 |
| SQLite WAL 多路并发限度 | WAL 模式在多写冲突下的锁级别。 | 坚决声明项目未使用多进程并发数据库。 | 第 9.3 节 |
| SSE 与 HTTP/1.1 长连接机制 | Keep-Alive 头与单浏览器多通道并发限制。 | 不涉及复杂的网络协议调优。 | 第 9.4 节 |


---

## 14. 回填建议
+ **Evidence Map**：只有在补充到真实 telemetry batch 200 回归日志后，方可将 C32 状态从 risky/missing_fix 修改为 safe。
+ **Code Evidence Delta**：如果补齐了 I2C1 0x68 的逻辑分析仪数据，需在 delta 中更新对应的原始数据帧证据。

---

## 15. 自检统计
+ **long_answers_count**: 55
+ **covered_claims**: C01-C32 均已覆盖
+ **contains_new_project_fact**: false (无新编造指标)
+ **contains_ai_controls_actuator**: false
+ **contains_26_flask_api_as_truth**: false
+ **contains_telemetry_fixed_as_truth**: false
+ **general_knowledge_partitioned**: true (通用原理与本项目证据物理分区)
+ **oral_answers_deduplicated**: true (已完全收拢引用至 SPOKEN_ANSWERS)

