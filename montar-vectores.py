#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import io
import sys
import csv
#reload(sys)
#sys.setdefaultencoding('utf8')

#source of problem, order of files 1. lista 2.csv
#we have lista_adjs, for the list that is the bow
# dict_frecuencia where we store absolute frequency of every word in the text file
# vector, that it is the filled bow for every text file
lista_adjs = []
dict_frecuencia = {}
vector = []

# function to fill in dict_frecuencia
def omplim_dict_frecuencia(namefilecsv,dict_frecuencia):
    with io.open(namefilecsv, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
          if row == '\n': 
             print("Fitxer buit")
          else:
             palabra = row[0]
             frecuencia = row[1]
             line_count += 1
             dict_frecuencia[palabra] = frecuencia

# function to fill in lista_adjs    
def omplim_llista_adjs(namefileadjs,lista_adjs):
   with io.open(namefileadjs, mode='r', encoding='utf8') as file:
        for uno in file:
           if uno  == '\n': 
                print("buida")
           else:
                #print(uno.rstrip('\n'))
                lista_adjs.append(uno.rstrip('\n'))

# function to create the bow vector
def al_vector(dict_frecuencia,lista_adjs,vector):
        for adjetivo in lista_adjs:
                #el orden tiene que ser el de lista
                #recuperemos el valor
                esta = dict_frecuencia.get(adjetivo)
                if esta:
                  #print(adjetivo)
                  valor = dict_frecuencia[adjetivo] 
                  #print("este es el valor del adjetivo en el dicc " + valor)
                  vector.append(valor)
                else:
                  #print(adjetivo + " no esta")
                  vector.append('0')
#fuction to write a file vectorarff with the vectors of different files
def pinta_vector(vector,clase,namefilecsv):
  vector.append(namefilecsv)
  #print(vector)
  contar_lineas = len(vector)
  #print(str(contar_lineas) + "antes")
  with open('vectorarff', 'a') as file:
        for valor in vector:
            #print(str(contar_lineas) + "antes")
            if contar_lineas > 1 :
               file.write(valor)
               file.write(',')
               contar_lineas = contar_lineas - 1
               #print(contar_lineas)
            else:
               #print(contar_lineas)
               file.write(valor)
               file.write(',')
               file.write(clase)
               file.write("\n")
               file.close() 

### we can work with a number of files (remember the class!!)
def main():
        if (len(sys.argv) != 4):
                print("Error, we need in this order: list of adjectives for the BoW, frequency file (as csv), and the class of the file: either deceptive non_deceptive.")
                print("Example: python listaAdjs.txt Pbo1.csv")
                sys.exit(1)

        # open files
        namefileadjs = sys.argv[1]
        namefilecsv  = sys.argv[2]
        clase        = sys.argv[3]

        print("Starting filling lista_adjs")
        omplim_llista_adjs(namefileadjs,lista_adjs)
        print("Starting filling dict_frecuencia")
        omplim_dict_frecuencia(namefilecsv,dict_frecuencia)
        print("Creating the vector")
        al_vector(dict_frecuencia,lista_adjs,vector)
        print("Printing the vector " + clase)
        pinta_vector(vector,clase,namefilecsv)

#call main
main()

### cosas que demuestran que hay entradas.
cuantas_en_diccionario = len(dict_frecuencia)
cuantas_en_lista_adj = len(lista_adjs)
cuantas_en_vector = len(vector)
 
#print cuantas_en_diccionario
#print cuantas_en_lista_adj
#print cuantas_en_vector

#aver = lista_adjs[6]
#aver = dict_frecuencia['ajeno'] #pero si no esta se rompe.
#print "esto es " +  aver

#namefileadjs = raw_input("Enter a adjs file: ")
#namefileadjs = "listaAdj.txt" 

