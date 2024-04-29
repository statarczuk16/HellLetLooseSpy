import asyncio
import logging
import tkinter
import datetime

import common
import game_clock
import resource_tracker


class DummyCommander:

    def __init__(self, clock, tracker, root):
        self.clock = game_clock.Clock()
        self.tracker = tracker
        self.match_remaining = 90
        self.gui_root = root

        self.gui_root.fuel_node_gui = tkinter.IntVar(value=0)
        self.gui_root.munitions_node_gui = tkinter.IntVar(value=0)
        self.gui_root.manpower_node_gui = tkinter.IntVar(value=0)

        self.settings_frame = None
        self.logger_frame = None
        self.button_frame = None
        self.resource_frame = None
        self.tc_frame = None

        self.recon_tank_alive = True
        self.medium_tank_alive = True
        self.light_tank_alive = True
        self.heavy_tanks_alive = 0

        self.heavy_tanks_desired = 6

        self.vehicle_lost_to_resource_cost = {
            "RECON_TANK_KILLED": common.COST_RECON_TANK_FUEL,
            "LIGHT_TANK_KILLED": common.COST_LIGHT_TANK_FUEL,
            "MEDIUM_TANK_KILLED": common.COST_MEDIUM_TANK_FUEL,
            "HEAVY_TANK_KILLED": common.COST_HEAVY_TANK_FUEL,
            "HALFTRACK_KILLED": common.COST_HALFTRACK_FUEL,
        }

        self.ability_to_active_cooldown_seconds = {}
        self.ability_to_resource_type = {
            "AIRHEAD": common.Resource.MANPOWER,
            "ENCOURAGE": common.Resource.MANPOWER,
            "REINFORCE": common.Resource.MANPOWER,
            "SUPPLY_DROP": common.Resource.MUNITIONS,
            "RECON_PLANE": common.Resource.MUNITIONS,
            "STRAFING_RUN": common.Resource.MUNITIONS,
            "BOMBING_RUN": common.Resource.MUNITIONS,
            "ROCKET_STRIKE": common.Resource.MUNITIONS,
            "PRECISION_STRIKE": common.Resource.MUNITIONS,
            "HALFTRACK": common.Resource.FUEL,
            "LIGHT_TANK": common.Resource.FUEL,
            "MEDIUM_TANK": common.Resource.FUEL,
            "HEAVY_TANK": common.Resource.FUEL,
            "RECON_TANK": common.Resource.FUEL,
            "JEEP": common.Resource.FUEL,
            "FREE_LIGHT_TANK_RESPAWN_TIME": common.Resource.FUEL,
            "FREE_MEDIUM_TANK_RESPAWN_TIME": common.Resource.FUEL,
            "FREE_RECON_TANK_RESPAWN_TIME": common.Resource.FUEL,
        }

        self.ability_to_resource_cost = {
            "AIRHEAD": common.COST_AIRHEAD_MAN,
            "ENCOURAGE": common.COST_ENCOURAGE_MAN,
            "REINFORCE": common.COST_REINFORCE_MAN,
            "SUPPLY_DROP": common.COST_SUPPLY_DROP_MUN,
            "RECON_PLANE": common.COST_RECON_PLANE_MUN,
            "STRAFING_RUN": common.COST_STRAFING_RUN_MUN,
            "BOMBING_RUN": common.COST_BOMBING_RUN_MUN,
            "ROCKET_STRIKE": common.COST_ROCKET_STRIKE_MUN,
            "PRECISION_STRIKE": common.COST_PRECISION_STRIKE_MUN,
            "HALFTRACK": common.COST_HALFTRACK_FUEL,
            "LIGHT_TANK": common.COST_LIGHT_TANK_FUEL,
            "MEDIUM_TANK": common.COST_MEDIUM_TANK_FUEL,
            "HEAVY_TANK": common.COST_HEAVY_TANK_FUEL,
            "RECON_TANK": common.COST_RECON_TANK_FUEL,
            "JEEP": common.COST_JEEP_FUEL,
            "FREE_LIGHT_TANK_RESPAWN_TIME": 0,
            "FREE_MEDIUM_TANK_RESPAWN_TIME": 0,
            "FREE_RECON_TANK_RESPAWN_TIME": 0,
        }

        self.ability_to_cooldown_cost_minutes = {
            "AIRHEAD": common.COOLDOWN_AIRHEAD_M,
            "ENCOURAGE": common.COOLDOWN_ENCOURAGE_M,
            "REINFORCE": common.COOLDOWN_REINFORCE_M,
            "SUPPLY_DROP": common.COOLDOWN_SUPPLY_DROP_M,
            "RECON_PLANE": common.COOLDOWN_RECON_PLANE_M,
            "STRAFING_RUN": common.COOLDOWN_STRAFING_RUN_M,
            "BOMBING_RUN": common.COOLDOWN_BOMBING_RUN_M,
            "ROCKET_STRIKE": common.COOLDOWN_ROCKET_STRIKE_M,
            "PRECISION_STRIKE": common.COOLDOWN_PRECISION_STRIKE_M,
            "HALFTRACK": common.COOLDOWN_HALFTRACK_M,
            "LIGHT_TANK": common.COOLDOWN_LIGHT_TANK_M,
            "MEDIUM_TANK": common.COOLDOWN_MEDIUM_TANK_M,
            "HEAVY_TANK": common.COOLDOWN_HEAVY_TANK_M,
            "RECON_TANK": common.COOLDOWN_RECON_TANK_M,
            "JEEP": common.COOLDOWN_JEEP_M,
            "FREE_LIGHT_TANK_RESPAWN_TIME": common.COOLDOWN_LIGHT_TANK_M,
            "FREE_MEDIUM_TANK_RESPAWN_TIME": common.COOLDOWN_MEDIUM_TANK_M,
            "FREE_RECON_TANK_RESPAWN_TIME": common.COOLDOWN_RECON_TANK_M,
        }




    def gui_update_resources(self):
        try:
            parent_frame = self.resource_frame
            self.tracker.fuel_nodes = self.gui_root.fuel_node_gui.get()
            self.tracker.manpower_nodes = self.gui_root.manpower_node_gui.get()
            self.tracker.munitions_nodes = self.gui_root.munitions_node_gui.get()
            parent_frame.children['fuel_count'].config(text=str(self.tracker.fuel))
            parent_frame.children['munitions_count'].config(text=str(self.tracker.munitions))
            parent_frame.children['manpower_count'].config(text=str(self.tracker.manpower))
            fuel_per = 30 + (self.tracker.fuel_nodes * 10)
            ammo_per = 30 + (self.tracker.munitions_nodes * 10)
            man_per = 30 + (self.tracker.manpower_nodes * 10)
            if self.tracker.encourage:
                fuel_per += (self.tracker.fuel_nodes * 10)
                ammo_per += (self.tracker.munitions_nodes * 10)
                man_per += (self.tracker.manpower_nodes * 10)
            parent_frame.children['fuel_gain'].config(text=str(fuel_per)+' /min')
            parent_frame.children['munitions_gain'].config(text=str(ammo_per)+' /min')
            parent_frame.children['manpower_gain'].config(text=str(man_per)+' /min')
        except Exception as ex:
            print("Exception in gui_update_resources")
            print(str(ex))

    async def restart_match(self, match_elapsed_time_s = 0):
        parent_frame = self.button_frame
        await self.clock.restart()
        self.ability_to_active_cooldown_seconds.clear()
        self.tracker = resource_tracker.Tracker()
        self.gui_update_resources()
        self.heavy_tanks_alive = 0
        self.medium_tank_alive = True
        self.recon_tank_alive = True
        self.light_tank_alive = True
        #start game with all abilities on cooldown
        for used_ability in self.ability_to_cooldown_cost_minutes:
            if 'FREE' not in used_ability:#except for natural spawn counter
                self.ability_to_active_cooldown_seconds[used_ability] = self.ability_to_cooldown_cost_minutes[used_ability] * 60.0
                button_name = "progress_" + used_ability
                parent_frame.children[button_name]["value"] = 100
                #gui_root.children['button_frame'].children[button_name]["text"] = str(self.ability_to_active_cooldown_seconds[used_ability])
                button_name = "button_" + used_ability
                parent_frame.children[button_name]["state"] = tkinter.DISABLED
        logging.info("New match started")

    def set_game_clock_from_string(self, new_time_string):
        try:
            h, m, s = new_time_string.split(':')
            desired_game_clock_s = int(h) * 3600 + int(m) * 60 + int(s)
            print("Set game clock to: " + new_time_string)
            self.set_game_clock_s(desired_game_clock_s)
        except:
            print("Bad input for set clock")

    def set_game_clock_s(self, desired_seconds):
        current_game_clock_s = self.clock.get_game_clock_s()
        #if current time is 1:00:00 hours and desired is 1:30:00, then diff is -30 minutes
        diff = current_game_clock_s - desired_seconds
        print("Set game clock to: " +  str(datetime.timedelta(seconds=desired_seconds)) + "from " +  str(datetime.timedelta(seconds=current_game_clock_s)) + " seconds by fast forward/backward seconds " +str(diff) + " or " + str(datetime.timedelta(seconds=diff)))
        self.fast_forward_s(diff)

    def fast_forward_s(self, time_skip_s):
        self.clock.advance_counter(time_skip_s * 1)
        minutes = round(time_skip_s / 60.0)
        print("Accumulating resources for " + str(minutes) + " minutes ")
        self.tracker.accumulate(minutes)
        for used_ability in self.ability_to_cooldown_cost_minutes:
            if used_ability in self.ability_to_active_cooldown_seconds:
                self.ability_to_active_cooldown_seconds[used_ability] -= time_skip_s
        self.gui_update_resources()


    def can_use_ability(self, ability):
        resource = self.ability_to_resource_type[ability]
        cost = self.ability_to_resource_cost[ability]
        success = True
        reason = ""

        if ability in self.ability_to_active_cooldown_seconds:
            reason = ("Commander cannot use " + ability + " cooldown remaining " + str(
                self.ability_to_active_cooldown_seconds[ability]) + " seconds")
            success = False
        elif resource == common.Resource.FUEL and self.tracker.fuel < cost:
            success = False
            reason = ("Commander cannot use " + ability + " cost too much: " + str(cost))
        elif resource == common.Resource.MANPOWER and self.tracker.manpower < cost:
            success = False
            reason = ("Commander cannot use " + ability + " cost too much: " + str(cost))
        elif resource == common.Resource.MUNITIONS and self.tracker.munitions < cost:
            success = False
            reason = ("Commander cannot use " + ability + " cost too much: " + str(cost))
        elif 'FREE' in ability:
            if ability == 'FREE_LIGHT_TANK_RESPAWN_TIME':
                if self.light_tank_alive:
                    success = False
                    reason = "Cannot start light tank respawn cooldown until light tank is destroyed"
            elif ability == 'FREE_MEDIUM_TANK_RESPAWN_TIME':
                if self.medium_tank_alive:
                    success = False
                    reason = "Cannot start medium tank respawn cooldown until light tank is destroyed"
            elif ability == 'FREE_SCOUT_TANK_RESPAWN_TIME':
                if self.recon_tank_alive:
                    success = False
                    reason = "Cannot start scout tank respawn cooldown until light tank is destroyed"

        return success, reason

    def record_loss(self, vehicle_lost):
        try:
            logging.debug("Enemy " + vehicle_lost)

            if vehicle_lost == "RECON_TANK_KILLED":
                if self.recon_tank_alive == False:
                    self.subtract_fuel(self.vehicle_lost_to_resource_cost[vehicle_lost])
                    logging.info("Enemy " + vehicle_lost + " was not natural spawn. Subtracting fuel.")
                else:
                    self.recon_tank_alive = False
                    self.use_ability('FREE_SCOUT_TANK_RESPAWN_TIME')
                    logging.info("Enemy NATURAL RECON killed")
            elif vehicle_lost == "LIGHT_TANK_KILLED":
                if self.light_tank_alive == False:
                    self.subtract_fuel(self.vehicle_lost_to_resource_cost[vehicle_lost])
                    logging.info("Enemy " + vehicle_lost + " was not natural spawn. Subtracting fuel.")
                else:
                    self.light_tank_alive = False
                    self.use_ability('FREE_LIGHT_TANK_RESPAWN_TIME')
                    logging.info("Enemy NATURAL LIGHT killed")
            elif vehicle_lost == "MEDIUM_TANK_KILLED":
                if self.medium_tank_alive == False:
                    self.subtract_fuel(self.vehicle_lost_to_resource_cost[vehicle_lost])
                    logging.info("Enemy " + vehicle_lost + " was not natural spawn. Subtracting fuel.")
                else:
                    self.medium_tank_alive = False
                    self.use_ability('FREE_MEDIUM_TANK_RESPAWN_TIME')
                    logging.info("Enemy NATURAL MEDIUM killed")
            elif vehicle_lost == "HALFTRACK_KILLED":
                self.subtract_fuel(self.vehicle_lost_to_resource_cost[vehicle_lost])
                logging.info("Enemy " + vehicle_lost + " was not natural spawn. Subtracting fuel.")
            elif vehicle_lost == "HEAVY_TANK_KILLED":
                self.heavy_tanks_alive -= 1
                if self.heavy_tanks_alive < 0:
                    logging.info("Enemy Heavy Tank was not expected to exist. Subtracting fuel.")
                    self.subtract_fuel(self.vehicle_lost_to_resource_cost[vehicle_lost])
                    self.heavy_tanks_alive = 0
                else:
                    logging.info("Enemy Heavy Tank was expected to exist. Fuel was already subtracted, earlier.")
        except Exception as ex:
            print("Exception using commander ability: " + str(vehicle_lost))
            print(str(ex))
    def use_ability(self, ability):
        try:
            logger = logging.getLogger()
            can_use, reason = self.can_use_ability(ability)

            if can_use:
                resource = self.ability_to_resource_type[ability]
                cost = self.ability_to_resource_cost[ability]
                if resource == common.Resource.FUEL:
                    self.subtract_fuel(cost)
                elif resource == common.Resource.MANPOWER:
                    self.subtract_manpower(cost)
                elif resource == common.Resource.MUNITIONS:
                    self.subtract_munitions(cost)
                self.ability_to_active_cooldown_seconds[ability] = self.ability_to_cooldown_cost_minutes[ability] * 60.0

                button_name = "button_" + ability
                self.button_frame.children[button_name]["state"]=tkinter.DISABLED
                button_name = "progress_" + ability
                self.button_frame.children[button_name]["value"] = 100

                if ability == "ENCOURAGE":
                    self.tracker.encourage = True
                    self.gui_update_resources()
                elif ability == "HEAVY_TANK":
                    self.heavy_tanks_alive += 1
                logger.info("Commander used ability: " + ability)
            else:
                logger.info("Commander cannot use ability " + ability + " because " + str(reason))

        except Exception as ex:
            print("Exception using commander ability: " + str(ability))
            print(str(ex))


    def subtract_fuel(self, amount):
        self.tracker.fuel -= amount
        if self.tracker.fuel < 0:
            self.tracker.fuel = 0
        self.gui_update_resources()


    def subtract_munitions(self, amount):
        self.tracker.munitions -= amount
        if self.tracker.munitions < 0:
            self.tracker.munitions = 0
        self.gui_update_resources()

    def subtract_manpower(self, amount):
        self.tracker.manpower -= amount
        if self.tracker.manpower < 0:
            self.tracker.manpower = 0
        self.gui_update_resources()

    async def run_accumulator(self):
        while True:
            start_time = self.clock.get_game_clock_s()
            await self.clock.wait_for_time(common.ACCUMULATE_INTERVAL_S)
            end_time = self.clock.get_game_clock_s()
            minutes_elapsed = int((start_time - end_time)/60)
            self.tracker.accumulate(minutes_elapsed)
            self.gui_update_resources()


    async def command_team(self):
        while True:
            try:
                await asyncio.sleep(1)
                gui_parent = self.settings_frame
                label_name = "label_" + "GAME_CLOCK"
                game_clock_seconds = self.clock.get_game_clock_s()
                if game_clock_seconds <= 0:
                    self.clock.pause = True

                game_clock_str = str(datetime.timedelta(seconds=game_clock_seconds))


                gui_parent.children[label_name]["text"] = "Game Clock: " + game_clock_str

                #Determine if an ability should come off cooldown
                abilities_no_longer_on_cooldown = []
                for used_ability in self.ability_to_active_cooldown_seconds:

                    self.ability_to_active_cooldown_seconds[used_ability] -= 1 * common.time_scale_global.get()
                    button_name = "progress_" + used_ability
                    value = self.ability_to_active_cooldown_seconds[used_ability] / (self.ability_to_cooldown_cost_minutes[used_ability] * 60.0)
                    value *= 100.0
                    self.button_frame.children[button_name]["value"] = value

                    if self.ability_to_active_cooldown_seconds[used_ability] <= 0:
                        abilities_no_longer_on_cooldown.append(used_ability)
                        button_name = "button_" + used_ability
                        self.button_frame.children[button_name]["state"] = tkinter.NORMAL
                        if used_ability == "ENCOURAGE":
                            self.tracker.encourage = False
                    elif self.ability_to_active_cooldown_seconds[used_ability] > self.ability_to_cooldown_cost_minutes[used_ability] * 60.0:
                        self.ability_to_active_cooldown_seconds[used_ability] = self.ability_to_cooldown_cost_minutes[used_ability] * 60.0

                for ability in abilities_no_longer_on_cooldown:
                    self.ability_to_active_cooldown_seconds.pop(ability, None)

                #if can use encourage, always use it
                can_use, reason = self.can_use_ability("ENCOURAGE")
                if can_use:
                    self.use_ability("ENCOURAGE")
                heavies_desired = int(self.settings_frame.children['entry_heavies_desired'].get())
                self.heavy_tanks_desired = heavies_desired
                can_use, reason = self.can_use_ability("HEAVY_TANK")
                if can_use and heavies_desired > self.heavy_tanks_alive:
                    self.use_ability("HEAVY_TANK")

                #These abilities are not used here. They are automatically called when the natural tanks are reported
                #destroyed. The abilities dont do anything except start a countdown timer.
                #When the "ability" can be used, it means the countdown is over and it is time for the natural spawn

                if self.recon_tank_alive == False:
                    can_use, reason = self.can_use_ability("FREE_RECON_TANK_RESPAWN_TIME")
                    if can_use:
                        self.recon_tank_alive = True
                        logging.info("Natural recon tank respawned")
                if self.light_tank_alive == False:
                    can_use, reason = self.can_use_ability("FREE_LIGHT_TANK_RESPAWN_TIME")
                    if can_use:
                        self.light_tank_alive = True
                        logging.info("Natural light tank respawned")
                if self.medium_tank_alive == False:
                    can_use, reason = self.can_use_ability("FREE_MEDIUM_TANK_RESPAWN_TIME")
                    if can_use:
                        self.medium_tank_alive = True
                        logging.info("Natural medium tank respawned")

                can_use, reason = self.can_use_ability("PRECISION_STRIKE")
                if can_use:
                    self.tc_frame.children['label_PRECISION_UP']["text"] = "UP"
                else:
                    self.tc_frame.children['label_PRECISION_UP']["text"] = "DOWN"


                if self.light_tank_alive == True:
                    self.tc_frame.children['label_LIGHT_UP']["text"] = "UP"
                else:
                    self.tc_frame.children['label_LIGHT_UP']["text"] = "DOWN"

                if self.recon_tank_alive == True:
                    self.tc_frame.children['label_RECON_UP']["text"] = "UP"
                else:
                    self.tc_frame.children['label_RECON_UP']["text"] = "DOWN"

                if self.medium_tank_alive == True:
                    self.tc_frame.children['label_MEDIUM_UP']["text"] = "UP"
                else:
                    self.tc_frame.children['label_MEDIUM_UP']["text"] = "DOWN"

                self.tc_frame.children['label_HEAVIES_UP']["text"] = str(self.heavy_tanks_alive)






            except Exception as ex:
                print("Error in command team")
                print(str(ex))