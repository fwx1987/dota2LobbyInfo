import pyscreenshot as ImageGrab
from screeninfo import get_monitors
import util.OSUtil as OSUtil
import config

from PIL import Image

__MainScreenResolution__ =None
__MainScreenResolution_width__ = None
__MainScreenResolution_height__ = None


def get_main_screen_resolution():
    global __MainScreenResolution__
    if __MainScreenResolution__ is not None:
        return __MainScreenResolution__

    print("get screen resolution")
    if OSUtil.getOSTYpe() == "WINDOWS":

        for m in get_monitors():
            main_monitor =  str(m)
            __MainScreenResolution__ = main_monitor.split("(")[1].split("+")[0]

            return __MainScreenResolution__
    else:
        __MainScreenResolution__ = "monitor(1440x900+0+0)".split("(")[1].split("+")[0]
        return __MainScreenResolution__


def getMainScreenHeight():
    global __MainScreenResolution__
    global __MainScreenResolution_width__
    global __MainScreenResolution_height__

    if __MainScreenResolution__ is None:
        get_main_screen_resolution()

    if __MainScreenResolution_height__ is None:
        __MainScreenResolution_height__ = __MainScreenResolution__.split("x")[1]
        return __MainScreenResolution_height__
    else:
        return __MainScreenResolution_height__


def getMainScreenWidth():
    global __MainScreenResolution__
    global __MainScreenResolution_width__
    global __MainScreenResolution_height__

    if __MainScreenResolution__ is None:
        get_main_screen_resolution()

    if __MainScreenResolution_width__ is None:
        __MainScreenResolution_width__ = __MainScreenResolution__.split("x")[0]
        return __MainScreenResolution_width__
    else:
        return __MainScreenResolution_width__

def imageResize(file,newfileName):
    im = Image.open(file)
    size = 1920,1080
    im.resize(size, Image.ANTIALIAS).save(newfileName, "PNG")


def captureScreenAndResize(newFileName):

    working_directory = config.get_root_directory()+"/data/temp/"

    im = ImageGrab.grab()  # X1,Y1,X2,Y2

    raw_file = working_directory +"raw_screenshot.png"
    resized_file = working_directory +"/"+newFileName+".png"

    im.save(raw_file)



    imageResize(raw_file,resized_file)

    pass


# box = (10,10,200,200)
# saved name = saved_corped
def crop_image_partial(box, savedname):
    im = Image.open("test-600.png")

    cropped_image = im.crop(box)
    cropped_image.save(savedname+'.png')


if __name__ == "__main__":

    #print(getMainScreenResolution())

    #print(getMainScreenWidth())
    #print(getMainScreenHeight())

    #print(getImageResolution())


    #im = ImageGrab.grab(bbox=(10, 10, 510, 510))  # X1,Y1,X2,Y2

    #im.save('screenshot.png')

    #captureScreenAndResize("test")
    crop_image_partial()
    #im.show()
    #size = 1920,1080
    #im = Image.open("screenshot.png")
    #im.resize(size, Image.ANTIALIAS).save("test-600.png","PNG")

    print("123")