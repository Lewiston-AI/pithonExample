import sys
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
import clr
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft.AF.PI import *
from OSIsoft.AF.Search import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *


attrs = [
        PICommonPointAttributes.Archiving,
        PICommonPointAttributes.Compressing,
        PICommonPointAttributes.CompressionDeviation,
        PICommonPointAttributes.CompressionMaximum,
        PICommonPointAttributes.CompressionMinimum,
        PICommonPointAttributes.CompressionPercentage,
        PICommonPointAttributes.Descriptor,
        PICommonPointAttributes.EngineeringUnits,
        PICommonPointAttributes.ExceptionDeviation,
        PICommonPointAttributes.ExceptionMaximum,
        PICommonPointAttributes.ExceptionMinimum,
        PICommonPointAttributes.ExceptionPercentage,
        PICommonPointAttributes.ExtendedDescriptor,
        PICommonPointAttributes.InstrumentTag,
        PICommonPointAttributes.Location1,
        PICommonPointAttributes.Location4,
        PICommonPointAttributes.PointID,
        PICommonPointAttributes.PointSource,
        PICommonPointAttributes.PointType,
        PICommonPointAttributes.SourcePointID,
        PICommonPointAttributes.Span,
        PICommonPointAttributes.Step,
        PICommonPointAttributes.Tag,
        PICommonPointAttributes.Zero,
    ]