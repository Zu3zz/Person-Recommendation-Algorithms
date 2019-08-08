# 个性化推荐算法笔记

## Chap0 CF (collaborative filtering)
### itemCf与userCf

#### 详见文件夹CF

- itemcf与usercf的优缺点
  - 推荐实时性 item快 点击了就可以推荐
  - 新用户/新物品的推荐
  - 推荐理由的可解释性
  - 使用场景
    - 性能层面 item适用于物品<<人数
    - 个性化层面考量

## Chap1 LFM (latent factor model)

- 工业界效果比较好
- 什么是LFM算法
  - 输入是每一个user向量和item向量的点赞矩阵
- 应用场景
  - user的item推荐度列表
  - item的相似度推荐列表
  - item之间的相似度隐含挖掘