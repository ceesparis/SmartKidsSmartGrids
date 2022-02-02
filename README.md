# Smart Grids

## Case
Dit project geeft een oplossing voor de smartgrid case. Het doel van deze case is huizen aan batterijen verbinden. Elk huis heeft een uitvoer van electriciteit, elke batterij een capaciteit. De capaciteit van de batterij mag niet door het totaal aantal verbonden huizen worden overschreden. Elk stuk kabel dat gelegd wordt kost 9 euro. Elke batterij kost 5000 euro. Het is mogelijk voor huizen die verbonden zijn aan dezelfde batterij om kabels te delen. Om deze opdracht goed uit te voeren moet er dus een oplossing gevonden worden waar er zo min mogelijk kabels gelegd hoeven te worden en zo veel mogelijk kabels gedeeld met elkaar.

## Vereisten
Onze code is volledig geschreven in Python 3.8. In requirements.txt staan alle packages die wij hebben gebruikt, en die dus nodig zijn om de code probleemloos te kunnen draaien. Dit is te installeren via pip door het runnen van de volgende command:

```
pip install -r requirements.txt
```
 
## Algoritmes
We hebben verschillende algoritmes geschreven om dit probleem op te lossen. Sommige algoritmes bouwen op elkaar voort, andere werken op zichzelf aan een oplossing. Hieronder worden de algoritmes geschreven.

### Verdeling over batterijen
Het eerste algoritme dat we hebben geschreven zoekt een slimmere manier om de huizen over de batterijen te verdelen. Als eerst legt het een baseline waarbij het verschilt tussen de dichtstbijzijnde batterij en de eerstvolgende batterij voor elk huis berekent. Hier maakt het een top n van, waarbij n bij elke loop random wordt bepaald. Deze huizen worden bij de dichtstbijzijnde batterij voor elk huis ingedeeld. Vervolgens gaat het de overige huizen verdelen over de batterijen, waarbij het eerst probeert het huis in de dichtstbijzijnde batterij in te delen, als dit niet lukt aangezien de capaciteit van deze batterij is gehaald, wordt het huis bij een batterij waar het nog wel past ingedeeld. Op het moment dat er geen batterijen zijn die passen, wordt er gezocht naar een huis dat al is ingedeeld bij een batterij, die geswitcht kan worden met het huis dat nog niet is ingedeeld. De switch wordt alleen gemaakt als dit de capaciteit van de batterij verbeterd, dus weer groter maakt. Mocht dit niet lukken, dan wordt deze oplossing afgekapt.

Bestandsnaam: ___batteryDistribution.py___

### Hillclimber over verdeling
Na de initiële verdeling van de huizen over de batterijen passen we een hillclimber algoritme toe, die de batterijen stapje voor stapje verbetert. Dit doet het door als eerst voor elk huis te checken of ze in hun dichtstbijzijnde batterij geplaatst kunnen worden, door te ruilen met een huis die dan in de op een na dichtstbijzijnde batterij geplaatst zal worden, namelijk de batterij waar het initiële huis nu nog in zit. Dit wordt alleen gedaan als het de totale afstand vermindert. Hierna worden er random huizen gekozen, en deze worden weer vergeleken met andere random gekozen huizen. Mocht de afstand worden verbeterd, worden de huizen geswitcht.

Bestandsnaam: ___distributionHill.py___

### Slimmere kabels leggen
Bij dit algoritme worden er als eerst grote radiussen gezocht die huizen aan elkaar gaan verbinden. De radiussen worden als volgt gemaakt: loop door alle huizen, zoek hierbij naar huizen die aan dezelfde batterij verbonden zijn, die binnen een random gekozen radius van dit huis liggen. Sla de radius met het grootste aantal huizen op. Haal vervolgens deze huizen uit de opties en zoek naar een radius voor het overige aantal huizen. Er mogen een random gekozen aantal huizen overblijven die niet binnen een radius geplaatst hoeven worden. Nadat deze grote radiussen gemaakt zijn worden binnen deze radiussen steeds kleinere radiussen gemaakt. Dit zullen huizen zijn die heel dichtbij elkaar liggen. Op deze manier worden een klein aantal huizen verbonden aan elkaar. Deze worden samen naar het middelpunt van het grotere aantal huizen geleid. Vervolgens wordt de groep vanaf hier naar de batterij geleid. 

