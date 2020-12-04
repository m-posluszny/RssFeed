import DataBase.connector
mydb = DataBase.connector.connect(
  wpisane_pole="Wpisz nazwe pola"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")
mycursor.execute("SHOW DATABASES")
sql = "SELECT * FROM URLHandler WHERE address ='wpisane_pole'"

mycursor.execute(sql)
myresult = mycursor.fetchall()

   #Odczytanie bazy
def odczytaj_baze():
   import DataBase.connector

mydb = DataBase.connector.connect(
  nazwa_pola="Nazwa danego pola"
  )

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM URLHandler) 

for x in myresult:
  print(x)

 
#Zapisanie czegoś w bazie
def zapisz_baze():
   lista = [""," - ",""]
   baza =sql 
   try:
       lista[0] = raw_input("Wpisz nazwe pola")
       print "Zapisuje do bazy"
       text = baza.writelines(lista)
   finally:
       baza.close()
   print "Zapisano"
  
menu = input("Wybierz pozycje z menu ")
if menu == 1:
   print odczytaj_baze()
elif menu==2:
   print zapisz_baze()
else:
   print "Nie wybrałeś odpowiedniej pozycji."
   
   
   
   
  