import os

from dotenv import load_dotenv
from pathlib import Path

from functions import getDocumentsClaim

dotenv_path = Path('C:\scraping\scrapingGenerali.env.development')
load_dotenv(dotenv_path=dotenv_path)

getDocumentsClaim.RevoveInitialFolderDownload(os.getenv('MAPFOLDER'))
