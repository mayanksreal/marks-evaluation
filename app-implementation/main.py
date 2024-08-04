#imports
#!pip install numpy tensorflow opencv-python easyocr pymupdf pillow

import cv2
import csv
import os
import io
import numpy as np

from libs.Read_pdf import read_pdf

read_pdf("../data/pdf-marked-demo.pdf")



