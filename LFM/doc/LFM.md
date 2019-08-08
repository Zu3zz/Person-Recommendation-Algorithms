# LFM 详细

## LFM 输入  
|     |Item1|Item2|Item3|
|-----|-----|-----|-----|
|User1|1    |0    |1    |
|User2|0    |1    |0    |
|User3|1    |1    |1    |

### 如果item没有被展示给user 直接跳过即可  
- User对于物品的喜好可以用矩阵表示  
  - ==> User1:[0.325, 0.456.....0.768]  
  - ==> User2:[0.215,0.569......0.368]
  - 维度数是设置的特征值
  
### LFM应用场景举例
- 计算用户toplike
- 计算item的topsim
- 计算item的topic

### 影响LFM效果的变量
- 负样本的选取
  - 充分展现但是用户没有点击的样本
  - 选取一定数目
  - 保证正负样本均衡

- 隐含特征F,正则参数,learning rate
  - F的一般范围:(6-32)
  - learning rate:(0.1-0.001)
  

## LFM VS CF
- 理论基础
  - LFM属于supervise learning 好一些
  - itemCF基于公式建模
- 离线计算空间时间复杂度
  - itemCf 物品的平方
  - LFM只需要两个向量 空间复杂度更低
  - LFM时间长一些 但是属于同一数量级
- 在线推荐与推荐解释
  - itemCf 实时性较好
  - CFM 离线计算toplike比较好