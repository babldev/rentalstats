import os
import sys

# Get rentalstats module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
from rentalstats import crawler

crawler.crawl()
