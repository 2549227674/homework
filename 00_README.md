# 智慧农业 × 嵌入式端边智能：研究素材包

**交付性质：** 综述前期研究与可追溯素材，不是Word综述成稿。依据任务书，以智慧农业为领域，支持后续撰写约8000–12000字课程综述。  
**检索截止/访问基准：** 2026-09-30。重点覆盖2023–2026，经典方法不限年份。  
**重要交付状态：** 图片采用任务书授权的“直链+版权记录”备用方式；包内实际图片0张、图源12项，PDF0篇。所有下载状态如实记录，未生成替代图片。

## 快速入口
先读01_key_findings.md获得逐章论据，再读09_gaps_and_notes.md了解不能采用的推论。正式引用时用02_sources.csv回到原文；定量作图从04_data筛选，不从段落摘出数字后丢失测量口径。图片链接见07_images/image_download_links.md。

## 实际数量与覆盖
| 类别 | 实际数量 | 说明 |
|---|---:|---|
| 论文 | 15 | 综述3篇；2024年及以后9篇；中文论文2篇 |
| 行业/背景及目标数据 | 12 | 10条行业、农业统计或机构预测，另2条政策目标 |
| 硬件平台 | 8 | MCU 2、中端SoC/板卡3、高端GPU/专用加速器3 |
| 案例 | 6 | 中国4、美国2；商业产品2、研究系统4 |
| 政策与标准 | 6 | 中国政策2、ISO标准3、NIST技术基线1 |
| 图片记录 | 12 | 原图直链12；本地图片0；开放许可9、未知许可3 |
| 图表构思 | 8 | 含端边云、部署流程、硬件、轻量化、任务、时间线与对比图 |
| 全部来源记录 | 61 | 包含12条图源；不是61份独立实验 |
| 案例/实验审计数据行 | 52 | 含原值和限制，不能全用于横向排名 |
| 逐章笔记 | 约3193中文字 | 仅计汉字，另有英文术语和数字；不是最终综述正文 |

## 检索策略与可复用检索式
中文交叉词：智慧农业、精准农业、病虫害、杂草、果园估产、农业无人机、温室监测 × 嵌入式、端侧推理、边缘智能、端边云协同、微控制器、模型量化、实时性、功耗、OTA。  
英文交叉词：smart agriculture / precision agriculture / crop disease / weed detection / pest trapping / orchard counting × edge AI / TinyML / on-device inference / cloud-edge-device / embedded deployment / TensorRT / Hailo / Jetson / ESP32。

可复用检索式例：`("edge AI" OR TinyML) agriculture review 2024 2025 2026`；`weed detection Hailo Raspberry Pi edge deployment`；`病虫害 边缘计算 Jetson 量化`；`智慧农业 行动计划 农业农村部 2024 2028`。这些是检索策略说明，不是带总命中数的系统综述日志。

最初检索范围包含IEEE Xplore、ACM DL、Elsevier/Springer、arXiv及中文期刊/CNKI线索；实际通过公开网页搜索回到原论文和官方页面核验，**未声称完成上述付费数据库的登录检索或全量筛选**。实际纳入来源包括NeurIPS、arXiv、IoT原版PDF、Frontiers、Scientific Reports、Springer Discover与《智慧农业》；厂商官网/工具文档；农业农村部、国家统计局、USDA、ISO和NIST；IDC及企业原始公开公告。

筛选标准：优先原论文、有明确设备与部署路径的农业研究、原厂规格及官方统计；排除只有搜索摘要而正文不可核实的数字、不明转载图和混合口径市场规模。先追踪任务和设备，再读原文指标与脚注，必要时查看PDF表格截图。没有保存可复现总命中数，因此本包是范围式资料搜集，不能标成遵循PRISMA的系统综述。

## 覆盖强弱
**较强：** 第2章硬件与工具链、第3章种植业视觉和执行系统，第4章测量边界与软硬件权衡。  
**较弱：** 长周期独立田间对照、全生命周期成本、同模型同平台端/云对照、农业联邦学习与持续学习成熟部署，以及畜牧/水产。部分2026新论文计时存在疑点，已保留而未粉饰。

## 目录
```text
research_pack_smart_agriculture/
  00_README.md
  01_key_findings.md
  02_sources.csv
  03_papers/                   # P01–P15，逐篇卡片
  04_data/
    market_data.csv
    hardware_specs.csv
    case_metrics.csv
  05_cases/                    # C01–C06
  06_policy_standards.md
  07_images/
    image_credits.csv          # downloaded均为no
    image_download_links.md
    download_images.py         # 本地有网络时使用；保留原图
  08_figure_ideas.md
  09_gaps_and_notes.md
```

