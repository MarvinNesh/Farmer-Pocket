import io
import re
import logging
from urllib.parse import urljoin
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from .extensions import db
from .models import Outbreak

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
