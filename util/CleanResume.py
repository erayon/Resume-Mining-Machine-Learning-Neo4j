import os
import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
import subprocess
import re
import numpy as np
from tqdm import tqdm
import pandas as pd
from nltk.corpus import stopwords

stop = stopwords.words("english")

def plan_text(path):
	'''
	Return in clean plane text without stop words in it  /// 
	'''
	proc = subprocess.Popen(['pdf2txt.py',path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	temp=proc.communicate()[0]
	temp = temp.decode('ascii', errors='ignore') 
	cleanText = re.sub("\n", "", temp)
	document = " ".join([i for i in cleanText.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	cleanText=" ".join(sentences)
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
