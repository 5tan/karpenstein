import os
from openai import AzureOpenAI
from datetime import datetime

endpoint = os.environ.get("OPENAI_ENDPOINT")
model_name = "gpt-5.1"
deployment = "gpt-5.1"

subscription_key = os.environ.get("OPENAI_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

BOOK_CONTENTS = ""
with open("ocr.txt", "r", encoding="utf-8") as f:
    BOOK_CONTENTS = f.read()

response = client.chat.completions.create(
    stream=True,
    messages=[
        {
            "role": "system",
            "content": """
Podam tekst książki napisanej w języku niemieckim.
Tekst jest lekko zaburzony, ze względu na zastosowanie OCR.
Dodałem # i ## w celu zaznaczenia rozdziałów i podrozdziałów.

Przetłumacz tekst na język polski.

W podanym tekście mogą wystąpić numery stron. Nie załączaj ich, pomiń je.

Trudności w tłumaczeniu lub niejasności, dodaj komentarz w Markdown Blockquote (>) na końcu kadego z rozdziałów.

Zwróć całe tłumaczenie w jednej odpowiedzi.

Zastosuj następujące tłumaczenia nazw własnych:

# Osoby (nazwiska, imiona, tytuły)

- Dr. Karl Wehse – dr Karl Wehse  
- Kögler – Kögler (nazwisko, bez zmiany)  
- von Hochberg – von Hochberg (ród Hochbergów)  
- Scholz – Scholz  
- von Wiese – von Wiese  
- Schiﬀus (Schi>fus) – Schiﬀus (Schiﬀus)  
- Aelurius – Aelurius  
- Hayek-Sandel – Hayek-Sandel  
- Müller – Müller  
- Grünhagen – Grünhagen  
- Markgraf – Markgraf  
- Graf Stillfried-Rattonitz – hrabia Stillfried-Rattonitz  
- Schultz – Schultz  
- Pfotenhauer – Pfotenhauer  
- Luchs (Direktor Dr. Luchs) – dyrektor dr Luchs  
- Baron H. von Saurma-Jeltsch – baron H. von Saurma-Jeltsch  
- Johann (król czeski Jan Luksemburski) – król Jan Luksemburski  
- König Johann der Luxemburger – król Jan Luksemburski  
- Kaiser Karl IV. – cesarz Karol IV  
- König Wenzel IV. – król Wacław IV  
- König Sigismund – król Zygmunt  
- König Georg (von Podiebrad) – król Jerzy z Podiebradów
- Kaiser Ferdinand II / III – cesarz Ferdynand II / III  
- Kaiser Rudolph II – cesarz Rudolf II  
- Kaiser Karl VI. – cesarz Karol VI  
- Kaiser Leopold I – cesarz Leopold I  
- König Friedrich (Brandenburg-Bayreuth) – margrabia Fryderyk z Bayreuth
- Ladislaus (Ladislaus Postumus) – Władysław Pogrobowiec  

# Rodziny / rody szlacheckie i osoby:

- von Glubos / Glubocz / Gloubus / Glubz (Glaubitz) – ród von Glaubitz
- Thamo (Tam, Thame, Thammo) von Glubos – Thamo von Glaubitz  
- Otto von Glubos – Otto von Glaubitz  
- Reinisch / Reinzo / Reinhard von Glubos – Reinisch (Reinhard) von Glaubitz  
- Nickel (Nikolaus) von Glubos – Mikołaj von Glaubitz  
- Jane von Glubz – Jan von Glaubitz  
- Bernhard von Schnallenstein (von Glubos) – Bernhard von Glaubitz na Schnallensteinie  
- Wolfram von Panewicz (Pannwitz) – Wolfram von Pannwitz  
- Tyczko von Pannewicz – Tyczko von Pannwitz  
- Otto Schüler (Schiler) – Otto Schüler (Schiller)  
- Tamo von Czechaw – Tamo von Czechau  
- Jeske von Horczicz – Jeske von Horczicz  
- Rupert und Jan von Glubos – Rupert i Jan von Glaubitz  
- Frizco von Talewitz (Dalwitz?) – Frizco von Talewitz (von Dalwitz)  
- Mersan von Parchowitz – Mersan von Parchowitz  
- Johann, Markgraf von Mähren – Jan, margrabia Moraw  
- Markgraf Jošt (Jodokus) von Mähren – margrabia Jošt (Jodok) Morawski  
- Konrad und Eberhard von Nymancz (Niemand, Niemitz) – Konrad i Eberhard von Niemitz  
- Familie Nimptsch (Nemcz) – ród von Nimptsch  
- Johann, Herzog von Troppau und Ratibor – Jan, książę Opawy i Raciborza  
- Stephan von Martinic, genannt Poduška – Stefan z Martinic, zwany Poduszka  
- Haßko von Waldstein – Haško von Waldstein  
- Marquard Ahrlik von Mezelezie – Marquard Ahrlik von Mezelezie  
- Hinko (Hynek, Heinrich) Krušina von Lichtenberg (Lichtemburg), auch Brušna von Arnau – Hynek (Henryk) Krušina z Lichtenberka (Lichtemburga)  
- Anna, Herzogin von Auschwitz – Anna, księżna Oświęcimska  
- Anna von Kolditz – Anna z Kolditz  
- Thimo von Kolditz – Thimo von Kolditz  
- Puota (Potho) von Častolowitz – Puta z Czastolowic  
- Haßko von Waldstein – Haško z Waldsteina  
- Herzog Wilhelm von Troppau – książę Wilhelm z Opawy  
- Opitz von Czirne – Opitz z Čirne (Czirne)  
- Hermann Zettriß – Hermann Zettriß  
- Heinze Peterswalde – Heinze von Peterswalde  
- Sigmund von Rachenau – Zygmunt von Rachenau  
- Kunz von Rachenau – Kunz von Rachenau  
- Gott(s)che und Hans Schoff – Gottsche i Hans Schoff  
- Hain von Czirne – Hain z Čirne  
- Johann Kolda von Žampach (Ziampach) – Jan Kolda ze Žampachu  
- Georg von Geißler – Georg von Geißler  
- Bernhard von Haugwitz – Bernhard von Haugwitz  
- Sigmund von Kauffung – Zygmunt von Kauffung  
- Christoph von Zedlitz auf Alzenau – Christoph von Zedlitz na Alzenau  
- Caspar Unwirde, Hans Unwirde, Friedrich Unwirde – Kaspar, Hans, Fryderyk Unwirde  
- Georg von Breitenstein – Georg von Breitenstein  
- Ulrich Freiherr von Prušchenk, Graf von Hardegg – Ulrich wolny pan von Prušchenk, hrabia von Hardegg  
- Hans von Hardegg – Hans von Hardegg  
- Christoph von Hardegg – Christoph von Hardegg  
- Johann von Bernstein von Helfenstein – Johann von Bernstein von Helfenstein  
- Franz Kallmann – Franz Kallmann  
- Simon Schubert – Simon Schubert  
- Heinrich Haberland von Machtersen auf Bischofswaldau – Heinrich Haberland von Machtersen na Bischofswaldau  
- Kremer (Wiener Arzt) – Kremer, lekarz wiedeński  
- Oehmb (Arzt) – Oehmb  
- Burghart (Arzt, Autor) – Burghart  
- Sigmund Hoffman Freiherr von Leichtenstern – Sigmund Hoffman, wolny pan von Leichtenstern  
- Franz Weighard (Weihard) von Hoffman – Franz Weighard von Hoffman  
- Leopold Graf Hoffman von Leichtenstern – hrabia Leopold Hoffman von Leichtenstern  
- Michael Wenzel Reichsgraf von Althann – hrabia Michael Wenzel von Althann  
- Anna Maria Gräfin von Aspermont und Reheim – hrabina Anna Maria von Aspermont i Reheim  
- Michael Friedrich von Althann, Kardinal und Bischof von Waitzen – kardynał Michael Friedrich von Althann, biskup Vacu  
- Georg Olivier Graf von Wallis – hrabia Georg Olivier von Wallis  
- Peter Stephan Olivier von Wallis – hrabia Peter Stephan Olivier von Wallis  
- Friedrich Wilhelm Graf von Schlabrendorf – hrabia Friedrich Wilhelm von Schlabrendorf  
- Joseph Franz Bernhard von Mutius – Joseph Franz Bernhard von Mutius  
- Franz von Mutius – Franz von Mutius  
- Karl Ludwig Eugen von Mutius – Karl Ludwig Eugen von Mutius  
- Freiin Louise Friederike Antonie Franziska von Plotho, geb. von Mutius – baronówna Louise Friederike Antonie Franziska von Plotho z domu von Mutius  
- Louis Franz Wilhelm von Mutius – Louis Franz Wilhelm von Mutius  
- S. Saul (Hof-Agent) – S. Saul, agent dworski  
- Prinzessin Marianne der Niederlande – księżniczka Marianna Orańska
- Prinz Albrecht von Preußen – książę Albrecht Pruski  

# Inne osoby lokalne (urzędnicy, mieszczanie, chłopi, rzemieślnicy):

- Martin Schubert – Martin Schubert  
- Simon Breiter – Simon Breiter  
- Jakob Stanke – Jakob Stanke  
- Georg Schubert – Georg Schubert  
- Noßig – Noßig  
- Christoph Wolff / Wolf – Christoph Wolf(f)  
- Georg Wolff – Georg Wolf(f)  
- Gottfried Daniel – Gottfried Daniel  
- Anna Susanna Brachvogel, geb. Krauß – Anna Susanna Brach  vogel z domu Krauß  
- Christoph Schmid – Christoph Schmid  
- Jakob Straube – Jakob Straube  
- Barthel Straube – Barthel Straube  
- Christoph Volkmer – Christoph Volkmer  
- Georg Bartsch – Georg Bartsch  
- Hans Bartsch – Hans Bartsch  
- Martin Gottwald – Martin Gottwald  
- Franz Schiedek (Schiede>) – Franz Schiedek  
- Johann Reichbrodt – Johann Reichbrodt  
- Frau Rauek – pani Rauek  
- Herr von Bujakowsky – pan von Bujakowsky  
- Frau Palmer von Palmgarten, geb. Weilner – pani Palmer von Palmgarten z domu Weilner  
- Anna Theresia von Schenkendorf – Anna Theresia von Schenkendorf  
- Johann Heinrich von Schenkendorf – Johann Heinrich von Schenkendorf  
- Maria Rosina von Schenkendorf – Maria Rosina von Schenkendorf  
- Johann Joseph von Schenkendorf und Mühlgast – Johann Joseph von Schenkendorf i Mühlgast  
- Georg Schön – Georg Schön  
- Friedrich Junk – Friedrich Junk  
- Christian Häßen – Christian Häßen  
- Georg Stein – Georg Stein  
- Jakob Esche – Jakob Esche  
- Mikulaš (Mikulasch) – Mikulasz  
- Anna Mikulasch – Anna Mikulasz
- Jakob Jung – Jakob Jung  
- Ernst Meyhern – Ernst Meyhern  
- Hans Heynel – Hans Heynel  
- Martin Heynel – Martin Heynel  
- Sigmund Straube – Sigmund Straube  
- Ernst Straube – Ernst Straube  
- Hans Riedel – Hans Riedel  
- Joseph Riedel – Joseph Riedel  
- Herrmann von Ludwig – Herrmann von Ludwig  
- Robert von Ludwig – Robert von Ludwig  
- Caspar Gebhard – Caspar Gebhard  
- Johann Paul Gebhard – Johann Paul Gebhard  
- Hauß (Hau>) – Hauß  
- Hans Kristen / Christen – Hans Kristen  
- Jeremias Kristen – Jeremias Kristen  
- Melchior Kristen – Melchior Kristen  
- Heinrich Kristen – Heinrich Kristen  
- Johann Heinrich Kristen – Johann Heinrich Kristen  
- Joseph Kristen – Joseph Kristen  
- Bonifaz Kristen – Bonifaz Kristen  
- Wenzel Gottwald – Wenzel Gottwald  
- Martin Straube – Martin Straube  
- Michael Knauer – Michael Knauer  
- Barthel Mann – Barthel Mann  
- Martin Hauß – Martin Hauß  
- Anna Regina Mentzel – Anna Regina Mentzel  
- Johann Heinrich Mentel – Johann Heinrich Mentel  
- Johann Heinrich Kristen – Johann Heinrich Kristen  
- Joseph Lachnit – Joseph Lachnit  
- Amand Lachnit – Amand Lachnit  
- Joseph Kolak – Joseph Kolak  
- Emilie Wontorski, geb. Norak – Emilie Wontorski z domu Norak  
- Joseph Raschdorf – Joseph Raschdorf  
- Melan / Milan / Mühlan (rodzina) – Melan / Milan / Mühlan  
- Martin Melan – Martin Melan  
- Hans Mylan – Hans Mylan  
- Sigmund, Valten, Nykel (Milan) – Sigmund, Valten, Nykel Milan  
- Adam Mühlan – Adam Mühlan  
- Simon Milan – Simon Milan  
- Hans Mühlan – Hans Mühlan  
- Melchior Milan – Melchior Milan  
- Anton Mühlan – Anton Mühlan  
- Maria, córka Antona Mühlana – Maria Mühlan  
- Joseph Jlgner – Joseph Jlgner  
- Ignaz Ulrich – Ignaz Ulrich  
- Franz Sappelt – Franz Sappelt  
- Emanuel Koschel – Emanuel Koschel  
- August Buhl – August Buhl  
- Georg Ebel – Georg Ebel  
- Georg Säbisch – Georg Säbisch  
- Pollexina Püler – Pollexina Püler  
- Caspar von Schenkendorf – Caspar von Schenkendorf  
- Heinrich von Reibnitz – Heinrich von Reibnitz  
- Jakob Git(t)ner – Jakob Gittner  
- Hans Welpen – Hans Welpen  
- Gabriel von Hundt – Gabriel von Hundt  
- Sigmund Hoffman Freiherr von Leichtenstern – (już wyżej)  
- Franz Schmidt – Franz Schmidt  
- Franz Schubert – Franz Schubert  
- Johann Christoph Nissler – Johann Christoph Nissler  
- Georg Blaschke – Georg Blaschke  
- Dominicus Blaschke – Dominicus Blaschke  
- Joseph Winkler – Joseph Winkler  
- Ignaz Gottschalk – Ignaz Gottschalk  
- Joseph Gottschalk (starszy i młodszy) – Joseph Gottschalk  
- August Buhl – August Buhl  

# Duchowni:

- Andreas Schwartz, Pfarrer zu Schreindorf – Andreas Schwartz, proboszcz w Skrzynce (Schreindorf)  
- Pfarrer Tobias in Landeck – pastor Tobiasz w Lądku  
- Konrad, Bischof von Breslau – Konrad, biskup wrocławski  

# Regiony, krainy, państwa

- Graf(s)chaft Glatz – Hrabstwo Kłodzkie  
- Glatzer Land – Ziemia Kłodzka  
- Schlesien – Śląsk  
- Mähren – Morawy  
- Königreich Böhmen – Królestwo Czech  
- Herzogtum Schlesien – księstwo śląskie (w sensie ogólnym)  
- Markgrafschaft Mähren – margrabstwo Moraw  
- Königgrätzer Kreis – powiat/kraj kralovohradecki (dawny okręg Königgrätz)  
- Fürstentum Breslau – księstwo wrocławskie  
- Fürstentum Schweidnitz-Jauer – księstwo świdnicko-jaworskie  
- Fürstentum Münsterberg – księstwo ziębickie  
- Fürstentum Oels – księstwo oleśnickie  
- Fürstentum Liegnitz – księstwo legnickie  
- Fürstentum Brieg – księstwo brzeskie  
- Fürstentum Jauer – księstwo jaworskie  
- Fürstentum Sagan – księstwo żagańskie  
- Markgrafschaft Mähren – margrabstwo Moraw  
- Reich (Heiliges Römisches Reich) – Rzesza (Święte Cesarstwo Rzymskie)  

# Miasta i miasteczka

- Glatz – Kłodzko  
- Breslau – Wrocław  
- Prag – Praga  
- Habelschwerdt – Bystrzyca Kłodzka  
- Wünsch(el)burg – Radków  
- Landeck (Bad Landeck) – Lądek-Zdrój  
- Mittelwalde – Międzylesie  
- Neurode – Nowa Ruda  
- Reinerz – Duszniki (Duszniki-Zdrój)  
- Lewin (Lewinice) – Lewin Kłodzki  
- Frankenstein – Ząbkowice Śląskie (historycznie Frankenstein in Schlesien)  
- Münsterberg – Ziębice  
- Ottmachau – Otmuchów  
- Neisse – Nysa  
- Brieg – Brzeg  
- Liegnitz – Legnica  
- Schweidnitz – Świdnica  
- Jauer – Jawor  
- Striegau – Strzegom  
- Glogau – Głogów  
- Brünn – Brno  
- Wien – Wiedeń  
- Riga – Ryga  
- Freiwaldau – Jesionik (Freiwaldau – dawna niem. nazwa Jesionika)  

### Zamki, twierdze, klasztory

- Burg / Schloß Karpenstein (Karpfenstein) – zamek Karpenstein (Karpfenstein)  
- Burg Schnallenstein (Snellstein, Schnellinstein) – zamek Schnallenstein  
- Burg Hummel (Homole) – zamek Hummel (Homole)  
- Schloß Glatz – zamek w Kłodzku (twierdza kłodzka)  
- Burg Neuhaus bei Patschkau – zamek Neuhaus koło Paczkowa  
- Burg Kaldenstein bei Friedberg – zamek Kaldenstein koło Friedbergu  
- Schloß Ottmachau – zamek w Otmuchowie  
- Burg Stein (Katzenstein) – zamek Stein (Katzenstein) w Czechach  
- Burg Greifenstein – zamek Greifenstein  
- Burg Tepliwode – zamek Tepliwode  
- Burg Rummelsburg – zamek Rummelsburg  
- Burg Bardun (Wartha) – zamek Bardun (Warta)  
- Burg Kamenz (Kamenecz) – zamek Kamenz (Kamieniec)  
- Burg Homole – zamek Homole (Hummel)  
- Kloster Kamenz – klasztor w Kamieńcu Ząbkowickim (cystersi)  
- Kloster Heinrichau – klasztor w Henrykowie  

# Hrabstwa, państwa stanowe, dominium

- Herrschaft Karpenstein – państwo Karpieńskie
- Herrschaft Mittelwalde – państwo stanowe Międzylesie
- Herrschaft Schnallenstein – państwo stanowe Schnallenstein  
- Herrschaft Wölfelsdorf – państwo stanowe Wilkanów  
- Herrschaft Hummel – państwo stanowe Homole (Hummel)
- Herrschaft Nachod – państwo stanowe Náchod  
- Herrschaft Seitenberg – państwo stanowe Seitenberg Stronie Śląskie
- Herrschaft Kunzendorf – państwo stan stanowe Trzebieszowice
- Herrschaft Homole – państwo stanowe Homole (Hummel)

### Wsze, osady, przysiółki (w obrębie dawnej Herrschaft Karpenstein)

- Alt-Altmannsdorf – Starczów
- Alt-Gersdorf / Neu-Gersdorf – Stary Gersdorf / Nowy Gersdorf
- Alt-Mohrau (Mora, Moraw; früher Hammer, Klessen-Mora) – Stara Morawa  
- Arnoldsdorf (Grafenort) – Arnoldsdorf (Gorzanów)  
- Bielendorf – Bielice
- Boigtsdorf Boigtsdorf?
- Ebersdorf b. H. – Domaszków
- Gallenau – Gallenau?
- Gompersdorf (Gumprechtsdorf) – Goszów
- Hain – Hain?
- Hausdorf – Hausdorf?
- Heidelberg – Wrzosówka
- Heinzendorf –  Skrzynka
- Heudorf – Heudorf?
- Johannesberg – Janowa Góra
- Kamnitz (Kaminice) – Kamienica 
- Karpenstein (Dorf) – wieś Karpień
- Klessengrund (Kleßengrund) –  Kletno
- Königswalde – Świerki
- Konradswalde (Conradi villa, Kunradswald) – Konradów
- Kunzendorf (Cunchouis villa, Kunczindorf) – Trzebieszowice
- Lauterbach – Lauterbach?
- Leuthen (Luczyn, Luthin, Lautten) – Lutynia
- Lichtenwalde – Lichtenwalde?
- Lomnitz – Łomnica 
- Ludwigsdorf – Ludwikowice  
- Martinsberg (Merbotindorf) – Marcinków
- Mühlbach (Buchdörfel) – Młynowiec
- Neu-Mohrau – Nowa Morawa  
- Neundorf – Nowa Wieś
- Ober-Langenau – Długopole
- Obergläsersdorf – Obergläsersdorf?
- Olbersdorf (Albert(s)dorf) – Stójków 
- Petersdorf – Piotrowice
- Pischkowitz – Piszkowice
- Pomsdorf – Pomianów
- Raier(s)dorf – Radochów
- Rengersdorf – Radochów 
- Rückers – Szczytna
- Schlottendorf – Schlottendorf?
- Schönau – Schönau?
- Schönfeld – Schönfeld?
- Schreindorf / Schreindorf (Srokkferi, Srekrsdorf, Schreersdorf, Grund) – Schreindorf?
- Seitenberg – Stronie Śląskie
- Thalheim (Nieder-Thalheim, Ober-Thalheim) – Thalheim; po 1688: Niederthalheim = Dolne Thalheim, Oberthalheim = Górne Thalheim
- Urnitz – Jaworek
- Verlorenwasser – Ponikwa
- Volpersdorf – Wolibórz
- Weißwasser – Biała Woda
- Wilhelmsthal (Neustädtel) – Bolesławów
- Winkeldorf (Winklersdorf, Winklendorf) – Kąty Bystrzyckie
- Wölfelsdorf (Weltflini villa, Wolvilsdorf) – Wilkanów
- Wolmsdorf (Wolframsdorf) – Rogóżka 

# Góry, szczyty, formy terenowe

- Karpenstein (Berg) – Karpenstein (skała/masyw Karpenstein)  
- Dreiecker (Dreiecker Berg) – Trojak
- Ringelstein – Ringelstein?
- Hohenzollern-Fels – Skała Hohenzollernów  
- Achilles-Fels – Skała Achillesa  
- Schollenstein – Schollenstein?
- Max’ Ruh – Max’ Ruh?
- Waldtempel – „Leśna Świątynia”
- Schneeberg – Śnieżni
- Heuberg – Heuberg?
- Schwarzer Berg – Czarna Góra  
- Dürrer Berg – Suchy Szczyt (Suchý vrch)
- Hutberg – ?
- Galgenberg – Góra Szubieniczna  
- Jauersberg – Jauersberg?
- Rotschenberg – Rotschenberg?
- Heuscheuer – Szczeliniec Wielki
- Eulengebirge – Góry Sowie  
- Glatzer Spitzberg – Kłodzka Góra
- Reinerzer Forst, Nesselgrunder Forst – Reinerzer Forst, Nesselgrunder Forst?

# Rzeki, potoki, doliny

- Biele – Biała Lądecka (rzeka Biała)  
- Neiße – Nysa Kłodzka  
- Weistritz (WeiStrik) – Bystrzyca
- Steine – Ścinawka (Steine)  
- Kraßbach – potok Kraßbach (dopływ Białej)  
- March – Morawa (rzeka)

# Dzieła, kroniki, pisma

- Kögler’s Chroniken der Grafschaft Glatz – „Kroniki hrabstwa kłodzkiego” Köglera  
- Glatzer Miszellen – „Miscellanea kłodzkie”  
- Vierteljahrsschrift für Geschichte und Heimatkunde der Grafschaft Glatz – „Kwartalnik historii i krajoznawstwa hrabstwa kłodzkiego”  
- Die Freirichter der Grafschaft Glatz – „Wolni sędziowie hrabstwa kłodzkiego”  
- Schlesische Chronik – „Kronika śląska”  
- Glätzische Chronik – „Kronika kłodzka”  
- Böhmische Chronik – „Kronika czeska”  
- Vaterländische Bilder – „Obrazy ojczyste”  
- Lehns- und Besitzurkunden Schlesiens – „Dokumenty lenne i własnościowe Śląska”  
- Zeitschrift des Vereins für Geschichte und Altertum Schlesiens – „Czasopismo Towarzystwa Historii i Starożytności Śląska”  
- Beiträge zur Geschichte des schlesischen Adels – „Przyczynki do historii śląskiej szlachty”  
- Die schlesischen Siegel bis zum Jahre 1300 – „Śląskie pieczęcie do roku 1300”  
- Urkunden des Klosters Kamenz – „Dokumenty klasztoru w Kamieńcu”  
- Dokumentirte Geschichte von Breslau – „Udokumentowana historia Wrocławia”  
- Beiträge zur Beschreibung von Schlesien – „Przyczynki do opisu Śląska”  
- Geschichte der Stadt Patschkau – „Historia miasta Paczków”  
- Nachrichten über die Stadt Reichenstein – „Wiadomości o mieście Reichenstein (Złoty Stok)”  
- Regesten der Stadt Patschkau – „Regesty miasta Paczków”  
- Schlesische Chronik (Schikfus) – „Kronika śląska” Schikfusa  
- Böhmische Chronik (Hayek) – „Kronika czeska” Hayka
""",
        },
        {
            "role": "user",
            "content": BOOK_CONTENTS,
        },
    ],
    temperature=0,
    model=deployment,
)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{timestamp}.txt"

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")
        # also write to file
        with open(filename, "a", encoding="utf-8") as f:
            f.write(update.choices[0].delta.content or "")

client.close()