## 文献索引
| ID | 年份 | 类型 | 文献卡 |
|---|---:|---|---|
| P01 | 2020 | 奠基性研究 | [MCUNet: Tiny Deep Learning on IoT Devices](03_papers/P01_MCUNet.md) |
| P02 | 2016 | 奠基性研究 | [Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding](03_papers/P02_Deep_Compression.md) |
| P03 | 2015 | 奠基性研究 | [Distilling the Knowledge in a Neural Network](03_papers/P03_Knowledge_Distillation.md) |
| P04 | 2019 | 奠基性研究 | [Searching for MobileNetV3](03_papers/P04_MobileNetV3.md) |
| P05 | 2025 | 综述 | [Emerging Developments in Real-Time Edge AIoT for Agricultural Image Classification](03_papers/P05_Agricultural_Edge_AI_Review.md) |
| P06 | 2025 | 综述 | [Cloud–edge–device collaborative computing in smart agriculture: architectures, applications, and future perspectives](03_papers/P06_Cloud_Edge_Device_Review.md) |
| P07 | 2023 | 综述 | [农业知识智能服务技术综述](03_papers/P07_Agricultural_Knowledge_Review.md) |
| P08 | 2023 | 农业部署研究 | [用于边缘计算设备的果树挂果量轻量化估测模型](03_papers/P08_Citrus_Edge_Counting.md) |
| P09 | 2025 | 农业部署研究 | [AI and IoT-powered edge device optimized for crop pest and disease detection](03_papers/P09_TinyLiteNet_Crop_Pests.md) |
| P10 | 2025 | 农业部署研究 | [YOLO-PLNet: a lightweight real-time detection model for peanut leaf diseases based on edge deployment](03_papers/P10_YOLO_PLNet.md) |
| P11 | 2025 | 农业部署研究 | [GAE-YOLO: a lightweight multimodal detection framework for tomato smart agriculture with edge computing](03_papers/P11_GAE_YOLO_Tomato.md) |
| P12 | 2026 | 农业部署研究（指标存疑） | [Automated tomato leaf disease detection and alert system using Internet of Things and TinyML](03_papers/P12_TinyML_Tomato_Alerts.md) |
| P13 | 2026 | 农业闭环原型研究 | [An integrated edge AI prototype for smart agriculture: real-time pest detection, physical trapping, and multi-node deployment analysis under field uncertainty](03_papers/P13_Integrated_Pest_Trap.md) |
| P14 | 2026 | 农业部署研究（计时存疑） | [Enabling scalable and energy-efficient weed detection using data-driven edge AI for precision agriculture](03_papers/P14_Hailo_Weed_Detection.md) |
| P15 | 2026 | 端边云对比研究（需复核） | [Hybrid LSTM-edge correction architecture for physics-informed crop health monitoring in distributed agricultural robotics](03_papers/P15_Hybrid_LSTM_Edge.md) |

## 案例索引
| ID | 国家 | 证据成熟度 | 案例卡 |
|---|---|---|---|
| C01 | 中国 | 研究原型；非商业销售验证 | [果园视频挂果量估测](05_cases/C01_Citrus_Counting.md) |
| C02 | 美国 | 商业产品；效果主要来自企业公开口径 | [LaserWeeder G2 600激光除草](05_cases/C02_Carbon_LaserWeeder.md) |
| C03 | 中国 | 商业产品；本包采用国际官网版本 | [P150农业无人机感知与作业控制](05_cases/C03_XAG_P150.md) |
| C04 | 中国 | 研究原型；实验室量化测试+室外观察+仿真 | [边缘识别—微控制器执行的水稻害虫诱捕原型](05_cases/C04_Rice_Pest_Trap.md) |
| C05 | 美国 | 研究原型；数据集部署评估，非已证实商业田间系统 | [树莓派与Hailo-8L的杂草检测部署](05_cases/C05_Hailo_Weeds.md) |
| C06 | 中国 | 论文报告田间监测；对比设计与测量口径待复核 | [本地LSTM与边缘物理模型协作监测](05_cases/C06_Hybrid_Crop_Monitoring.md) |

## 引用、标签与核验方式
统一来源前缀：P论文、R报告/统计、N新闻（本包无独立N记录）、O官方页面、H硬件资料、S政策标准、I图源。C/M/D只是案例或数据行编号，使用时仍应带来源ID。

【事实】指可以追溯到原始文件的公开内容；论文实验要加“作者报告”。【机构预测】不因预测年份已经过去就自动变历史实绩。【厂商宣传口径】明确保留最高值、适用条件与自报性质。【你的推断】表示本包组织的工程建议或论证，不冒称已部署。

“可信度高”主要说明来源身份与可追溯性，不是对所有实验方法、商业效果或法规符合性的保证。每条DOI在原文核读且解析入口已尝试，但有7个解析失败，详见09；所有主证据URL均有可用内容。日级日期不明或页面版本冲突已明确标注，未补造。

## 图片使用
9项论文图片有CC许可记录，其中I09带非商业/禁止演绎限制；3项官方图许可未知。下载完成后核对清晰度、实际尺寸与署名，尽量控制每张1.5 MB以内；不要擅自改动受禁止演绎限制的原图。脚本不会压缩或改编图片，也不会把下载成功当作版权授权。

## 给后续撰写者的交接
优先展开P01/P05/P06的技术框架、P08/P13的系统问题与各类官方软件资料；商业案例保留厂商标签。P10/P12/P14/P15的性能疑点必须随引用保留。提交前最应人工复核的三组事项：**计时和功耗定义、具体设备/产品版本、图片许可与标准适用边界**。不得把本素材包写成“所有实验已独立复现”。
