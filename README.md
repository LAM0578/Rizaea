

# Rizaea

本工具为 Arcaea 自制谱面辅助工具，用于生成类似 Rizline 的谱面动画

## 使用说明

**本工具只在 Python 3.12.0 中测试过, 请尽量使用 Python 3.8 及以上版本**

暂时还没有测试三个组 (`moveGroup`) 及以上的效果，如果有问题日后修复

本工具没有提供图形化界面，需自己打开 VSCode 等支持运行 Python 的编辑器编写代码

### 代码示例
```python
from MakeData import *

groups = [
  [
    '''
    timing(0,100.00,4.00);
    arc(5000,10000,0.00,0.00,s,1.00,1.00,0,none,true);
    ''',
    [
      [
        2000, # 动画开始时间
        500, # 动画持续时间
        'CubicOut', # 动画缓动
        makeFuncFromPos(1, 1), # 计算开始位置的函数
        makeFuncFromPos(0, 0), # 计算结束位置的函数
        True # 决定动画开始时是否使用计算后位置
      ]
    ]
  ]
]

datas = generateFromGroups(groups)
generateFromDatas(datas, 'output.aff')
```

如果你不嫌麻烦可以参考以下格式

### JSON 示例
```jsonc
{
  "timings": [ // 定义的 timing 事件列表
    {
      "timing": 0,
      "bpm": 100.0,
      "beats": 4.0
    },
    {
      // ...
    }
  ],
  "notes": [ // 定义的 note 列表
    {
      "timing": 5000, // int: arc 开始时间
      "endTiming": 10000, // int: arc 结束时间
      "easing": "s", // str: arc 缓动
      "color": 0, // int: arc 颜色
      "isTrace": true, // bool: arc 是否为音轨
      "arctaps": [], // list[int]: 天空音符列表
      "moveGroup": [
        {
          "timing": 5000, // int: 动画开始时间
          "duration": 500, // int: 动画持续时间
          "easing": "CubicOut", // str: 动画缓动
          "start": {
            "startPos": [ 1.0, 1.0 ], // list[float, float]: 动画开始时 arc 的开始位置
            "endPos": [ 0.0, 0.0 ] // list[float, flaot]: 动画开始时 arc 的结束位置
          },
          "end": {
            "startPos": [ 0.0, 0.0 ], // list[float, float]: 动画结束时 arc 的开始位置
            "endPos": [ 1.0, 1.0 ] // list[float, float]: 动画结束时 arc 的结束位置
          }
        },
        {
          // ...
        }
      ]
    },
    {
      // ...
    }
  ]
}
```

### 动画相关参数修改
- 修改生成帧率
```python
_FPS = 60 # int
```
- 修改初始化隐藏 Note 的时间
```python
_PRELOAD_HIDE_TIME = 0 # int
```

以上描述的 [`动画相关参数修改`](#动画相关参数修改) 都位于 `Rizaea.py` 中

### 可用缓动列表
| 缓动编号 | 缓动名称 |
|---|---|
| 0 | Linear |
| 1 | InSine |
| 2 | OutSine |
| 3 | InOutSine |
| 4 | InQuad |
| 5 | OutQuad |
| 6 | InOutQuad |
| 7 | InCubic |
| 8 | OutCubic |
| 9 | InOutCubic |
| 10 | InQuart |
| 11 | OutQuart |
| 12 | InOutQuart |
| 13 | InQuint |
| 14 | OutQuint |
| 15 | InOutQuint |
| 16 | InExpo |
| 17 | OutExpo |
| 18 | InOutExpo |
| 19 | InCric |
| 20 | OutCric |
| 21 | InOutCric |
| 22 | InBack |
| 23 | OutBack |
| 24 | InOutBack |
| 25 | InElastic |
| 26 | OutElastic |
| 27 | InOutElastic |
| 28 | InBounce |
| 29 | OutBounce |
| 30 | InOutBounce |
| 31 | Bezier |

---

祝您创作出更好的谱面