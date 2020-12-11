
#Senor Data Parser
####Facultatea de Inginerie Mecanica si Mecatronica
#####Specializarea Robotica, grupa 542B


Proiect: https://sensor-data-parser.herokuapp.com/

Surse: https://github.com/etrandafir93/sensor-data-parser

SwaggerUI: https://sensor-data-parser.herokuapp.com/swagger/



##Introducere
	
Se cerea realizarea unei aplicatii desktop care sa faciliteze parsarea unor fisiere csv ce contineau datele inregistrate de la diversi senzori si analizarea acestora.
O alta functionalitate a aplicatiei era sa permita comunicarea cu un microcontroller pe serial.

Alegerea limajului de programare si a librariilor folosite a fost lasata la latitudinea studentului – cu mentiunea ca se va folosi un limbaj de prgramare orientata pe obiect (ex.: Python, Java).
Pentru puncte bonus, aplicatia trebuia sa permita comunicarea printr-un port TCP, sa aiba o interfata grafica sis a faciliteze comunicarea cu un microcontroller.



##Solutie proprie

•	**Python**

Am ales sa folosesc Python ca limbaj de programare, deoarece il consider mai potrivit pentru proiecte de tip POC (Proof Of Concept), la care se lucreaza in echipe mici / un singur programator. 
Desi codul nu este la fel de decuplat, mentenabil si testabil ca si in Java,  viteza de scriere net superioara a consituit un plus in luarea acestei decizii.

•	**Web**

Deoarece una din cerinte era permiterea comunicarii prin port TCP cu aplicatia, am decis sa o construiesc ca pe un serviciu REST care va permite requesturi HTTP – asa ca am folosit frameworkul Flask (https://flask.palletsprojects.com/en/1.1.x/quickstart/#) pentru acest task.

Intre punctele bonus se afla si realizarea unei interfete grafice. Avand in vedere ca imi construisem deja aplicatia ca un serivciu REST care primea fisierul csv si returna imaginile cu graficele in base64, am decis ca cel mai simplu mod de a le afisa ar fi sa creez o pagina web simpla care sa execute aceste requesturi si sa afiseze rezultatele. Aceasta pagina ar putea fi servita local de aplicatie.

Apoi am realizat ca pe platforma Heroku (www.heroku.com) exista o optiune pentru a hosta gratis o varietate de aplicatii, rintre care si aplicatii de Python – construite cu Flask, asa ca am uploadat aplicatia acolo (https://sensor-data-parser.herokuapp.com/).

Chiar daca este un website, aplicatia poate fi pornita ca aplicatie desktop, folosind scriptul start.bat, sau ruland urmatoarea comanda in linia de comanda :
 ```
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --app=http://sensor-data-parser.herokuapp.com/
```

•	**Componente**

Clasa SensorData se ocupa de prelucrarea datelor de la sezori – aceasta va  returna datele necesarepentru genearrea graficelor.

Clasa ChartGenerator se ocupa cu generarea graficelor ca imagini encodate in base64, cu salvarea lor in fisiere text si cu citirea si returnarea lor in functie de un nume unic.
Restul metodelor se ocupa de interceptarea requesturilor si returnarea raspunsurilor adecvate.

•	**Application Flow – Chart Generator**
Punctele de intrare in aplicatie sunt endponturile din imagine:
 
 ```
@app.route('/csv_data/text', methods=['POST'])
def parse_csv_text():
    ....

@app.route('/csv_data/file', methods=['POST'])
def parse_csv_file():
    ....
```
 
Acestea citesc continutul fisierului ca text (daca nu este trimis deja ca text si apeleaza metoda ‘on_csv_data’). 
Aceasta metoda creeaza un obiect de tip SensorData pe baza continutului fisierului csv si foloseste aceasta instanta pentru a creea graficele cu ajutorul unei instante de ChartGenerator.
De asemenea, in acest moment se genereaza un nume random de 10 caractere. Acesta va fi returnat ca si cheie a acestui set de date si va fi folosit la salvarea graficelor pe disk.
 
Raspunsul intors de aceste endpointuri este generat de metoda generate_links_response si va continue un dictionar cu link-uri catre resurele create.
 
In acest moment, clientul poate face un GET request la oricare din aceste link-uri pentru a primi graficele encodate in base64 sau elemental html catre trebuie introdus in pagina web pentru a le randa.
Metodele pentru returnarea graficelor nu fac altceva decat sa citeasca graficul potrivit folosnf cheia unica sis a il intoarca in formatul adecvat.
 


•	**Application Flow – Microcontroller Communication**

Pentru comunicarea cu microcontroller-ul am folosit un Arduino uno pe care am  incarcat un sketch ce simuleaza preluarea datelor de la niste senzori. 
Codul poate fi gasit in fisierul Arduino/schetch.ino

Scriptul serial.py citeste valorilede la microcontroller, parseaza acest format si le salveaza intr-un fisier csv asemanator cu cel primit ca exemplu.

 
 


## Testare

Pentru facilizarea testarii am pus la dispozitie o colectie de requesturi care poate fi importata in Postman pentru a verifica serviciul.

De asemenea, interfata aplicatiei poate fi vazuta/testat si folosind link-ul pentru SwaggerUI (https://sensor-data-parser.herokuapp.com/swagger/)

Cel mai simplu mod de a testa aplicatia si a verifica rezultatele, insa, este folosind pagina home – fie incarcand un fisier csv propriu sau folosid datele de test si apoi apasand pe butonul “Analyze Data”.



## Concluzii

Momentan toate graficele generate sunt salvate pe server, cee ace nu este efficient. Ar fi nevoie de un fir de executie separat care sa verifice periodic sis a stearga fisierele mai vechi de un anumit numar de zile.

O solutie si mai buna ar fi salvarea datelor din csv intr-o baza de date sub un id unic (cheia setului de date care va fi generate si returnata de server) si generarea graficelor si returnarea lor la fiecare request de tip GET, pe baza cheii trimise.

Alta posibila imbunataire ar fi parsarea dinamica a fisierelor, fara a tine cont de  o structura prestabilta (ex: temp1, temp2, temp3… etc). Aceasta solutie ar putea genera grafice pe orice fisier csv de intrare. Aditional se pot adauga parametri care sa specific timpul de grafic si coloanele luate in considerare. (ex: ip:port/barchart?cols=[1,2,3,5]&rowFrom=1&rowTo=55)
 