import osr
import numpy
import gdal
import math
 
width = 10
height = 20
 
format = "GTiff"
driver = gdal.GetDriverByName( format )
 
dst_ds = driver.Create( "test.tiff", width, height, 1, gdal.GDT_Byte )
 
dst_ds.SetGeoTransform( [ 444720, 30, 0, 3751320, 0, -30 ] )
 
srs = osr.SpatialReference()
srs.ImportFromEPSG(25832)
dst_ds.SetProjection( srs.ExportToWkt() )
 
raster = numpy.zeros( (height, width))

raster[0:5, 0:5] += 64
raster[5:, 5:] += 92
 
dst_ds.GetRasterBand(1).WriteArray( raster )