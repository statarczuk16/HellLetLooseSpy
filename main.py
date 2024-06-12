# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import logging
import sys
import tkinter
import tkinter as tk
from tkinter import ttk, DISABLED, END, messagebox, scrolledtext
from idlelib.tooltip import Hovertip
from tkinter.scrolledtext import ScrolledText


import common
import game_clock
import resource_tracker
import commander
import hll_logger


def create_resource_frame(gui_parent, commander):
    try:
        frame = ttk.Frame(gui_parent, name="resource_count_frame")

        # frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text='Munitions').grid(column=0, row=0)
        ttk.Label(frame, text='500', name="munitions_count").grid(column=1, row=0)
        ttk.Label(frame, text='30 /min', name="munitions_gain").grid(column=2, row=0)
        ttk.Label(frame, text='Manpower').grid(column=3, row=0)
        ttk.Label(frame, text='500', name="manpower_count").grid(column=4, row=0)
        ttk.Label(frame, text='30 /min', name="manpower_gain").grid(column=5, row=0)
        ttk.Label(frame, text='Fuel').grid(column=6, row=0)
        ttk.Label(frame, text='500', name="fuel_count").grid(column=7, row=0)
        ttk.Label(frame, text='30 /min', name="fuel_gain").grid(column=8, row=0)

       # for widget in frame.winfo_children():
        #    widget.grid(padx=5, pady=5)

        return frame
    except Exception as ex:
        print("Exception in create_resource_frame")
        print(str(ex))

def create_tc_frame(gui_parent, commander):
    try:
        frame = ttk.Frame(gui_parent, name="tc_frame")

        row = 0
        ttk.Label(frame, text='Tank Commander Panel').grid(column=0, row=row)
        row+=1
        ttk.Label(frame, text='Enemy Heavies Possible:').grid(column=0,row=row)
        ttk.Label(frame, name='label_HEAVIES_UP', text='0').grid(column=1, row=row)
        row += 1
        ttk.Label(frame, text='Enemy Medium is :').grid(column=0, row=row)
        ttk.Label(frame, name='label_MEDIUM_UP', text='UP').grid(column=1, row=row)
        row += 1
        ttk.Label(frame, text='Enemy Recon is :').grid(column=0, row=row)
        ttk.Label(frame, name='label_RECON_UP', text='UP').grid(column=1, row=row)
        row += 1
        ttk.Label(frame, text='Enemy Light is :').grid(column=0, row=row)
        ttk.Label(frame, name='label_LIGHT_UP', text='UP').grid(column=1, row=row)
        row += 1
        ttk.Label(frame, text='Precision Strike is :').grid(column=0, row=row)
        ttk.Label(frame,  name='label_PRECISION_UP', text='DOWN').grid(column=1, row=row)
        row += 1

        ttk.Label(frame, text='Record Destroyed Vehicle').grid(column=0, row=row)
        row += 1

        ttk.Button(frame, name='button_LIGHT_TANK_KILLED', command=lambda: commander.record_loss("LIGHT_TANK_KILLED"),
                   text='Light Tank', width=common.BUTTON_WIDTH).grid(column=0, row=row)
        ttk.Button(frame, name='button_MEDIUM_TANK_KILLED', command=lambda: commander.record_loss("MEDIUM_TANK_KILLED"),
                   text='Medium Tank', width=common.BUTTON_WIDTH).grid(column=1, row=row)
        ttk.Button(frame, name='button_HEAVY_TANK_KILLED', command=lambda: commander.record_loss("HEAVY_TANK_KILLED"),
                   text='Heavy Tank', width=common.BUTTON_WIDTH).grid(column=2, row=row)
        row +=1
        ttk.Button(frame, name='button_HALFTRACK_KILLED', command=lambda: commander.record_loss("HALFTRACK_KILLED"),
                   text='Halftrack', width=common.BUTTON_WIDTH).grid(column=0, row=row)
        ttk.Button(frame, name='button_RECON_TANK_KILLED', command=lambda: commander.record_loss("RECON_TANK_KILLED"),
                   text='Recon Tank', width=common.BUTTON_WIDTH).grid(column=1, row=row)
        row +=1
        ttk.Button(frame, name='button_PRECISION_STRIKE_USED', command=lambda: commander.use_ability("PRECISION_STRIKE"),
                   text='Record Precision Strike', width=common.BUTTON_WIDTH).grid(column=1, row=row)

        #for widget in frame.winfo_children():
        #    widget.grid(padx=5, pady=5)

        return frame
    except Exception as ex:
        print("Exception in create_log_frame")
        print(str(ex))

