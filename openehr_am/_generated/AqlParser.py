# Generated from grammars/aql/AqlParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,91,400,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,1,0,
        1,0,1,0,3,0,70,8,0,1,0,3,0,73,8,0,1,0,3,0,76,8,0,1,0,3,0,79,8,0,
        1,0,1,0,1,1,1,1,3,1,85,8,1,1,1,3,1,88,8,1,1,1,1,1,1,1,5,1,93,8,1,
        10,1,12,1,96,9,1,1,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,5,4,
        109,8,4,10,4,12,4,112,9,4,1,5,1,5,1,5,1,5,3,5,118,8,5,1,6,1,6,1,
        6,3,6,123,8,6,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,135,8,
        8,1,8,1,8,1,8,1,8,1,8,1,8,5,8,143,8,8,10,8,12,8,146,9,8,1,9,1,9,
        3,9,150,8,9,1,10,1,10,1,10,1,10,3,10,156,8,10,1,11,1,11,1,11,3,11,
        161,8,11,1,11,1,11,3,11,165,8,11,1,11,1,11,1,11,1,11,3,11,171,8,
        11,1,11,1,11,1,11,1,11,1,11,1,11,5,11,179,8,11,10,11,12,11,182,9,
        11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,
        12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,3,12,206,8,12,1,
        13,1,13,3,13,210,8,13,1,13,3,13,213,8,13,1,13,1,13,3,13,217,8,13,
        1,13,1,13,1,13,1,13,3,13,223,8,13,3,13,225,8,13,1,14,1,14,1,14,1,
        14,3,14,231,8,14,1,15,1,15,3,15,235,8,15,1,15,1,15,3,15,239,8,15,
        1,16,1,16,1,16,1,16,3,16,245,8,16,1,16,1,16,1,17,1,17,1,17,1,17,
        1,18,1,18,1,19,1,19,1,19,1,19,3,19,259,8,19,1,19,1,19,1,19,3,19,
        264,8,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,3,19,275,8,
        19,1,19,1,19,1,19,1,19,1,19,1,19,5,19,283,8,19,10,19,12,19,286,9,
        19,1,20,1,20,1,20,3,20,291,8,20,1,21,1,21,1,21,1,21,1,21,3,21,298,
        8,21,1,22,1,22,1,22,5,22,303,8,22,10,22,12,22,306,9,22,1,23,1,23,
        3,23,310,8,23,1,24,1,24,1,25,1,25,1,25,1,25,5,25,318,8,25,10,25,
        12,25,321,9,25,1,25,1,25,1,25,1,25,1,25,1,25,3,25,329,8,25,1,26,
        1,26,1,26,3,26,334,8,26,1,27,1,27,1,27,1,27,1,27,1,27,1,27,3,27,
        343,8,27,1,28,1,28,1,28,1,28,1,28,1,28,3,28,351,8,28,1,29,1,29,1,
        29,1,29,1,29,1,29,5,29,359,8,29,10,29,12,29,362,9,29,3,29,364,8,
        29,1,29,3,29,367,8,29,1,30,1,30,1,30,3,30,372,8,30,1,30,1,30,3,30,
        376,8,30,1,30,1,30,1,30,1,30,1,30,1,30,3,30,384,8,30,1,31,1,31,1,
        31,1,31,1,31,1,31,1,31,1,31,1,31,1,32,1,32,1,32,3,32,398,8,32,1,
        32,0,3,16,22,38,33,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,
        34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,0,8,1,0,10,13,2,
        0,56,56,60,60,1,0,57,58,3,0,56,58,62,62,72,72,2,0,56,56,72,72,2,
        0,32,34,61,61,1,0,51,54,1,0,22,23,444,0,66,1,0,0,0,2,82,1,0,0,0,
        4,97,1,0,0,0,6,100,1,0,0,0,8,103,1,0,0,0,10,113,1,0,0,0,12,119,1,
        0,0,0,14,124,1,0,0,0,16,134,1,0,0,0,18,147,1,0,0,0,20,155,1,0,0,
        0,22,170,1,0,0,0,24,205,1,0,0,0,26,224,1,0,0,0,28,230,1,0,0,0,30,
        232,1,0,0,0,32,240,1,0,0,0,34,248,1,0,0,0,36,252,1,0,0,0,38,274,
        1,0,0,0,40,290,1,0,0,0,42,297,1,0,0,0,44,299,1,0,0,0,46,307,1,0,
        0,0,48,311,1,0,0,0,50,328,1,0,0,0,52,333,1,0,0,0,54,342,1,0,0,0,
        56,350,1,0,0,0,58,366,1,0,0,0,60,383,1,0,0,0,62,385,1,0,0,0,64,394,
        1,0,0,0,66,67,3,2,1,0,67,69,3,4,2,0,68,70,3,6,3,0,69,68,1,0,0,0,
        69,70,1,0,0,0,70,72,1,0,0,0,71,73,3,8,4,0,72,71,1,0,0,0,72,73,1,
        0,0,0,73,75,1,0,0,0,74,76,3,10,5,0,75,74,1,0,0,0,75,76,1,0,0,0,76,
        78,1,0,0,0,77,79,5,91,0,0,78,77,1,0,0,0,78,79,1,0,0,0,79,80,1,0,
        0,0,80,81,5,0,0,1,81,1,1,0,0,0,82,84,5,4,0,0,83,85,5,16,0,0,84,83,
        1,0,0,0,84,85,1,0,0,0,85,87,1,0,0,0,86,88,3,64,32,0,87,86,1,0,0,
        0,87,88,1,0,0,0,88,89,1,0,0,0,89,94,3,12,6,0,90,91,5,82,0,0,91,93,
        3,12,6,0,92,90,1,0,0,0,93,96,1,0,0,0,94,92,1,0,0,0,94,95,1,0,0,0,
        95,3,1,0,0,0,96,94,1,0,0,0,97,98,5,6,0,0,98,99,3,14,7,0,99,5,1,0,
        0,0,100,101,5,7,0,0,101,102,3,16,8,0,102,7,1,0,0,0,103,104,5,8,0,
        0,104,105,5,9,0,0,105,110,3,18,9,0,106,107,5,82,0,0,107,109,3,18,
        9,0,108,106,1,0,0,0,109,112,1,0,0,0,110,108,1,0,0,0,110,111,1,0,
        0,0,111,9,1,0,0,0,112,110,1,0,0,0,113,114,5,14,0,0,114,117,5,65,
        0,0,115,116,5,15,0,0,116,118,5,65,0,0,117,115,1,0,0,0,117,118,1,
        0,0,0,118,11,1,0,0,0,119,122,3,20,10,0,120,121,5,5,0,0,121,123,5,
        61,0,0,122,120,1,0,0,0,122,123,1,0,0,0,123,13,1,0,0,0,124,125,3,
        22,11,0,125,15,1,0,0,0,126,127,6,8,-1,0,127,135,3,24,12,0,128,129,
        5,27,0,0,129,135,3,16,8,4,130,131,5,80,0,0,131,132,3,16,8,0,132,
        133,5,81,0,0,133,135,1,0,0,0,134,126,1,0,0,0,134,128,1,0,0,0,134,
        130,1,0,0,0,135,144,1,0,0,0,136,137,10,3,0,0,137,138,5,25,0,0,138,
        143,3,16,8,4,139,140,10,2,0,0,140,141,5,26,0,0,141,143,3,16,8,3,
        142,136,1,0,0,0,142,139,1,0,0,0,143,146,1,0,0,0,144,142,1,0,0,0,
        144,145,1,0,0,0,145,17,1,0,0,0,146,144,1,0,0,0,147,149,3,30,15,0,
        148,150,7,0,0,0,149,148,1,0,0,0,149,150,1,0,0,0,150,19,1,0,0,0,151,
        156,3,30,15,0,152,156,3,54,27,0,153,156,3,60,30,0,154,156,3,58,29,
        0,155,151,1,0,0,0,155,152,1,0,0,0,155,153,1,0,0,0,155,154,1,0,0,
        0,156,21,1,0,0,0,157,158,6,11,-1,0,158,164,3,26,13,0,159,161,5,27,
        0,0,160,159,1,0,0,0,160,161,1,0,0,0,161,162,1,0,0,0,162,163,5,24,
        0,0,163,165,3,22,11,0,164,160,1,0,0,0,164,165,1,0,0,0,165,171,1,
        0,0,0,166,167,5,80,0,0,167,168,3,22,11,0,168,169,5,81,0,0,169,171,
        1,0,0,0,170,157,1,0,0,0,170,166,1,0,0,0,171,180,1,0,0,0,172,173,
        10,3,0,0,173,174,5,25,0,0,174,179,3,22,11,4,175,176,10,2,0,0,176,
        177,5,26,0,0,177,179,3,22,11,3,178,172,1,0,0,0,178,175,1,0,0,0,179,
        182,1,0,0,0,180,178,1,0,0,0,180,181,1,0,0,0,181,23,1,0,0,0,182,180,
        1,0,0,0,183,184,5,28,0,0,184,206,3,30,15,0,185,186,3,30,15,0,186,
        187,5,29,0,0,187,188,3,28,14,0,188,206,1,0,0,0,189,190,3,58,29,0,
        190,191,5,29,0,0,191,192,3,28,14,0,192,206,1,0,0,0,193,194,3,30,
        15,0,194,195,5,30,0,0,195,196,3,48,24,0,196,206,1,0,0,0,197,198,
        3,30,15,0,198,199,5,31,0,0,199,200,3,50,25,0,200,206,1,0,0,0,201,
        202,5,80,0,0,202,203,3,24,12,0,203,204,5,81,0,0,204,206,1,0,0,0,
        205,183,1,0,0,0,205,185,1,0,0,0,205,189,1,0,0,0,205,193,1,0,0,0,
        205,197,1,0,0,0,205,201,1,0,0,0,206,25,1,0,0,0,207,209,5,61,0,0,
        208,210,5,61,0,0,209,208,1,0,0,0,209,210,1,0,0,0,210,212,1,0,0,0,
        211,213,3,32,16,0,212,211,1,0,0,0,212,213,1,0,0,0,213,225,1,0,0,
        0,214,216,5,17,0,0,215,217,5,61,0,0,216,215,1,0,0,0,216,217,1,0,
        0,0,217,222,1,0,0,0,218,219,5,87,0,0,219,220,3,40,20,0,220,221,5,
        88,0,0,221,223,1,0,0,0,222,218,1,0,0,0,222,223,1,0,0,0,223,225,1,
        0,0,0,224,207,1,0,0,0,224,214,1,0,0,0,225,27,1,0,0,0,226,231,3,54,
        27,0,227,231,5,56,0,0,228,231,3,30,15,0,229,231,3,58,29,0,230,226,
        1,0,0,0,230,227,1,0,0,0,230,228,1,0,0,0,230,229,1,0,0,0,231,29,1,
        0,0,0,232,234,5,61,0,0,233,235,3,32,16,0,234,233,1,0,0,0,234,235,
        1,0,0,0,235,238,1,0,0,0,236,237,5,83,0,0,237,239,3,44,22,0,238,236,
        1,0,0,0,238,239,1,0,0,0,239,31,1,0,0,0,240,244,5,87,0,0,241,245,
        3,34,17,0,242,245,3,36,18,0,243,245,3,38,19,0,244,241,1,0,0,0,244,
        242,1,0,0,0,244,243,1,0,0,0,245,246,1,0,0,0,246,247,5,88,0,0,247,
        33,1,0,0,0,248,249,3,44,22,0,249,250,5,29,0,0,250,251,3,42,21,0,
        251,35,1,0,0,0,252,253,7,1,0,0,253,37,1,0,0,0,254,255,6,19,-1,0,
        255,258,7,2,0,0,256,257,5,82,0,0,257,259,7,3,0,0,258,256,1,0,0,0,
        258,259,1,0,0,0,259,275,1,0,0,0,260,263,5,60,0,0,261,262,5,82,0,
        0,262,264,7,3,0,0,263,261,1,0,0,0,263,264,1,0,0,0,264,275,1,0,0,
        0,265,275,5,56,0,0,266,267,3,44,22,0,267,268,5,29,0,0,268,269,3,
        42,21,0,269,275,1,0,0,0,270,271,3,44,22,0,271,272,5,31,0,0,272,273,
        5,59,0,0,273,275,1,0,0,0,274,254,1,0,0,0,274,260,1,0,0,0,274,265,
        1,0,0,0,274,266,1,0,0,0,274,270,1,0,0,0,275,284,1,0,0,0,276,277,
        10,2,0,0,277,278,5,25,0,0,278,283,3,38,19,3,279,280,10,1,0,0,280,
        281,5,26,0,0,281,283,3,38,19,2,282,276,1,0,0,0,282,279,1,0,0,0,283,
        286,1,0,0,0,284,282,1,0,0,0,284,285,1,0,0,0,285,39,1,0,0,0,286,284,
        1,0,0,0,287,291,5,18,0,0,288,291,5,19,0,0,289,291,3,34,17,0,290,
        287,1,0,0,0,290,288,1,0,0,0,290,289,1,0,0,0,291,41,1,0,0,0,292,298,
        3,54,27,0,293,298,3,44,22,0,294,298,5,56,0,0,295,298,5,57,0,0,296,
        298,5,58,0,0,297,292,1,0,0,0,297,293,1,0,0,0,297,294,1,0,0,0,297,
        295,1,0,0,0,297,296,1,0,0,0,298,43,1,0,0,0,299,304,3,46,23,0,300,
        301,5,83,0,0,301,303,3,46,23,0,302,300,1,0,0,0,303,306,1,0,0,0,304,
        302,1,0,0,0,304,305,1,0,0,0,305,45,1,0,0,0,306,304,1,0,0,0,307,309,
        5,61,0,0,308,310,3,32,16,0,309,308,1,0,0,0,309,310,1,0,0,0,310,47,
        1,0,0,0,311,312,7,4,0,0,312,49,1,0,0,0,313,314,5,89,0,0,314,319,
        3,52,26,0,315,316,5,82,0,0,316,318,3,52,26,0,317,315,1,0,0,0,318,
        321,1,0,0,0,319,317,1,0,0,0,319,320,1,0,0,0,320,322,1,0,0,0,321,
        319,1,0,0,0,322,323,5,90,0,0,323,329,1,0,0,0,324,329,3,62,31,0,325,
        326,5,89,0,0,326,327,5,63,0,0,327,329,5,90,0,0,328,313,1,0,0,0,328,
        324,1,0,0,0,328,325,1,0,0,0,329,51,1,0,0,0,330,334,3,54,27,0,331,
        334,5,56,0,0,332,334,3,62,31,0,333,330,1,0,0,0,333,331,1,0,0,0,333,
        332,1,0,0,0,334,53,1,0,0,0,335,343,5,72,0,0,336,343,3,56,28,0,337,
        343,5,69,0,0,338,343,5,70,0,0,339,343,5,71,0,0,340,343,5,64,0,0,
        341,343,5,20,0,0,342,335,1,0,0,0,342,336,1,0,0,0,342,337,1,0,0,0,
        342,338,1,0,0,0,342,339,1,0,0,0,342,340,1,0,0,0,342,341,1,0,0,0,
        343,55,1,0,0,0,344,351,5,65,0,0,345,351,5,66,0,0,346,351,5,67,0,
        0,347,351,5,68,0,0,348,349,5,86,0,0,349,351,3,56,28,0,350,344,1,
        0,0,0,350,345,1,0,0,0,350,346,1,0,0,0,350,347,1,0,0,0,350,348,1,
        0,0,0,351,57,1,0,0,0,352,367,3,62,31,0,353,354,7,5,0,0,354,363,5,
        80,0,0,355,360,3,28,14,0,356,357,5,82,0,0,357,359,3,28,14,0,358,
        356,1,0,0,0,359,362,1,0,0,0,360,358,1,0,0,0,360,361,1,0,0,0,361,
        364,1,0,0,0,362,360,1,0,0,0,363,355,1,0,0,0,363,364,1,0,0,0,364,
        365,1,0,0,0,365,367,5,81,0,0,366,352,1,0,0,0,366,353,1,0,0,0,367,
        59,1,0,0,0,368,369,5,50,0,0,369,375,5,80,0,0,370,372,5,16,0,0,371,
        370,1,0,0,0,371,372,1,0,0,0,372,373,1,0,0,0,373,376,3,30,15,0,374,
        376,5,84,0,0,375,371,1,0,0,0,375,374,1,0,0,0,376,377,1,0,0,0,377,
        384,5,81,0,0,378,379,7,6,0,0,379,380,5,80,0,0,380,381,3,30,15,0,
        381,382,5,81,0,0,382,384,1,0,0,0,383,368,1,0,0,0,383,378,1,0,0,0,
        384,61,1,0,0,0,385,386,5,55,0,0,386,387,5,80,0,0,387,388,5,72,0,
        0,388,389,5,82,0,0,389,390,5,72,0,0,390,391,5,82,0,0,391,392,5,72,
        0,0,392,393,5,81,0,0,393,63,1,0,0,0,394,395,5,21,0,0,395,397,5,65,
        0,0,396,398,7,7,0,0,397,396,1,0,0,0,397,398,1,0,0,0,398,65,1,0,0,
        0,51,69,72,75,78,84,87,94,110,117,122,134,142,144,149,155,160,164,
        170,178,180,205,209,212,216,222,224,230,234,238,244,258,263,274,
        282,284,290,297,304,309,319,328,333,342,350,360,363,366,371,375,
        383,397
    ]

