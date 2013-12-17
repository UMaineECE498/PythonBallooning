#!/usr/bin/python
import wx
import wx.lib.masked as masked
import os
import strmdata

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		self.dirname='.'

		self.values = {'lat' : '10', 
			'lon' : 0, 
			'ltime' : 0, 
			'ldate' : 0, 
			'stime' : 0, 
			'sdate' : 0, 
			'alt' : 0, 
			'arate' : 0, 
			'balt' : 0, 
			'drate' : 0,
		}

		# -1 indicates to use default size
		# this uses a window 200px wide and 100px high
		wx.Frame.__init__(self, parent, title=title, size=(200,200))

		# inputs
		self.inputSizer = wx.BoxSizer(wx.VERTICAL)

		# latitude
		self.latitudeInput = masked.NumCtrl(self, fractionWidth=4, min=0, max=90, limitOnFieldChange=True, value=44.8994)
		self.latitudeDirection = wx.RadioBox(self, choices = ['N','S'])
		self.latitudeLabel = wx.StaticText(self, label="Latitudue:  ")
		self.latitudeSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.latitudeSizer.Add(self.latitudeLabel, 1, wx.EXPAND)
		self.latitudeSizer.Add(self.latitudeInput, 1, wx.EXPAND)
		self.latitudeSizer.Add(self.latitudeDirection, 1, wx.EXPAND)
		self.inputSizer.Add(self.latitudeSizer, 1, wx.EXPAND)
		self.Bind(masked.EVT_NUM, lambda event: self.EvtNum(event, 0), self.latitudeInput)
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxNS, self.latitudeDirection)
		self.directionNS = 0
		self.latitudeDirection.Selection = self.directionNS
		self.values['lat'] = str(self.latitudeInput.GetValue())
		self.SetDirection('lat', 0)

		# longitude
		self.longitudeInput = masked.NumCtrl(self, fractionWidth=4, min=0, max=180, limitOnFieldChange=True, value=68.6681)
		self.longitudeDirection = wx.RadioBox(self, choices = ['E','W'])
		self.longitudeLabel = wx.StaticText(self, label="Longitude:  ")
		self.longitudeSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.longitudeSizer.Add(self.longitudeLabel, 1, wx.EXPAND)
		self.longitudeSizer.Add(self.longitudeInput, 1, wx.EXPAND)
		self.longitudeSizer.Add(self.longitudeDirection, 1, wx.EXPAND)
		self.inputSizer.Add(self.longitudeSizer, 1, wx.EXPAND)
		self.Bind(masked.EVT_NUM, lambda event: self.EvtNum(event, 1), self.longitudeInput)
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxEW, self.longitudeDirection)
		self.directionEW = 1
		self.longitudeDirection.Selection = self.directionEW
		self.values['lon'] = str(self.longitudeInput.GetValue())
		self.SetDirection('lon', 1)

		# altitude
		self.altitudeInput = masked.NumCtrl(self, fractionWidth=2, min=0, limitOnFieldChange=True)
		self.altitudeLabel = wx.StaticText(self, label="Altitude:  ")
		self.altitudeCheckBox = wx.CheckBox(self, label="User Defined")
		self.altitudeSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.altitudeSizer.Add(self.altitudeLabel, 1, wx.EXPAND)
		self.altitudeSizer.Add(self.altitudeInput, 1, wx.EXPAND)
		self.altitudeSizer.Add(self.altitudeCheckBox, 1, wx.EXPAND)
		self.inputSizer.Add(self.altitudeSizer, 1, wx.EXPAND)
		self.Bind(masked.EVT_NUM, lambda event: self.EvtNum(event, 2), self.altitudeInput)
		self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.altitudeCheckBox)
		self.values['alt'] = str(self.altitudeInput.GetValue())
		self.userDefinedAlt = 0

		# launch time
		self.launchTimeInput = masked.TimeCtrl(self, -1, fmt24hr=False, displaySeconds=False)
		self.launchTimeLabel = wx.StaticText(self, label="Launch Time:  ")
		self.launchTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.launchTimeSizer.Add(self.launchTimeLabel, 1, wx.EXPAND)
		self.launchTimeSizer.Add(self.launchTimeInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.launchTimeSizer, 1, wx.EXPAND)
		self.launchTimeInput.Bind(masked.EVT_TIMEUPDATE, self.EvtTimeCtrl, self.launchTimeInput)
		self.values['ltime'] = str(self.launchTimeInput.GetValue())

		# launch date
		self.launchDateInput = wx.DatePickerCtrl(self, -1)
		self.launchDateLabel = wx.StaticText(self, label="Launch Date:  ")
		self.launchDateSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.launchDateSizer.Add(self.launchDateLabel, 1, wx.EXPAND)
		self.launchDateSizer.Add(self.launchDateInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.launchDateSizer, 1, wx.EXPAND)
		self.Bind(wx.EVT_DATE_CHANGED, self.EvtDatePickerCtrl, self.launchDateInput)
		self.values['ldate'] = str(self.FindDate(self.launchDateInput))

		# start time
		self.startTimeInput = masked.TimeCtrl(self, -1, fmt24hr=False, displaySeconds=False)
		self.startTimeLabel = wx.StaticText(self, label="Start Time:  ")
		self.startTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.startTimeSizer.Add(self.startTimeLabel, 1, wx.EXPAND)
		self.startTimeSizer.Add(self.startTimeInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.startTimeSizer, 1, wx.EXPAND)
		self.startTimeInput.Bind(masked.EVT_TIMEUPDATE, self.EvtTimeCtrl, self.startTimeInput)
		self.values['stime'] = str(self.startTimeInput.GetValue())

		# start date
		self.startDateInput = wx.DatePickerCtrl(self, -1)
		self.startDateLabel = wx.StaticText(self, label="Start Date:  ")
		self.startDateSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.startDateSizer.Add(self.startDateLabel, 1, wx.EXPAND)
		self.startDateSizer.Add(self.startDateInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.startDateSizer, 1, wx.EXPAND)
		self.Bind(wx.EVT_DATE_CHANGED, self.EvtDatePickerCtrl, self.startDateInput)
		self.values['sdate'] = str(self.FindDate(self.startDateInput))

		# ascent rate
		self.ascentRateInput = masked.NumCtrl(self, fractionWidth=3)
		self.ascentRateLabel = wx.StaticText(self, label="Ascent Rate:  ")
		self.ascentRateSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.ascentRateSizer.Add(self.ascentRateLabel, 1, wx.EXPAND)
		self.ascentRateSizer.Add(self.ascentRateInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.ascentRateSizer, 1, wx.EXPAND)
		self.Bind(masked.EVT_NUM, lambda event: self.EvtNum(event, 5), self.ascentRateInput)
		self.values['arate'] = str(self.ascentRateInput.GetValue())

		# burst altitude
		self.burstAltitudeInput = masked.NumCtrl(self, fractionWidth=2, min=0, limitOnFieldChange=True)
		self.burstAltitudeLabel = wx.StaticText(self, label="Burst Altitude:  ")
		self.burstAltitudeSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.burstAltitudeSizer.Add(self.burstAltitudeLabel, 1, wx.EXPAND)
		self.burstAltitudeSizer.Add(self.burstAltitudeInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.burstAltitudeSizer, 1, wx.EXPAND)
		self.Bind(masked.EVT_NUM, lambda event: self.EvtNum(event, 6), self.burstAltitudeInput)
		self.values['balt'] = str(self.burstAltitudeInput.GetValue())

		# descent rate
		self.descentRateInput = masked.NumCtrl(self, fractionWidth=3)
		self.descentRateLabel = wx.StaticText(self, label="Descent Rate:  ")
		self.descentRateSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.descentRateSizer.Add(self.descentRateLabel, 1, wx.EXPAND)
		self.descentRateSizer.Add(self.descentRateInput, 1, wx.EXPAND)
		self.inputSizer.Add(self.descentRateSizer, 1, wx.EXPAND)
		self.Bind(masked.EVT_NUM, lambda event: self.EvtNum(event, 7), self.descentRateInput)
		self.values['drate'] = str(self.descentRateInput.GetValue())

		# buttons
		self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.mySetButton = wx.Button(self, wx.ID_OK, "Set Values")
		self.buttonSizer.Add(self.mySetButton, 2)
		self.Bind(wx.EVT_BUTTON, self.OnClick, self.mySetButton)

		# creates the status bar at the bottom of the window
		self.CreateStatusBar()

		# Some sizers to see layout options
		self.sizer2 = wx.BoxSizer(wx.VERTICAL)
		self.sizer2.Add(self.inputSizer, 0, wx.EXPAND)
		self.sizer2.Add(self.buttonSizer, 0, wx.EXPAND)

		# Layout Sizers
		self.SetSizer(self.sizer2)
		self.SetAutoLayout(1)
		self.sizer2.Fit(self)
		self.Show()

	def EvtCheckBox(self, event):
		self.userDefinedAlt = event.GetInt()

	def EvtTimeCtrl(self, event):
		self.values[3] = event.GetValue()

	def EvtDatePickerCtrl(self, event, index):
		self.values[index] = self.FindDate(event)
		self.values[index] = self.FindDate(event)

	def EvtRadioBoxNS(self, event):
		self.directionNS = event.GetInt()
		self.SetDirection(0, self.directionNS)

	def EvtRadioBoxEW(self, event):
		self.directionEW = event.GetInt()
		self.SetDirection(1, self.directionEW)

	def EvtNum(self, event, index):
		self.values[index] = str(event.GetValue())

	def FindDate(self, selection):
		val = selection.GetValue()
		month = val.Month+1
		day = val.Day
		year = val.Year
		dateStr = "%02d/%02d/%4d" % (month, day, year)
		return dateStr

	def SetDirection(self, index, direction):
		if (direction == 0):
			self.values[index] = str(abs(float(self.values[index])))
		else:
			self.values[index] = str(-1*abs(float(self.values[index])))
		
	# needs to take all the events
	def OnClick(self, event):
		# check validity of latitude
		if (strmdata.getDottedDecimal(self.values['lat']) == None):
			# need to add dialog for this
			print("Invalid Latitude")
			return None

		# check validity of longitude
		if (strmdata.getDottedDecimal(self.values['lon']) == None):
			# need to add dialog for this
			print("Invalid Longitude")
			return None
		
		# check to see if using user supplied
		if (self.userDefinedAlt == 0):
			print("Using Calculated Altitude")
			self.values['alt'] = str(strmdata.getElevation(self.values['lat'], self.values['lon']))
		else:
			print("Using User Defined Altitude")

		print("Valid Data")

		# write all the values somewhere or something instead of printing them out 
		for string in self.values:
			print (string + ' = ' + self.values[string])


app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()
