
from libs.build_model import build_model

model = build_model()

def hand_prediction(image, model=model):
    import cv2
    import numpy as np

    def remove_borders(image, border_size=5):
        return image[border_size:-border_size, border_size:-border_size]
    
    image = remove_borders(image)


    #Convert to Grayscale
    image = cv2. cvtColor(image, cv2. COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by x
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    global result
    global probab
    global n
    result = 0
    probab = 0
    n = 0

    for ctr in contours:
    
        result = result*10

        # Get bounding box 
        x, y, w, h = cv2.boundingRect(ctr)
        
        # Add padding 
        padding = 5
        x = max(x - padding, 0)
        y = max(y - padding, 0)
        w = min(w + 2 * padding, image.shape[1] - x)
        h = min(h + 2 * padding, image.shape[0] - y)
        
        # Extract digit from bounding box
        digit = thresh[y:y+h, x:x+w]
        

        resized_digit = cv2.resize(digit, (28, 28), interpolation=cv2.INTER_AREA)


        # Normalization
        digit = resized_digit / 255.0

        #prediction
        r = model.predict(digit.reshape(1,28,28,1))
        result = result + np.argmax(r)
        n = n+1
        probab = probab + max(max(r))
        
    try:
        return [result,probab/n]
    except Exception:
        return[result, 0]