import re

class ImageAnalyzer:
    @staticmethod
    def get_number_and_size(pil_img):
        """
        Note: Android build ke waqt hum ismein Kivy-OCR ya 
        Google Vision ka link dalenge. Filhal testing ke liye 
        ye dummy data ya basic OCR handle karega.
        """
        try:
            if pil_img is None:
                return "?", "N/A"
            
            # PC testing ke liye basic logic (agar Tesseract installed ho)
            # Lekin APK build ke liye hum ise bypass karte hain
            # Filhal testing ke liye 'BIG' return kar raha hai
            return "5", "BIG" 
                
        except Exception as e:
            print(f"Analyzer Error: {e}")
            return "?", "ERR"