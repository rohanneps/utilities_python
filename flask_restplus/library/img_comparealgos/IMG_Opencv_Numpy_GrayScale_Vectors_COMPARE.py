import os, time
from PIL import Image
import logging
import functools
import sys


def main(download_base_directory,log_dir,src_f,dst_f):

    begin_similarty_compare(download_base_directory,log_dir,src_f,dst_f)


def begin_similarty_compare(download_base_directory,log_dir,src_f,dst_f):

    logging.basicConfig(filename=log_dir, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    for rt, dr, file in os.walk(download_base_directory + src_f):
        for rt2, dr2, file2 in os.walk(download_base_directory +dst_f):
            for file1 in file:
                image_fp1 = rt + '/' + file1
                for file3 in file2:
                    image_fp2 =  rt2+'/'+file3
                    if file3.split('_')[0][:1]==file1.split('.')[0][:1]:
    
                        t1 = time.time()

                        similarity1 = image_similarity_pctchange_via_opencv(image_fp1, image_fp2)

                        duration1 = "%0.1f" % ((time.time() - t1) * 1000)
                        similarity1=str(similarity1)
                        duration1=str(duration1)

                        t2 = time.time()

                        similarity2 = image_similarity_bands_via_numpy(image_fp1, image_fp2)

                        duration2 = "%0.1f" % ((time.time() - t2) * 1000)

                        similarity2 = str(similarity2)
                        duration2 = str(duration2)


                        t3 = time.time()

                        similarity3 = image_similarity_histogram_via_pil(image_fp1, image_fp2)

                        duration3 = "%0.1f" % ((time.time() - t3) * 1000)
                        similarity3 = str(similarity3)
                        duration3 = str(duration3)

                        t4 = time.time()

                        similarity4 = image_similarity_vectors_via_numpy(image_fp1, image_fp2)

                        duration4 = "%0.1f" % ((time.time() - t4) * 1000)

                        similarity4 = str(similarity4)
                        duration4 = str(duration4)

                        t5 = time.time()

                        similarity5 = image_similarity_greyscale_hash_code(image_fp1, image_fp2)

                        duration5 = "%0.1f" % ((time.time() - t5) * 1000)
                        similarity5 = str(similarity5)
                        duration5 = str(duration5)
                        logger.info(image_fp1+ ',' + image_fp2+ ',' +similarity1+ ',' + duration1+ ',' +similarity2+ ',' + duration2+ ',' +similarity3+ ',' + duration3+ ',' +similarity4+ ',' + duration4+ ',' +similarity5+ ',' + duration5)



def image_similarity_pctchange_via_opencv(filepath1, filepath2):
    import cv2
    import numpy as np

    img1 = cv2.imread(filepath1)
    img2 = cv2.imread(filepath2)
    img1 = cv2.resize(img1, (200, 200), interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(img2, (200, 200), interpolation=cv2.INTER_CUBIC)

    diff = img1 - img2
    matrix = np.asarray(diff)
    flat = matrix.flatten()
    numchange = np.count_nonzero(flat)
    percentchange = 100 * float(numchange) / float(len(flat))
    if percentchange == 0:
        diff = img1 - img2

        matrix = np.array(diff)
        flat = matrix.flatten()
        numchange = np.count_nonzero(flat)
        percentchange = 100 * float(numchange) / float(len(flat))

    return percentchange


def image_similarity_bands_via_numpy(filepath1, filepath2):
    import math
    import operator
    import numpy
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    # create thumbnails - resize em
    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)

    # this eliminated unqual images - though not so smarts....
    if image1.size != image2.size or image1.getbands() != image2.getbands():
        return -1
    s = 0
    for band_index, band in enumerate(image1.getbands()):
        m1 = numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size)
        m2 = numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size)
        s += numpy.sum(numpy.abs(m1 - m2))
    return s


def image_similarity_histogram_via_pil(filepath1, filepath2):
    from PIL import Image
    import math
    import operator

    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)

    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(functools.reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return rms


def image_similarity_vectors_via_numpy(filepath1, filepath2):
    from numpy import average, linalg, dot
    import sys

    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    image1 = get_thumbnail(image1, stretch_to_fit=True)
    image2 = get_thumbnail(image2, stretch_to_fit=True)

    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # ValueError: matrices are not aligned !
    res = dot(a / a_norm, b / b_norm)
    return res


def image_similarity_greyscale_hash_code(filepath1, filepath2):


    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    image1 = get_thumbnail(image1, greyscale=True)
    image2 = get_thumbnail(image2, greyscale=True)

    code1 = image_pixel_hash_code(image1)
    code2 = image_pixel_hash_code(image2)
    # use hamming distance to compare hashes
    res = hamming_distance(code1, code2)
    return res


def image_pixel_hash_code(image):
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))  # '00010100...'
    hexadecimal = int(bits, 2).__format__('016x').upper()
    return hexadecimal


def hamming_distance(s1, s2):
    len1, len2 = len(s1), len(s2)
    if len1 != len2:
        "hamming distance works only for string of the same length, so i'll chop the longest sequence"
        if len1 > len2:
            s1 = s1[:-(len1 - len2)]
        else:
            s2 = s2[:-(len2 - len1)]
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])


def get_thumbnail(image, size=(200, 200), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size);  # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image

if __name__ == "__main__":
    download_base_directory=sys.argv[1]
    log_dir = sys.argv[2]
    src_f=sys.argv[3]
    dst_f = sys.argv[4]
    main(download_base_directory,log_dir,src_f,dst_f)