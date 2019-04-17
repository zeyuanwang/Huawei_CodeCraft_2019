# Huawei_CodeCraft_2019 2019年华为软件精英挑战赛

### 题目定义：
在模拟的道路图上为每一辆车规划行驶路线，系统会自动根据规划路线运行。在路线合法的前提下，最终所有车辆按照规划的路线到达目的地。

### 系统假定：
1.路口完全立交：  
假定在每一个路口交汇的所有道路都可以完全互连，且车辆通过路口时不考虑在路口的通行时间。  
2.无限神奇车库：  
假定系统中的每个地点都有一个无限容量的“神奇车库”。车辆在未到既定出发时间前，或者到达目的后，就停放在“神奇车库”中，完全不影响其他车辆通过。但车辆一旦出发，在行驶过程中则不允许进入车库空间。

### 约束条件：
1.不允许超车变道：  
即车辆一旦进入某条车道，就必须在此车道内从道路起点驶向道路终点，中途不允许变道，即使前车速度缓慢，也不允许超车。  
2.排队先到先行：  
在一条道路前排队等待的所有车辆，按照到达时间先后进入道路。若多辆车在同一时间到达，按如下规则进入下一道路：  
（1）同一道路牌车道号小（车道的编号）的车辆优先于车道号大的车辆；  
（2）按现实交通规则，直行车辆有优先通行权，直行车辆优先于转弯车辆；  
（3）处于左转进入道路的车辆优先于右转进入道路的车辆。  
3.车道固定进入：  
车辆在进入一段道路时按照车道编号从小到大的优先级选择可以进入的车道驶入，与前车的行驶速度无关。即就是：车辆优先按车道编号由小到大依次进入，除非车道号小的车道没有空位可进入。  
4.（仅复赛）优先车辆有优先通行权：  
优先车辆比非优先车辆有优先通行权，要求优先保证优先车辆的路权。  
5.（仅复赛）预置车辆：  
预置车辆的行驶轨迹由系统指定车辆的出发时间和行驶线路。参赛选手在此基础上计算非预置车辆的行驶轨迹。  

