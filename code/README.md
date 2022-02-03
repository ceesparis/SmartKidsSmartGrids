# Code
We hebben deze folder ingedeeld in zes sub-folders aan code, verdeeld op basis van hun functie.

## Algorithms
Deze folder bevat de grote basis algoritmes waar onze experimenten op gebaseerd zijn. Omdat het Smart Distribution algoritme op zichzelf
weer bestaat uit verschillende algoritmes die op elkaar voort bouwen, hebben we deze samen gegroepeerd in een folder met corresponderende naam.
Deze bestaat uit:
* batteryDistribution.py: Een algoritme dat batterijen over huizen distribueert;
* connectionClimber.py: Een algoritme dat verbindingen legt maar deze verbetert in het geval het betere opties vindt;
* distributionClimber.py: Een soortgelijk werkend algoritme dat de dichtstbijzijnde huizen aan een batterij koppelt, maar ook deze verandert in geval van betere opties;
* randomCables.py: Een algoritme dat op willekeurige volgorde kabels legt in vrijwel rechte lijnen (zo ver mogelijk verticaal, dan horizontaal, of andersom);
* smartCableClimber.py: Een algoritme dat op basis van radiussen kabel afstanden verkort;
* En smartCables.py: een algoritme dat ook op basis van radiussen huizen samen groepeert en daar gedeelde kabels op baseert.

Omdat het Cluster algoritme afgezien van verdere classes, experiment bestanden, en visualisaties, uit maar 1 bestand bestaat, is deze los te
vinden in de folder.

## Calculations
Deze folder bevat:
* sharedCostsCluster.py: Een berekenaar van de gedeelde kosten voor het Cluster algoritme;
* costCalculation.py: Een algemene berekenaar van de totale kosten van het aantal batterijen en de prijs van de gelegde kabels;
* distanceCalc.py: Een berekenaar van de afstanden tussen huis en batterij;
* en sharedCosts.py: Een berekenaar van de gedeelde kosten voor het Smart Distribution algoritme.

## Classes
In deze folder staan alle classes voor de benodigde onderdelen voor de grid en het kabels leggen, waaronder de grid zelf. Er zijn classes voor:
* battery.py: De batterijen op de grid;
* cluster.py: De clusters die gebruikt worden in het Cluster algoritme;
* district.py: Initialiseert de eigenschappen van de districten op de grid;
* grid.py: De class die een lege 50 bij 50 grid genereert;
* house.py: De huizen op de grid;
* loader.py: Het bestand dat de districten inleest op de grid vanuit een csv bestand;
* en randomizer.py: Dit bestand legt uit willekeurige volgorde combinaties tussen huizen en batterijen, en gaat door tot het een goed resultaat vindt;
hier was onze baseline op gebaseerd.

## Experiments
Deze folder bevat:
* clusterExperimentRunner.py: De algemene runner van het experiment voor het Cluster algoritme, gebaseerd op tijd;
* clusterExperiment.py: Het daadwerkelijke experiment voor het Cluster algoritme, met aanpasbare parameters;
* en experimentSmartDistribution.py: Het experiment voor het runnen van het Smart Distribution algoritme, met alle benodigde aanpasbare parameters.

## Helpers
In deze folder hebben we als het ware de hulpjes van de algoritmes gezet. Zo hebben we:
* createRoute.py; Een bij-algoritme dat huizen en batterijen blijft verbinden zo lang er geen geldige uitkomst is;
* en distributeLoop.py; Deze loopt het Smart Distribution algoritme en slaat alle uitkomsten op, en print deze uit.

## Visualisation
Deze folder bevat twee bestanden die door middel van matplotlib de uitkomsten visualiseren naar daadwerkelijke grids gevuld met nodes voor de huizen
en batterijen, en lijnen voor de kabels. Het ene bestand is voor het Cluster algoritme, en de ander is om de uitkomsten van het Cluster experiment te visualiseren. De visualisatie voor de Smart Distribution staat al inbegrepen in diens code zelf.
