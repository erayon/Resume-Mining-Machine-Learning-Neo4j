import os
import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
import subprocess
import re
import numpy as np
from tqdm import tqdm
import pandas as pd


def term_match(string_to_search, term):
    """
    A utility function which return the first match to the `regex_pattern` in the `string_to_search`
    :param string_to_search: A string which may or may not contain the term.
    :type string_to_search: str
    :param term: The term to search for the number of occurrences for
    :type term: str
    :return: The first match of the `regex_pattern` in the `string_to_search`
    :rtype: str
    """
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return result[0]
    except:
        return 0


def extract_basic_table(l):
    """
    param l : cleantext 
    based on match criteria : ['email','phone_no','machine learning','analytics','exp']
    Return  : pandas dataframe
    """
    basic=['email','phone_no','machine learning','analytics','exp']
    hold=[]
    for i in tqdm(range(len(l))):
        email              = term_match(l[i],r'[\w\.-]+@[\w\.-]+')
        phone              = term_match(l[i],r"([+]\d{12}|\d{10})")
        ml                 = term_match(l[i],r"machine learning")
        analytics          = term_match(l[i],r"analytics")
        exp                = term_match(l[i],r'experience')
        hold.append([email,phone,ml,analytics,exp])
    df1 = pd.DataFrame(hold,columns=basic)
    return df1


def extract_programing_language_table(l):

    """
    param l : cleantext 
    based on match criteria : ['c','c++','java','python','php','sql','javascript','c#','perl','ruby','matlab','r','hadoop']
    Return  : pandas dataframe
    """
    prg_lng = ['c','c++','java','python','php','sql','javascript','c#','perl','ruby','matlab','r','hadoop']
    pd.options.mode.chained_assignment = None
    ind = np.arange(len(l))
    df_ = pd.DataFrame(index=ind,columns=prg_lng)
    df_ = df_.fillna(0) # with 0s rather than NaNs
    for i in tqdm(range(len(l))):
        for k in range(len(prg_lng)):
            pat = r"\W"+prg_lng[k]+r"\W"
            df_[prg_lng[k]][i]=term_match(l[i],pat)
    return df_



def extract_qualification_table(l):

    """
    param l : cleantext 
    based on match criteria : ['msc','mtech','mca','mba','btech','bsc','bca']
    Return  : pandas dataframe
    """

    qualification = ['msc','mtech','mca','mba','btech','bsc','bca']
    hold=[]
    for i in tqdm(range(len(l))):
        msc                = term_match(l[i],r'(msc|m.sc)')
        mtech              = term_match(l[i],r'(mtech|m.tech|\sme\s|"m.e")')
        mca                = term_match(l[i],r"\smca\s")
        mba                = term_match(l[i],r"\smba\s")
        btech              = term_match(l[i],r'(btech|b.tech|\sbe\s|"b.e")')
        bsc                = term_match(l[i],r'(bsc|b.sc)')
        bca                = term_match(l[i],r'(bca|b.c.a)')
        hold.append([msc,mtech,mca,mba,btech,bsc,bca])
    df1 = pd.DataFrame(hold,columns=qualification)
    return df1
