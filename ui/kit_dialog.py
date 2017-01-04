#!/usr/bin/python
# -*- coding: utf-8 -*-


# http://jenyay.net/Programming/WxSizer

import wx
import wx.grid as gridlib

import hpd20
from instrumentname import get_instrument_pitch, get_instrument_name, get_complete_instrument_list

wx.SetDefaultPyEncoding('utf-8')

class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="HPD-20 Editor", size=(1050, 860))
        self.panel = wx.Panel(self)
        self.layout_menu()
        self.layout_kit_grid()

    def layout_menu(self):
        menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        menu1.Append(wx.ID_OPEN, '&Open memory dump')
        menu1.Append(wx.ID_SAVE, '&Save memory dump')
        menu1.AppendSeparator()
        menu1.Append(wx.ID_ANY, 'Load Kit (overwrites current)')
        menu1.Append(wx.ID_ANY, 'Save Kit')
        menu1.AppendSeparator()
        fitem = menu1.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menu2 = wx.Menu()
        menuBar.Append(menu2, '&Edit')
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
        self.columns = ['Instr', 'nr', 'vol', 'cents', 'note', 'muff', 'color', 'swp', 'ambsend']
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
            #self.kit_grid.SetReadOnly(i, 0)
            self.kit_grid.SetRowLabelValue(i * 2, self.pad_names[i])
            self.kit_grid.SetRowLabelValue(i * 2+1, '')
        self.kit_grid.SetColSize(0, 200)
        #        self.kit_grid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        print self.kit_grid.GetCellValue(0, 0)
        self.kit_grid.SetCellValue(1, 1, "127")
        self.kit_grid.SetCellTextColour(1, 1, wx.RED)

        self.kit_grid.SetCellBackgroundColour(2, 2, wx.CYAN)

        self.kit_grid.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1, 1000))
        self.kit_grid.SetCellValue(5, 0, "123")
        self.kit_grid.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        self.kit_grid.SetCellValue(6, 0, "123.34")
        self.kit_grid.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())

        #toolbar2 = wx.ToolBar(self, wx.TB_HORIZONTAL | wx.TB_TEXT)

        self.fill_kit(130)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((50, 50), 0)
        sizer.Add(self.kit_grid)
        sizer.Add((50, 50), 0)
        self.panel.SetSizer(sizer)


    def fill_kit(self, kit):
        for i in range(17):
            pad = hpd.pads.get_pad(kit * hpd20.HPD.PADS_PER_KIT + i)
            if pad.get_layer() == 0:
                for j in range(len(self.columns)):
                    self.kit_grid.SetCellTextColour(i * 2 + 1, j, wx.YELLOW)
            for instr in range(2):
                choice_editor = gridlib.GridCellChoiceEditor(get_complete_instrument_list(), True)
                self.kit_grid.SetCellEditor(i * 2 + instr, 0, choice_editor)
                self.kit_grid.SetCellValue(i * 2 + instr, 5, str(pad.get_layer()))
                self.kit_grid.SetCellValue(i * 2 + instr, 0, get_instrument_name(pad.get_patch(instr)))
                self.kit_grid.SetCellValue(i * 2 + instr, 1, str(pad.get_patch(instr)+1))
                self.kit_grid.SetCellEditor(i * 2 + instr, 2, gridlib.GridCellNumberEditor(0, 1900))
                self.kit_grid.SetCellValue(i * 2 + instr, 2, str(pad.get_volume(instr)))
                self.kit_grid.SetCellEditor(i * 2 + instr, 2, gridlib.GridCellNumberEditor(0, 127))
                pitch = pad.get_pitch(instr)
                self.kit_grid.SetCellValue(i * 2 + instr, 3, str(pitch))
                self.kit_grid.SetCellEditor(i * 2 + instr, 3, gridlib.GridCellNumberEditor(-2400, 2400))
                pitch = pitch + get_instrument_pitch(pad.get_patch(instr))
                real_note = hpd20.get_note_name(pitch / 100)
                self.kit_grid.SetCellValue(i * 2 + instr, 4, str(real_note))


if __name__ == "__main__":
    hpd = hpd20.HPD('Backup/BKUP-022.HS0')
    app = wx.PySimpleApp()
    frame = MyForm()
    frame.Show()
    app.MainLoop()