def create_log_frame(gui_parent, commander):
    try:
        frame = ttk.Frame(gui_parent, name="logger_frame")

        log_text = ScrolledText(frame)
        log_text.pack(fill=tk.BOTH, expand=True)

        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        widget_logger = hll_logger.WidgetLogger(log_text, logging.INFO, '%(message)s')
        logger = logging.getLogger()
        logger.addHandler(widget_logger)
        logging.info("Program Start")
        logging.debug("Debug output enabled")

        #for widget in frame.winfo_children():
        #    widget.grid(padx=5, pady=5)

        return frame
    except Exception as ex:
        print("Exception in create_log_frame")
        print(str(ex))


def create_button_frame(gui_parent, commander):
    try:


        frame = ttk.Frame(gui_parent, name="button_frame", width=400, height=650)
        frame.grid(row=0,column=0)

        munitions_row = 0
        prog_bar = munitions_row + 1

        ### Munitions Buttons
        ttk.Label(frame, text='Munition Abilities').grid(column=0, row=munitions_row)
        munitions_row += 1
        prog_bar = munitions_row + 1
        ttk.Button(frame, name='button_SUPPLY_DROP', command=lambda: commander.use_ability("SUPPLY_DROP"),
                   text='Supply Drop', width=common.BUTTON_WIDTH).grid(column=0, row=munitions_row)
        ttk.Progressbar(frame, name='progress_SUPPLY_DROP', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=0, row=prog_bar)
        ttk.Button(frame, name='button_RECON_PLANE', command=lambda: commander.use_ability("RECON_PLANE"),
                   text='Recon Plane', width=common.BUTTON_WIDTH).grid(column=1, row=munitions_row)
        ttk.Progressbar(frame, name='progress_RECON_PLANE', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=1, row=prog_bar)
        ttk.Button(frame, name='button_PRECISION_STRIKE', command=lambda: commander.use_ability("PRECISION_STRIKE"),
                   text='Precision Strike', width=common.BUTTON_WIDTH).grid(column=2, row=munitions_row)
        ttk.Progressbar(frame, name='progress_PRECISION_STRIKE', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=2, row=prog_bar)

        munitions_row += 2
        prog_bar = munitions_row + 1

        ttk.Button(frame, name='button_BOMBING_RUN', command=lambda: commander.use_ability("BOMBING_RUN"),
                   text='Bombing Run', width=common.BUTTON_WIDTH).grid(column=0, row=munitions_row)
        ttk.Progressbar(frame, name='progress_BOMBING_RUN', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=0, row=prog_bar)
        prog_bar = munitions_row + 1
        ttk.Button(frame, name='button_ROCKET_STRIKE', command=lambda: commander.use_ability("ROCKET_STRIKE"),
                   text='Katyusha Run', width=common.BUTTON_WIDTH).grid(column=1, row=munitions_row)
        ttk.Progressbar(frame, name='progress_ROCKET_STRIKE', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=1, row=prog_bar)
        ttk.Button(frame, name='button_STRAFING_RUN', command=lambda: commander.use_ability("STRAFING_RUN"),
                   text='Strafing Run', width=common.BUTTON_WIDTH).grid(column=2, row=munitions_row)
        ttk.Progressbar(frame, name='progress_STRAFING_RUN', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=2, row=prog_bar)

        ### Fuel Buttons
        fuel_row = munitions_row + 2
        prog_bar = fuel_row + 1
        ttk.Label(frame, text='Fuel Abilities').grid(column=0, row=fuel_row)

        fuel_row += 2
        prog_bar = fuel_row + 1
        ttk.Button(frame, name='button_RECON_TANK', command=lambda: commander.use_ability("RECON_TANK"),
                   text='Recon Tank', width=common.BUTTON_WIDTH).grid(column=0, row=fuel_row)
        ttk.Progressbar(frame, name='progress_RECON_TANK', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=0, row=prog_bar)
        ttk.Button(frame, name='button_LIGHT_TANK', command=lambda: commander.use_ability("LIGHT_TANK"),
                   text='Light Tank', width=common.BUTTON_WIDTH).grid(column=1, row=fuel_row)
        ttk.Progressbar(frame, name='progress_LIGHT_TANK', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=1, row=prog_bar)
        ttk.Button(frame, name='button_MEDIUM_TANK', command=lambda: commander.use_ability("MEDIUM_TANK"),
                   text='Medium Tank', width=common.BUTTON_WIDTH).grid(column=2, row=fuel_row)
        ttk.Progressbar(frame, name='progress_MEDIUM_TANK', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=2, row=prog_bar)

        fuel_row += 2
        prog_bar = fuel_row + 1

        ttk.Button(frame, name='button_HEAVY_TANK', command=lambda: commander.use_ability("HEAVY_TANK"),
                   text='Heavy Tank', width=common.BUTTON_WIDTH).grid(column=0, row=fuel_row)
        ttk.Progressbar(frame, name='progress_HEAVY_TANK', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=0, row=prog_bar)
        ttk.Button(frame, name='button_HALFTRACK', command=lambda: commander.use_ability("HALFTRACK"), text='Halftrack',
                   width=common.BUTTON_WIDTH).grid(column=1, row=fuel_row)
        ttk.Progressbar(frame, name='progress_HALFTRACK', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=1, row=prog_bar)
        ttk.Button(frame, name='button_JEEP', command=lambda: commander.use_ability("JEEP"), text='Jeep',
                   width=common.BUTTON_WIDTH).grid(column=2, row=fuel_row)
        ttk.Progressbar(frame, name='progress_JEEP', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=2, row=prog_bar)

        ### Manpower Buttons
        man_row = fuel_row + 2
        prog_bar = man_row + 1
        ttk.Label(frame, text='Manpower Abilities').grid(column=0, row=man_row)
        man_row += 2
        prog_bar = man_row + 1
        ttk.Button(frame, name='button_AIRHEAD', command=lambda: commander.use_ability("AIRHEAD"), text='Airhead',
                   width=common.BUTTON_WIDTH).grid(column=0, row=man_row)
        ttk.Progressbar(frame, name='progress_AIRHEAD', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=0, row=prog_bar)

        ttk.Button(frame, name='button_REINFORCE', command=lambda: commander.use_ability("REINFORCE"), text='Reinforce',
                   width=common.BUTTON_WIDTH).grid(column=1, row=man_row)
        ttk.Progressbar(frame, name='progress_REINFORCE', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=1, row=prog_bar)

        encourage_button = ttk.Button(frame, name='button_ENCOURAGE',
                                      command=lambda: commander.use_ability("ENCOURAGE"), text='Encourage',
                                      width=common.BUTTON_WIDTH)
        encourage_button.grid(column=2, row=man_row)
        encourage_tip = Hovertip(encourage_button, 'App will assume encourage is being used when manpower is available')
        ttk.Progressbar(frame, name='progress_ENCOURAGE', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=2, row=prog_bar)

        ### Natural Spawns
        nat_row = man_row + 2
        prog_bar = nat_row + 1
        ttk.Label(frame, text='Natural Spawns').grid(column=0, row=nat_row)
        nat_row += 2
        prog_bar = nat_row + 1
        ttk.Button(frame, name='button_FREE_RECON_TANK_RESPAWN_TIME',text='Natural Scout Tank Respawn',
                   width=common.BUTTON_WIDTH).grid(column=0, row=nat_row)
        ttk.Progressbar(frame, name='progress_FREE_RECON_TANK_RESPAWN_TIME', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=0, row=prog_bar)

        ttk.Button(frame, name='button_FREE_LIGHT_TANK_RESPAWN_TIME', text='Natural Light Tank Respawn',
                   width=common.BUTTON_WIDTH).grid(column=1, row=nat_row)
        ttk.Progressbar(frame, name='progress_FREE_LIGHT_TANK_RESPAWN_TIME', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=1, row=prog_bar)

        ttk.Button(frame, name='button_FREE_MEDIUM_TANK_RESPAWN_TIME', text='Natural Medium Tank Respawn',
                   width=common.BUTTON_WIDTH).grid(column=2, row=nat_row)
        ttk.Progressbar(frame, name='progress_FREE_MEDIUM_TANK_RESPAWN_TIME', orient='horizontal', mode='determinate',
                        length=common.PROGRESS_WIDTH).grid(column=2, row=prog_bar)


        #for widget in frame.winfo_children():
        #    widget.grid(padx=5, pady=5)



        return frame
    except Exception as ex:
        print("Exception in create_button_frame")
        print(str(ex))


