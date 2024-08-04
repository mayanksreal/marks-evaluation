from libs.ocr import ocr_prediction
from libs.cnn import hand_prediction
import csv
import cv2
import numpy as np

rows_written = 0

def extract_cells(table_image,  page_no, pdf_name):
    csv_filename = f'outputs/{pdf_name}/output.csv'
    image = table_image
    global rows_written
    # Determine number of rows using page height
    # height = 181 + 59*rows
    height = len(image)
    num_rows = round((height - 181) / 59)
    
    # Parameters (adjust these values as needed)
    title_offset = 106 + (num_rows * 2)  # Offset to skip the title
    header_row_height = 75  # Height of the header row
    row_height = 57  # Height of each subsequent row
    
    # Column widths (adjust these values according to your table)
    col_names = ["SNo.","ID","NAME","DOB","INTERVIEW MARKS"]
    column_widths = [67, 73, 392 + (num_rows * 2), 175, 420]
    
    # Function to get the column boundaries
    def get_column_boundaries(column_widths):
        boundaries = [0]
        for width in column_widths:
            boundaries.append(boundaries[-1] + width)
        return boundaries
    
    column_boundaries = get_column_boundaries(column_widths)
    
    # Open a CSV file to write the results
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Extract header row
        header_row = image[title_offset:title_offset + header_row_height, :]
        header_cells = []
        
        # Process each cell of the header row
        if page_no == 0:
            for col in range(0,5):
                cell = header_row[:, column_boundaries[col]:column_boundaries[col + 1]]
                cell_image = np.array(cell)
                try:
                    header_cells.append(ocr_prediction(cell_image)[0][1])
                except Exception:
                    header_cells.append("ERR")
            # Write the header row to the CSV
            csv_writer.writerow(header_cells)
        
        # Extract subsequent rows
        for row in range(1, num_rows + 1):
            row_start = title_offset + header_row_height + (row - 1) * row_height
            row_end = row_start + row_height
            table_row = image[row_start:row_end, :]
            row_cells = []
            
            # Process each cell of the row
            row_cells.append(f'{row + rows_written}')
            for col in range(1,5):
                cell = table_row[:, column_boundaries[col]:column_boundaries[col + 1]]
                cell_image = np.array(cell)
                if col < 4:
                    try:
                        row_cells.append(ocr_prediction(cell_image)[0][1])
                        if len(ocr_prediction(cell_image)) > 1:
                            txt_file = open(f"outputs/{pdf_name}/attention.txt", "a", newline="\n")
                            txt_file.write(f"Attention needed at: SNo. {rows_written + row} , {col_names[col]} \n")
                    except Exception:
                        row_cells.append("ERR")
                        txt_file = open(f"outputs/{pdf_name}/attention.txt", "a", newline="\n")
                        txt_file.write(f"Attention needed at: SNo. {rows_written + row} , {col_names[col]} \n")

                if col == 4:
                    pred = hand_prediction(cell_image)
                    row_cells.append(pred[0])
                    if (pred[1] < 0.90 ):
                        txt_file = open(f"outputs/{pdf_name}/attention.txt", "a", newline="\n")
                        txt_file.write(f"Attention needed at: SNo. {rows_written + row} , {col_names[col]} \n")
                        
            
            # Write the row to the CSV
            csv_writer.writerow(row_cells)
            
    print(f"Written {num_rows} row(s) to '{csv_filename}'.")
    rows_written += num_rows


def reset_rows():
    global rows_written
    rows_written = 0
