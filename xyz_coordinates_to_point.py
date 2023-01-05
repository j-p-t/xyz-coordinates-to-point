'''
MIT License

Copyright (c) 2022 Juha Toivola

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import arcpy
import os
from datetime import datetime


def is_wkt(spatial_ref):
    if "[" in spatial_ref:
        return True
    else:
        return False


# This is used to execute code if the file was run but not imported
if __name__ == '__main__':
    # Tool parameter accessed with GetParameter or GetParameterAsText
    x = arcpy.GetParameterAsText(0)
    y = arcpy.GetParameterAsText(1)
    z = arcpy.GetParameterAsText(2)
    out_sr = arcpy.GetParameterAsText(3)
    output_fc = arcpy.GetParameterAsText(4)

    if z != "":
        pnt = arcpy.Point(float(x), float(y), float(y))
        has_z = True
    else:
        pnt = arcpy.Point(float(x), float(y))
        has_z = False

    now = datetime.now()
    if output_fc == "":
        project_dir = os.path.dirname(os.path.realpath(__file__))
        now = datetime.now()
        output_fc = project_dir + "/" + "pnt_" + now.strftime("%d_%b_%Y_%H_%M_%S") + ".shp"

    if is_wkt(out_sr):
        sr = arcpy.SpatialReference(text=out_sr)
    else:
        sr = arcpy.SpatialReference(out_sr)

    gcs_sr = sr.GCS

    pnt_geometry = arcpy.PointGeometry(pnt, spatial_reference=gcs_sr, has_z=has_z)

    if gcs_sr.name == sr.name:
        arcpy.CopyFeatures_management(pnt_geometry, output_fc)
    else:
        arcpy.management.Project(pnt_geometry, output_fc, sr)

    # add to map if map active
    aprx = arcpy.mp.ArcGISProject('CURRENT')
    try:
        active_map = aprx.activeMap.name
        aprxMap = aprx.listMaps(active_map)[0]
        aprxMap.addDataFromPath(output_fc)
    except:
        pass