async def restart_match_async():
    await commander.restart_match()
''

def create_config_frame(gui_parent, commander):
    try:
        frame = ttk.Frame(gui_parent, name="config_frame")
        # grid layout for the input frame
        # frame.columnconfigure(0, weight=1)
        # frame.columnconfigure(0, weight=3)

        config_row = 0
        # Find what
        ttk.Label(frame, text='Config').grid(column=0, row=config_row)

        config_row += 1

        ttk.Label(frame, name="label_TIME_SCALE", text='Time Scale: ' + str(1) + ' Seconds = ' + str(
            1 * common.DEFAULT_TIME_SCALE) + ' Seconds').grid(column=0, row=config_row)

        config_row += 1

        time_scale_entry = ttk.Entry(frame, width=10, name="entry_TIME_SCALE")
        time_scale_entry.delete(0, END)
        time_scale_entry.insert(0, "1")
        # fast_forward_entry.focus()
        time_scale_entry.grid(column=0, row=config_row)

        config_row += 1

        ttk.Label(frame, text='Game Clock: ', name="label_GAME_CLOCK").grid(column=0, row=config_row)

        config_row += 1

        munition_node_frame = ttk.Frame(frame, name="munition_node_frame")

        ttk.Label(munition_node_frame, text='Munition Nodes').grid(column=0, row=config_row, sticky=tk.W)

        config_row += 1

        commander.gui_root.fuel_node_gui = tkinter.IntVar(value=0)
        commander.gui_root.munitions_node_gui = tkinter.IntVar(value=0)
        commander.gui_root.manpower_node_gui = tkinter.IntVar(value=0)

        ttk.Radiobutton(munition_node_frame, text="0", variable=commander.gui_root.munitions_node_gui,
                        command=lambda: commander.gui_update_resources(), value=0).grid(column=1, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="1", variable=commander.gui_root.munitions_node_gui,
                        command=lambda: commander.gui_update_resources(), value=1).grid(column=2, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="2", variable=commander.gui_root.munitions_node_gui,
                        command=lambda: commander.gui_update_resources(), value=2).grid(column=3, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="3", variable=commander.gui_root.munitions_node_gui,
                        command=lambda: commander.gui_update_resources(), value=3).grid(column=4, row=config_row,
                                                                                        sticky=tk.W)

        config_row += 1

        ttk.Label(munition_node_frame, text='Manpower Nodes').grid(column=0, row=config_row, sticky=tk.W)

        config_row += 1

        ttk.Radiobutton(munition_node_frame, text="0", variable=commander.gui_root.manpower_node_gui,
                        command=lambda: commander.gui_update_resources(), value=0).grid(column=1, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="1", variable=commander.gui_root.manpower_node_gui,
                        command=lambda: commander.gui_update_resources(), value=1).grid(column=2, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="2", variable=commander.gui_root.manpower_node_gui,
                        command=lambda: commander.gui_update_resources(), value=2).grid(column=3, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="3", variable=commander.gui_root.manpower_node_gui,
                        command=lambda: commander.gui_update_resources(), value=3).grid(column=4, row=config_row,
                                                                                        sticky=tk.W)

        config_row += 1

        ttk.Label(munition_node_frame, text='Fuel Nodes').grid(column=0, row=config_row, sticky=tk.W)

        config_row += 1

        ttk.Radiobutton(munition_node_frame, text="0", variable=commander.gui_root.fuel_node_gui,
                        command=lambda: commander.gui_update_resources(), value=0).grid(column=1, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="1", variable=commander.gui_root.fuel_node_gui,
                        command=lambda: commander.gui_update_resources(), value=1).grid(column=2, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="2", variable=commander.gui_root.fuel_node_gui,
                        command=lambda: commander.gui_update_resources(), value=2).grid(column=3, row=config_row,
                                                                                        sticky=tk.W)
        ttk.Radiobutton(munition_node_frame, text="3", variable=commander.gui_root.fuel_node_gui,
                        command=lambda: commander.gui_update_resources(), value=3).grid(column=4, row=config_row,
                                                                                        sticky=tk.W)

        config_row +=1

        ttk.Label(frame, text='Heavy Tanks Desired').grid(column=0, row=config_row, sticky=tk.W)
        entry = ttk.Entry(frame, name='entry_heavies_desired')
        entry.grid(row=config_row, column=1, sticky=tk.W)
        entry.insert(0, '3')
        config_row += 1

        ttk.Button(frame, name='button_RESTART', command=lambda: asyncio.create_task(restart_match_async()), text='Restart Match',
                   width=common.BUTTON_WIDTH).grid(column=0, row=config_row)

        config_row += 1
        ttk.Button(frame, name='button_SET_GAME_CLOCK',
                   command=lambda: commander.set_game_clock_from_string(fast_forward_entry.get()),
                   text='Set Game Clock',
                   width=common.BUTTON_WIDTH).grid(column=0, row=config_row)

        config_row += 1
        fast_forward_entry = ttk.Entry(frame, width=10)
        fast_forward_entry.delete(0, END)
        fast_forward_entry.insert(0, "1:28:00")
        # fast_forward_entry.focus()
        fast_forward_entry.grid(column=0, row=config_row)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame
    except Exception as ex:
        print("Exception in create_config_frame")
        print(str(ex))




