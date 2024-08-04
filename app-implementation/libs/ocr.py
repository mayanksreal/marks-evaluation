
import easyocr

def ocr_prediction(img_obj):
    reader = easyocr.Reader(['en'])
    try:
        results = reader.readtext(img_obj)
        if results:
            return results
        else:
            return 'ERR'
    except Exception as e:
        return 'ERR'