class AqlParser ( Parser ):

    grammarFileName = "AqlParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "';'", "'<'", "'>'", "'<='", "'>='", "'!='", 
                     "'='", "'('", "')'", "','", "'/'", "'*'", "'+'", "'-'", 
                     "'['", "']'", "'{'", "'}'", "'--'" ]

    symbolicNames = [ "<INVALID>", "WS", "UNICODE_BOM", "COMMENT", "SELECT", 
                      "AS", "FROM", "WHERE", "ORDER", "BY", "DESC", "DESCENDING", 
                      "ASC", "ASCENDING", "LIMIT", "OFFSET", "DISTINCT", 
                      "VERSION", "LATEST_VERSION", "ALL_VERSIONS", "NULL", 
                      "TOP", "FORWARD", "BACKWARD", "CONTAINS", "AND", "OR", 
                      "NOT", "EXISTS", "COMPARISON_OPERATOR", "LIKE", "MATCHES", 
                      "STRING_FUNCTION_ID", "NUMERIC_FUNCTION_ID", "DATE_TIME_FUNCTION_ID", 
                      "LENGTH", "POSITION", "SUBSTRING", "CONCAT", "CONCAT_WS", 
                      "ABS", "MOD", "CEIL", "FLOOR", "ROUND", "CURRENT_DATE", 
                      "CURRENT_TIME", "CURRENT_DATE_TIME", "NOW", "CURRENT_TIMEZONE", 
                      "COUNT", "MIN", "MAX", "SUM", "AVG", "TERMINOLOGY", 
                      "PARAMETER", "ID_CODE", "AT_CODE", "CONTAINED_REGEX", 
                      "ARCHETYPE_HRID", "IDENTIFIER", "TERM_CODE", "URI", 
                      "BOOLEAN", "INTEGER", "REAL", "SCI_INTEGER", "SCI_REAL", 
                      "DATE", "TIME", "DATETIME", "STRING", "SYM_SEMICOLON", 
                      "SYM_LT", "SYM_GT", "SYM_LE", "SYM_GE", "SYM_NE", 
                      "SYM_EQ", "SYM_LEFT_PAREN", "SYM_RIGHT_PAREN", "SYM_COMMA", 
                      "SYM_SLASH", "SYM_ASTERISK", "SYM_PLUS", "SYM_MINUS", 
                      "SYM_LEFT_BRACKET", "SYM_RIGHT_BRACKET", "SYM_LEFT_CURLY", 
                      "SYM_RIGHT_CURLY", "SYM_DOUBLE_DASH" ]

    RULE_selectQuery = 0
    RULE_selectClause = 1
    RULE_fromClause = 2
    RULE_whereClause = 3
    RULE_orderByClause = 4
    RULE_limitClause = 5
    RULE_selectExpr = 6
    RULE_fromExpr = 7
    RULE_whereExpr = 8
    RULE_orderByExpr = 9
    RULE_columnExpr = 10
    RULE_containsExpr = 11
    RULE_identifiedExpr = 12
    RULE_classExprOperand = 13
    RULE_terminal = 14
    RULE_identifiedPath = 15
    RULE_pathPredicate = 16
    RULE_standardPredicate = 17
    RULE_archetypePredicate = 18
    RULE_nodePredicate = 19
    RULE_versionPredicate = 20
    RULE_pathPredicateOperand = 21
    RULE_objectPath = 22
    RULE_pathPart = 23
    RULE_likeOperand = 24
    RULE_matchesOperand = 25
    RULE_valueListItem = 26
    RULE_primitive = 27
    RULE_numericPrimitive = 28
    RULE_functionCall = 29
    RULE_aggregateFunctionCall = 30
    RULE_terminologyFunction = 31
    RULE_top = 32

    ruleNames =  [ "selectQuery", "selectClause", "fromClause", "whereClause", 
                   "orderByClause", "limitClause", "selectExpr", "fromExpr", 
                   "whereExpr", "orderByExpr", "columnExpr", "containsExpr", 
                   "identifiedExpr", "classExprOperand", "terminal", "identifiedPath", 
                   "pathPredicate", "standardPredicate", "archetypePredicate", 
                   "nodePredicate", "versionPredicate", "pathPredicateOperand", 
                   "objectPath", "pathPart", "likeOperand", "matchesOperand", 
                   "valueListItem", "primitive", "numericPrimitive", "functionCall", 
                   "aggregateFunctionCall", "terminologyFunction", "top" ]

    EOF = Token.EOF
    WS=1
    UNICODE_BOM=2
    COMMENT=3
    SELECT=4
    AS=5
    FROM=6
    WHERE=7
    ORDER=8
    BY=9
    DESC=10
    DESCENDING=11
    ASC=12
    ASCENDING=13
    LIMIT=14
    OFFSET=15
    DISTINCT=16
    VERSION=17
    LATEST_VERSION=18
    ALL_VERSIONS=19
    NULL=20
    TOP=21
    FORWARD=22
    BACKWARD=23
    CONTAINS=24
    AND=25
    OR=26
    NOT=27
    EXISTS=28
    COMPARISON_OPERATOR=29
    LIKE=30
    MATCHES=31
    STRING_FUNCTION_ID=32
    NUMERIC_FUNCTION_ID=33
    DATE_TIME_FUNCTION_ID=34
    LENGTH=35
    POSITION=36
    SUBSTRING=37
    CONCAT=38
    CONCAT_WS=39
    ABS=40
    MOD=41
    CEIL=42
    FLOOR=43
    ROUND=44
    CURRENT_DATE=45
    CURRENT_TIME=46
    CURRENT_DATE_TIME=47
    NOW=48
    CURRENT_TIMEZONE=49
    COUNT=50
    MIN=51
    MAX=52
    SUM=53
    AVG=54
    TERMINOLOGY=55
    PARAMETER=56
    ID_CODE=57
    AT_CODE=58
    CONTAINED_REGEX=59
    ARCHETYPE_HRID=60
    IDENTIFIER=61
    TERM_CODE=62
    URI=63
    BOOLEAN=64
    INTEGER=65
    REAL=66
    SCI_INTEGER=67
    SCI_REAL=68
    DATE=69
    TIME=70
    DATETIME=71
    STRING=72
    SYM_SEMICOLON=73
    SYM_LT=74
    SYM_GT=75
    SYM_LE=76
    SYM_GE=77
    SYM_NE=78
    SYM_EQ=79
    SYM_LEFT_PAREN=80
    SYM_RIGHT_PAREN=81
    SYM_COMMA=82
    SYM_SLASH=83
    SYM_ASTERISK=84
    SYM_PLUS=85
    SYM_MINUS=86
    SYM_LEFT_BRACKET=87
    SYM_RIGHT_BRACKET=88
    SYM_LEFT_CURLY=89
    SYM_RIGHT_CURLY=90
    SYM_DOUBLE_DASH=91

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SelectQueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selectClause(self):
            return self.getTypedRuleContext(AqlParser.SelectClauseContext,0)


        def fromClause(self):
            return self.getTypedRuleContext(AqlParser.FromClauseContext,0)


        def EOF(self):
            return self.getToken(AqlParser.EOF, 0)

        def whereClause(self):
            return self.getTypedRuleContext(AqlParser.WhereClauseContext,0)


        def orderByClause(self):
            return self.getTypedRuleContext(AqlParser.OrderByClauseContext,0)


        def limitClause(self):
            return self.getTypedRuleContext(AqlParser.LimitClauseContext,0)


        def SYM_DOUBLE_DASH(self):
            return self.getToken(AqlParser.SYM_DOUBLE_DASH, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_selectQuery

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectQuery" ):
                listener.enterSelectQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectQuery" ):
                listener.exitSelectQuery(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectQuery" ):
                return visitor.visitSelectQuery(self)
            else:
                return visitor.visitChildren(self)




    def selectQuery(self):

        localctx = AqlParser.SelectQueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_selectQuery)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.selectClause()
            self.state = 67
            self.fromClause()
            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 68
                self.whereClause()


            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 71
                self.orderByClause()


            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 74
                self.limitClause()


            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==91:
                self.state = 77
                self.match(AqlParser.SYM_DOUBLE_DASH)


            self.state = 80
            self.match(AqlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SELECT(self):
            return self.getToken(AqlParser.SELECT, 0)

        def selectExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.SelectExprContext)
            else:
                return self.getTypedRuleContext(AqlParser.SelectExprContext,i)


        def DISTINCT(self):
            return self.getToken(AqlParser.DISTINCT, 0)

        def top(self):
            return self.getTypedRuleContext(AqlParser.TopContext,0)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.SYM_COMMA)
            else:
                return self.getToken(AqlParser.SYM_COMMA, i)

        def getRuleIndex(self):
            return AqlParser.RULE_selectClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectClause" ):
                listener.enterSelectClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectClause" ):
                listener.exitSelectClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectClause" ):
                return visitor.visitSelectClause(self)
            else:
                return visitor.visitChildren(self)




    def selectClause(self):

        localctx = AqlParser.SelectClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_selectClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(AqlParser.SELECT)
            self.state = 84
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 83
                self.match(AqlParser.DISTINCT)


            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 86
                self.top()


            self.state = 89
            self.selectExpr()
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==82:
                self.state = 90
                self.match(AqlParser.SYM_COMMA)
                self.state = 91
                self.selectExpr()
                self.state = 96
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FromClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(AqlParser.FROM, 0)

        def fromExpr(self):
            return self.getTypedRuleContext(AqlParser.FromExprContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_fromClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFromClause" ):
                listener.enterFromClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFromClause" ):
                listener.exitFromClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFromClause" ):
                return visitor.visitFromClause(self)
            else:
                return visitor.visitChildren(self)




    def fromClause(self):

        localctx = AqlParser.FromClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_fromClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(AqlParser.FROM)
            self.state = 98
            self.fromExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHERE(self):
            return self.getToken(AqlParser.WHERE, 0)

        def whereExpr(self):
            return self.getTypedRuleContext(AqlParser.WhereExprContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_whereClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhereClause" ):
                listener.enterWhereClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhereClause" ):
                listener.exitWhereClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereClause" ):
                return visitor.visitWhereClause(self)
            else:
                return visitor.visitChildren(self)




    def whereClause(self):

        localctx = AqlParser.WhereClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_whereClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(AqlParser.WHERE)
            self.state = 101
            self.whereExpr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderByClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ORDER(self):
            return self.getToken(AqlParser.ORDER, 0)

        def BY(self):
            return self.getToken(AqlParser.BY, 0)

        def orderByExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.OrderByExprContext)
            else:
                return self.getTypedRuleContext(AqlParser.OrderByExprContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.SYM_COMMA)
            else:
                return self.getToken(AqlParser.SYM_COMMA, i)

        def getRuleIndex(self):
            return AqlParser.RULE_orderByClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderByClause" ):
                listener.enterOrderByClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderByClause" ):
                listener.exitOrderByClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderByClause" ):
                return visitor.visitOrderByClause(self)
            else:
                return visitor.visitChildren(self)




    def orderByClause(self):

        localctx = AqlParser.OrderByClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_orderByClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.match(AqlParser.ORDER)
            self.state = 104
            self.match(AqlParser.BY)
            self.state = 105
            self.orderByExpr()
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==82:
                self.state = 106
                self.match(AqlParser.SYM_COMMA)
                self.state = 107
                self.orderByExpr()
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LimitClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.limit = None # Token
            self.offset = None # Token

        def LIMIT(self):
            return self.getToken(AqlParser.LIMIT, 0)

        def INTEGER(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.INTEGER)
            else:
                return self.getToken(AqlParser.INTEGER, i)

        def OFFSET(self):
            return self.getToken(AqlParser.OFFSET, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_limitClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLimitClause" ):
                listener.enterLimitClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLimitClause" ):
                listener.exitLimitClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLimitClause" ):
                return visitor.visitLimitClause(self)
            else:
                return visitor.visitChildren(self)




    def limitClause(self):

        localctx = AqlParser.LimitClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_limitClause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(AqlParser.LIMIT)
            self.state = 114
            localctx.limit = self.match(AqlParser.INTEGER)
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==15:
                self.state = 115
                self.match(AqlParser.OFFSET)
                self.state = 116
                localctx.offset = self.match(AqlParser.INTEGER)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.aliasName = None # Token

        def columnExpr(self):
            return self.getTypedRuleContext(AqlParser.ColumnExprContext,0)


        def AS(self):
            return self.getToken(AqlParser.AS, 0)

        def IDENTIFIER(self):
            return self.getToken(AqlParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_selectExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectExpr" ):
                listener.enterSelectExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectExpr" ):
                listener.exitSelectExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectExpr" ):
                return visitor.visitSelectExpr(self)
            else:
                return visitor.visitChildren(self)




    def selectExpr(self):

        localctx = AqlParser.SelectExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_selectExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.columnExpr()
            self.state = 122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 120
                self.match(AqlParser.AS)
                self.state = 121
                localctx.aliasName = self.match(AqlParser.IDENTIFIER)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FromExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def containsExpr(self):
            return self.getTypedRuleContext(AqlParser.ContainsExprContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_fromExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFromExpr" ):
                listener.enterFromExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFromExpr" ):
                listener.exitFromExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFromExpr" ):
                return visitor.visitFromExpr(self)
            else:
                return visitor.visitChildren(self)




    def fromExpr(self):

        localctx = AqlParser.FromExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_fromExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.containsExpr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifiedExpr(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedExprContext,0)


        def NOT(self):
            return self.getToken(AqlParser.NOT, 0)

        def whereExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.WhereExprContext)
            else:
                return self.getTypedRuleContext(AqlParser.WhereExprContext,i)


        def SYM_LEFT_PAREN(self):
            return self.getToken(AqlParser.SYM_LEFT_PAREN, 0)

        def SYM_RIGHT_PAREN(self):
            return self.getToken(AqlParser.SYM_RIGHT_PAREN, 0)

        def AND(self):
            return self.getToken(AqlParser.AND, 0)

        def OR(self):
            return self.getToken(AqlParser.OR, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_whereExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhereExpr" ):
                listener.enterWhereExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhereExpr" ):
                listener.exitWhereExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereExpr" ):
                return visitor.visitWhereExpr(self)
            else:
                return visitor.visitChildren(self)



    def whereExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = AqlParser.WhereExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_whereExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 127
                self.identifiedExpr()
                pass

            elif la_ == 2:
                self.state = 128
                self.match(AqlParser.NOT)
                self.state = 129
                self.whereExpr(4)
                pass

            elif la_ == 3:
                self.state = 130
                self.match(AqlParser.SYM_LEFT_PAREN)
                self.state = 131
                self.whereExpr(0)
                self.state = 132
                self.match(AqlParser.SYM_RIGHT_PAREN)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 144
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 142
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
                    if la_ == 1:
                        localctx = AqlParser.WhereExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_whereExpr)
                        self.state = 136
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 137
                        self.match(AqlParser.AND)
                        self.state = 138
                        self.whereExpr(4)
                        pass

                    elif la_ == 2:
                        localctx = AqlParser.WhereExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_whereExpr)
                        self.state = 139
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 140
                        self.match(AqlParser.OR)
                        self.state = 141
                        self.whereExpr(3)
                        pass

             
                self.state = 146
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class OrderByExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.order = None # Token

        def identifiedPath(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedPathContext,0)


        def DESCENDING(self):
            return self.getToken(AqlParser.DESCENDING, 0)

        def DESC(self):
            return self.getToken(AqlParser.DESC, 0)

        def ASCENDING(self):
            return self.getToken(AqlParser.ASCENDING, 0)

        def ASC(self):
            return self.getToken(AqlParser.ASC, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_orderByExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderByExpr" ):
                listener.enterOrderByExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderByExpr" ):
                listener.exitOrderByExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderByExpr" ):
                return visitor.visitOrderByExpr(self)
            else:
                return visitor.visitChildren(self)




    def orderByExpr(self):

        localctx = AqlParser.OrderByExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_orderByExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.identifiedPath()
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 15360) != 0):
                self.state = 148
                localctx.order = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 15360) != 0)):
                    localctx.order = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ColumnExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifiedPath(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedPathContext,0)


        def primitive(self):
            return self.getTypedRuleContext(AqlParser.PrimitiveContext,0)


        def aggregateFunctionCall(self):
            return self.getTypedRuleContext(AqlParser.AggregateFunctionCallContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(AqlParser.FunctionCallContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_columnExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterColumnExpr" ):
                listener.enterColumnExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitColumnExpr" ):
                listener.exitColumnExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColumnExpr" ):
                return visitor.visitColumnExpr(self)
            else:
                return visitor.visitChildren(self)




    def columnExpr(self):

        localctx = AqlParser.ColumnExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_columnExpr)
        try:
            self.state = 155
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 151
                self.identifiedPath()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 152
                self.primitive()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 153
                self.aggregateFunctionCall()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 154
                self.functionCall()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContainsExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classExprOperand(self):
            return self.getTypedRuleContext(AqlParser.ClassExprOperandContext,0)


        def CONTAINS(self):
            return self.getToken(AqlParser.CONTAINS, 0)

        def containsExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.ContainsExprContext)
            else:
                return self.getTypedRuleContext(AqlParser.ContainsExprContext,i)


        def NOT(self):
            return self.getToken(AqlParser.NOT, 0)

        def SYM_LEFT_PAREN(self):
            return self.getToken(AqlParser.SYM_LEFT_PAREN, 0)

        def SYM_RIGHT_PAREN(self):
            return self.getToken(AqlParser.SYM_RIGHT_PAREN, 0)

        def AND(self):
            return self.getToken(AqlParser.AND, 0)

        def OR(self):
            return self.getToken(AqlParser.OR, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_containsExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContainsExpr" ):
                listener.enterContainsExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContainsExpr" ):
                listener.exitContainsExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContainsExpr" ):
                return visitor.visitContainsExpr(self)
            else:
                return visitor.visitChildren(self)



    def containsExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = AqlParser.ContainsExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_containsExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17, 61]:
                self.state = 158
                self.classExprOperand()
                self.state = 164
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                if la_ == 1:
                    self.state = 160
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==27:
                        self.state = 159
                        self.match(AqlParser.NOT)


                    self.state = 162
                    self.match(AqlParser.CONTAINS)
                    self.state = 163
                    self.containsExpr(0)


                pass
            elif token in [80]:
                self.state = 166
                self.match(AqlParser.SYM_LEFT_PAREN)
                self.state = 167
                self.containsExpr(0)
                self.state = 168
                self.match(AqlParser.SYM_RIGHT_PAREN)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 180
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 178
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
                    if la_ == 1:
                        localctx = AqlParser.ContainsExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_containsExpr)
                        self.state = 172
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 173
                        self.match(AqlParser.AND)
                        self.state = 174
                        self.containsExpr(4)
                        pass

                    elif la_ == 2:
                        localctx = AqlParser.ContainsExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_containsExpr)
                        self.state = 175
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 176
                        self.match(AqlParser.OR)
                        self.state = 177
                        self.containsExpr(3)
                        pass

             
                self.state = 182
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class IdentifiedExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXISTS(self):
            return self.getToken(AqlParser.EXISTS, 0)

        def identifiedPath(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedPathContext,0)


        def COMPARISON_OPERATOR(self):
            return self.getToken(AqlParser.COMPARISON_OPERATOR, 0)

        def terminal(self):
            return self.getTypedRuleContext(AqlParser.TerminalContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(AqlParser.FunctionCallContext,0)


        def LIKE(self):
            return self.getToken(AqlParser.LIKE, 0)

        def likeOperand(self):
            return self.getTypedRuleContext(AqlParser.LikeOperandContext,0)


        def MATCHES(self):
            return self.getToken(AqlParser.MATCHES, 0)

        def matchesOperand(self):
            return self.getTypedRuleContext(AqlParser.MatchesOperandContext,0)


        def SYM_LEFT_PAREN(self):
            return self.getToken(AqlParser.SYM_LEFT_PAREN, 0)

        def identifiedExpr(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedExprContext,0)


        def SYM_RIGHT_PAREN(self):
            return self.getToken(AqlParser.SYM_RIGHT_PAREN, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_identifiedExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifiedExpr" ):
                listener.enterIdentifiedExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifiedExpr" ):
                listener.exitIdentifiedExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifiedExpr" ):
                return visitor.visitIdentifiedExpr(self)
            else:
                return visitor.visitChildren(self)




    def identifiedExpr(self):

        localctx = AqlParser.IdentifiedExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_identifiedExpr)
        try:
            self.state = 205
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 183
                self.match(AqlParser.EXISTS)
                self.state = 184
                self.identifiedPath()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 185
                self.identifiedPath()
                self.state = 186
                self.match(AqlParser.COMPARISON_OPERATOR)
                self.state = 187
                self.terminal()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 189
                self.functionCall()
                self.state = 190
                self.match(AqlParser.COMPARISON_OPERATOR)
                self.state = 191
                self.terminal()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 193
                self.identifiedPath()
                self.state = 194
                self.match(AqlParser.LIKE)
                self.state = 195
                self.likeOperand()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 197
                self.identifiedPath()
                self.state = 198
                self.match(AqlParser.MATCHES)
                self.state = 199
                self.matchesOperand()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 201
                self.match(AqlParser.SYM_LEFT_PAREN)
                self.state = 202
                self.identifiedExpr()
                self.state = 203
                self.match(AqlParser.SYM_RIGHT_PAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassExprOperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return AqlParser.RULE_classExprOperand

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ClassExpressionContext(ClassExprOperandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AqlParser.ClassExprOperandContext
            super().__init__(parser)
            self.variable = None # Token
            self.copyFrom(ctx)

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.IDENTIFIER)
            else:
                return self.getToken(AqlParser.IDENTIFIER, i)
        def pathPredicate(self):
            return self.getTypedRuleContext(AqlParser.PathPredicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassExpression" ):
                listener.enterClassExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassExpression" ):
                listener.exitClassExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassExpression" ):
                return visitor.visitClassExpression(self)
            else:
                return visitor.visitChildren(self)


    class VersionClassExprContext(ClassExprOperandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a AqlParser.ClassExprOperandContext
            super().__init__(parser)
            self.variable = None # Token
            self.copyFrom(ctx)

        def VERSION(self):
            return self.getToken(AqlParser.VERSION, 0)
        def SYM_LEFT_BRACKET(self):
            return self.getToken(AqlParser.SYM_LEFT_BRACKET, 0)
        def versionPredicate(self):
            return self.getTypedRuleContext(AqlParser.VersionPredicateContext,0)

        def SYM_RIGHT_BRACKET(self):
            return self.getToken(AqlParser.SYM_RIGHT_BRACKET, 0)
        def IDENTIFIER(self):
            return self.getToken(AqlParser.IDENTIFIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionClassExpr" ):
                listener.enterVersionClassExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionClassExpr" ):
                listener.exitVersionClassExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionClassExpr" ):
                return visitor.visitVersionClassExpr(self)
            else:
                return visitor.visitChildren(self)



    def classExprOperand(self):

        localctx = AqlParser.ClassExprOperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_classExprOperand)
        try:
            self.state = 224
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [61]:
                localctx = AqlParser.ClassExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 207
                self.match(AqlParser.IDENTIFIER)
                self.state = 209
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
                if la_ == 1:
                    self.state = 208
                    localctx.variable = self.match(AqlParser.IDENTIFIER)


                self.state = 212
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
                if la_ == 1:
                    self.state = 211
                    self.pathPredicate()


                pass
            elif token in [17]:
                localctx = AqlParser.VersionClassExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 214
                self.match(AqlParser.VERSION)
                self.state = 216
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
                if la_ == 1:
                    self.state = 215
                    localctx.variable = self.match(AqlParser.IDENTIFIER)


                self.state = 222
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
                if la_ == 1:
                    self.state = 218
                    self.match(AqlParser.SYM_LEFT_BRACKET)
                    self.state = 219
                    self.versionPredicate()
                    self.state = 220
                    self.match(AqlParser.SYM_RIGHT_BRACKET)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TerminalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive(self):
            return self.getTypedRuleContext(AqlParser.PrimitiveContext,0)


        def PARAMETER(self):
            return self.getToken(AqlParser.PARAMETER, 0)

        def identifiedPath(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedPathContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(AqlParser.FunctionCallContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_terminal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminal" ):
                listener.enterTerminal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminal" ):
                listener.exitTerminal(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerminal" ):
                return visitor.visitTerminal(self)
            else:
                return visitor.visitChildren(self)




    def terminal(self):

        localctx = AqlParser.TerminalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_terminal)
        try:
            self.state = 230
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 226
                self.primitive()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.match(AqlParser.PARAMETER)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 228
                self.identifiedPath()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 229
                self.functionCall()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifiedPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(AqlParser.IDENTIFIER, 0)

        def pathPredicate(self):
            return self.getTypedRuleContext(AqlParser.PathPredicateContext,0)


        def SYM_SLASH(self):
            return self.getToken(AqlParser.SYM_SLASH, 0)

        def objectPath(self):
            return self.getTypedRuleContext(AqlParser.ObjectPathContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_identifiedPath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifiedPath" ):
                listener.enterIdentifiedPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifiedPath" ):
                listener.exitIdentifiedPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifiedPath" ):
                return visitor.visitIdentifiedPath(self)
            else:
                return visitor.visitChildren(self)




    def identifiedPath(self):

        localctx = AqlParser.IdentifiedPathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_identifiedPath)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self.match(AqlParser.IDENTIFIER)
            self.state = 234
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
            if la_ == 1:
                self.state = 233
                self.pathPredicate()


            self.state = 238
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.state = 236
                self.match(AqlParser.SYM_SLASH)
                self.state = 237
                self.objectPath()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathPredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LEFT_BRACKET(self):
            return self.getToken(AqlParser.SYM_LEFT_BRACKET, 0)

        def SYM_RIGHT_BRACKET(self):
            return self.getToken(AqlParser.SYM_RIGHT_BRACKET, 0)

        def standardPredicate(self):
            return self.getTypedRuleContext(AqlParser.StandardPredicateContext,0)


        def archetypePredicate(self):
            return self.getTypedRuleContext(AqlParser.ArchetypePredicateContext,0)


        def nodePredicate(self):
            return self.getTypedRuleContext(AqlParser.NodePredicateContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_pathPredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathPredicate" ):
                listener.enterPathPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathPredicate" ):
                listener.exitPathPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathPredicate" ):
                return visitor.visitPathPredicate(self)
            else:
                return visitor.visitChildren(self)




    def pathPredicate(self):

        localctx = AqlParser.PathPredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_pathPredicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 240
            self.match(AqlParser.SYM_LEFT_BRACKET)
            self.state = 244
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                self.state = 241
                self.standardPredicate()
                pass

            elif la_ == 2:
                self.state = 242
                self.archetypePredicate()
                pass

            elif la_ == 3:
                self.state = 243
                self.nodePredicate(0)
                pass


            self.state = 246
            self.match(AqlParser.SYM_RIGHT_BRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StandardPredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def objectPath(self):
            return self.getTypedRuleContext(AqlParser.ObjectPathContext,0)


        def COMPARISON_OPERATOR(self):
            return self.getToken(AqlParser.COMPARISON_OPERATOR, 0)

        def pathPredicateOperand(self):
            return self.getTypedRuleContext(AqlParser.PathPredicateOperandContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_standardPredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStandardPredicate" ):
                listener.enterStandardPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStandardPredicate" ):
                listener.exitStandardPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStandardPredicate" ):
                return visitor.visitStandardPredicate(self)
            else:
                return visitor.visitChildren(self)




    def standardPredicate(self):

        localctx = AqlParser.StandardPredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_standardPredicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.objectPath()
            self.state = 249
            self.match(AqlParser.COMPARISON_OPERATOR)
            self.state = 250
            self.pathPredicateOperand()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArchetypePredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ARCHETYPE_HRID(self):
            return self.getToken(AqlParser.ARCHETYPE_HRID, 0)

        def PARAMETER(self):
            return self.getToken(AqlParser.PARAMETER, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_archetypePredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArchetypePredicate" ):
                listener.enterArchetypePredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArchetypePredicate" ):
                listener.exitArchetypePredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArchetypePredicate" ):
                return visitor.visitArchetypePredicate(self)
            else:
                return visitor.visitChildren(self)




    def archetypePredicate(self):

        localctx = AqlParser.ArchetypePredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_archetypePredicate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            _la = self._input.LA(1)
            if not(_la==56 or _la==60):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodePredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID_CODE(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.ID_CODE)
            else:
                return self.getToken(AqlParser.ID_CODE, i)

        def AT_CODE(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.AT_CODE)
            else:
                return self.getToken(AqlParser.AT_CODE, i)

        def SYM_COMMA(self):
            return self.getToken(AqlParser.SYM_COMMA, 0)

        def STRING(self):
            return self.getToken(AqlParser.STRING, 0)

        def PARAMETER(self):
            return self.getToken(AqlParser.PARAMETER, 0)

        def TERM_CODE(self):
            return self.getToken(AqlParser.TERM_CODE, 0)

        def ARCHETYPE_HRID(self):
            return self.getToken(AqlParser.ARCHETYPE_HRID, 0)

        def objectPath(self):
            return self.getTypedRuleContext(AqlParser.ObjectPathContext,0)


        def COMPARISON_OPERATOR(self):
            return self.getToken(AqlParser.COMPARISON_OPERATOR, 0)

        def pathPredicateOperand(self):
            return self.getTypedRuleContext(AqlParser.PathPredicateOperandContext,0)


        def MATCHES(self):
            return self.getToken(AqlParser.MATCHES, 0)

        def CONTAINED_REGEX(self):
            return self.getToken(AqlParser.CONTAINED_REGEX, 0)

        def nodePredicate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.NodePredicateContext)
            else:
                return self.getTypedRuleContext(AqlParser.NodePredicateContext,i)


        def AND(self):
            return self.getToken(AqlParser.AND, 0)

        def OR(self):
            return self.getToken(AqlParser.OR, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_nodePredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodePredicate" ):
                listener.enterNodePredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodePredicate" ):
                listener.exitNodePredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNodePredicate" ):
                return visitor.visitNodePredicate(self)
            else:
                return visitor.visitChildren(self)



    def nodePredicate(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = AqlParser.NodePredicateContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 38
        self.enterRecursionRule(localctx, 38, self.RULE_nodePredicate, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 274
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.state = 255
                _la = self._input.LA(1)
                if not(_la==57 or _la==58):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 258
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                if la_ == 1:
                    self.state = 256
                    self.match(AqlParser.SYM_COMMA)
                    self.state = 257
                    _la = self._input.LA(1)
                    if not(((((_la - 56)) & ~0x3f) == 0 and ((1 << (_la - 56)) & 65607) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                pass

            elif la_ == 2:
                self.state = 260
                self.match(AqlParser.ARCHETYPE_HRID)
                self.state = 263
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
                if la_ == 1:
                    self.state = 261
                    self.match(AqlParser.SYM_COMMA)
                    self.state = 262
                    _la = self._input.LA(1)
                    if not(((((_la - 56)) & ~0x3f) == 0 and ((1 << (_la - 56)) & 65607) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                pass

            elif la_ == 3:
                self.state = 265
                self.match(AqlParser.PARAMETER)
                pass

            elif la_ == 4:
                self.state = 266
                self.objectPath()
                self.state = 267
                self.match(AqlParser.COMPARISON_OPERATOR)
                self.state = 268
                self.pathPredicateOperand()
                pass

            elif la_ == 5:
                self.state = 270
                self.objectPath()
                self.state = 271
                self.match(AqlParser.MATCHES)
                self.state = 272
                self.match(AqlParser.CONTAINED_REGEX)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 284
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,34,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 282
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
                    if la_ == 1:
                        localctx = AqlParser.NodePredicateContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_nodePredicate)
                        self.state = 276
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 277
                        self.match(AqlParser.AND)
                        self.state = 278
                        self.nodePredicate(3)
                        pass

                    elif la_ == 2:
                        localctx = AqlParser.NodePredicateContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_nodePredicate)
                        self.state = 279
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 280
                        self.match(AqlParser.OR)
                        self.state = 281
                        self.nodePredicate(2)
                        pass

             
                self.state = 286
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,34,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class VersionPredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LATEST_VERSION(self):
            return self.getToken(AqlParser.LATEST_VERSION, 0)

        def ALL_VERSIONS(self):
            return self.getToken(AqlParser.ALL_VERSIONS, 0)

        def standardPredicate(self):
            return self.getTypedRuleContext(AqlParser.StandardPredicateContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_versionPredicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionPredicate" ):
                listener.enterVersionPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionPredicate" ):
                listener.exitVersionPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionPredicate" ):
                return visitor.visitVersionPredicate(self)
            else:
                return visitor.visitChildren(self)




    def versionPredicate(self):

        localctx = AqlParser.VersionPredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_versionPredicate)
        try:
            self.state = 290
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 287
                self.match(AqlParser.LATEST_VERSION)
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 288
                self.match(AqlParser.ALL_VERSIONS)
                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 3)
                self.state = 289
                self.standardPredicate()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathPredicateOperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive(self):
            return self.getTypedRuleContext(AqlParser.PrimitiveContext,0)


        def objectPath(self):
            return self.getTypedRuleContext(AqlParser.ObjectPathContext,0)


        def PARAMETER(self):
            return self.getToken(AqlParser.PARAMETER, 0)

        def ID_CODE(self):
            return self.getToken(AqlParser.ID_CODE, 0)

        def AT_CODE(self):
            return self.getToken(AqlParser.AT_CODE, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_pathPredicateOperand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathPredicateOperand" ):
                listener.enterPathPredicateOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathPredicateOperand" ):
                listener.exitPathPredicateOperand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathPredicateOperand" ):
                return visitor.visitPathPredicateOperand(self)
            else:
                return visitor.visitChildren(self)




    def pathPredicateOperand(self):

        localctx = AqlParser.PathPredicateOperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_pathPredicateOperand)
        try:
            self.state = 297
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20, 64, 65, 66, 67, 68, 69, 70, 71, 72, 86]:
                self.enterOuterAlt(localctx, 1)
                self.state = 292
                self.primitive()
                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 2)
                self.state = 293
                self.objectPath()
                pass
            elif token in [56]:
                self.enterOuterAlt(localctx, 3)
                self.state = 294
                self.match(AqlParser.PARAMETER)
                pass
            elif token in [57]:
                self.enterOuterAlt(localctx, 4)
                self.state = 295
                self.match(AqlParser.ID_CODE)
                pass
            elif token in [58]:
                self.enterOuterAlt(localctx, 5)
                self.state = 296
                self.match(AqlParser.AT_CODE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjectPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pathPart(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.PathPartContext)
            else:
                return self.getTypedRuleContext(AqlParser.PathPartContext,i)


        def SYM_SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.SYM_SLASH)
            else:
                return self.getToken(AqlParser.SYM_SLASH, i)

        def getRuleIndex(self):
            return AqlParser.RULE_objectPath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObjectPath" ):
                listener.enterObjectPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObjectPath" ):
                listener.exitObjectPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObjectPath" ):
                return visitor.visitObjectPath(self)
            else:
                return visitor.visitChildren(self)




    def objectPath(self):

        localctx = AqlParser.ObjectPathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_objectPath)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 299
            self.pathPart()
            self.state = 304
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,37,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 300
                    self.match(AqlParser.SYM_SLASH)
                    self.state = 301
                    self.pathPart() 
                self.state = 306
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,37,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathPartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(AqlParser.IDENTIFIER, 0)

        def pathPredicate(self):
            return self.getTypedRuleContext(AqlParser.PathPredicateContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_pathPart

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathPart" ):
                listener.enterPathPart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathPart" ):
                listener.exitPathPart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathPart" ):
                return visitor.visitPathPart(self)
            else:
                return visitor.visitChildren(self)




    def pathPart(self):

        localctx = AqlParser.PathPartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_pathPart)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 307
            self.match(AqlParser.IDENTIFIER)
            self.state = 309
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,38,self._ctx)
            if la_ == 1:
                self.state = 308
                self.pathPredicate()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LikeOperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AqlParser.STRING, 0)

        def PARAMETER(self):
            return self.getToken(AqlParser.PARAMETER, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_likeOperand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikeOperand" ):
                listener.enterLikeOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikeOperand" ):
                listener.exitLikeOperand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLikeOperand" ):
                return visitor.visitLikeOperand(self)
            else:
                return visitor.visitChildren(self)




    def likeOperand(self):

        localctx = AqlParser.LikeOperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_likeOperand)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 311
            _la = self._input.LA(1)
            if not(_la==56 or _la==72):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MatchesOperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYM_LEFT_CURLY(self):
            return self.getToken(AqlParser.SYM_LEFT_CURLY, 0)

        def valueListItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.ValueListItemContext)
            else:
                return self.getTypedRuleContext(AqlParser.ValueListItemContext,i)


        def SYM_RIGHT_CURLY(self):
            return self.getToken(AqlParser.SYM_RIGHT_CURLY, 0)

        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.SYM_COMMA)
            else:
                return self.getToken(AqlParser.SYM_COMMA, i)

        def terminologyFunction(self):
            return self.getTypedRuleContext(AqlParser.TerminologyFunctionContext,0)


        def URI(self):
            return self.getToken(AqlParser.URI, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_matchesOperand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMatchesOperand" ):
                listener.enterMatchesOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMatchesOperand" ):
                listener.exitMatchesOperand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMatchesOperand" ):
                return visitor.visitMatchesOperand(self)
            else:
                return visitor.visitChildren(self)




    def matchesOperand(self):

        localctx = AqlParser.MatchesOperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_matchesOperand)
        self._la = 0 # Token type
        try:
            self.state = 328
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,40,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 313
                self.match(AqlParser.SYM_LEFT_CURLY)
                self.state = 314
                self.valueListItem()
                self.state = 319
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==82:
                    self.state = 315
                    self.match(AqlParser.SYM_COMMA)
                    self.state = 316
                    self.valueListItem()
                    self.state = 321
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 322
                self.match(AqlParser.SYM_RIGHT_CURLY)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 324
                self.terminologyFunction()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 325
                self.match(AqlParser.SYM_LEFT_CURLY)
                self.state = 326
                self.match(AqlParser.URI)
                self.state = 327
                self.match(AqlParser.SYM_RIGHT_CURLY)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueListItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive(self):
            return self.getTypedRuleContext(AqlParser.PrimitiveContext,0)


        def PARAMETER(self):
            return self.getToken(AqlParser.PARAMETER, 0)

        def terminologyFunction(self):
            return self.getTypedRuleContext(AqlParser.TerminologyFunctionContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_valueListItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValueListItem" ):
                listener.enterValueListItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValueListItem" ):
                listener.exitValueListItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueListItem" ):
                return visitor.visitValueListItem(self)
            else:
                return visitor.visitChildren(self)




    def valueListItem(self):

        localctx = AqlParser.ValueListItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_valueListItem)
        try:
            self.state = 333
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20, 64, 65, 66, 67, 68, 69, 70, 71, 72, 86]:
                self.enterOuterAlt(localctx, 1)
                self.state = 330
                self.primitive()
                pass
            elif token in [56]:
                self.enterOuterAlt(localctx, 2)
                self.state = 331
                self.match(AqlParser.PARAMETER)
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 3)
                self.state = 332
                self.terminologyFunction()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(AqlParser.STRING, 0)

        def numericPrimitive(self):
            return self.getTypedRuleContext(AqlParser.NumericPrimitiveContext,0)


        def DATE(self):
            return self.getToken(AqlParser.DATE, 0)

        def TIME(self):
            return self.getToken(AqlParser.TIME, 0)

        def DATETIME(self):
            return self.getToken(AqlParser.DATETIME, 0)

        def BOOLEAN(self):
            return self.getToken(AqlParser.BOOLEAN, 0)

        def NULL(self):
            return self.getToken(AqlParser.NULL, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_primitive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitive" ):
                listener.enterPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitive" ):
                listener.exitPrimitive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimitive" ):
                return visitor.visitPrimitive(self)
            else:
                return visitor.visitChildren(self)




    def primitive(self):

        localctx = AqlParser.PrimitiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_primitive)
        try:
            self.state = 342
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [72]:
                self.enterOuterAlt(localctx, 1)
                self.state = 335
                self.match(AqlParser.STRING)
                pass
            elif token in [65, 66, 67, 68, 86]:
                self.enterOuterAlt(localctx, 2)
                self.state = 336
                self.numericPrimitive()
                pass
            elif token in [69]:
                self.enterOuterAlt(localctx, 3)
                self.state = 337
                self.match(AqlParser.DATE)
                pass
            elif token in [70]:
                self.enterOuterAlt(localctx, 4)
                self.state = 338
                self.match(AqlParser.TIME)
                pass
            elif token in [71]:
                self.enterOuterAlt(localctx, 5)
                self.state = 339
                self.match(AqlParser.DATETIME)
                pass
            elif token in [64]:
                self.enterOuterAlt(localctx, 6)
                self.state = 340
                self.match(AqlParser.BOOLEAN)
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 7)
                self.state = 341
                self.match(AqlParser.NULL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumericPrimitiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(AqlParser.INTEGER, 0)

        def REAL(self):
            return self.getToken(AqlParser.REAL, 0)

        def SCI_INTEGER(self):
            return self.getToken(AqlParser.SCI_INTEGER, 0)

        def SCI_REAL(self):
            return self.getToken(AqlParser.SCI_REAL, 0)

        def SYM_MINUS(self):
            return self.getToken(AqlParser.SYM_MINUS, 0)

        def numericPrimitive(self):
            return self.getTypedRuleContext(AqlParser.NumericPrimitiveContext,0)


        def getRuleIndex(self):
            return AqlParser.RULE_numericPrimitive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumericPrimitive" ):
                listener.enterNumericPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumericPrimitive" ):
                listener.exitNumericPrimitive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumericPrimitive" ):
                return visitor.visitNumericPrimitive(self)
            else:
                return visitor.visitChildren(self)




    def numericPrimitive(self):

        localctx = AqlParser.NumericPrimitiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_numericPrimitive)
        try:
            self.state = 350
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [65]:
                self.enterOuterAlt(localctx, 1)
                self.state = 344
                self.match(AqlParser.INTEGER)
                pass
            elif token in [66]:
                self.enterOuterAlt(localctx, 2)
                self.state = 345
                self.match(AqlParser.REAL)
                pass
            elif token in [67]:
                self.enterOuterAlt(localctx, 3)
                self.state = 346
                self.match(AqlParser.SCI_INTEGER)
                pass
            elif token in [68]:
                self.enterOuterAlt(localctx, 4)
                self.state = 347
                self.match(AqlParser.SCI_REAL)
                pass
            elif token in [86]:
                self.enterOuterAlt(localctx, 5)
                self.state = 348
                self.match(AqlParser.SYM_MINUS)
                self.state = 349
                self.numericPrimitive()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def terminologyFunction(self):
            return self.getTypedRuleContext(AqlParser.TerminologyFunctionContext,0)


        def SYM_LEFT_PAREN(self):
            return self.getToken(AqlParser.SYM_LEFT_PAREN, 0)

        def SYM_RIGHT_PAREN(self):
            return self.getToken(AqlParser.SYM_RIGHT_PAREN, 0)

        def STRING_FUNCTION_ID(self):
            return self.getToken(AqlParser.STRING_FUNCTION_ID, 0)

        def NUMERIC_FUNCTION_ID(self):
            return self.getToken(AqlParser.NUMERIC_FUNCTION_ID, 0)

        def DATE_TIME_FUNCTION_ID(self):
            return self.getToken(AqlParser.DATE_TIME_FUNCTION_ID, 0)

        def IDENTIFIER(self):
            return self.getToken(AqlParser.IDENTIFIER, 0)

        def terminal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AqlParser.TerminalContext)
            else:
                return self.getTypedRuleContext(AqlParser.TerminalContext,i)


        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.SYM_COMMA)
            else:
                return self.getToken(AqlParser.SYM_COMMA, i)

        def getRuleIndex(self):
            return AqlParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = AqlParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.state = 366
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [55]:
                self.enterOuterAlt(localctx, 1)
                self.state = 352
                self.terminologyFunction()
                pass
            elif token in [32, 33, 34, 61]:
                self.enterOuterAlt(localctx, 2)
                self.state = 353
                localctx.name = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2305843039278465024) != 0)):
                    localctx.name = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 354
                self.match(AqlParser.SYM_LEFT_PAREN)
                self.state = 363
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2413929430336405504) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 4194815) != 0):
                    self.state = 355
                    self.terminal()
                    self.state = 360
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==82:
                        self.state = 356
                        self.match(AqlParser.SYM_COMMA)
                        self.state = 357
                        self.terminal()
                        self.state = 362
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 365
                self.match(AqlParser.SYM_RIGHT_PAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AggregateFunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def SYM_LEFT_PAREN(self):
            return self.getToken(AqlParser.SYM_LEFT_PAREN, 0)

        def SYM_RIGHT_PAREN(self):
            return self.getToken(AqlParser.SYM_RIGHT_PAREN, 0)

        def COUNT(self):
            return self.getToken(AqlParser.COUNT, 0)

        def identifiedPath(self):
            return self.getTypedRuleContext(AqlParser.IdentifiedPathContext,0)


        def SYM_ASTERISK(self):
            return self.getToken(AqlParser.SYM_ASTERISK, 0)

        def DISTINCT(self):
            return self.getToken(AqlParser.DISTINCT, 0)

        def MIN(self):
            return self.getToken(AqlParser.MIN, 0)

        def MAX(self):
            return self.getToken(AqlParser.MAX, 0)

        def SUM(self):
            return self.getToken(AqlParser.SUM, 0)

        def AVG(self):
            return self.getToken(AqlParser.AVG, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_aggregateFunctionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAggregateFunctionCall" ):
                listener.enterAggregateFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAggregateFunctionCall" ):
                listener.exitAggregateFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAggregateFunctionCall" ):
                return visitor.visitAggregateFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def aggregateFunctionCall(self):

        localctx = AqlParser.AggregateFunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_aggregateFunctionCall)
        self._la = 0 # Token type
        try:
            self.state = 383
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [50]:
                self.enterOuterAlt(localctx, 1)
                self.state = 368
                localctx.name = self.match(AqlParser.COUNT)
                self.state = 369
                self.match(AqlParser.SYM_LEFT_PAREN)
                self.state = 375
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [16, 61]:
                    self.state = 371
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==16:
                        self.state = 370
                        self.match(AqlParser.DISTINCT)


                    self.state = 373
                    self.identifiedPath()
                    pass
                elif token in [84]:
                    self.state = 374
                    self.match(AqlParser.SYM_ASTERISK)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 377
                self.match(AqlParser.SYM_RIGHT_PAREN)
                pass
            elif token in [51, 52, 53, 54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 378
                localctx.name = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 33776997205278720) != 0)):
                    localctx.name = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 379
                self.match(AqlParser.SYM_LEFT_PAREN)
                self.state = 380
                self.identifiedPath()
                self.state = 381
                self.match(AqlParser.SYM_RIGHT_PAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TerminologyFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TERMINOLOGY(self):
            return self.getToken(AqlParser.TERMINOLOGY, 0)

        def SYM_LEFT_PAREN(self):
            return self.getToken(AqlParser.SYM_LEFT_PAREN, 0)

        def STRING(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.STRING)
            else:
                return self.getToken(AqlParser.STRING, i)

        def SYM_COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(AqlParser.SYM_COMMA)
            else:
                return self.getToken(AqlParser.SYM_COMMA, i)

        def SYM_RIGHT_PAREN(self):
            return self.getToken(AqlParser.SYM_RIGHT_PAREN, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_terminologyFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminologyFunction" ):
                listener.enterTerminologyFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminologyFunction" ):
                listener.exitTerminologyFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerminologyFunction" ):
                return visitor.visitTerminologyFunction(self)
            else:
                return visitor.visitChildren(self)




    def terminologyFunction(self):

        localctx = AqlParser.TerminologyFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_terminologyFunction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 385
            self.match(AqlParser.TERMINOLOGY)
            self.state = 386
            self.match(AqlParser.SYM_LEFT_PAREN)
            self.state = 387
            self.match(AqlParser.STRING)
            self.state = 388
            self.match(AqlParser.SYM_COMMA)
            self.state = 389
            self.match(AqlParser.STRING)
            self.state = 390
            self.match(AqlParser.SYM_COMMA)
            self.state = 391
            self.match(AqlParser.STRING)
            self.state = 392
            self.match(AqlParser.SYM_RIGHT_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.direction = None # Token

        def TOP(self):
            return self.getToken(AqlParser.TOP, 0)

        def INTEGER(self):
            return self.getToken(AqlParser.INTEGER, 0)

        def FORWARD(self):
            return self.getToken(AqlParser.FORWARD, 0)

        def BACKWARD(self):
            return self.getToken(AqlParser.BACKWARD, 0)

        def getRuleIndex(self):
            return AqlParser.RULE_top

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTop" ):
                listener.enterTop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTop" ):
                listener.exitTop(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTop" ):
                return visitor.visitTop(self)
            else:
                return visitor.visitChildren(self)




    def top(self):

        localctx = AqlParser.TopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_top)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 394
            self.match(AqlParser.TOP)
            self.state = 395
            self.match(AqlParser.INTEGER)
            self.state = 397
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==22 or _la==23:
                self.state = 396
                localctx.direction = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==22 or _la==23):
                    localctx.direction = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[8] = self.whereExpr_sempred
        self._predicates[11] = self.containsExpr_sempred
        self._predicates[19] = self.nodePredicate_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def whereExpr_sempred(self, localctx:WhereExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def containsExpr_sempred(self, localctx:ContainsExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         

    def nodePredicate_sempred(self, localctx:NodePredicateContext, predIndex:int):
            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 1)
         




