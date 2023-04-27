from PIL import Image
from PIL import ImageFilter

from gif import GIF, CreateGIF
from glob import glob
import os

class Pixelate:
    def __init__(self, obj, basewidth, real_width=None):
        try: self.content = obj.content
        except:
            try: self.content = list(obj)
            except: self.content = [obj, ]
        self.basewidth = basewidth
        self.real_width = real_width

    def process(self, output_dir = None):
        out = []
        ln = len(self.content)
        if ln < 2: ln = 2
        for i, img in enumerate(self.content):

            print(f'Pixelating: {round(i/(ln-1)*100)}%')

            basewidth = self.basewidth
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            

            if self.real_width and self.real_width != self.basewidth:
                img = img.resize((basewidth,hsize), Image.NEAREST)
                
                basewidth = self.real_width
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.BOX)
            else:
                img = img.resize((basewidth,hsize), Image.BOX)
            if len(self.content) < 2:
                img.save(output_dir)
            elif output_dir:
                img.save(f'{output_dir}\\{i+1}.png')

            out.append(img)

        return out


##for i in glob('out\\*'):
##    os.remove(i)
##        
##image = GIF('test.gif')
##psession = Pixelate(image, 96, 512)
##psession.process('out')
##
##
##process = CreateGIF()
##process.load_dir('out\\*.png')
##process.generate('output.gif', duration=100)
