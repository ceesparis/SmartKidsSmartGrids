# SmartKidsSmartGrids

## Case
Dit project geeft een oplossing voro de smartgrid case. Het doel van deze case is huizen aan batterijen verbinden. Elk huis heeft een uitvoer van electriciteit, elke batterij een capaciteit. De capaciteit van de batterij mag niet door het totaal aantal verbonden huizen worden overschreden. Elke kabel die gelegd wordt kost 9 euro. Elke batterij kost 5000 euro. Het is mogelijk voor huizen die verbonden zijn aan dezelfde batterij om kabels te delen. Om deze opdracht goed uit te voeren moet er dus een oplossing gevonden worden waar er zo min mogelijk kabels gelegd hoeven te worden en zo veel mogelijk kabels gedeeld met elkaar.
 
## Algoritmes
We hebben verschillende algoritmes geschreven om dit probleem op te lossen. Sommige algoritmes bouwen op elkaar voort, andere werken op zichzelf aan een oplossing. Hieronder worden de algoritmes geschreven.

### Verdeling over batterijen
Het eerste algoritme dat we hebben geschreven zoekt een slimmere manier om de huizen over de batterijen te verdelen. Als eerst legt het een baseline waarbij het verschilt tussen de dichtstbijzijnde batterij en de eerstvolgende batterij voor elk huis berekent. Hier maakt het een top n van, waarbij n bij elke loop random wordt bepaald. Deze huizen worden bij de dichtstbijzijnde batterij voor elk huis ingedeeld. Vervolgens gaat het de overige huizen verdelen over de batterijen, waarbij het eerst probeert het huis in de dichtstbijzijnde batterij in te delen, als dit niet lukt aangezien de capaciteit van deze batterij is gehaald, wordt het huis bij een batterij waar het nog wel past ingedeeld. Op het moment dat er geen batterijen zijn die passen, wordt er gezocht naar een huis die al is ingedeeld bij een batterij, die geswitcht kan worden met het huis dat nog niet is ingedeeld. De switch wordt alleen gemaakt als dit de capaciteit van de batterij verbeterd, dus weer groter maakt. Mocht dit niet lukken wordt deze oplossing afgekapt. 

batteryDistribution.py

### Hillclimber over verdeling
Na de initiële verdeling van de huizen over de batterijen passen we een hillclimber algoritme toe die de batterijen stapje voor stapje verbetert. Dit doet het door als eerst voor elk huis te checken of ze in hun dichtstbijzijnde batterij geplaatst te worden, door te ruilen met een huis die dan in het op een na dichtstbijzijnde batterij geplaatst zal worden, namelijk de batterij waar het initiële huis nu nog in zit. Dit wordt alleen gedaan als het de totale afstand vermindert. Hierna worden er random huizen gekozen, deze worden vergeleken met andere random gekozen huizen. Mocht de afstand worden verbeterd, worden de huizen geswitcht.

Bestandsnaam: distributionHill.py

### Slimmere kabels leggem
Bij dit algoritme wordt als eerst worden er grote radiussen gezocht die huizen aan elkaar gaan verbinden. De radiussen worden als volgt gemaakt: loop door alle huizen, zoek hierbij naar huizen die aan dezelfde batterij verbonden zijn die binnen een random gekozen radius van dit huis liggen. Sla de radius met het grootste aantal huizen op. Haal vervolgens deze huizen uit de opties en zoek naar een radius voor het overige aantal huizen. Er mogen een random gekozen aantal huizen overblijven die niet binnen een radius geplaatst hoeven worden. Nadat deze grote radiussen gemaakt zijn worden binnen deze radiussen kleinere radiussen gemaakt. Dit zullen huizen zijn die heel dichtbij elkaar liggen. Op deze manier worden een klein aantal huizen verbonden aan elkaar. Deze worden samen naar het middelpunt van het grotere aantal huizen geleid. Vervolgens wordt de groep vanaf hier naar de batterij geleid. 

Bestandsnaan: smartCables.py

### Hillclimber over connecties van kabels
Nadat de bulk van de connecties van huis tot een andere kabel, ander huis of batterij is gelegd, kunnen we per huis kijken of er misschien een andere kabel in de buurt ligt die voor een kortere route naar de batterij zorgt dan het huidige punt waar het aan verbonden is. Dit gebeurt bij dit algoritme. Per huis checkt het aan welk centrale punt het momenteel is verbonden. Hierna zoekt het naar een kabel die naar dezelfde batterij leidt die minder stappen kost om mee te verbinden dan de verbinding van het huidige centrale punt. Als dit een verbetering van lengte is zal het deze switch maken. Op het moment dat een huis aan de kabels van een ander huis is verbonden, mag het huis geen nieuwe kabels meer leggen om problemen te voorkomen.

Bestandsnaam: connectionClimber.py

### Cluster Algortime
Dit algoritme staat helemaal los van eerder beschreven algoritmes. Het centrale idee van dit algoritme is om eerst de huizen die dicht bij elkaar staan onderling te verbinden, alvorens ze met een batterij te verbinden. De optimale radius om in te zoeken bleek 5 ticks te zijn (deze afstand kan verdeeld zijn over de x en de y as). 
De huizen van een 'huizencluster' worden onderling verbonden in drie stappen. De eerste stap bestaat uit een greedy algoritme dat vanaf elk huis in het cluster begint, en die de meest voordelige route om de huizen met elkaar te verbinden onthoudt. Bij de tweede stap wordt er in het cluster nog een laatste kabel gelegd van het laatste huis tot het eerste huis, waardoor er een gesloten cirkel van kabels tussen de huizen ontstaat. Bij de laatste stap wordt er gekeken naar de langste kabel van het cluster, en deze wordt vernietigd. De huizen zijn dan nog steeds onderling verbonden vanwege stap 2. 
Vervolgens worden deze clusters in een random volgorde verbonden aan de dichstbijzijnde mogelijke batterij. Mocht de grid dan nog niet geldig zijn, husselt het algoritme met de clusters net zo lang tot het wel mogelijk is een geldige grid te maken. 

Bestandsnaam: cluster_alg.py

## Commands
- Run de algoritmes:
    Command line: python3 main.py [district nummer] [algorime afkorting]
    De districts zijn: 1, 2, 3
    De algorimes zijn: Smart Distribution (SD) and ClusterWebz (CW)
- Hoe run je de experimenten?
    Het experiment van de smart distribution run je door de experimentSmartDistribution.py te verplaatsen naar het mapje waar de main in geplaatst is. Vervolgens run je het experimentSmartDistribution.py bestand.

    Het experiment van de clusterwebz run je door in de main de file te importeren:
    from code.experiments.clus_exp import clus_experiment
    Vervolgens roep je clus_exp() aan als bovenaan de code. 
    Roep main als normaal aan. Dit zal het experiment starten.
