import sys
import time
import requests
from astropy.io import ascii
import astropy.coordinates as coord

url = "http://skyserver.sdss3.org/dr9/en/tools/search/x_sql.asp"
query = ("SELECT TOP 10000 "
        "p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z "
        "FROM BESTDR9..Star AS p "
        "JOIN dbo.fGetNearbyObjEq({ra},{dec},{radius}) AS b ON b.objID = p.objID")
        
clusters = ascii.read("data/sdss_clusters.txt", names=['name', 'size_arcmin'])
for row in clusters:
    filename = "data/cluster_photometry/{0}.csv".format(row['name'].strip())
    print(filename)
    
    icrs = coord.ICRSCoordinates.from_name(row['name'])
    
    this_query = query.format(ra=icrs.ra.degrees,
                              dec=icrs.dec.degrees,
                              radius=row['size_arcmin']/2.)
    
    params = dict(cmd=this_query, format='csv')
    r = requests.post(url, params=params)
    with open(filename,'w') as f:
        csv = r.text
        f.write(csv)
        f.close()
    
    time.sleep(10)