import easings
import json
import math

_FPS = 60
_PRELOAD_HIDE_TIME = 0
_EASING_FUNC_MAP = {
    k[5:].lower() : getattr(easings, k) for k in easings.__all__
}

class rizaea:
    def __init__(self, data):
        self.timings = data['timings']
        self.notes = data['notes']

    def __lerpPos(self, a, b, t):
        def lerp(a, b, t):
            return a + (b - a) * t
        return [lerp(a[0], b[0], t), lerp(a[1], b[1], t)]
    
    def __makeNote(self, note, move, p):
        start = self.__lerpPos(move['start']['startPos'], move['end']['startPos'], p)
        end = self.__lerpPos(move['start']['endPos'], move['end']['endPos'], p)
        timing = note['timing']
        endTiming = note['endTiming']
        easing = note['easing']
        color = note['color']
        isTrace = note['isTrace']
        arctaps = note['arctaps']
        result = '  arc({:.0f},{:.0f},{:.2f},{:.2f},{},{:.2f},{:.2f},{:.0f},none,{})'.format(
            timing,
            endTiming,
            start[0],
            end[0],
            easing,
            start[1],
            end[1],
            color,
            str(isTrace).lower()
        )
        if arctaps != []:
            result += '['
            arctapsRaw = []
            for at in arctaps:
                arctapsRaw += [ f'arctap({at:.0f})' ]
            result += ','.join(arctapsRaw)
            result += ']'
        result += ';'
        return result
    
    def makeGroup(self):
        global _FPS
        timings = self.timings
        timingsRaw = []
        for timing in timings:
            t = timing['timing']
            bpm = timing['bpm']
            beats = timing['beats']

            timingsRaw += [ f'  timing({t:.0f},{bpm:.2f},{beats:.2f});' ]

        notes = self.notes
        result = []
        for note in notes:
            noteTiming = note['timing']
            moveGroup = note['moveGroup']

            groupCount = len(moveGroup)
            for i in range(groupCount):
                group = moveGroup[i]

                timing = group['timing']

                nextGroupTiming = -0x7fffffff
                if i < groupCount - 1:
                    nextGroupTiming = moveGroup[i + 1]['timing']

                groupEasing = group['easing']

                isFirstGroup = i == 0

                interval = 1000. / _FPS
                count = int(math.ceil(group['duration'] / interval)) + 1
                for i in range(count + 1):
                    isLast = i == count
                    
                    tgProperty = ''
                    shouldHide = (
                        (noteTiming >= nextGroupTiming and nextGroupTiming >= 0)
                        or
                        (noteTiming < timing and not isFirstGroup)
                    )
                    if not isLast or shouldHide:
                        tgProperty = 'noinput'
                    result += [ f'timinggroup({tgProperty})' + '{' ]

                    result += timingsRaw

                    if not(isFirstGroup and i == 0):
                        result += [ f'  scenecontrol({_PRELOAD_HIDE_TIME},hidegroup,0.00,1);' ]
                        t = int(timing + interval * (i))
                        result += [ f'  scenecontrol({t:.0f},hidegroup,0.00,0);' ]

                    p = i / float(count)
                    p = _EASING_FUNC_MAP[groupEasing.lower()](p)
                    result += [ self.__makeNote(note, group, p) ]

                    if not isLast:
                        t = int(timing + interval * (i + 1))
                        result += [ f'  scenecontrol({t:.0f},hidegroup,0.00,1);' ]

                    if noteTiming >= nextGroupTiming and nextGroupTiming >= 0:
                        result += [ f'  scenecontrol({nextGroupTiming:.0f},hidegroup,0.00,1);' ]

                    result += [ '};' ]

        return result
    
def generateFromDatas(datas, outputPath):
    with open(outputPath, 'w') as f:
        rawLines = []
        for data in datas:
            rawLines += rizaea(data).makeGroup()
        f.write('\n'.join(rawLines))