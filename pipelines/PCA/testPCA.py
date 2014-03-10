"""
Usage:
    testPCA.py -k <k> -l <labelerfile> -s <statfile> [-a <additional_file>]

Options:
    -k=<k>  the number of clusters
    -l=<labelerfile>    the file containing the labeler
    -s=<statfile>   the file containing status info
    -a=<additional_file>    a file containing additional data to be plotted, in SIFT format
"""
from docopt import docopt
from pipelines.formats.KMeans import *
from data_manager.OSM import object_from_file
from PCA import *
from json import loads

def main():
    a = docopt(__doc__, version="0.1a")
    labelerfile=a["-l"]
    statfile = a["-s"]
    K = int(a["-k"])
    labeler=object_from_file(KMeansLabeler, labelerfile)
    statcnt = object_from_file(str, statfile)
    stats = loads(statcnt)
    #print stats
    additional_data = None
    if a["-a"]:
        with open(a["-a"], "r") as f:
            additional_data = []
            for line in f.readlines():
                additional_data.append(loads(line))
    red = "r"
    green = "g"

    colors = [green]*K
    for x in stats:
        colors[x] = red

    plot_PCA(labeler.cluster_centers_, colors, additional_data)

if __name__ == "__main__":
    main()
