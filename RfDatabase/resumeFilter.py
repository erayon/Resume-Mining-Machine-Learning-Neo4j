import subprocess
import re
import numpy as np
import pandas as pd
from os import path
import sys

sys.path.append(path.abspath('../util'))

from CleanResume import *
from matchingTerm import *

pdf_loc  = "../example/"

cleanR            = pdf2CleanResume(pdf_loc)
basictab          = extract_basic_table(cleanR)
prgtab            = extract_programing_language_table(cleanR)
qualifiactionatab = extract_qualification_table(cleanR)
