# C02｜LaserWeeder G2 600激光除草

**机构：** Carbon Robotics  
**国家：** 美国  
**证据成熟度：** 商业产品；效果主要来自企业公开口径  
**适用章节：** 3、4、5  
**访问日期：** 2026-09-30

## 场景与问题
在田间区分作物与杂草并定点作用，以机械视觉和激光执行替代部分人工或化学除草环节。

## 硬件、模型与系统架构
【厂商宣传口径】G2 600产品页列12模块、24个240 W激光器和36相机。另一企业委托页面称LaserWeeder系列采用24个NVIDIA GPU、当前RTX 4000；并非可独立核对的G2 600整机物料清单。[O12,O13]

【厂商宣传口径】本地深度学习作物/杂草识别；具体网络权重、训练集、精度与模型版本未公开。企业材料提及CUDA/cuDNN。[O12,O13]

【你的推断】可画为“多相机→机载GPU识别定位→激光瞄准控制→作业记录”，这是依据产品功能作出的系统化概括，不代表取得了厂商内部架构图。[O12,O13]

## 公开效果及其口径
【厂商宣传口径】1.50–3.00 acre/h（官网同时列0.61–1.21 ha/h），最高约10000次杂草作用/分钟，除草效果宣传为最高99%。条件依作物、密度和作业环境，不作为第三方田间试验。[O12]

结构化数据见04_data/case_metrics.csv，筛选system_id=C02。未公开字段不是零，也不是可由类似产品代填。

## 证据局限
推理延迟、统一数据集准确率、整机电耗、购买及维护成本未公开。不能把24×240 W激光额定功率当AI计算功耗；不能把计划升级RTX Pro 4000写成已完成。

## 来源与可信度
- [O12] LaserWeeder G2 600 — product specifications：https://carbonrobotics.com/laserweeder-g2-600（企业官方/原厂资料）
- [O13] From Farm to Fork: How AI Is Transforming Food Safety：https://www.multivu.com/carbon-robotics/9391051-en-nvidia-and-carbon-robotics-revolutionizing-agriculture-with-ai-and-robotics（企业官方/原厂资料）

论文与原厂页面能确认其公开陈述；商业效果缺少独立审计，论文原型也不自动代表长期田间有效。分项可信度与理由见02_sources.csv。
