1. Informacje jak scrapowac w Wikipedii z robots.txt.

Wikipedia blokuje pewne znane boty, ale w ogólności pozwala na scrapowanie. Nas obowiązuje sekcja ostatnia, zaczynająca się od “User-agent:”. Pozwalają kontaktować się przez API, ale możliwe jest też bezpośrednie pobieranie html z url (takiego samego jak w przeglądarce). 
Najważniejszym aspektem jest mała agresywność crawlera - powinien odpytywać o kolejne artykuły z odstępami czasowymi. Wikipedia nie określa konkretnej wartości opóźnień, ale znany bot Inktomi's "Slurp" często używa domyślnej wartości 15s - może warto więc taką samą wartość zastosować.

2. Ustawienie środowiska AF lokalnie

Zainstalowanie Visual Studio Code z rozszerzeniami Python i Azure Functions. Dodatkowo doinstalowanie przez npm modułu azure-functions-core-tools. Postępować zgodnie z tutorialem:
https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-01
Napotkaliśmy kilka problemów. Udało nam się odnaleźć ich przyczyny.
Należy mieć zainstalowaną wersję Pythona wcześniejszą niż 3.9 (3.6, 3.7 lub 3.8).
Do projektu funkcji może się pobierać Python z conda (jeśli mamy condę), należy pamiętać o tym i wybrać naszą odpowiednią wersję.
Należy zwrócić uwagę na bitową wersję Pythona. Powinna być 64-bit.

3. Przygotowanie danych (BS/parsing/genism/keras).

requests - biblioteka do prostego wywoływania zapytań http. Pozwala na wykonanie zapytania w jednej linii, bez potrzeby budowania zaawansowanych klientów. Dla naszego rozwiązania wystarczające.

BeautifulSoup4 - pozwala na parsowanie html i xml, a następnie wydobycie z nich danych. Pozwala na wyszukiwanie po id segmentu html (np. “firstHeading” dla tytułu na wikipedii) lub po tagu (np. pierwsze <p> w sekcji o id “bodyContent” dla pierwszego akapitu tesktu w wikipedii). Dzięki temu można będzie łatwo zdobyć całą treść artykułu (lub jego część) oczyszczoną z tagów html. Biblioteka dostępna jest w anacondzie.

Gensim/keras - biblioteki do ML, obie dostępne są w pakiecie anacondy.. Skupimy się na start na gensim, który pozwala w łatwy sposób stworzyć modele “embeddingu” dokumentów (następna sekcja). Dodatkowo jest to szybka biblioteka, oparta “pod spodem” o język C. 

4. Word to vec czy doc to vec?

Word2Vec - algorytm zamieniający słowa w specjalne wektory, dzięki którym można skategoryzować jego znaczenie. Pozwala na znalezienie słów o podobnym znaczeniu dzięki odległości kosinusowej między wektorami

Doc2Vec - działa na podobnej zasadzie jak Word2Vec, ale dla całych dokumentów. Dokumenty są zamieniane na znaczące, unikalne wektory. Takie wektory pozwalają na porównanie i kategoryzację tych dokumentów.

My decydujemy się na doc2vec.

5. Ilość artykułów + uzasadnienie.

Proponujemy kategorie: Animals, Sports, Painters, Instruments, Countries. Z każdej z nich wybierzemy po 15 artykułów. Dzięki temu uzyskamy bazę 75 dokumentów do nauczenia modelu. 
http://mlg.ucd.ie/datasets/bbc.html 
