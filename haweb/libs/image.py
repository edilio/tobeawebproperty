from PIL import Image


def resize(photo, size=(1500, 300)):
    pw = photo.width
    ph = photo.height
    nw = size[0]
    nh = size[1]
    # only do this if the image needs resizing
    if (pw, ph) != (nw, nh):
        filename = str(photo.path)
        image = Image.open(filename)
        pr = float(pw) / float(ph)
        nr = float(nw) / float(nh)

        ratio = min(nw/pw, nh/ph)

        new_size = (pw*ratio, ph*ratio)

        if pr > nr:
            # photo aspect is wider than destination ratio
            tw = int(round(nh * pr))
            image = image.resize((tw, nh), Image.ANTIALIAS)
            l = int(round((tw - nw) / 2.0))
            image = image.crop((l, 0, l + nw, nh))
        elif pr < nr:
            # photo aspect is taller than destination ratio
            th = int(round(nw / pr))
            image = image.resize((nw, th), Image.ANTIALIAS)
            t = int(round(( th - nh) / 2.0))
            print(0, t, nw, t + nh)
            image = image.crop((0, t, nw, t + nh))
        else:
            # photo aspect matches the destination ratio
            image = image.resize(new_size, Image.ANTIALIAS)

        image.save(filename)


# just for testing
def new_resize():
    img = Image.open('/Users/edilio/Downloads/team.jpg')
    wpercent = (800/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((800, hsize), Image.ANTIALIAS)
    img.save('/Users/edilio/projects/tobeawebproperty/media/photos/team.jpg')