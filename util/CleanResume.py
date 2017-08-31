import os
import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
import subprocess
import re
import numpy as np
from tqdm import tqdm
import pandas as pd

def plan_text(path):
    '''
    Return in lower case 
    
    '''
    proc = subprocess.Popen(['pdf2txt.py',path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    temp=proc.communicate()[0]
    temp = temp.decode("utf-8") 
    cleanText = re.sub("\n", "", temp)
    cleanText =cleanText.lower()
    return cleanText



def pdf2CleanResume(directory):
	""" directory is the location of all Resume in PDF format.
	for example: ./ResumePdf/ 

	Return is the Clean Resume format as a plan text

	"""
	DEBUG =False
	directory=directory
	l = []
	for file in os.listdir(directory):
		fl = directory + file
		if DEBUG : print (fl)
		l.append(fl)
	# the os.listdir function do not give the files in the right order 
	#so we need to sort them
	l=sorted(l)
	clean_resume=[]
	for i in tqdm(range(len(l))):
		clean_resume.append(plan_text(l[i]))

	return clean_resume