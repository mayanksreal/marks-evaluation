from libs.Get_table import get_table
from libs.Extract_cells import reset_rows

import os
import io
import csv
import pymupdf
from PIL import Image as PILImage
import numpy as np


def read_pdf(pdf_path):
    pdf_document = pymupdf.open(pdf_path)
    global rows_written

    pdf_name = pdf_path[:-4]

    if not os.path.exists(f'outputs/{pdf_name}'):
        os.makedirs(f'outputs/{pdf_name}')
    
    
    #Clearing any past file
    with open(f'outputs/{pdf_name}/output.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
    
    with open(f'outputs/{pdf_name}/attention.txt', mode='w') as txt_file:
        txt_write = txt_file.write('')

    

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        # To image (using matrix transformation)
        zoom = 2  # Adjust zoom level as needed
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # pixmap to PIL Image
        img_bytes = pix.tobytes("ppm")
        image = PILImage.open(io.BytesIO(img_bytes))

        image = np.array(image)
        get_table(image, page_number, pdf_name)

    reset_rows()
