#!/usr/bin/python
# -*- coding: utf-8 -*-


# http://jenyay.net/Programming/WxSizer
import ConfigParser
import os
import wx
import wx.grid as gridlib

import hpd20

from instrumentname import get_instrument_pitch, get_instrument_name, get_complete_instrument_list

wx.SetDefaultPyEncoding('utf-8')

class MyForm(wx.Frame):

    def load_config(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.add_section('Settings')
        self.config_filename = os.path.expanduser('~/.hpd.cfg')
        self.current_kit = 1
        try:
            self.config.read(os.path.expanduser('~/.hpd.cfg'))
            self.default_kits_dir = self.config.get('Settings', 'kits_directory')
            self.default_backup_dir = self.config.get('Settings', 'backup_directory')
            self.current_kit = self.config.get_int('Settings', 'current_kit')

        except:
            self.default_kits_dir = ""
            self.default_backup_dir = ""
            self.current_kit = 1

    def __init__(self, file_name):
        self.load_config()
        self.invisible_color = wx.Colour(200, 200, 200)
        self.neutral_color = wx.Colour(230, 230, 230)
        self.o_colors = [wx.Colour(210, 210, 250), wx.Colour(235, 235, 255)]
        self.s_colors = [wx.Colour(210, 250, 210), wx.Colour(235, 255, 235)]
        self.m_colors = [wx.Colour(250, 210, 210), wx.Colour(255, 235, 235)]

        self.hpd = hpd20.hpd(file_name)
        wx.Frame.__init__(self, parent=None, title="hpd-20 Editor", size=(1200, 830))
        self.panel = wx.Panel(self)
        self.layout_menu()
        self.layout_kit_grid()
        self.main_param_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_kit = wx.ComboBox(self.panel, -1, choices=self.hpd.kits.get_list_of_kits(), style=wx.TE_PROCESS_ENTER|wx.CB_READONLY)
        self.cb_kit.Bind(wx.EVT_COMBOBOX, self.select_kit)
        self.cb_kit_name = wx.TextCtrl(self.panel, size=(300, -1), value="current kit name", style=wx.TE_PROCESS_ENTER)
        self.cb_kit.Bind(wx.EVT_CHAR, self.change_kit_name)
        self.main_param_sizer.Add(self.cb_kit)
        self.main_param_sizer.Add(self.cb_kit_name)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.main_param_sizer)
        sizer.Add(self.kit_grid)
        self.panel.SetSizer(sizer)

    def select_kit(self, event):
        kit = self.cb_kit.GetCurrentSelection()
        self.fill_kit(kit)

    def change_kit_name(self, event):
        pass


    def layout_menu(self):
        menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        open_item = menu1.Append(wx.ID_OPEN, '&Open memory dump')

        self.Bind(wx.EVT_MENU, self.load_memory_backup, open_item)
        save_item = menu1.Append(wx.ID_SAVE, '&Save memory dump')
        self.Bind(wx.EVT_MENU, self.save_memory_backup, save_item)
        menu1.AppendSeparator()
        loadkit_item = menu1.Append(wx.ID_ANY, 'Load Kit (overwrites current)')
        self.Bind(wx.EVT_MENU, self.load_kit, loadkit_item)
        savekit_item = menu1.Append(wx.ID_ANY, 'Save Kit')
        self.Bind(wx.EVT_MENU, self.save_kit, savekit_item)
        menu1.AppendSeparator()
        fitem = menu1.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menu6 = wx.Menu()
        menuBar.Append(menu6, '&Tools')
        menu7 = wx.Menu()
        menuBar.Append(menu7, '&Macros')
        menu7.Append(wx.ID_ANY, 'Set Scale')
        menu7.Append(wx.ID_ANY, 'Pan')

        menu8 = wx.Menu()
        menuBar.Append(menu8, '&Help')

        self.SetMenuBar(menuBar)

    def layout_kit_grid(self):
        self.columns = ['Layer', 'fade', 'trigger', 'velo', 'mutgrp', 'mn/ply','Instrument', 'nr', 'vol', 'cents', 'note', 'muff', 'color', 'swp', 'ambsend']
        self.pad_names = ['M1 ◵', 'M2 ◶', 'M3 ◴', 'M4 ◷', 'M5 ●',
                          'S1', 'S2', 'S3', 'S4',
                          'S5', 'S6', 'S7', 'S8',
                          'D-Beam', 'Head', 'Rim', 'HH']
        self.kit_grid = gridlib.Grid(self.panel)
        self.kit_grid.CreateGrid(len(self.pad_names)*2, len(self.columns))
        for i in range(len(self.columns)):
            self.kit_grid.SetColLabelValue(i, self.columns[i])
            self.kit_grid.SetColSize(i, 48)
        for i in range(len(self.pad_names)):
            self.kit_grid.SetRowSize(i, 24)
            self.kit_grid.SetRowLabelValue(i * 2, self.pad_names[i])
            self.kit_grid.SetRowLabelValue(i * 2+1, '')
            for col in range(len(self.columns)):
                if self.pad_names[i][0] == 'M':
                    color = self.m_colors[i % 2]
                elif self.pad_names[i][0] == 'S':
                    color = self.s_colors[i % 2]
                else:
                    color = self.o_colors[i % 2]
                self.kit_grid.SetCellBackgroundColour(i*2, col, color)
                if col < 6:
                    self.kit_grid.SetCellBackgroundColour(i*2+1, col, self.neutral_color)
                else:
                    self.kit_grid.SetCellBackgroundColour(i*2+1, col, color)

        self.kit_grid.SetColSize(6, 200)
        #        self.kit_grid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        #print self.kit_grid.GetCellValue(0, 0)

        self.kit_grid.SetCellTextColour(1, 1, wx.RED)
        self.kit_grid.SetCellBackgroundColour(2, 2, wx.CYAN)
        self.fill_kit(self.current_kit)

    def fill_kit(self, kit):

        instr_index = 6
        layer_type = ['off', 'mix', 'velo mix', 'velo fade', 'velo sw']

        for i in range(17):
            pad = self.hpd.pads.get_pad(kit * hpd20.hpd.PADS_PER_KIT + i)
            if pad.get_layer() == 0:
                for j in range(len(self.columns)):
                    self.kit_grid.SetCellTextColour(i * 2 + 1, j, self.invisible_color)
            else:
                for j in range(len(self.columns)):
                    self.kit_grid.SetCellTextColour(i * 2 + 1, j, wx.BLACK)
            self.kit_grid.SetCellValue(i * 2, 0, layer_type[pad.get_layer()])
            for instr in range(2):
                choice_editor = gridlib.GridCellChoiceEditor(get_complete_instrument_list(), True)
                self.kit_grid.SetCellEditor(i * 2 + instr, instr_index+0, choice_editor)
                self.kit_grid.SetCellValue(i * 2 + instr, instr_index+0, get_instrument_name(pad.get_patch(instr)))
                self.kit_grid.SetCellValue(i * 2 + instr, instr_index+1, str(pad.get_patch(instr)+1))
                self.kit_grid.SetCellEditor(i * 2 + instr, instr_index+2, gridlib.GridCellNumberEditor(0, 1900))
                self.kit_grid.SetCellValue(i * 2 + instr, instr_index+2, str(pad.get_volume(instr)))
                self.kit_grid.SetCellEditor(i * 2 + instr, instr_index+2, gridlib.GridCellNumberEditor(0, 127))
                pitch = pad.get_pitch(instr)
                self.kit_grid.SetCellValue(i * 2 + instr, instr_index+3, str(pitch))
                self.kit_grid.SetCellEditor(i * 2 + instr, instr_index+3, gridlib.GridCellNumberEditor(-2400, 2400))
                pitch = pitch + get_instrument_pitch(pad.get_patch(instr))
                real_note = hpd20.get_note_name(pitch / 100)
                self.kit_grid.SetCellValue(i * 2 + instr, instr_index+4, str(real_note))

    def load_kit(self, event):
        openFileDialog = wx.FileDialog(self, "Load Kit to current set", self.default_kits_dir, "",
                                       "hpd-20 Kit (*.kit)|*.kit",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        openFileDialog.Destroy()
        self.default_kits_dir = path
        self.config.set('Settings', 'kits_directory', os.path.dirname(path))
        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)
        self.fill_kit(2)

    def save_kit(self, event):
        openFileDialog = wx.FileDialog(self, "Save Kit", self.default_kits_dir, "",
                                       "hpd-20 Kit (*.kit)|*.kit",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        openFileDialog.Destroy()
        self.default_kits_dir = path
        self.config.set('Settings', 'kits_directory', os.path.dirname(path))
        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)
        self.fill_kit(3)

    def load_memory_backup(self, event):
        openFileDialog = wx.FileDialog(self, "Open a memory dump", self.default_backup_dir, "",
                                       "hpd-20 Dump (*.HS0)|*.HS0",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        openFileDialog.Destroy()
        self.default_backup_dir = path
        self.config.set('Settings', 'backup_directory', os.path.dirname(path))
        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)
        self.hpd = hpd20.hpd(str(path))

    def save_memory_backup(self, event):
        saveFileDialog = wx.FileDialog(self, "Save memory dump as", self.default_backup_dir, "",
                                             "hpd-20 Dump (*.HS0)|*.HS0",
                                             wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        path = saveFileDialog.GetPath()
        saveFileDialog.Destroy()
        self.default_backup_dir = path
        self.config.set('Settings', 'backup_directory', os.path.dirname(path))
        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)
        self.hpd.save_file(str(path))

def run_main():
    app = wx.App(False)
    frame = MyForm('Backup/BKUP-022.HS0')
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    run_main()

