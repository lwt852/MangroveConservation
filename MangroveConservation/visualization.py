from shapely.geometry import Polygon
import geopandas as gpd
import matplotlib.pyplot as plt
"""
Created on April 16th
@author: Mimi Gong
A few functions to visualize the geometry of twitter data.
"""
def geo_polygon(row):
    """
    Helper function to return the geometry of a polygonal 
    bounding box of longitude, latitude coordinates of twitter data
    Reference: https://github.com/shawn-terryah/Twitter_Geolocation
    Reference:https://shapely.readthedocs.io/en/latest/manual.html]
    """
    try:
        row_ = eval(row)
        lst_of_coords = [item for sublist in row_ for item in sublist]
        polygon = Polygon(p for p in lst_of_coords)
        return polygon
    except BaseException:
        return None
def clip_polygon(data):
    """
    Helper function to select high spatial accuracy of twitter data 
    and clip their spatial boundary into global administrative boundary
    Reference: https://geopandas.org/reference/geopandas.clip.html#geopandas.clip
    """
    temp = data[data.coordinates.notnull()]
    temp['polygon'] = list(map(lambda row: geo_polygon(row), temp['coordinates']))
#    have_coordinates['long_list']=[x[0] for x in have_coordinates['temp']]
#    have_coordinates['lat_list']=[x[1] for x in have_coordinates['temp']]
    temp1 = temp.drop(columns='coordinates')
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world.name != "Antarctica"]
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(temp1, geometry=temp1['polygon'], crs=crs)
#    gdf_fix = gdf[gdf.geometry.type=='Polygon']
    gdf_fix = gdf[gdf["geometry"].area <= 20]
#    overlay = gpd.clip(gdf_fix,world)
    return gdf_fix, world
def centroid_polygon(data):
    """
    Helper function to return the geometry of the centroid 
    of a polygonal bounding box of longitude, latitude coordinates of twitter data
    """
    data['centroid_points'] = data["geometry"].centroid
    points = data.centroid
    return data, points
def visualization_polygons(data, basemap):
    """
    Helper function to map the geometry of a polygonal
    bounding box of longitude, latitude coordinates of twitter 
    data and their centroid
    """
    fig, ax = plt.subplots(figsize=(15, 15))
#    points.plot(ax=ax,color = 'black',alpha = 0.4,markersize = 0.6)
    data.boundary.plot(ax=ax, alpha=1, color="red")
    basemap.boundary.plot(color="grey", ax=ax, alpha=0.2)
    ax.set_axis_off()
