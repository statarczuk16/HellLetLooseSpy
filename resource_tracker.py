import logging


class Tracker:

    def __init__(self):
        self.fuel = 500
        self.munitions = 500
        self.manpower = 500
        self.fuel_nodes = 0
        self.munitions_nodes = 0
        self.manpower_nodes = 0
        self.encourage = False


    def accumulate(self, minutes):
        try:
            logging.info("Accumulating resources for " + str(minutes) + " minutes ")
            fuel_from_nodes = minutes * 10 * self.fuel_nodes
            mun_from_nodes = minutes * 10 * self.munitions_nodes
            man_from_nodes = minutes * 10 * self.manpower_nodes
            if self.encourage:
                fuel_from_nodes *= 2
                mun_from_nodes *= 2
                man_from_nodes *= 2
            total_fuel = minutes * 30 + fuel_from_nodes
            total_mun = minutes * 30 + mun_from_nodes
            total_man = minutes * 30 + man_from_nodes
            self.fuel += total_fuel
            self.manpower += total_man
            self.munitions += total_mun
            if self.fuel < 0:
                self.fuel = 0
            if self.manpower < 0:
                self.manpower = 0
            if self.munitions < 0:
                self.munitions = 0
        except Exception as ex:
            print("Exception in accumulate")
            print(str(ex))

    def __str__(self):
        return "[" + str(self.data) + "]"