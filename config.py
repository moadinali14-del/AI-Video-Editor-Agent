"""
Configuration management for AI Video Editor Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent
    PROJECTS_DIR = BASE_DIR / "projects"
    MEDIA_DIR = BASE_DIR / "media"
    LOGS_DIR = BASE_DIR / "logs"
    CACHE_DIR = BASE_DIR / "cache"
    
    # Create directories if they don't exist
    for dir_path in [PROJECTS_DIR, MEDIA_DIR, LOGS_DIR, CACHE_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # AI Configuration
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")
    AI_MODEL = os.getenv("AI_MODEL", "qwen2.5")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Kdenlive Configuration
    KDENLIVE_PATH = os.getenv("KDENLIVE_PATH", "kdenlive")
    KDENLIVE_TIMEOUT = int(os.getenv("KDENLIVE_TIMEOUT", "30"))
    
    # FFmpeg Configuration
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
    FFPROBE_PATH = os.getenv("FFPROBE_PATH", "ffprobe")
    
    # Application Settings
    APP_TITLE = os.getenv("APP_TITLE", "AI Video Editor Agent")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Video Export Settings
    DEFAULT_EXPORT_FORMAT = os.getenv("DEFAULT_EXPORT_FORMAT", "mp4")
    DEFAULT_EXPORT_QUALITY = os.getenv("DEFAULT_EXPORT_QUALITY", "high")
    DEFAULT_FPS = int(os.getenv("DEFAULT_FPS", "30"))
    
    # Screen capture settings
    SCREENSHOT_QUALITY = 95
    SCREENSHOT_FORMAT = "png"
    
    # OCR settings
    ENABLE_OCR = True
    OCR_LANGUAGE = "eng+ara"  # English and Arabic
    
    # Timeout settings (in seconds)
    ACTION_TIMEOUT = 10
    VERIFICATION_TIMEOUT = 5
    IMPORT_TIMEOUT = 30
    EXPORT_TIMEOUT = 120
    
    # Supported media formats
    VIDEO_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
    IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"}
    AUDIO_FORMATS = {".mp3", ".wav", ".aac", ".flac", ".m4a", ".wma"}
    
    # Application UI Settings
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    THEME_COLOR = "#1e1e1e"
    ACCENT_COLOR = "#00d4ff"

config = Config()
