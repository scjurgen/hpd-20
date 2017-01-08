#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

from hpd20 import Semantics
from instrumentname import get_instrument_name, get_instrument_pitch
from melodypadpattern import melody_pad_pattern
from scales import Scale
import wx.grid as gridlib

class SetScaleDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(SetScaleDialog, self).__init__(*args, **kw)
        self.init_ui()
        self.SetSize((1024, 800))
        self.SetTitle("Set Scale to Kit Dialog")

    def set_hpd(self, hpd, current_kit):
        self.current_kit = current_kit
        self.hpd = hpd

    def init_ui(self):
        self.panel = wx.Panel(self)
        top_sizer = wx.BoxSizer(wx.VERTICAL)

        label_instrument = wx.StaticText(self.panel,  label="Instrument")
        msets = Scale.melodic_sets.keys()
        msets.sort()
        self.cb_instrument = wx.ComboBox(self.panel,  0, choices=msets, style=wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_instrument.Bind(wx.EVT_COMBOBOX, self.select_instrument)

        scales = Scale.scale_patterns.keys()
        scales.sort()
        label_scale = wx.StaticText(self.panel,  label="Scale")
        self.cb_scale = wx.ComboBox(self.panel,  0, choices=scales, style=wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_scale.Bind(wx.EVT_COMBOBOX, self.select_scale)

        label_mode = wx.StaticText(self.panel,  label="Mode")
        self.cb_mode = wx.ComboBox(self.panel,  0, choices=[str(i) for i in range(12)], style=wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_mode.Bind(wx.EVT_COMBOBOX, self.select_mode)

        label_key = wx.StaticText(self.panel, label="Root note")
        self.cb_key = wx.ComboBox(self.panel,  0, choices=Scale.get_root_notes(), style=wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_key.Bind(wx.EVT_COMBOBOX, self.select_key)
        self.cb_key.SetSelection(3*12)  # set default selection to first C4

        label_pattern = wx.StaticText(self.panel, label="Pad layout")
        mpat = melody_pad_pattern.keys()
        mpat.sort()
        self.cb_pad_pattern = wx.ComboBox(self.panel,  0, choices=mpat, style=wx.TE_PROCESS_ENTER | wx.CB_READONLY)
        self.cb_pad_pattern.Bind(wx.EVT_COMBOBOX, self.select_pad_pattern)

        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        setButton = wx.Button(self.panel, label='set')
        closeButton = wx.Button(self.panel, label='close')
        setButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

        horizontal_box_sizer.Add(setButton)
        horizontal_box_sizer.Add(closeButton, flag=wx.LEFT, border=5)

        fgs = wx.FlexGridSizer(5, 2, 9, 10)

        fgs.AddMany([(label_instrument, 1, wx.EXPAND), (self.cb_instrument, 1, wx.EXPAND),
                            (label_scale, 1, wx.EXPAND), (self.cb_scale, 1, wx.EXPAND),
                            (label_mode, 1, wx.EXPAND), (self.cb_mode, 1, wx.EXPAND),
                            (label_key, 1, wx.EXPAND), (self.cb_key, 1, wx.EXPAND),
                            (label_pattern, 1, wx.EXPAND), (self.cb_pad_pattern, 1, wx.EXPAND)
                            ])

        self.result_grid = gridlib.Grid(self.panel)
        self.result_grid.CreateGrid(17, 4)
        self.result_grid.SetColSize(0, 200)
        self.result_grid.SetColLabelValue(0, 'instrument')
        self.result_grid.SetColLabelValue(1, 'note')
        self.result_grid.SetColLabelValue(2, 'cents')
        self.result_grid.SetColLabelValue(3, 'pan')

        top_sizer.Add(self.result_grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        top_sizer.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        top_sizer.Add(horizontal_box_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        self.panel.SetSizer(top_sizer)
        self.select_pad_pattern(None)

    def copy_current_selection_to_result_grid(self, event):
        instrument = self.cb_instrument.GetStringSelection()
        pad_pattern = self.cb_pad_pattern.GetStringSelection()
        note_count = len(melody_pad_pattern[pad_pattern])
        scale_name = self.cb_scale.GetStringSelection()
        first_note = Scale.get_height_of_note(self.cb_key.GetStringSelection())
        mode = int(self.cb_mode.GetStringSelection())
        scale = Scale.get_scale(instrument, first_note, note_count, scale_name, mode=mode)
        for i in range(0, 17):
            self.result_grid.SetCellValue(i, 0, "")
            self.result_grid.SetCellValue(i, 1, "")
            self.result_grid.SetCellValue(i, 2, "")
            self.result_grid.SetCellBackgroundColour(i, 1, wx.WHITE)
        for i in range(len(scale)):
            index = i
            self.result_grid.SetCellValue(index, 0, get_instrument_name(scale[i][0]))
            if abs(scale[i][1]) > 2400:
                self.result_grid.SetCellBackgroundColour(index, 1, wx.RED)
            else:
                self.result_grid.SetCellBackgroundColour(index, 1, wx.WHITE)
            pitch = scale[i][1] + get_instrument_pitch(scale[i][0])
            real_note = Scale.get_note_name(int((pitch+50) / 100))

            self.result_grid.SetCellValue(index, 1, real_note)
            self.result_grid.SetCellValue(index, 2, str(scale[i][1]))

    def show_result(self):
        self.copy_current_selection_to_result_grid(None)

    def select_scale(self, event):
        self.copy_current_selection_to_result_grid(None)

    def select_mode(self, event):
        self.copy_current_selection_to_result_grid(None)

    def select_pad_pattern(self, event):
        for i in range(len(Semantics.pad_names)):
            self.result_grid.SetCellEditor(2, i, gridlib.GridCellNumberEditor(-2400, 2400))
            self.result_grid.SetCellEditor(3, i, gridlib.GridCellNumberEditor(-15, 15))
            self.result_grid.SetRowLabelValue(i, "")

        pad_pattern = self.cb_pad_pattern.GetStringSelection()
        current_pattern = melody_pad_pattern[pad_pattern]

        for i in range(len(current_pattern)):
            self.result_grid.SetRowLabelValue(i, Semantics.pad_names[current_pattern[i]])
        self.copy_current_selection_to_result_grid(None)

    def select_key(self, event):
        self.copy_current_selection_to_result_grid(None)

    def select_instrument(self, event):
        self.copy_current_selection_to_result_grid(None)

    def OnOk(self, e):
        instrument = self.cb_instrument.GetStringSelection()
        pad_pattern = self.cb_pad_pattern.GetStringSelection()
        current_pattern = melody_pad_pattern[pad_pattern]
        scale_name = self.cb_scale.GetStringSelection()
        first_note = int(Scale.get_height_of_note(self.cb_key.GetStringSelection()))
        mode = int(self.cb_mode.GetStringSelection())
        self.hpd.apply_scale(instrument, scale_name, mode, first_note, int(self.current_kit), current_pattern)
        self.Close()
        self.Destroy()

    def OnClose(self, e):
        self.Close()
        self.Destroy()


