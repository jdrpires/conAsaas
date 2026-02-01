import logging
import sys
from app.core.config import get_settings


def setup_logging():
    settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    return logging.getLogger("conassas")


logger = setup_logging()
