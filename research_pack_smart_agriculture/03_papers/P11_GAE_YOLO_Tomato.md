# P11｜GAE-YOLO: a lightweight multimodal detection framework for tomato smart agriculture with edge computing

**作者：** Xiaoke Liu; Wenjie Teng; Haoran Yu; Zhuoyi Yao; Chengzhen Wang; Yuzhong Peng; Xiaoqing Han; Jianming Liu  
**年份/日期：** 2025；2025-11-19  
**期刊/会议：** Frontiers in Plant Science, 16  
**类型：** 农业部署研究  
**DOI：** 10.3389/fpls.2025.1712432  
**核实页面：** https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1712432/full  
**访问日期：** 2026-09-30  
**适用章节：** 3、4、6  
**可信度：** 高（书目信息与论文本身可追溯；实验仍为作者报告）

## 150–250字要点（独立改写）
研究围绕番茄识别构建轻量多模态检测与边缘计算框架，并通过双目相机、Jetson TX2和移动机器人连接目标检测、成熟度及空间信息。该材料适合说明农业视觉任务如何从单张图像分类扩展到机器人可使用的感知结果，也能支持对相机、主控和模型部署关系的讨论。论文涉及咨询等附加功能，但本包未核实大语言模型的具体执行位置，不能把系统能够调用问答功能改写为全部大模型都在板端运行。检测性能仍需与移动速度、遮挡及不同种植条件一起评估。

## 可提取的实验数据
【事实：作者报告】mAP@50为93.5%，Jetson TX2报告10.2 FPS；硬件图包括ZED双目相机和移动平台。其他优化场景的帧率没有纳入本包。

## 局限与禁止外推
多模态系统包含多个功能环节；不能把检测、测距和问答混成同一个端侧模型的成绩。没有可据此计算长期投资回报的公开成本数据。

## 核验范围
出版社HTML全文、硬件图3、DOI落地页。DOI解析成功。
本文中的已发表内容标为【事实：原文陈述/作者报告】，不等于独立复现；农业工程建议标为【你的推断】。引用本卡片时使用来源ID [P11]，不要把来源可信度理解为实验所有指标均无争议。
