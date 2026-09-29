# P13｜An integrated edge AI prototype for smart agriculture: real-time pest detection, physical trapping, and multi-node deployment analysis under field uncertainty

**作者：** Kunfu Wang; Shirong Guo; Xinyue Yang; Botao Lin; Weihua Cai; Rui Tang; Jianpu Lin  
**年份/日期：** 2026；2026-06（页面日级显示有22/23日差异）  
**期刊/会议：** Frontiers in Plant Science, 17  
**类型：** 农业闭环原型研究  
**DOI：** 10.3389/fpls.2026.1853368  
**核实页面：** https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2026.1853368/full  
**访问日期：** 2026-09-30  
**适用章节：** 2、3、4、5  
**可信度：** 高（书目信息与论文本身可追溯；实验仍为作者报告）

## 150–250字要点（独立改写）
论文把水稻害虫识别、物理诱捕和节点部署分析结合，采用边缘计算板与微控制器分担视觉推理和执行控制，补足了只做离线识别研究的系统环节。其设备连接和实物图可用于讲解传感、串口通信、继电器及诱捕装置组成的闭环。证据应按层级拆开：训练平台性能、设备推理、实验室控制成功率、室外观察和多节点仿真不是同一种实证。尤其不能把训练服务器帧率当作端侧结果，或把实验室触发成功率写成田间灭虫率、农药减少量或增产效果。

## 可提取的实验数据
【事实：作者报告】表4的59.4 FPS属于NVIDIA TESLA T4；Xavier NX设备值44.5 FPS。系统报告采集到执行36.8 ms；双节点实验室约150次呈现中142次成功、94.7%。LoRa视距500 m丢包<1.2%。

## 局限与禁止外推
田间图像1500张、12类；增广后训练集2727，未增广验证152/测试59。测试集较小；实验室执行与田间农业效果需严格区分，多节点优化主要是仿真。

## 核验范围
出版社HTML全文、表4脚注、控制测试、图1/2；日级日期不确定而保留月份。DOI解析已尝试但失败；出版社正文及DOI标识已核读。
本文中的已发表内容标为【事实：原文陈述/作者报告】，不等于独立复现；农业工程建议标为【你的推断】。引用本卡片时使用来源ID [P13]，不要把来源可信度理解为实验所有指标均无争议。