Bestandsnaan: ___smartCables.py___

### Hillclimber over connecties van kabels
Nadat de bulk van de connecties van huis tot een andere kabel, ander huis, of batterij is gelegd, kunnen we per huis kijken of er misschien een andere kabel in de buurt ligt, die voor een kortere route naar de batterij zorgt dan het huidige punt waar het aan verbonden is. Dat gebeurt bij dit algoritme. Per huis checkt het aan welk centraal punt het momenteel is verbonden. Hierna zoekt het naar een kabel die naar dezelfde batterij leidt, die minder stappen kost om mee te verbinden dan de verbinding van het huidige centrale punt. Als dit een verbetering van lengte is zal het deze switch maken. Op het moment dat een huis aan de kabels van een ander huis is verbonden, mag het huis geen nieuwe kabels meer leggen om problemen te voorkomen.

Bestandsnaam: ___connectionClimber.py___

### Cluster Algoritme
Dit algoritme staat helemaal los van eerder beschreven algoritmes. Het centrale idee van dit algoritme is om eerst de huizen die dicht bij elkaar staan onderling te verbinden, alvorens ze met een batterij te verbinden. De optimale radius om in te zoeken bleek 5 ticks te zijn (deze afstand kan verdeeld zijn over de x- en de y-as). 
De huizen van een 'huizencluster' worden onderling verbonden in drie stappen. De eerste stap bestaat uit een greedy algoritme, dat vanaf elk huis in het cluster begint, en de meest voordelige route om de huizen met elkaar te verbinden onthoudt. Bij de tweede stap wordt er in het cluster nog een laatste kabel gelegd van het laatste huis tot het eerste huis, waardoor er een gesloten cirkel van kabels tussen de huizen ontstaat. Bij de laatste stap wordt er gekeken naar de langste kabel van het cluster, en deze wordt vernietigd. De huizen zijn dan nog steeds onderling verbonden vanwege stap 2. 
Vervolgens worden deze clusters in een random volgorde verbonden aan de dichstbijzijnde mogelijke batterij. Mocht de grid dan nog niet geldig zijn, husselt het algoritme met de clusters net zo lang tot het wel mogelijk is een geldige grid te maken. 

Bestandsnaam: ___cluster_alg.py___

## Structuur
Alle code die we hebben gebruikt, met uitzondering van de main, staat in onze code folder. In onze data map staan de initieel gegeven district csv bestanden die wij hebben gebruikt om grids in te lezen, en in de results map zijn zowel onze volledige experiment runs als diens beste uitkomsten te vinden, ingedeeld per experiment.

## Algoritmes testen
Om onze algoritmes te testen valt de volgende command line te runnen:
```
python3 main.py <district_nummer> <algoritme_afkorting>
```
De mogelijke districten zijn 1, 2, en 3, en de mogelijke afkortingen zijn SD (Smart Distribution), en CW (ClusterWebz).

## Experimenten testen
Om het Smart Distribution experiment te runnen, moet het bestand experimentSmartDistribution.py bestand verplaatst worden naar de main repository, waar main.py in geplaatst is. Vervolgens valt het te runnen door middel van
```
python3 experimentSmartDistribution.py
```
<br/>

Om het ClusterWebz experiment te runnen importeer je in de main de file door middel van:
```
from code.experiments.clus_exp import clus_experiment
```

Vervolgens roep je:  ```clus_exp()``` aan bovenaan de code. Roep vervolgens main als normaal aan; dit zal het experiment starten.

## Auteurs
* Sanne de Bruin
* Bas Kooter
* Cees Paris

## Dankwoord
* Minor Programmeren UvA
