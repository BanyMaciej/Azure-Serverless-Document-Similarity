## PROJEKT
### LINGARO x Bany Maciej x Krupińska Izabela
### Serverless real-time document similarity engine using Python and Azure Functions
### Cel projektu
Celem projektu było stworzenie silnika wyszukującego podobne artykuły z Wikipedii do zadanego tytułu lub adresu url bazowego dokumentu Wikipedii.
Projekt zakładał przetestowanie i wdrożenie komponentów Azure, głównie Azure Functions i Azure Blob Storage.

### Rozwiązanie i funkcjonalności
Rozwiązanie zostało oparte na chmurze Azure i wykorzystuje serwisy Azure Table Storage, Azure Blob Storage, Azure Functions.

Silnik został obudowany w statycznej stronie web, która jest hostowana za pomocą Azure Blob Storage.

Ze stworzonej wyszukiwarki można korzystać podając tytuł bądź adres url. Podane dane są przesyłane do Azure Function, w której scrapowany jest pierwszy akapit treści (nagłówek) danego artykułu. Następnie treść jest oczyszczana oraz przekazywana do pobieranych z Blob Storage Modeli (doc2vec oraz logistic regression). Na tej podstawie określana jest kategoria artykułu i zwracany podobny wynik. Dane wyświetlane są w tabeli z nazwami tytułów jako linki do WIkipedii oraz pierwszymi 100 znakami nagłówka artykułu.

### Diagram architektury
Poniżej znajduje się diagram architektury projektu. Dane są pobierane z Wikipedii, przygotowywane do modelu, następnie odbywa się trening sieci. Model zostaje zapisany w Azure Blob Storage. Ostateczny wynik uzysuje się w przygotowanej przeglądarce Wikipedia Similarity Engine. Wpisane zadanie trafia do Azure Function, z której dostajemy wynik końcowy.
<img src="azDiagram3.png" width = 600> 

Przepływ projektu można podzielić na trzy główne części:
* web scrapping i przygotowanie danych,
* stworzenie modelu,
* dostarczenie usługi
jak pokazano na poniższym diagramie.
<img src="azDiagram4.png" width = 600> 

#### Web Scrapping and Data Preparation

#### Modeling

#### Live serving


### Instrukcja reprodukcji rozwiązania


### Ngranie video 
Po tym linkiem można znaleźć prezentację naszego projektu: https://youtu.be/5TFOnCP0Y_E.

Link do rozwiązania: https://asdsstorageaccount.z6.web.core.windows.net/.

