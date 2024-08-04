from libs.Extract_cells import extract_cells
import cv2

def get_table(image_name, page_no, pdf_name):
    image = image_name
    
    ## Filters
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    
    ## Contour detection
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    table_contour = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
        if len(approx) == 4:
            table_contour = approx
            break
    
    if table_contour is not None:
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(table_contour)
    
        # Crop the table region from the original image
        table_image = image[y:y+h, x:x+w]
        num_rows = 0
        extract_cells(table_image, page_no, pdf_name)
    else:
        print("error")
