#!/usr/bin/python
from PIL import Image
import os, argparse, sys
import time

desc = "====== MyResampler - made for mum with love ======"
f_path = ""
dirs = dir()

 # Instantiate the parser and give it a description that will show before help
parser = argparse.ArgumentParser(description=desc)
print(desc)

parser.add_argument('--prompt', dest='prompt', type=bool, help='Włącza zapytanie o ścieżkę przy uruchomieniu', default=True)
parser.add_argument('--path', dest='runpath', type=str, help='Ścieżka w której znajdują się obrazy do resamplingu', default='images')
parser.add_argument('--x_size', dest='x_size', type=str,  help='Rozmiar osi X zdjęcia (w pixelach) - domyślnie 1000', default=1000)
parser.add_argument('--y_size', dest='y_size', type=str,  help='Rozmiar osi Y zdjęcia (w pixelach) - domyślnie adaptacyjnie do oryginalnego zdjęcia', default=0)
parser.add_argument('--rotate', dest='rotate', type=bool, help='Zmień orientacje zdjęć na pionową  - domyślnie wyłączone ', default=False)

def main():
    global f_path 

    # Run method to parse the arguments
    args = parser.parse_args()
    
    while True:
        try:
            if args.prompt:
                path = str(input("Podaj nazwę podfolderu do resamplingu: "))
                runpath = os.getcwd()+'\\'+path+'\\'
            else:
                runpath = os.getcwd()+'\\'+args.runpath+'\\'

            dirs = os.listdir(runpath)

            folder = "resampled"
            f_path = os.path.join(runpath, folder)
            if not os.path.exists(f_path):
                os.makedirs(f_path)
                print("Stworzono folder "+str(folder))
                print(f_path)
            break

        except Exception as error:
            print("Podana ścieżka nie istnieje!")
            print("Spróbuj jeszcze raz.")

    for item in dirs:
        if os.path.isfile(runpath+item):
            try:
                im = Image.open(runpath+item)
                f, e = os.path.splitext(runpath+item)
                
                if(im.size[0] > im.size[1] and args.rotate == 1):
                    im = im.rotate(-90, Image.NEAREST, expand=1)
                
                if(args.y_size == 0):
                    y_size = int(im.size[1]*args.x_size/im.size[0])
                
                imResize = im.resize((args.x_size,y_size))

                # Path workaround
                file_name = str(item)
                final_path = os.path.join(f_path, file_name)
                imResize.save(final_path, 'JPEG', quality=90)
                print("Pomyślnie zmniejszono plik "+file_name)

            except Exception as error:
                print("Plik "+str(item)+" nie może być zmniejszony. \n("+str(error)+")")
                print("")

    print("Program zakończył działanie.")
    input("Naciśnij ENTER żeby zakończyć.")


if __name__ == "__main__":
    sys.exit(main())
