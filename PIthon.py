import sys
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
import clr
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft.AF.PI import *
from OSIsoft.AF.Search import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *


from System import Array
from System import Type

import numpy as np
import pandas as pd
import math
import time

import ptattr

def connect_to_Server(serverName):
    piServers = PIServers()
    global piServer
    piServer = piServers[serverName]
    if piServer != None:
        piServer.Connect(False)
    else:
        print("unable to connect to: {serverName}")

def get_tag_snapshot(tagname):
    tag = PIPoint.FindPIPoint(piServer, tagname)
    lastData = tag.Snapshot()
    return lastData.Value, lastData.Timestamp

def get_tags_ptsource(ptSource: str) -> PIPointList:
    ptQuery = PIPointQuery(PICommonPointAttributes.PointSource, AFSearchOperator.Equal, ptSource )
    i = 0
    attributesToLoad = Array[str](len(ptattr.attrs))
    for attr in ptattr.attrs:
        attributesToLoad[i]= attr
        i = i + 1

    queries = Array[PIPointQuery](1)
    queries[0] = ptQuery
    points = PIPoint.FindPIPoints(piServer, queries, attributesToLoad)
    return points

def points_archive_report (points: Array[PIPoint]) -> dict:
    # if we get too many points in the Array, we would need to chunk the calls
    end = 'y'
    start = 'y-31d'
    timeRange = AFTimeRange(start, end)
    boundaryType: AFBoundaryType = 0
    filterExpression = ''
    includeFilteredValues = False
    pageSize = 100000
    pagingConfig = PIPagingConfiguration(PIPageType.TagCount, pageSize);
    maxCount = 0
    #public AFValues RecordedValues(AFTimeRange timeRange, AFBoundaryType boundaryType, string filterExpression,
    #   bool includeFilteredValues, int maxCount = 0);
    values: AFValues
    dictOfTables = dict()
    for pt in points:
        tag = pt.GetAttribute(PICommonPointAttributes.Tag)
        print(f'Getting RecordedValues for: {tag}')
        try:
            st1 = time.time()
            values = pt.RecordedValues(timeRange, AFBoundaryType.Outside, '', False)
            et1 = time.time()
            st2 = et1
            ptType = pt.GetAttribute(PICommonPointAttributes.PointType)
            table = archive_values_to_list1(values, ptType, pt.GetAttribute(PICommonPointAttributes.Span))
            et2 = time.time()
            dictOfTables[tag] = table

            print(f'Got RecordedValues for: {tag} in {et1 - st1} sec. Converted in {et2 - st2} {values.Count}')
        except Exception as ex:
            print(f'\tRecordedValues Error: {tag} {ex}')
            dictOfTables[tag] = list() # empty list means unable to get data

    return dictOfTables

def archive_values_to_list1(values: AFValues, ptType: PIPointType, span: float) -> list():
    table = list() # list of dictionaries (dict for each value)
    try:
        for val in values:
            try:
                row = dict()
                row['value'] = val.Value
                row['time'] = val.Timestamp.UtcSeconds
                row['isgood'] = val.IsGood
                table.append(row)
            except Exception as ex:
                print(f'Converting AFValues error {ex}')
    except Exception as ex:
        print (f'Converting AFValues error {ex}')
    return table
