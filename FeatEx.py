﻿import sys
import cv2
import os
import glob
import numpy as np

# Extracts SIFT descriptors from images in a specified directory.
# The descriptors are saved in a separate *.fts file for each image.
#
# Arguments:
# 	- image_dir (required)	: directory containing the image files.
#	- max_F (optional)		: the maximum number of descriptors to be extracted from an image. If none given, as many as possible will be extracted.
#
# Example call: "python FeatEx.py imageclef/train 100".
#

def update_progress(current, total, maxNumKeypoints):
	print('Info: Processed [{0}/{1}]'.format(current, total))
	if (current == total):
		print('Info: Processing done!')
		if not maxNumKeypoints == 0:
			print('Info: {0} data points written.'.format(maxNumKeypoints * 128))
		else:
			print('Info: No maximum number of keypoints was specified so there may be discrepancies.')

def write_to_file(name, dir, data):
	file = open(dir + '/' + name + '.fts', 'w')
	temp_data = str(data).strip('[]').replace('.', '')
	clean_data = " ".join(temp_data.split())
	file.write(clean_data)
	file.close()

def prepare_sift(maxNumKeypoints = 0):
	sift = cv2.SIFT()
	if not maxNumKeypoints == 0:
		sift = cv2.SIFT(maxNumKeypoints)
	return sift
	
	
def extract_features(img, filename, dir, sift):
	# Apply mask so SIFT features are only extracted from unmasked (foreground) area.
	mask = cv2.threshold(img, 200, 255, cv2.THRESH_TOZERO_INV)[1]

	kps, des = sift.detectAndCompute(img, mask)
	
	if (des is None) :
		print filename + ' has no extractable features!'
		cv2.imwrite(dir + '/' + filename + '_mask.jpg',mask)
		return []
	return des.flatten()

def convert_to_grayscale(filepath):
	img = cv2.imread(filepath, cv2.IMREAD_COLOR)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return gray

def get_filenames(dir):
	files = []
	files.extend(glob.glob1(dir, '*.jpg'))
	files.extend(glob.glob1(dir, '*.jpeg'))
	files.extend(glob.glob1(dir, '*.png'))
	return files

def main(argv):
	argc = len(argv)

	np.set_printoptions(threshold=np.nan)

	if (argc > 1):
		dir = argv[1]
		files = get_filenames(dir);

		maxNKey = 0
		if argc > 2:
			maxNKey = int(argv[2])
			
		sift = prepare_sift(maxNKey)

		index = 0
		for file in files:
			img = convert_to_grayscale(dir + '/' + file)

			features = extract_features(img, file, dir, sift)
			write_to_file(os.path.splitext(file)[0], dir, features)
			index = index + 1
			update_progress(index, len(files), maxNKey)

		if (len(files) == 0):
			print('Warning: Could not find images of type png, jpg, jpeg in directory!')
	else:
		print('Warning: No directory specified!')


if __name__ == "__main__":
	main(sys.argv)