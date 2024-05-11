import json
from Rizaea import generateFromDatas

def generateTiming(t):
    splits = t[len("timing(") : -2].split(",")
    timing = int(splits[0])
    bpm = float(splits[1])
    beats = float(splits[2])
    return {"timing": timing, "bpm": bpm, "beats": beats}


def makeFuncFromPos(*pos):
    return [lambda x: pos[0], lambda y: pos[1]]


def generateFromArc(a, groups):
    def makePosDict(start, end, startFunc, endFunc, onStart):
        def callFunc(func, p):
            return [func[0](p[0]), func[1](p[1])]

        if onStart:
            return {
                "start": {
                    "startPos": callFunc(startFunc, start),
                    "endPos": callFunc(endFunc, end),
                },
                "end": {"startPos": start, "endPos": end},
            }
        else:
            {
                "start": {"startPos": start, "endPos": end},
                "end": {
                    "startPos": callFunc(startFunc, start),
                    "endPos": callFunc(endFunc, end),
                },
            }

    def makeGroup(
        changeTime,
        changeDuration,
        changeEasing,
        startFunc,
        endFunc,
        onStart,
        start,
        end,
    ):
        posDict = makePosDict(start, end, startFunc, endFunc, onStart)
        return {
            "timing": changeTime,
            "duration": changeDuration,
            "easing": changeEasing,
            "start": posDict["start"],
            "end": posDict["end"],
        }

    rawSplits = a[4:-1].split("[")
    arcSplit = rawSplits[0][:-1].split(",")
    timing = int(arcSplit[0])
    endTiming = int(arcSplit[1])
    startX = float(arcSplit[2])
    endX = float(arcSplit[3])
    easing = arcSplit[4]
    startY = float(arcSplit[5])
    endY = float(arcSplit[6])
    color = int(arcSplit[7])
    isTrace = arcSplit[9] == "true"
    arctaps = []
    if len(rawSplits) > 1:
        arctapsRaw = rawSplits[1][:-1].split(",")
        for at in arctapsRaw:
            at = at[len("arctap(") : -1]
            arctaps += [int(at)]
    return {
        "timing": timing,
        "endTiming": endTiming,
        "easing": easing,
        "color": color,
        "isTrace": isTrace,
        "arctaps": arctaps,
        "moveGroup": [
            makeGroup(*group, [startX, startY], [endX, endY]) for group in groups
        ],
    }


def parseFromAFF(aff, groups):
    result = {"timings": [], "notes": []}
    for line in aff.splitlines():
        line = line.strip()
        if line.startswith("timing("):
            result["timings"] += [generateTiming(line)]
        elif line.startswith("arc("):
            result["notes"] += [generateFromArc(line, groups)]
    return result


def generateFromGroups(groups):
    '''
    通过多个 AFF 片段生成用于生成动画的 dict

    ---
    示例
    ```python
    groups = [
        [
            \'\'\'
            timing(0,100.00,4.00);
            arc(5000,10000,0.00,0.00,s,1.00,1.00,0,none,true);
            \'\'\',
            [
                [
                    2000,
                    500,
                    'CubicOut',
                    makeFuncFromPos(1, 1),
                    makeFuncFromPos(0, 0),
                    True
                ]
            ]
        ]
    ]
    ```
    ---
    参数
    - groups - list[list[str, list[list]]] : 组参数列表
    ---
    返回
    - list[dict] : 用于生成动画的 dict 列表
    ---
    组参数
    - changeTime - int : 动画开始时间
    - changeDuration - int : 动画持续时间
    - changeEasing - str : 动画缓动
    - startFunc - list[function, function]: 计算开始位置的函数
    - endFunc - list[function, function]: 计算结束位置的函数
    - onStart - bool : 决定动画开始时是否使用计算后位置
    '''
    result = []
    for group in groups:
        result += [parseFromAFF(*group)]
    return result

