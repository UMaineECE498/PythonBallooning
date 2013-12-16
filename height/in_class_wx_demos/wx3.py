#!/usr/bin/python
import wx

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(200,100))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar()

		filemenu = wx.Menu()

		filemenu.Append(wx.ID_ABOUT, "&About", "Info about this prgm.")
		filemenu.AppendSeparator()
		filemenu.Append(wx.ID_EXIT, "E&xit", " terminate the program")

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)
		self.Show(True)

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()