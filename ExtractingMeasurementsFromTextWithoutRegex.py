#Last updated 7/29/2023
import numpy as np
import re
cur = [["None. Something unrelated"],
    ["WxHxT:"],
    ["WxHxT: 11x11x11.5"],
    ["""WxHxT: 12'x12'x12'8" """],
    [None],
    ["N/A"],
    ["Stained Glass: 13x12x12; Snoop Spot: 54x64x54"],
    ["16x24x16, 12x24x64"],
    ["""12Wx36Hx1TH TOP, 12Wx12Hx1TH BOTTOM"""],
    ["""12Wx12Hx1TH:TOP"""],
    ["""A = 12"W x 12"H x .5"TH"""],
    ["""A = 12"W x 12"H x .5"TH, Side = (left) 12"W x 12"H x .5"TH, Side = (right) 12"W x 12"H x .5"TH"""],
    ["""A = 12"W x 12"H x .5"TH, Each side = '12"W x 12"H x .5"TH"""],
    ["""W=(12Wx12.5Hx1.0TH), HW=12Wx12H. Something else = properties, something else = other."""],
    ["""W=A(12Wx12Hx1.0TH),B(12Wx12x1.0TH)"""],
    ["""W=(12Wx12Hx1.0TH), Some unrelated note"""],
    ["""A:(12Wx12Hx1.0TH) B:(12Wx12Hx1.0TH)"""],
    ["""Window = A =12Wx12H, B =12Wx12H"""],
    ["""W=12Wx12H, Stained Glass, rating"""],
    ["""HW =12Wx12H. SG=12Wx12H"""],
    ["""12Wx12Hx.1TH:"""],
    ["""12Wx12Hx1.1TH"""],
    ["""12Wx12Hx.1TH: 12Wx12Hx1TH:"""],
    ["""WxHxTH:12x12x.1"""],
    ["""SG = 12 x 12 x .5"""],
    ["""Vent 12x12"""]]

measurements = np.zeros((len(cur), 15)) -1 #maximum 5 possible windows w/ W, H, T

for j, row in enumerate(cur): #pretend this is an ArcGIS cursor
    val = "" 
    if row[0] is not None:
        val += row[0]
    ##this replaces periods which do not have a digit following with a colon for the split
    temp = list(val)
    val = ""
    for charidx in range(len(temp)):
        if temp[charidx] == "." and (charidx+2 <= len(temp) and not temp[charidx+1].isdigit()):
            temp[charidx] = temp[charidx].replace(".", ":")
        val += temp[charidx]
    val = re.split(":|;|,", val)
    #print(val) #debugging
    ##I'm assuming order is always w, h, sometimes t, or else I can't consistently parse unlabled ones
    for i in range(len(val)):
        #measurements[j, i] is width, i+1 is height, i+2 is thickness
        #print(val[i]) #debugging
        k = 0
        #print(measurements[j, 2]) #debugging
        for trip in [0, 3, 6, 5, 9, 12]:
            if measurements[j, trip] == -1: #this is messed up with second one overwriting
                localtrip = trip
                break
        temp = ""
        tempfeet = 0
        for charidx in range(len(val[i])):
            if val[i][charidx].isdigit() or (val[i][charidx] == "." and "." not in temp):
                temp = temp + val[i][charidx]
            elif val[i][charidx] == "'" and len(temp) > 0:
                tempfeet = float(temp) * 12 #convert feet to inches
                temp = "" #this is causing us to miss 
            if val[i][charidx] == "'" or val[i][charidx] == ".": #breaking this out because the if was getting too long
                continue
            elif (len(temp) > 0 or tempfeet > 0) and (charidx + 1  == len(val[i]) or not val[i][charidx].isdigit()):
                if len(temp) > 0 and tempfeet > 0: #case with inches and feet
                    temp = float(temp)
                    temp += tempfeet
                elif len(temp) == 0 and tempfeet > 0: #case with only feet but no inches
                    temp = tempfeet #I think this is causing it to fill in empty values in the measurements tab
                elif len(temp) > 0 and tempfeet == 0 : #case where there are no feet
                    temp = float(temp)
                else: #case where it is the last part of the string, but there were no digits in the string
                    pass #is this case ever possible given the above if?
                measurements[j, trip +k] = temp #need a way to skip on th if missing but not skip past the next triplet
                k += 1
                temp = "" #reset
                tempfeet = 0
    print(measurements[j], val) #debugging
    print("\n")
    #Then we would write each value into fields 1 through 15, which are Width_N, Height_N, and Thickness_N in N(1-5)
    
