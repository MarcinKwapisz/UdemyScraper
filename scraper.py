from bs4 import BeautifulSoup
import requests
import sys
import time

# wykop
page = requests.get('https://www.wykop.pl/tag/kursyudemy/')
soup = BeautifulSoup(page.content, "html.parser")
link = soup.find("li", { "class" : "iC" })
numer = link.find("div")
last_id = numer['data-id']
plik = open("spr.txt","r+")
check = plik.read()
if check == last_id:
	plik.close()
	sys.exit("Nic nowego")
else:
	plik.seek(0)
	plik.truncate()
	plik.write(last_id)
	plik.close()
klucze= ["python","sql","php","it","jquery","security","master","program","linux","business","microsoft","amazon","finan","dev","android","swift","ios","hack","coding","game","adobe","web","bootcamp","command","unity","website","windows","c++","ruby","design","admin","workflow","css","html","cisco","siec","shell","root","cad","aws","network","server","ccna","git","protect","java","ajax","json","js","iphone","code","product","machine","arduino","data","analys","sale","digital"]
lista = []
temp=[]
for x in link.find_all("a", href=True):
	if "https://www.udemy.com/" in x["href"]:
		temp.append((x["href"]))
for y in temp:
	for z in klucze:
		if z in y:
			if y in lista:
				pass
			else:
				lista.append(y)
# for x in lista:
# 	print(x)
sesja = requests.Session()
logrequest = sesja.get("https://www.udemy.com/join/login-popup/")
url = "https://www.udemy.com/join/login-popup/"
logowanie = BeautifulSoup(logrequest.content, "html.parser")
input = logowanie.find('form', {"class" : "signin-form dj"})  # przygotowywuje do wyciagniecia tokenu csrf
csrf = ((logowanie.find('input',{'name' : 'csrfmiddlewaretoken'}))['value']) # wyciaga token csrf
logdata = {'email': '########', 'password': '#########', 'csrfmiddlewaretoken': csrf} #przygotowywuje dane do logowania
sesja.post(url,data=logdata, headers={'referer': url})
for kurs in lista:
	try:
		page = sesja.get(kurs) #zaczyna sesje
		soup = BeautifulSoup(page.content, "html.parser") #wyciaga dane ze strony
		# print(soup.prettify()) #wyswietla strone
		nazwa_kursu = (soup.find('h1', {'class' : 'clp-lead__title'})).text #zapisuje nazwe kursu
		cena = soup.find("span", {"class" : "price-text__current"}) #zapisuje cene
		free = "free"
		if "Bezpłatny" in cena.text:
			free = "Bezpłatny"
		print (nazwa_kursu)
		print (cena.text)
		if free in cena.text: #jezeli darmo to biere #cebula
			button = soup.find("a", {"data-purpose" : "buy-this-course-button"}) #zapisuje przycisk ktorym mozna sie zapisac
			zapisz = "https://www.udemy.com"+button["href"] # sklada link do zapisu
			dolacz = sesja.get(zapisz) # nawiazuje polaczenie z linkiem do zapisu
			print ("dodano - "+ nazwa_kursu+"\n")
			time.sleep(3)
		else:
			print("Za pozno - "+ nazwa_kursu+"\n")
			time.sleep(3)
	except AttributeError:
		print("nie udalo sie - "+nazwa_kursu+"\n")
		time.sleep(3)
	except TypeError:
		# print(strona1.prettify())
		time.sleep(3)
		
