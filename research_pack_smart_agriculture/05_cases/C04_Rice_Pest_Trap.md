# C04｜边缘识别—微控制器执行的水稻害虫诱捕原型

**机构：** 福州大学等联合研究团队  
**国家：** 中国  
**证据成熟度：** 研究原型；实验室量化测试+室外观察+仿真  
**适用章节：** 2、3、4、5  
**访问日期：** 2026-09-30

## 场景与问题
把害虫识别结果及时转为物理诱捕动作，并研究节点通信与布设问题，避免仅停留在离线检测。

## 硬件、模型与系统架构
【事实】Jetson Xavier NX负责视觉；ESP32负责执行控制；系统含光源、风扇、LoRa、GPS和供电组件。未证明ESP32是S3型号。[P13]

【事实】轻量YOLOv13-M-G-P3及TensorRT部署；UART连接计算与控制单元，按识别结果触发执行器。[P13]

【事实】论文给出实物与连接图，能支持“相机→Xavier NX→串口→ESP32→光源/风扇”的闭环。多节点策略的优化收益主要来自仿真，不能画成已完成大规模田间组网验证。[P13]

## 公开效果及其口径
【事实：作者报告】端侧44.5 FPS，采集到执行36.8 ms；约150次实验室呈现中142次成功，控制成功率94.7%。训练测试表59.4 FPS属于T4，不属于Xavier NX。[P13]

结构化数据见04_data/case_metrics.csv，筛选system_id=C04。未公开字段不是零，也不是可由类似产品代填。

## 证据局限
短时实验不能证明全年灭虫效果；控制成功率不是昆虫死亡率，仿真覆盖收益不是实测节药收益。无可核实的单位面积全生命周期成本。

## 来源与可信度
- [P13] An integrated edge AI prototype for smart agriculture: real-time pest detection, physical trapping, and multi-node deployment analysis under field uncertainty：https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2026.1853368/full（论文）

论文与原厂页面能确认其公开陈述；商业效果缺少独立审计，论文原型也不自动代表长期田间有效。分项可信度与理由见02_sources.csv。
