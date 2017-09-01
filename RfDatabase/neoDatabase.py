from os import path
import sys
import re
import numpy as np
from tqdm import tqdm
import pandas as pd
from time import sleep
import getpass
from py2neo import authenticate, Graph, Node, Relationship

sys.path.append(path.abspath('../util'))

from CleanResume import *
from matchingTerm import *

pdf_loc  = "../example/"

uname = input("username: ")
passw = getpass.getpass(uname+" password: ")

try:
	authenticate("localhost:7474",uname,passw)
	# connect to authenticated graph database 
	graph = Graph("http://localhost:7474/db/data/") # create instances of a Graph() class 
	graph.delete_all()
	print("Extract information from sample Resume!")
	cleanR = pdf2CleanResume(pdf_loc)
	print("Extraction Done!")

	#######################################################
	
	def create_node(types,namex):
		node_ =[]
		for i in types:
			nodex = Node(namex,name=i)
			graph.create(nodex)
			node_.append(nodex)
		return node_

	def create_realtionship(nodeId,targetNode,nameOfRelation,Qlist,cleanR):
		for i in tqdm(range(len(cleanR))):
			for k in range(len(Qlist)):
				term = term_match(cleanR[i],Qlist[k])
				if term!=0:
					rel = Relationship(nodeId[i],nameOfRelation,targetNode[k])
					graph.create(rel)
					sleep(0.1)

	#######################################################

	print("create Node corresponding to no of application of resume")
	print(" based on some ID = 0 ")

	total_no   = len(cleanR)
	prg_lng    = ['c','c++','java','python','php','sql','javascript','c#','perl','ruby','matlab','r','hadoop']
	Genrate_ID = ["Id-"+str(i) for i in range(total_no)]
	qualify_   = ['msc','mtech','mca','mba','btech','bsc','bca']
	basic      = ['machine learning','analytics','exp']

	print("Node create of applicant and features! ")

	nodeId      = create_node(Genrate_ID,"ID_no") 
	nodePrg_lng = create_node(prg_lng,"Progrming_language")
	nodeQualify = create_node(qualify_,"Qualification")
	nodeBasic   = create_node(basic,"basicQuality")


    ########################################################
	print("Done!")
	print("Find relationship among entity based on features: ")
	
	# define pattern : 
	
	Qualification_pat = [r'(msc|m.sc)',r'(mtech|m.tech|\sme\s|"m.e")',r"\smca\s",r"\smba\s",r'(btech|b.tech|\sbe\s|"b.e")',r'(bsc|b.sc)',r'(bca|b.c.a)']
	Progrming_pat     = prg_lng
	Basic_pat         = [r"machine learning",r"analytics",r'experience']


	create_realtionship(nodeId,nodePrg_lng,"know_language",Progrming_pat,cleanR)
	create_realtionship(nodeId,nodeQualify,"Qualification_is",Qualification_pat,cleanR)
	create_realtionship(nodeId,nodeBasic,"knows",Basic_pat,cleanR)

	print("Done Create Database! ")


except KeyError:
	print("Enter Proper userId or Password! status.Unauthorized: http://localhost:7474/db/data/")
