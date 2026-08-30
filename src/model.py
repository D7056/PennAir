from PIL import Image
import numpy as np
from scipy.optimize import minimize
import math


img=Image.open("imgs/static.png")

img_array = np.array(img)

window_size=7

padding_size=window_size//2

pad_width=(
    (padding_size,padding_size),
    (padding_size,padding_size),
    (0,0)
)

padded_img=np.pad(img_array, pad_width=pad_width, mode="edge")

height, width, channel = img_array.shape

norm_array=np.zeros_like(img_array)

print(padded_img.shape)

for i in range(padding_size,height+3):

    for k in range(padding_size,width+3):

        kernel= padded_img[i-padding_size : i-padding_size + window_size, k-padding_size : k-padding_size+window_size, :] 

       

        kernel=kernel.reshape(-1, channel)
       
        
        norm_array[i-padding_size][k-padding_size]=np.median(kernel, axis=0)

print(norm_array)

img=Image.fromarray(norm_array, "RGB")

img.show()

        

        









