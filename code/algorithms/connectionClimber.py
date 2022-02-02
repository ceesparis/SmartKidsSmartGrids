from code.algorithms.randomCables import randomizeCables


class ClimbConnections():
    def __init__(self, batteries, houses, centralPoints, allCentrals, batteryHouses):
        self._batteries = batteries
        self._houses = houses
        self._centralPoints = centralPoints
        self._allCentrals = allCentrals
        self._batteryLocs = []
        self._batteryHouses = batteryHouses
        self.findBatteries()

    def findBatteries(self):
        for battery in self._batteries:
            self._batteryLocs.append(tuple(battery.location))

        self._batteryLocs = tuple(self._batteryLocs)

    def calculateDistance(self, houseLocation, secondLocation):
        distance = 0
        distance += abs(houseLocation[0] - secondLocation[0])
        distance += abs(houseLocation[1] - secondLocation[1])
        return distance

    def findConnections(self):
        cableTuples = {}
        # Maak per batterij een tuple van tuples van alle kabels
        for battery in self._batteries:
            for house in battery.houses:
                cableTuples[battery] = tuple(map(tuple, house.cables))

        # loop door alle batterijen
        for battery in self._batteries:
            lockedHouses = set()
            # loop door alle huizen:
            for houseOne in battery.houses:
                if tuple(houseOne.location) in self._allCentrals:
                    continue
                if houseOne in lockedHouses:
                    continue
                bestImprovement = 0
                cableHouseOne = None
                coordinateCableTwo = None
                # Bereken de afstand naar het centrale punt vanaf het huis
                if houseOne in self._centralPoints:
                    distanceCentral = self.calculateDistance(
                        houseOne.location, self._centralPoints[houseOne])
                else:
                    distanceCentral = self.calculateDistance(
                        houseOne.location, self._batteryHouses[houseOne].location)
                # Loop door al de kabels van dit huis heen
                for cableOne in houseOne.cables:
                    distanceCentral -= 1
                    # Is er een coordinaat van een ander huis die
                    # een afstand heeft kleiner dan de afstand die het
                    # huis vanaf dit coordinaat nog moet naar de batterij?
                    for i in range((-distanceCentral - 1), (distanceCentral - 1), 1):
                        for j in range(-distanceCentral, distanceCentral, 1):
                            if ((cableOne[0] + i), (cableOne[1]) + j) in cableTuples[battery]:
                                distanceCable = self.calculateDistance(
                                    cableOne, ((cableOne[0] + i), (cableOne[1]) + j))
                                distanceImprovement = distanceCentral - distanceCable
                                # Is deze afstandverschil kleiner dan eerder opgeslagen?
                                # Sla het verschil tussen de afstanden op
                                # Sla de coordinaat van de andere kabel op
                                # Sla de index van huidige coordinaat op
                                if distanceImprovement > bestImprovement:
                                    if ((cableOne[0] + i), (cableOne[1]) + j) not in self._batteryLocs:
                                        bestImprovement = distanceImprovement
                                        coordinateCableTwo = (
                                            (cableOne[0] + i), (cableOne[1]) + j)
                                        cableHouseOne = cableOne
                                        secondCentral = coordinateCableTwo

                if coordinateCableTwo != None:
                    indexCable = houseOne.cables.index(
                        list(cableHouseOne)) + 1
                    # print(f"coordinate: {cableHouseOne}")
                    # print(f"cables: {houseOne.cables}")

                    houseOne.cables = houseOne.cables[:indexCable]
                    # print(f"after remove: {houseOne.cables}")
                    pathToNew = randomizeCables(
                        houseOne.location, [coordinateCableTwo[0], coordinateCableTwo[1]])
                    pathToGattery = randomizeCables(
                        [coordinateCableTwo[0], coordinateCableTwo[1]], self._batteryHouses[houseOne].location)
                    houseOne.cables = pathToNew + pathToGattery

                    for house in battery.houses:
                        if house != houseOne:
                            if secondCentral in tuple(map(tuple, house.cables)):
                                lockedHouses.add(house)
                                break

            # Verwijder alles na de beste index
            # Maak een pad naar de coordinaat van de andere kabel
