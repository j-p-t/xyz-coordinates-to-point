# Copyright (c) 2022 Juha Toivola
# Licensed under the terms of the MIT License

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
