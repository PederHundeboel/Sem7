from glob import glob

import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

import rasterio as rio
import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

import plotly.graph_objects as go


np.seterr(divide='ignore', invalid='ignore')

S_sentinel_bands = glob("Bands/*.jp2")

S_sentinel_bands.sort()

image0 = cv2.imread('NIR.jp2')
resized_nir = cv2.resize(image0, (5490, 5490))
cv2.imwrite('Bands/NIR.jp2', resized_nir)

l = []

for i in S_sentinel_bands:
    with rio.open(i, 'r') as f:
        l.append(f.read(1))

arr_st = np.stack(l)

ep.plot_bands(arr_st,
              cmap = 'gist_earth',
              figsize = (20, 12),
              cols = 6,
              cbar = False)
#plt.show()

ndmi = es.normalized_diff(arr_st[0], arr_st[1])

ep.plot_bands(ndmi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))

plt.show()
