"""
Screen vision system for UI detection and interaction
"""
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
from logger import setup_logger

logger = setup_logger("ScreenVision")

class ScreenVision:
    """Captures and analyzes screen content"""
    
    def __init__(self):
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
    def capture_screen(self, region=None, save=False) -> Image.Image:
        """
        Capture screen or region
        
        Args:
            region: (x, y, width, height) or None for full screen
            save: Save screenshot to file
        
        Returns:
            PIL Image object
        """
        try:
            if region:
                x, y, w, h = region
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
            else:
                screenshot = pyautogui.screenshot()
            
            if save:
                filename = self.screenshot_dir / f"screenshot_{len(list(self.screenshot_dir.glob('*')))}.png"
                screenshot.save(filename)
                logger.info(f"Screenshot saved: {filename}")
            
            return screenshot
        except Exception as e:
            logger.error(f"Failed to capture screen: {e}")
            return None
    
    def ocr_screen(self, image: Image.Image = None) -> str:
        """
        Extract text from screen using OCR
        
        Args:
            image: PIL Image object, if None captures current screen
        
        Returns:
            Extracted text
        """
        try:
            if image is None:
                image = self.capture_screen()
            
            text = pytesseract.image_to_string(image, lang='eng+ara')
            logger.info(f"OCR extracted {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
    
    def detect_ui_elements(self, image: Image.Image = None, threshold=0.7) -> list:
        """
        Detect buttons, text fields, and other UI elements
        
        Args:
            image: PIL Image object
            threshold: Detection confidence threshold
        
        Returns:
            List of detected elements with coordinates
        """
        try:
            if image is None:
                image = self.capture_screen()
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Detect edges
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            elements = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 20 and h > 20:  # Filter small noise
                    elements.append({
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h,
                        'center_x': x + w // 2,
                        'center_y': y + h // 2
                    })
            
            logger.info(f"Detected {len(elements)} UI elements")
            return elements
        except Exception as e:
            logger.error(f"UI detection failed: {e}")
            return []
    
    def find_text_in_screen(self, text: str, threshold=0.6) -> list:
        """
        Find specific text on screen
        
        Args:
            text: Text to find
            threshold: Match threshold
        
        Returns:
            List of coordinates where text is found
        """
        try:
            image = self.capture_screen()
            extracted_text = self.ocr_screen(image)
            
            # Simple text matching
            positions = []
            lines = extracted_text.split('\n')
            
            for line in lines:
                if text.lower() in line.lower():
                    positions.append(line)
            
            logger.info(f"Found '{text}' in {len(positions)} locations")
            return positions
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return []
    
    def highlight_region(self, image: Image.Image, x: int, y: int, w: int, h: int, color=(255, 0, 0)) -> Image.Image:
        """
        Highlight a region in image for debugging
        
        Args:
            image: PIL Image object
            x, y, w, h: Region coordinates
            color: RGB color
        
        Returns:
            Modified image
        """
        draw = ImageDraw.Draw(image)
        draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
        return image
    
    def wait_for_element(self, element_name: str, timeout=10) -> bool:
        """
        Wait for an element to appear on screen
        
        Args:
            element_name: Name/text of element to find
            timeout: Maximum wait time in seconds
        
        Returns:
            True if element found, False otherwise
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            image = self.capture_screen()
            text = self.ocr_screen(image)
            
            if element_name.lower() in text.lower():
                logger.info(f"Element '{element_name}' found")
                return True
            
            time.sleep(0.5)
        
        logger.warning(f"Element '{element_name}' not found after {timeout}s")
        return False

screen_vision = ScreenVision()
