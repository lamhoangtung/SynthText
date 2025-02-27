#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Author: Ankush Gupta
# Date: 2015

"""
Entry-point for generating synthetic text images, as described in:

@InProceedings{Gupta16,
      author       = "Gupta, A. and Vedaldi, A. and Zisserman, A.",
      title        = "Synthetic Data for Text Localisation in Natural Images",
      booktitle    = "IEEE Conference on Computer Vision and Pattern Recognition",
      year         = "2016",
    }
"""

import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
from synthgen import *
from common import *
import wget, tarfile
import cv2
import cPickle as cp
import time
from tqdm import tqdm

### IGNORE THIS PART ###
# path to the data-file, containing image, depth and segmentation:
DATA_PATH = 'data'
DB_FNAME = osp.join(DATA_PATH, 'dset.h5')
# url of the data (google-drive public file):
DATA_URL = 'http://www.robots.ox.ac.uk/~ankush/data.tar.gz'
### IGNORE THIS PART ###

## Define some configuration variables:
NUM_IMG = -1  # no. of images to use for generation (-1 to use all available):
INSTANCE_PER_IMAGE = 5  # no. of times to use the same image
SECS_PER_IMG = None  # max time per image in seconds

# Real generation
BACKGROUND_IM_DIR = 'background/bg_img'
DEPTH_DB_DIR = 'background/depth.h5'
SEG_DB_DIR = 'background/seg.h5'
IMNAMES_DB_DIR = 'background/imnames.cp'
OUT_FILE = 'results/linus_JPN.h5'
OUT_DIR = 'results'

def get_data():
    """
    Download the image,depth and segmentation data:
    Returns, the h5 database.
    """
    if not osp.exists(DB_FNAME):
        try:
            colorprint(Color.BLUE, '\tdownloading data (56 M) from: ' + DATA_URL, bold=True)
            print
            sys.stdout.flush()
            out_fname = 'data.tar.gz'
            wget.download(DATA_URL, out=out_fname)
            tar = tarfile.open(out_fname)
            tar.extractall()
            tar.close()
            os.remove(out_fname)
            colorprint(Color.BLUE, '\n\tdata saved at:' + DB_FNAME, bold=True)
            sys.stdout.flush()
        except:
            print colorize(Color.RED, 'Data not found and have problems downloading.', bold=True)
            sys.stdout.flush()
            sys.exit(-1)
    # open the h5 file and return:
    return h5py.File(DB_FNAME, 'r')


def add_res_to_db(imgname, res, db):
    """
    Add the synthetically generated text image instance
    and other metadata to the dataset.
    """
    ninstance = len(res)
    for i in xrange(ninstance):
        dname = "%s_%d" % (imgname, i)
        db['data'].create_dataset(dname, data=res[i]['img'])
        db['data'][dname].attrs['charBB'] = res[i]['charBB']
        db['data'][dname].attrs['wordBB'] = res[i]['wordBB']

        text_utf8 = [char.encode('utf8') for char in res[i]['txt']]
        db['data'][dname].attrs['txt'] = text_utf8


def save_res_to_imgs(imgname, res):
    """
    Add the synthetically generated text image instance
    and other metadata to the dataset.
    """
    ninstance = len(res)
    for i in xrange(ninstance):
        filename = "{}/{}_{}.png".format(OUT_DIR, imgname, i)
        # Swap bgr to rgb so we can save into image file
        img = res[i]['img'][..., [2, 1, 0]]
        cv2.imwrite(filename, img)


def main(viz=False):
    # open databases:
    print colorize(Color.BLUE, 'getting data..', bold=True)
    # db = get_data()
    depth_db = h5py.File(DEPTH_DB_DIR, 'r')
    seg_db = h5py.File(SEG_DB_DIR, 'r')
    imnames = sorted(depth_db.keys())
    with open(IMNAMES_DB_DIR, 'rb') as f:
        imnames = list(set(cp.load(f)))
    print colorize(Color.BLUE, '\t-> done', bold=True)

    # open the output h5 file:
    out_db = h5py.File(OUT_FILE,'w')
    out_db.create_group('/data')
    print colorize(Color.GREEN,'Storing the output in: '+OUT_FILE, bold=True)

    N = len(imnames)
    global NUM_IMG
    if NUM_IMG < 0:
        NUM_IMG = N
    start_idx, end_idx = 0, min(NUM_IMG, N)

    time_db = []

    RV3 = RendererV3(DATA_PATH, max_time=SECS_PER_IMG, lang=args.lang)
    for i in tqdm(xrange(start_idx, end_idx)):
        imname = imnames[i]
        try:
            start_time = time.time()
            # # get the image:
            # img = Image.fromarray(db['image'][imname][:])
            # # get the pre-computed depth:
            # #  there are 2 estimates of depth (represented as 2 "channels")
            # #  here we are using the second one (in some cases it might be
            # #  useful to use the other one):
            # depth = db['depth'][imname][:].T
            # depth = depth[:, :, 1]
            # # get segmentation:
            # seg = db['seg'][imname][:].astype('float32')
            # area = db['seg'][imname].attrs['area']
            # label = db['seg'][imname].attrs['label']

            img = Image.open(os.path.join(BACKGROUND_IM_DIR, imname)).convert('RGB')
            # get depth:
            depth = depth_db[imname][:].T
            depth = depth[:,:,0]

            # get segmentation info:
            seg = seg_db['mask'][imname][:].astype('float32')
            area = seg_db['mask'][imname].attrs['area']
            label = seg_db['mask'][imname].attrs['label']

            # re-size uniformly:
            sz = depth.shape[:2][::-1]
            img = np.array(img.resize(sz, Image.ANTIALIAS))
            seg = np.array(Image.fromarray(seg).resize(sz, Image.NEAREST))

            print colorize(Color.RED, '    %d of %d' % (i, end_idx - 1), bold=True)
            res = RV3.render_text(img, depth, seg, area, label,
                                  ninstance=INSTANCE_PER_IMAGE, viz=viz)
            if len(res) > 0:
                # non-empty : successful in placing text:
                add_res_to_db(imname,res,out_db)
                # save_res_to_imgs(imname, res)

            # visualize the output:
            if viz:
                save_res_to_imgs(imname, res)
                if 'q' in raw_input(colorize(Color.RED, 'continue? (enter to continue, q to exit): ', True)):
                    break
            total_time = time.time()-start_time
            time_db.append(total_time)
            print colorize(Color.GREEN, 'Took {} secs for {}. Avg {} secs/img'.format(total_time, imname, np.mean(time_db)))
        except:
            traceback.print_exc()
            print colorize(Color.GREEN, '>>>> CONTINUING....', bold=True)
            continue
    # db.close()
    out_db.close()
    depth_db.close()
    seg_db.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Genereate Synthetic Scene-Text Images')
    parser.add_argument('--viz', action='store_true', dest='viz', default=False,
                        help='flag for turning on visualizations')
    parser.add_argument('--lang', default='JPN',
                        help='Select language : ENG/JPN')
    args = parser.parse_args()
    main(args.viz)
