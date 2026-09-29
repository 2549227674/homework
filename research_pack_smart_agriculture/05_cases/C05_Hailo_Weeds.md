# C05｜树莓派与Hailo-8L的杂草检测部署

**机构：** North Dakota State University研究团队  
**国家：** 美国  
**证据成熟度：** 研究原型；数据集部署评估，非已证实商业田间系统  
**适用章节：** 2、3、4、5  
**访问日期：** 2026-09-30

## 场景与问题
将作物/杂草识别模型转换为低功耗外接加速器可运行的模型，面向精细化除草的视觉感知。

## 硬件、模型与系统架构
【事实】Raspberry Pi 5 + Hailo-8L；系统功率从USB输入侧测量，不能与Hailo芯片典型功耗直接等同。[P14,H06]

【事实】YOLO系列模型经ONNX导出、Hailo Dataflow Compiler与校准生成HEF，由HailoRT/GStreamer执行；不是模型文件复制到板上就完成部署。[P14]

【事实】论文图1呈现训练、硬件优化与部署测评链；本包没有证据证明其已经接入喷头、机械臂或激光执行器，不补画已实现的除草闭环。[P14]

## 公开效果及其口径
【事实：作者报告】输入供电侧系统功耗约5.4–7.2 W。所报低于5 ms等时延因计时从已处理buffer回调开始，不能当作核实的完整推理时延。[P14]

结构化数据见04_data/case_metrics.csv，筛选system_id=C05。未公开字段不是零，也不是可由类似产品代填。

## 证据局限
需取得计时代码，核对回调前推理与NMS是否计入；需要连续视频、田间域变化与执行器闭环验证。论文系统功耗不能代表所有Pi+Hailo运行负载。

## 来源与可信度
- [P14] Enabling scalable and energy-efficient weed detection using data-driven edge AI for precision agriculture：https://www.frontiersin.org/journals/agronomy/articles/10.3389/fagro.2026.1808404/full（论文）
- [H05] Raspberry Pi 5（以8 GB配置说明） official specifications：https://www.raspberrypi.com/products/raspberry-pi-5/（企业官方/原厂资料）
- [H06] Hailo-8L official specifications：https://hailo.ai/wp-content/uploads/2024/02/hailo8l_product_brief_1.2.pdf（企业官方/原厂资料）

论文与原厂页面能确认其公开陈述；商业效果缺少独立审计，论文原型也不自动代表长期田间有效。分项可信度与理由见02_sources.csv。
