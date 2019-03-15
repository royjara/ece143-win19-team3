import imageio
import os
import os.path
    '''
    Author: Xu Zhu
    Generate gif file from a folder of PNGs.
    '''
    
def create_gif(gif_name, path, duration = 0.8):
    '''
    Generate gif file from a folder of PNGs.
    gif_name: str, file name to generate
    path: path to PNG folder
    duration: duration of each frame
    '''

    frames = []
    pngFiles = os.listdir(path)
    image_list = [os.path.join(path, f) for f in pngFiles]
    for image_name in image_list:
        frames.append(imageio.imread(image_name)[:1500])
    #save as gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = duration)
    return

if __name__ == "__main__":
    create_gif('2018TimePeriod.gif', path = 'C:\\Users\XZ\ECE143Proj\TimePeriod' , duration = 0.8)
