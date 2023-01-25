#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf8')


#General Comments
# I couldn't use a python library to process the XML files, as they are not correctly formatted:
# ExpatError: junk after document element: line 2, column 0
# In order to prevent this error I parse the file without using any XML library

# Example of how to call the script: 
# python FLtoBRAT.py /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/input-csv-lists/acro.csv /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/input-csv-lists/abbr.csv /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/input-csv-lists/symbol.csv /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/negation_iac_1_corr.xml /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/output-files/output1.ann

# Initialize the positive dictionary 
positiveDict = {}

# Initialize the negative dictionary 
negativeDict = {}

# the form of the dictionary is language;wordtobefound;rate
def fillPositiveDict(positiveDict, positiveCvsFile):
    # open the poistiveCvsFile file and read it using ";" as delimiter 
    with io.open(positiveCvsFile, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        # each line is an array
        for row in reader:
            i = 2
            while(i < len(row) -1):
                # for every position different to row[0]
                # if it contains a term, we add it to the dictionary
                if row[i].encode('utf-8') != '':
                    if row[1].encode('utf-8') in positiveDict:
                        positiveDict[row[1].encode('utf-8')].append(row[i].encode('utf-8'))
                    else:
                        positiveDict[row[1].encode('utf-8')] = [row[i].encode('utf-8')]
                    #print "We add " + row[0] + "\t" + row[i]
                    i += 1
                else: # otherwise, break the while
                    break

def fillNegativeDict(negativeDict, negativeCvsFile):
    # open the abbrevCvsFile file and read it using ";" as delimiter 
    with io.open(negativeCvsFile, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        # each line is an array
        for row in reader:
            i = 2
            while(i < len(row) -1):
                # for every position different to row[0]
                # if it contains a term, we add it to the dictionary
                if row[i].encode('utf-8') != '':
                    if row[1].encode('utf-8') in abbrevDict:
                        negativeDict[row[1].encode('utf-8')].append(row[i].encode('utf-8'))
                    else:
                        negativeDict[row[1].encode('utf-8')] = [row[i].encode('utf-8')]
                    #print "We add " + row[0] + "\t" + row[i]
                    i += 1
                else: # otherwise, break the while
                    break

                
def generateOutputFile(outputFile, inputXMLFreelingFile):
    # initialize function counters
    num = 1
    numterm = 1
    for line in inputXMLFreelingFile:
        #print line
        if (line.find("<token ") > -1):
            # split line using "\""
            lineSplit = line.split("\"")
            begin = lineSplit[3] # value for begin
            end = lineSplit[5] # value for end
            form = lineSplit[7].encode('utf-8') # value for form (must be read in 'utf-8')
            
            # 1.- we check if the form is in the positive dictionary
            if form in positiveDict.keys(): # if so
                class_value = "POSITIVE" # we specify the class_value to "POSITIVE" 
                # write the corresponding line to the output file 
                outputFile.write("T" + str(num) + "\t" + class_value + " " + begin + " " + end + "\t" + form + "\n")
                # we collect the terms associated to the acronym (lo dejo, pero no tendremos mas valores ..)
                terms = ''
                termNumberForAcronym = 1
                for term in positiveDict.get(form):
                    terms += term
                    if termNumberForAcronym < len(positiveDict[form]):
                        terms += ", "
                    termNumberForAcronym +=1
                # write the associated terms to the output file
                outputFile.write(unicode("#" + str(numterm) + "\t" + "AnnotatorNotes" + " " + "T" + str(num) + "\t" +  terms + "\n"))
                # update function counters
                num += 1
                numterm += 1
                
            # 2.- we check if the form is in the negative dictionary
            if form in negativeDict.keys(): #if si
                class_value = "NEGATIVE" # we specify the class_value to "NEGATIVE"
                # write the corresponding line to the output file
                outputFile.write("T" + str(num) + "\t" + class_value + " " + begin + " " + end + "\t" + form + "\n")
                # we collect the terms associated to the abbreviation
                terms = ''
                termNumberForAbbreviation = 1
                for term in negativeDict.get(form):
                    terms += term
                    if termNumberForAbbreviation < len(abbrevDict[form]):
                        terms += ", "
                    termNumberForAbbreviation +=1
                # write the associated terms to the output file
                outputFile.write(unicode("#" + str(numterm) + "\t" + "AnnotatorNotes" + " " + "T" + str(num) + "\t" +  terms + "\n"))
                # update function counters
                num += 1
                numterm += 1
                
       
        
def main():
     if (len(sys.argv) != 6):
         print "Error, we need the following arguments (in the same order): positive-cvs-file neegative-cvs-file  xml-Freeling-file output-file"
         print "Example: python FLtoBRAT.py positive-cvs-file negative-cvs-file  xml-Freeling-file output-file"
         sys.exit(1)
     
     # open input files. First the CVS files
     positiveCvsFile = sys.argv[1]
     negativeCvsFile = sys.argv[2]
    # symbolCvsFile = sys.argv[3]
     # then the xml file generated by freeling... he cambiado a valor 3 y 4
     inputXMLFreelingFile = io.open(sys.argv[3], 'r', encoding='utf8')
     # and finally open the outputfile 
     outputFile = io.open(sys.argv[4], 'w', encoding='utf8')
     
     print "Thanks for using the FLtoBRAT.py script! \n"
     print "IMPORTANT INFORMATION"
     print "This script assumes that all input files are encoded in \'utf-8\'"
     print "Please ensure that this is the case: otherwise the output file will not be correctly encoded \n"
     
     print "Starting the conversion from FL to BRAT file \n"
     
     print "Step 1: Load the list of positive words into a dictionary"
     fillPositiveDict(positiveDict, positiveCvsFile)
     print "Step 1 completed. Positive words correctly loaded\n"
     
     #for key, value in accroDict.iteritems() :
     #    print key, value
     
     print "Step 2: Load the list of negative words into a dictionary"
     fillNegativeDict(negativeDict, negativeCvsFile)
     print "Step 2 completed. Negative words correctly loaded\n"
     
     #for key, value in abbrevDict.iteritems() :
     #    print key, value
     
#     print "Step 3: Load the list of symbols into a dictionary"
#     fillSymbolDict(symbolDict, symbolCvsFile)
#     print "Step 2 completed. Symbols correctly loaded\n"
     
     #for key, value in symbolDict.iteritems() :
     #    print key, value
     
     print "Step 3: generating the output file..."
     generateOutputFile(outputFile, inputXMLFreelingFile)
     print "Step 3 completed. Output file generated"
     
     print "Bye"
    

#call main    
main()
