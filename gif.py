from PIL import Image
import glob

class GIF:
    def __init__(self, dir_: str, samples: int = None, extract_dir: str = None):
        '''
        Initialize the GIF object by extracting key frames from the specified GIF file.

        Parameters:
            dir_ (str): The filepath of the input GIF file.
            samples (int): The number of key frames to extract (None to extract all key frames).
            extract_dir (str): The directory to extract the key frames to (None to skip extraction).
        '''
        self.content = []

        with Image.open(dir_) as im:
            try: self.duration = im.info['duration']
            except: self.duration = 200
            if samples is None:
                samples = im.n_frames
            for i in range(1, samples+1):
                im.seek(im.n_frames // samples * (i-1))
                self.content.append(im.copy())
                if extract_dir:
                    im.save(f'{extract_dir}/{i}.png')

    def extract(self, extract_dir: str):
        '''
        Extract the key frames to the specified directory.

        Parameters:
            extract_dir (str): The directory to extract the key frames to.
        '''
        for i, im in enumerate(self.content):
            im.save(f'{extract_dir}/{i+1}.png')


            

class CreateGIF:
    def __init__(self):
        self.content = []

    def append(self, img: Image.Image):
        """
        Append a new image to the list of images to be included in the GIF.

        Parameters:
            img (PIL.Image.Image): The image to be added to the GIF.
        """
        self.content.append(img)

    def load_dir(self, dir_: str):
        """
        Load all images from the specified directory and append them to the list of images to be included in the GIF.

        Parameters:
            dir_ (str): The directory containing the images to be added to the GIF. (in glob format)
        """
        globed = sorted(glob.glob(dir_), key=lambda x: int(x.split('.')[0].split('\\')[-1]))
        for i, file_path in enumerate(globed):
            print(f'Loading Frames: {round(i/(len(globed)-1)*100)}%')
            with Image.open(file_path) as img:
                self.content.append(img.copy())

    def generate(self,  fp_out: str = 'output.gif', duration: int = 200, loop: int = 0):
        """
        Generate a GIF from the list of images and save it to the specified file.

        Parameters:
            fp_out (str): The filepath to save the GIF to.
            duration (int): The number of milliseconds to display each image in the GIF.
            loop (int): The number of times the GIF should loop (0 for infinite).
        """
        img_first = self.content[0]
        imgs = self.content[1:]
        print(f'Generating GIF...')
        img_first.save(fp=fp_out, format='GIF', append_images=imgs,
                       save_all=True, duration=duration, loop=loop)


##image = GIF('test.gif')#, extract_dir='.\\out')
##image.extract('.\\out')


