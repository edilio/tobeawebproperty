from PIL import Image


def resize(photo, size=(1024, 300)):
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
            # print "photo aspect is wider than destination ratio"
            tw = int(round(nh * pr))
            image = image.resize((tw, nh), Image.ANTIALIAS)
            l = int(round((tw - nw) / 2.0))
            image = image.crop((l, 0, l + nw, nh))
        elif pr < nr:
            # photo aspect is taller than destination ratio
            # print "photo aspect is taller than destination ratio"
            th = int(round(nw / pr))
            image = image.resize((nw, th), Image.ANTIALIAS)
            t = int(round((th - nh) / 2.0))
            print(0, t, nw, t + nh)
            image = image.crop((0, t, nw, t + nh))
        else:
            # photo aspect matches the destination ratio
            image = image.resize(new_size, Image.ANTIALIAS)

        image.save(filename)