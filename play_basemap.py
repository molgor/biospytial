import basemap as bs
import matplotlib.pyplot as plt


def plot(map,name):
    map.drawmapboundary(fill_color='aqua')
    map.drawcoastlines()
    map.fillcontinents(color='gray',lake_color='aqua')
    map.drawcountries(color='black')
    plt.savefig('juego_bm/%s.png'%name)
    plt.close()
    #plt.show()
    return map

def create_anim(lat,lon,name):

    mapa=bs.Basemap(resolution='l', 
                  satellite_height=3000000.,
                  projection='nsper', 
                  lat_0 = lat, lon_0 = lon,
                  llcrnrx=500000.,llcrnry=500000.,urcrnrx=2700000.,urcrnry=2700000.
                 )

    m = plot(mapa,name)
    