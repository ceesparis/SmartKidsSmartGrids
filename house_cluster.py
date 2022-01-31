import copy


class Cluster():

    def __init__(self, houses):
        self.houses = sorted(houses, key=lambda x: x.location[1]+x.location[0])
        self.output = 0
        self.total_cables = []


    def add_cluster_cables(self):
        houses_copy = copy.deepcopy(self.houses)
        for house in houses_copy:
            start_x = house.location[0]
            start_y = house.location[1]




    def add_cluster_cables(self):
        # print('begin cluster')
        # for house in self.houses:
        #     print(house.location)
        # print('end cluster')
        smallest_path = []

        short_cable_clus = []
        # poppin_houses = copy.deepcopy(self.houses)
        possible_paths = []
        for house in self.houses:
            # print(house.location)
            possible_path = []
            starter = house
            poppin_houses = copy.deepcopy(self.houses)
            for pop_house in poppin_houses:
                if pop_house.location == house.location:
                    starter = pop_house
                    # print(starter.location)
            while poppin_houses:
                possible_path.append(starter)
                begin_x = starter.location[0]
                begin_y = starter.location[1]
                end_house = starter.find_closest(poppin_houses)
                poppin_houses.remove(starter)
                starter = end_house
            possible_paths.append(possible_path)
            # print(possible_path)

        # part 1 put cables in each greedy config
        for path in possible_paths:
            i = 0
            # add cables from first to last house
            while i < (len(path)-1):
                begin_house = path[i]
                begin_x = begin_house.location[0]
                begin_y = begin_house.location[1]
                end_house = path[i+1]
                end_x = end_house.location[0]
                end_y = end_house.location[1]

                while begin_x < end_x:
                    begin_x += 1
                    begin_house.add_cable(begin_x, begin_y)
                while begin_x > end_x:
                    begin_x -= 1
                    begin_house.add_cable(begin_x, begin_y)
                while begin_y < end_y:
                    begin_y += 1
                    begin_house.add_cable(begin_x, begin_y)
                while begin_y > end_y:
                    begin_y -= 1
                    begin_house.add_cable(begin_x, begin_y)
                i += 1
                # if (begin_house.cables) < smallest_path:
                #     smallest_path = begin_house.cables
                # if smallest_path == False:
                #     smallest_path = begin_house.cables
                # print(begin_house.cables)
                # if smallest_path:
                #     print(shortest_path.cables)


            # part 2 complete circle
            if len(path) > 1:
                begin_house = path[i]
                begin_x = begin_house.location[0]
                begin_y = begin_house.location[1]
                end_house = path[0]
                end_x = end_house.location[0]
                end_y = end_house.location[1]
                while begin_x < end_x:
                    begin_x += 1
                    begin_house.add_cable(begin_x, begin_y)
                while begin_x > end_x:
                    begin_x -= 1
                    begin_house.add_cable(begin_x, begin_y)
                while begin_y < end_y:
                    begin_y += 1
                    begin_house.add_cable(begin_x, begin_y)
                while begin_y > end_y:
                    begin_y -= 1
                    begin_house.add_cable(begin_x, begin_y)

            # part 3 break circle optimallly
            biggest_cable = []
            print('begin cluster')
            for house in path:
                print(house.location)
                if len(house.cables) > len(biggest_cable):
                    biggest_cable = house.cables
            print('end cluster')
            sentence = 'biggest cable is {}'.format(biggest_cable)
            for house in path:
                if house.cables == biggest_cable:
                    house.cables = []
            print(sentence)



        # for house in self.houses:
        #     print(house.cables)
        # print('one hosue')
        # print(begin_house.cables)




