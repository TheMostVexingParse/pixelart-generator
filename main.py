import argparse
import os
from PIL import Image
from gif import GIF, CreateGIF
from pixelate import Pixelate
from glob import glob


#python main.py test.gif -o new.gif -b 96 -r 384

#python main.py test.png -o new.jpg -b 96 -r 384


TYPE_ERROR_MUST_MATCH = "Input and output types must match."
TYPE_ERROR_INVALID_FILETYPE = "Invalid filetype, can not process."



def pixelate_image(img_path, output_path, basewidth, real_width=None):
    with Image.open(img_path) as img:
        psession = Pixelate(img, basewidth, real_width)
        psession.process(output_path)


def pixelate_gif(gif_path, output_dir, basewidth, real_width=None):
    gif = GIF(gif_path)
    psession = Pixelate(gif, basewidth, real_width)
    psession.process(output_dir)


def create_gif(input_dir, output_path, duration=200, loop=0):
    process = CreateGIF()
    process.load_dir(input_dir)
    process.generate(duration=duration, loop=loop, fp_out=output_path)


def main():
    parser = argparse.ArgumentParser(description='Convert images and GIFs to pixel art.')
    parser.add_argument('input', type=str, help='path to input file or directory')
    parser.add_argument('-o', '--output', type=str, help='path to output file or directory')
    parser.add_argument('-b', '--basewidth', type=int, default=128, help='pixel width of output images')
    parser.add_argument('-r', '--realwidth', type=int, default=None, help='real width of output images (default is None)')
    parser.add_argument('-d', '--duration', type=int, default=0, help='duration of GIF frames in milliseconds')
    parser.add_argument('-l', '--loop', type=int, default=0, help='number of times to loop GIF (0 for infinite)')
    args = parser.parse_args()

    if args.input.endswith('.gif'):
        if not args.output.endswith('.gif'):
            raise TypeError(TYPE_ERROR_MUST_MATCH)

        out_loc = '.'.join(args.output.split('.')[:-1])+'_output'

        try: os.mkdir(out_loc)
        except: pass

        for i in glob(f'{out_loc}\\*'): os.remove(i)
            
        image = GIF(os.getcwd()+'\\'+args.input)
        psession = Pixelate(image, args.basewidth, args.realwidth)
        psession.process(out_loc)

        if args.duration:
            duration = args.duration
        else:
            duration = image.duration


        process = CreateGIF()
        process.load_dir(f'{out_loc}\\*.png')
        process.generate(args.output, duration=duration)

    elif args.input.split('.')[-1] in ['png', 'jpg', 'jpeg']:
        psession = Pixelate(Image.open(os.getcwd()+'\\'+args.input), args.basewidth, args.realwidth)
        psession.process(args.output)

    else:
        raise TypeError(TYPE_ERROR_INVALID_FILETYPE)

    #print(args, out_loc)

if __name__ == '__main__':
    main()
