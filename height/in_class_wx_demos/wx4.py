#!/usr/bin/python
import wx

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(200,100))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar()

		filemenu = wx.Menu()

		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Info about this prgm.")
		filemenu.AppendSeparator()
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " terminate the program")

		self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.onExit, menuExit)

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)
		self.Show(True)
	def onAbout(self, event):
		dlg = wx.MessageDialog(self, "A small text editor", "About sample editor", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def onExit(self, event):
		self.Close(True)

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()