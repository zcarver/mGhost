import argparse
import numpy as np
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from lxml import html
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spp", type=str)
    parser.add_argument("--lim", type=str,
                        help="enter number of result pages from herbarium")
    return parser.parse_args()


def protologue(spp):
    SearchText = "<SearchText>" + spp + "</SearchText>"
    url = "http://www.indexfungorum.org/ixfwebservice/fungus.asmx?WSDL"
    headers = {'content-type': 'text/xml'}
    b1 = """<?xml version='1.0' encoding='utf-8'?>
            <soap12:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'\
            xmlns:xsd='http://www.w3.org/2001/XMLSchema'\
            xmlns:soap12='http://www.w3.org/2003/05/soap-envelope'>
            <soap12:Body>
            <NameSearch xmlns='http://Cabi/FungusServer/'>"""
    b2 = SearchText
    b3 = """<AnywhereInText>true</AnywhereInText>
            <MaxNumber>2</MaxNumber>
            </NameSearch>
            </soap12:Body>
            </soap12:Envelope>"""
    body = b1+b2+b3
    r = requests.post(url, data=body, headers=headers)
    r = r.content
    #print(r)
    #root = ET.fromstring(r)
    parser = ET.XMLPullParser()
    parser.feed(r)
    ls = list(parser.read_events())
    #for event, elem in parser.read_events():
    #print(ls)
    ls = ls[9][1]
    return "protologue:", ls.text


def host(spp):
    query = {'whichone': 'FungusHost',
             'thisName': spp,
             'organismtype': 'Fungus',
             'fromAllCount': 'yes',
             }
    r = requests.get('http://nt.ars-grin.gov/fungaldatabases/new_allView.cfm',
                     params=query
                     ).text
    p = html.fromstring(r)
    taxa = p.xpath('//p[@class="Hanging "]/text()')
    #print(taxa)[0]
    genusSpecies = []
    for t in taxa:
        #g = t.split()[0]
        #s = t.split()[1]
        if not t.startswith(","):
            g = t.split()[0]
            s = t.split()[1]
            s = s.split(':')[0]
            hostTaxon = g+" "+s
            if hostTaxon not in genusSpecies:            
                genusSpecies.append(g+" "+s)
    print(genusSpecies)
    #classp = [e.get('class') for e in p.xpath(p)]
    ##print(classp.text)
    #print(r)
    #print(r)
    link = p.cssselect("A")[30]
    #print(link.text_content())


def host_geo(h, f, lim):
    url = "http://data.cyberfloralouisiana.com/lsu/api/silvercollection.php"
    f = '''{"ScientificName":"'''+h+'''"}'''
    payload = {"cmd": "search",
               "limit": lim,
               "filter": f,
               "sort": "Family"
               }
    r = requests.get(url, payload)
    herba_result = r.json()
    la_dicts = herba_result['results']
    la_dicts = [d for d in la_dicts if d['StateProvince'] == 'Louisiana']
    #print(len(la_dicts))
    return la_dicts


def pdcsv(la_dicts, f, p):
    la_dframe = pd.DataFrame(la_dicts)
    fungus_prot = pd.DataFrame({'Fungus': f, 'Links': p})
    la_dframe = pd.concat([la_dframe, fungus_prot],
                          axis=1,
                          join_axes=[la_dframe.index])
    #print(la_dframe)
    la_dframe.drop(la_dframe.columns[[0, 1, 3, 7, 9, 10, 11,
                                      12, 13, 14, 17, 19, 21,
                                      22, 23, 24, 25, 26, 27]], axis=1, inplace=True)
    ladf = la_dframe[['Family', 'ScientificName', 'common_name',
                      'StateProvince', 'County', 'Locality',
                      'DecimalLatitude', 'DecimalLongitude', 'Collector',
                      'Fungus', 'Links']]
    #print(ladf)
    lat_list = ladf['DecimalLatitude'].tolist()
    lon_list = ladf['DecimalLongitude'].tolist()
    ladf.to_csv('host_fungi.csv', sep=',', encoding='utf-8')
    return lat_list, lon_list


def plot(lon, lat, h):
    m = Basemap(projection='gall',
                llcrnrlon=-94.5,
                llcrnrlat=28.5,
                urcrnrlon=-88.5,
                urcrnrlat=34,
                resolution='f',
                area_thresh=50.0,
                lat_0=31.30, lon_0=-92.60
                )
    fig = plt.figure()
    fig.suptitle('Local of Type host '+h, fontsize=10)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawrivers(linewidth=0.5, linestyle='solid', color='steelblue',
                 antialiased=1, ax=None, zorder=None)
    parallels = np.arange(0., 90, 0.5)
    m.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., 1)
    m.drawmeridians(meridians, labels=[True, False, False, True])
    m.fillcontinents(color='gainsboro')
    m.drawmapboundary(fill_color='steelblue')
    xpt, ypt = m(lon, lat)
    lonpt, latpt = m(xpt, ypt, inverse=True)
    m.plot(xpt, ypt, 'bo')
    plt.show()



def main():
    arg = args()
    f = arg.spp
    p = protologue(f)
    h = host(f)
    la_dicts = host_geo(h, f, arg.lim)
    pd_tuple = pdcsv(la_dicts, f, p)
    lat = pd_tuple[0]
    lon = pd_tuple[1]
    plot(lon, lat, h)
    print("fungus:", arg.spp, '\n', "protologue:", p)

if __name__ == '__main__':
    main()