def on_closing(commander):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        loop = asyncio.get_running_loop()
        loop.stop()
        commander.gui_root.destroy()
        sys.exit(0)


async def run_gui(commander):
    commander.gui_root.title('Hell Let Loose Tank Commander Assistant')
    #commander.gui_root.resizable(0, 0)
    try:
        # windows only (remove the minimize/maximize button)
        commander.gui_root.attributes('-toolwindow', True)
    except tk.TclError:
        print('Not supported on your platform')

    try:
        #commander.gui_root.maxsize(800, 500)
        commander.gui_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(commander))

        commander.gui_root.minsize(800, 600)
        base_frame = tk.Frame(commander.gui_root)
        base_frame.pack(fill="both",expand=True)

        # layout on the root window

        #### Header for resource counts
        resource_frame = create_resource_frame(gui_parent=base_frame, commander=commander)
        resource_frame.grid(row=0, column=0, sticky="nw")
        resource_frame.configure(borderwidth=2, relief=tk.SUNKEN)
        commander.gui_root.rowconfigure(0, weight=1)
        commander.resource_frame = resource_frame


        #### Logger f
        logger_frame = create_log_frame(gui_parent=base_frame, commander=commander)
        logger_frame.grid(row=3, column=0, sticky="nw")
        logger_frame.configure(borderwidth=2, relief=tk.SUNKEN)
        commander.gui_root.rowconfigure(0, weight=5)
        commander.logger_frame = logger_frame

        #### Notebook tabs
        notebook = ttk.Notebook(base_frame, width=600, height=400)
        notebook.grid(row=2, column=0, sticky="nw")
        commander.gui_root.rowconfigure(0, weight=2)
        commander.gui_root.notebook = notebook

        ## Settings (Notebook)
        settings_frame = create_config_frame(gui_parent=base_frame, commander=commander)
        settings_frame.configure(borderwidth=2, relief=tk.SUNKEN)
        notebook.add(settings_frame, text="Configure")
        commander.settings_frame = settings_frame

        ## Commander Abilities (Notebook)
        button_frame = create_button_frame(gui_parent=base_frame, commander=commander)
        button_frame.configure(borderwidth=2, relief=tk.SUNKEN)
        notebook.add(button_frame, text="Commander Abilities")
        commander.button_frame = button_frame

        ## TC (Notebook)
        tc_frame = create_tc_frame(gui_parent=base_frame, commander=commander)
        tc_frame.configure(borderwidth=2, relief=tk.SUNKEN)
        notebook.add(tc_frame, text="Commander's Seat")
        commander.tc_frame = tc_frame



    except Exception as ex:
        print("Exception in run_gui")
        print(str(ex))

    try:
        while True:
            commander.gui_root.update_idletasks()
            commander.gui_root.update()
            scale = commander.settings_frame.children["entry_TIME_SCALE"].get()
            if scale != "":
                try:
                    scale = int(scale)
                    if scale != common.time_scale_global.get():
                        common.time_scale_global.set(scale)
                        commander.settings_frame.children["label_TIME_SCALE"][
                            "text"] = 'Time Scale: 1 Seconds = ' + str(
                            1 * scale) + ' Seconds'
                except ValueError:
                    print("Bad Time Scale Input")
            await asyncio.sleep(0.001)
    except Exception as ex:
        print("Exception in run_gui")
        print(str(ex))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clock = game_clock.Clock(1)
    tracker = resource_tracker.Tracker()
    gui_root = tk.Tk()
    commander = commander.DummyCommander(clock, tracker, gui_root)

    common.time_scale_global = tkinter.IntVar(gui_root, common.DEFAULT_TIME_SCALE)

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(run_gui(commander)),
        loop.create_task(commander.run_accumulator()),
        loop.create_task(commander.command_team()),
        loop.create_task(commander.restart_match())
    ]

    loop.run_forever()
    loop.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
