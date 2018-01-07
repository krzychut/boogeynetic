# -*- coding: cp1250 -*-
import linecache

global DEBUG
DEBUG = True

global esc
esc = 27
global m_key
m_key = ord('m')
global n_key
n_key = ord('n')
global b_key
b_key = ord('b')
global q_key
q_key = ord('q')
global v_key
v_key = ord('v')

#TODO: tutaj beda wszystkie ustawienia wczytywane z jakiegos pliku txt

#KLASA OBSLUGUJACA PODSTAWOWE PARAMETRY
class Parameters:
    def __init__(self,data):
        self.n=0 #liczba wezlow
        self.pop_count=0#liczba populacji
        self.map='terrain.png'#lokalizacja mapy
        self.file=data#lokalizacja danych
        self.beta=0#beta rozk�ady wyk�adniczego
        self.top_percent = 1
        self.crossingF='pathMean' #wektor operatorów
 #---------------------------------------------------------------------
    def getNodNum(self,num):   #pobiera liczbe wezlow
        self.n=num
    def getNodNumKeypad(self):    #pobiera liczbe wezlow z klawiatury
        self.n=input('Podaj liczb� w�z��w: ')
 #-------------------------------------------------------------------
    def getPopNum(self,num):   #pobiera liczbe populacji
        self.pop_count=num
    def getPopNumKeypad(self):    #pobiera liczbe populacji z klawiatury
        self.pop_count=input('Podaj liczb� populacji: ')
#--------------------------------------------------------------------
    def getMapAdr(self,num):   #pobiera lokalizacje mapy
        self.map=num
    def getMapAdrKeypad(self):    #pobiera lokalizacje mapy z klawiatury z klawiatury
        _map=input('Podaj lokalizacje: ')
        self.map=_map
  #-------------------------------------------------------------------------
    def getBeta(self,num):   #pobiera bete
        self.beta=num
    def getBetaKeypad(self):    #pobiera bete z klawiatury
        self.beta=input('Podaj bete: ')
#-------------------------------------------------------------------------

    def getcrossingF(self,num):   #pobiera wektro operatorów krzyzowania
        self.crossingF=num
    def getcrossingFKeypad(self):    #tu nie wiem jak sie podaje te dict ~michalek
        self.crossingF=input('Podaj Funkcje krzyzowania: ')

  #------------------------------------------------------------------------
    def NumOfPack(self):#zwraca ilosc zestaw�w danych
        count = len(open(self.file, 'rU').readlines())
        count=count-2
        return count
    def SetPack(self,number):#ustawia zestaw parametr�w z pliku
        wiersz = linecache.getline(self.file, number+2)
        str_vec=wiersz.split(' ')
        self.n,self.pop_count,self.map,self.beta,self.top_percent=str_vec[0:5]#pierwsze 5 parametrów wczytane
        self.crossingF=str_vec[5:]#pozostałe elementy czyli wektor operatorow krzyzowania plu 'END'
        del self.crossingF[-1]#usuwanie 'END'
        l=len(self.map)
        self.map=self.map[1:l-1]
        self.n=int(float(self.n))
        self.pop_count=int(float(self.pop_count))
        self.beta=int(float(self.beta))
        print self.crossingF[0:]

        return wiersz
