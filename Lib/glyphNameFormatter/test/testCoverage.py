from __future__ import print_function
from glyphNameFormatter.unicodeRangeNames import getAllRangeNames, rangeNameToModuleName, getRangeByName
from glyphNameFormatter import GlyphName
import unicodedata

from glyphNameFormatter.data import name2unicode_AGD
import importlib
from pprint import pprint

#   find which unicode ranges are needed to cover the AGD names
#   so we can prioritize the support

def testCoverage():
    text = []
    text.append("# Coverage")
    wantRanges = {}
    glyphCount = {}
    for thisRange in getAllRangeNames():
        a, b = getRangeByName(thisRange)
        if thisRange.find('Private')!=-1:
            #print("skipping private", thisRange)
            continue

        moduleName = rangeNameToModuleName(thisRange)
        if thisRange not in glyphCount:
            glyphCount[thisRange] = {'uniNames':0, 'total':b-a, 'rangeProcessor':None}
        try:
            module = importlib.import_module('glyphNameFormatter.rangeProcessors.%s' % moduleName)
            glyphCount[thisRange]['rangeProcessor']=True
        except ImportError:
            pass
        for uniNumber in range(a,b):
            g = GlyphName(uniNumber)
            if g.uniName is not None:
                glyphCount[thisRange]['uniNames'] += 1

    totalGlyphs = 0     # the total of all glyph counts in all ranges
    totalCovered = 0    # the total of all glyphs that this package has rangeprocessors for
    totalPoints = 0     # the total of all ranges

    for key, items in glyphCount.items():
        #print(key, items)
        totalGlyphs += items['uniNames']
        totalPoints += items['total']
        if items['rangeProcessor'] is not None:
            totalCovered += items['uniNames']

    text = []
    text.append("")
    text.append("## unicodedata.unidata_version: %s"%unicodedata.unidata_version)
    text.append("")
    text.append('| Total code points in the available ranges | %d |'%totalPoints)
    text.append('| Total named glyphs | %d |'%totalGlyphs)
    text.append(('| Work done so far | %d |'%(totalGlyphs-totalCovered)) + " or %3.3f%%"%(100.0*totalCovered/totalGlyphs))
    text.append('| Total names covered in GlyphNameFormatter | %d |'%totalCovered)

    text.append("")
    text.append("| Range name | has processor | Start | End |")
    text.append("| ----- | ----- | ----- | ----- |")

    for thisRange in getAllRangeNames():
        if not thisRange in glyphCount: continue
        a, b = getRangeByName(thisRange)
        items = glyphCount[thisRange]
        text.append("| %s | %s | %04X | %04X |"%(thisRange, items['rangeProcessor']!=None, a, b))

    path = "../../../coverage.md"
    f = open(path, 'w')
    f.write("\n".join(text))
    f.close()


if __name__ == "__main__":
    testCoverage()