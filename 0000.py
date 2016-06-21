# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
#from PIL import ImageTk, Image
from subprocess import PIPE, Popen
import definitions as defs
import helping_functions as h_f
import GetScanners, subprocess, time, sys

class Application(Frame):
	""" A GUI for the Bookscanner"""	
	def __init__(self, master, StepperSignalGeneration,TMC5130):
		"""Initialization of the Frame"""
		self.StepperSignalGeneration = StepperSignalGeneration
		self.TMC5130 = TMC5130
		Frame.__init__(self,master)
		self.grid()
		self.create_widgets()		
		
	def my_output_written (*args):
		print "my_output_written",my_output.get()
		update_output(my_output.get())	
		
	def create_widgets(self):		
		#img = PhotoImage(file='Logo_small.gif')
		
		#self.im_label = Label (self, image = img)
		#self.im_label.grid(row = 0, column = 0)
		
		self.ScannerDetection_button = Button (self, text = "Detect Scanners", command = lambda: self.GetScanners(my_output))
		self.ScannerDetection_button.grid(row = 1, column = 0, sticky = W)
		
		justDriveNoScanVar = IntVar()
		self.justDriveNoScan = Checkbutton(self,text="Just Drive No Scanning", variable=justDriveNoScanVar)
		self.justDriveNoScan.toggle()
		self.justDriveNoScan.grid(row = 1, column = 1)

		self.label4 = Label(self, text= self.StepperSignalGeneration)		
		self.label4.grid(row = 1, column = 2, sticky = E)
		
		self.scan_book_button = Button (self, text="Start Book Scan", command = lambda: self.StartBookScan(justDriveNoScanVar.get()))
		self.scan_book_button.grid(row = 2, column = 2, sticky = E)
		
		self.label2 = Label(self, text= "Travel times:")		
		self.label2.grid(row = 2, column = 0, sticky = E)
		
		self.travel_times = Entry(self)
		self.travel_times.insert(0,"1")
		self.travel_times.grid(row = 2, column = 1, sticky = E)		

		ttk.Separator(self, orient=HORIZONTAL).grid(row=3, columnspan = 3, sticky = EW)               
		
		self.label3 = Label(self, text= "Feedback:")		
		self.label3.grid(row = 4, column = 0, sticky = E)
		
		self.text = Text(self, width = 45, height = 2, wrap = WORD)
		self.text.grid(row = 4, column = 1, columnspan = 3,  sticky = W)
		
		ttk.Separator(self, orient=HORIZONTAL).grid(row=5, columnspan = 3, sticky = EW)
		
		self.instructionMoveDistance = Label(self, text= "Enter the distance in MM and choose direction and speed!")		
		self.instructionMoveDistance.grid(row = 6, column = 0, columnspan = 2, sticky = W)
		
		self.move_MM_entry = Entry(self)
		self.move_MM_entry.grid(row = 7, column = 0, sticky = W)
		
		direction = StringVar (self)
		direction.set("towards Scanner")
		self.ChooseDirection = OptionMenu(self,direction,"towards Scanner","towards Motor")
		self.ChooseDirection.grid(row = 7, column = 1)
		
		mode = StringVar (self)
		mode.set("Travel mode")
		self.ChooseMode = OptionMenu(self,mode,"Travel mode","Scan mode")
		self.ChooseMode.grid(row = 7, column = 2, sticky = E)

		self.move_steps_button = Button (self, text="Move distance", command = lambda: self.MoveSteps(direction.get(),mode.get()))
		self.move_steps_button.grid(row = 8, column = 0, sticky = W)
		
		self.label1 = Label(self, text= "or")		
		self.label1.grid(row = 8, column = 1, sticky = W)
		
		self.move2endstop_button = Button (self, text="Move to Endstop", command = lambda: self.move2endstop(direction.get(),mode.get()))
		self.move2endstop_button.grid(row = 8, column = 2, sticky = E)
		
		ttk.Separator(self, orient=HORIZONTAL).grid(row=9, columnspan = 3, sticky = EW)
		
		testPin_for_output = StringVar (self)
		testPin_for_output.set("IR LED Enable")
		self.ChoosetestPin = OptionMenu(self,testPin_for_output,"IR LED Enable","Stepper Direction", "Scanner1 Endstop", "Scanner2 Endstop", "Coanda Effector","PWM Clock Pin","TMC Enable")
		self.ChoosetestPin.grid(row = 10, column = 1, sticky = W)
		
		self.testPin_button = Button(self, text="Test Pin Output", command = lambda: self.testPinOutput(testPin_for_output.get()))
		self.testPin_button.grid(row = 10, column = 0, sticky = W)

		self.startMotor_button = Button(self, text="Start Motor", state=DISABLED, command = lambda: self.startMotor())
		self.startMotor_button.grid(row = 10, column = 2, sticky = E)
		
		testPin_for_input = StringVar (self)
		testPin_for_input.set("Endstop Scanner")
		self.ChoosetestPinInput = OptionMenu(self,testPin_for_input,"Endstop Scanner", "Endstop Motor","TMC Position Compare","TMC Interrupt Event","Emergency Stop")
		self.ChoosetestPinInput.grid(row = 11, column = 1, sticky = W)
		
		self.testPinInput_button = Button (self, text="Test Pin Input", command = lambda: self.testPinInput(testPin_for_input.get()))
		self.testPinInput_button.grid(row = 11, column = 0, sticky = W)

		self.stopMotor_button = Button(self, text="Stop Motor", state=DISABLED, command = lambda: self.stopMotor())
		self.stopMotor_button.grid(row = 11, column = 2, sticky = E)
		
		ttk.Separator(self, orient=HORIZONTAL).grid(row=12, columnspan = 3, sticky = EW)	
						
		self.Homing_button = Button (self, text="Home Position",state=DISABLED, command = lambda: self.setHomePosition())
		self.Homing_button.grid(row = 13, column = 0, sticky = W)

		self.readPosition_button = Button (self, text="Read Position", state=DISABLED, command = lambda: self.readXACTUAL())
		self.readPosition_button.grid(row = 13, column = 1, sticky = W)

		self.readIOIN_button = Button (self, text="Read IOIN", state=DISABLED, command = lambda: self.readIOIN())
		self.readIOIN_button.grid(row = 13, column = 2, sticky = E)

		self.readSPI_button = Button (self, text="Read SPI Status", state=DISABLED, command = lambda: self.readSPI())
		self.readSPI_button.grid(row = 14, column = 0, sticky = W)

		self.readRAMP_STAT_button = Button (self, text="Read RAMP_STAT", state=DISABLED, command = lambda: self.readRAMP_STAT())
		self.readRAMP_STAT_button.grid(row = 14, column = 1, sticky = W)
		
		self.readSW_MODE_button = Button (self, text="Read SW_MODE", state=DISABLED, command = lambda: self.readSW_MODE())
		self.readSW_MODE_button.grid(row = 14, column = 2, sticky = E)

		self.quit_button = Button (self, text="Quit", command = self.quit)
		self.quit_button.grid(row = 15, column = 2, sticky = E)

		self.activateButtons()
##		my_output = StringVar()	
##		my_output.trace("w",my_output_written())
##		
##		self.text2 = Label(self, textvariable = my_output, width = 45, height = 2, bg = "#fff")
##		self.text2.grid(row = 13, column = 0, columnspan = 2,  sticky = W)

	def activateButtons(self):
		if self.TMC5130 != 'none':
			self.startMotor_button['state'] = 'normal'
			self.stopMotor_button['state'] = 'normal'
			self.Homing_button['state'] = 'normal'
			self.readPosition_button['state'] = 'normal'
			self.readIOIN_button['state'] = 'normal'
			self.readSPI_button['state'] = 'normal'
			self.readRAMP_STAT_button['state'] = 'normal'
			self.readSW_MODE_button['state'] = 'normal'
		
	def testPinInput(self,pin):
		''' Read GPIO Input Signal'''
		self.text.delete(0.0, END)
		self.text.insert(0.0, "Input of Pin " + str(h_f.translate_pin(pin)) + " is " + str(GPIOFunc.readPinInput(h_f.translate_pin(pin))))
	
	def testPinOutput(self,pin):
		''' Test GPIO Output '''
		GPIOFunc.testPinOutput(h_f.translate_pin(pin))

	def startMotor(self):
		self.TMC5130.setCHOPCONFStandard()
		self.text.delete(0.0, END)
		self.text.insert(0.0, "Motor ready!")

	def stopMotor(self):
		self.TMC5130.stopMotor()
		self.text.delete(0.0, END)
		self.text.insert(0.0, "Motor stopped!")

	def setHomePosition(self):
		self.TMC5130.writeIntegerValue2Adress('RAMPMODE',3,0)
		self.TMC5130.setHomePosition()
		self.TMC5130.writeIntegerValue2Adress('RAMPMODE',0,0)
		self.text.delete(0.0, END)
		self.text.insert(0.0, "Actual Position set to Zero!")

	def readXACTUAL(self):
		Position = self.TMC5130.readIntegerfromAdress('XACTUAL')
		Position = - (2**32 - Position) if Position > (2**31)-1 else Position
		self.text.delete(0.0, END)
		self.text.insert(0.0, "Actual Position is: " + str(Position / self.TMC5130.readStepResolution() / float(defs.STEPS_PER_MM)) + ' mm!')            

	def readIOIN(self):
		self.text.delete(0.0, END)
		self.TMC5130.readIOIN()
		self.text.insert(0.0, 'Please see Console for Output!')

	def readSPI (self):
		self.text.delete(0.0, END)
		response = self.TMC5130.readSettings('XACTUAL',1)
		self.TMC5130.readSPIStatus()
		self.text.insert(0.0, 'Please see Console for Output!')

	def readRAMP_STAT (self):
		self.text.delete(0.0, END)
		self.TMC5130.readRAMP_STAT()
		self.text.insert(0.0, 'Please see Console for Output!')

	def readSW_MODE (self):
		self.text.delete(0.0, END)
		self.TMC5130.readSW_MODE()
		self.text.insert(0.0, 'Please see Console for Output!')
	
	def move2endstop(self,direction,mode):
		''' Move in Direction to Start until EndStop is triggert '''
		self.text.delete(0.0, END)
		self.text.insert(0.0, "Moving to start position!")
		StepsDone = GPIOFunc.moveSliderToEndstop(h_f.translate_direction(direction),h_f.translate_operation_mode(mode),self.TMC5130)
		if not GPIOFunc.readPinInput(defs.SLIDER_START_LATCH_PORT):
			self.text.insert(15.1, "\nStart position reached." + str(StepsDone) + " Steps done!")
		elif  not GPIOFunc.readPinInput(defs.SLIDER_END_LATCH_PORT):
			self.text.insert(15.1, "\nEnd position reached." + str(StepsDone) + " Steps done!")
		else:
			self.text.insert(15.1, "\nError! No Endstop found")		
	
	def MoveSteps(self,direction,mode):
		distanceMM = self.move_MM_entry.get()
		if h_f.is_number(distanceMM) and (h_f.translate_direction(direction) != -1):
			self.text.delete(0.0, END)
			self.text.insert(0.0, "Moving: " + str(distanceMM) + " mm " + direction + "!")			
			StepsDone = GPIOFunc.moveSliderSteps(h_f.translate_direction(direction),distanceMM,h_f.translate_operation_mode(mode),self.TMC5130)
			self.text.insert(15.1, "\n" + str(StepsDone) + " Steps done!")
		else:
			self.text.delete(0.0, END)
			self.text.insert(0.0, "Wrong distance or direction entry")              
				
	def GetScanners(self,my_output):
		while True:
			Scanner = GetScanners.getScanner()
			if Scanner[0] == "":
				Scanner[0] = "Error: Not enough Scanners detected!!"
				Scanner[1] = "Trying again..."
				time.sleep(0.5)
				self.text.delete(0.0, END)
				self.text.insert(0.0, Scanner[0] + "\n" + Scanner[1])				
			else: 
				self.text.delete(0.0, END)
				self.text.insert(0.0, Scanner[0] + "\n" + Scanner[1])
				#my_output.set(Scanner[0] + "\n" + Scanner[1])
				break	
		
	def StartBookScan(self,justDriveNoScan):
		#self.text.delete(0.0, END)
		#self.text.insert(0.0, justDriveNoScan)
		#my_output.set(justDriveNoScan)
		Scanner = ["none","none"]
		if not justDriveNoScan:
			while True:
				Scanner = GetScanners.getScanner()
				if Scanner[0] == "":
					Scanner[0] = "Error: Not enough Scanners detected!!"
					Scanner[1] = "Trying again..."
					time.sleep(0.5)
					self.text.delete(0.0, END)
					self.text.insert(0.0, Scanner[0] + "\n" + Scanner[1])
				else: 
					self.text.delete(0.0, END)
					self.text.insert(0.0, Scanner[0] + "\n" + Scanner[1])
					break                
		[pages,error] = self.ScanBook(Scanner,justDriveNoScan,int(self.travel_times.get()),self.TMC5130)
		self.text.delete(0.0, END)
		self.text.insert(0.0, str(pages) + " scanned\n")
		if not error:
			self.text.insert(15.1,"Error detected")                
		
	def ScanBook(self,Scanner,justDriveNoScan,travel_times,TMC5130):	
		GPIOFunc.moveSliderToEndstop (defs.DIRECTION_TO_START,defs.TRAVEL_MODE,TMC5130)	
		#Start Scanprocesses
		args0 = ["sudo scanimage -d " + Scanner[0] + " --batch=/home/pi/maeqaedat/scans/%06da.pnm --batch-prompt"] #Scanner1 Start Command
		args1 = ["sudo scanimage -d " + Scanner[1] + " --batch=/home/pi/maeqaedat/scans/%06db.pnm --batch-prompt"] #Scanner1 Start Command
		if not justDriveNoScan:
			p0 = subprocess.Popen(args0, stdout=subprocess.PIPE, stdin=PIPE, shell=True) #Start Scanner1 Sub Process
			p1 = subprocess.Popen(args1, stdout=subprocess.PIPE, stdin=PIPE, shell=True) #Start Scanner2 Sub Process
			time.sleep(1)
			p0.stdin.write("\n") #Send ENTER to Scanner1
			p1.stdin.write("\n") #Send ENTER to Scanner2
		
			GPIOFunc.setPinOutput(defs.SCANNER1_ENDSTOP_PORT,defs.HIGH) #Send ENDSTOP to Scanner1
			GPIOFunc.setPinOutput(defs.SCANNER2_ENDSTOP_PORT,defs.HIGH) #Send ENDSTOP to Scanner2
			time.sleep (0.1)
			GPIOFunc.setPinOutput(defs.SCANNER1_ENDSTOP_PORT,defs.LOW) #Release ENDSTOP of Scanner1
			GPIOFunc.setPinOutput(defs.SCANNER2_ENDSTOP_PORT,defs.LOW) #Release ENDSTOP of Scanner2
		# Decide if TMC5130 or PiPWM is used
		if TMC5130 == 'none':
			if not justDriveNoScan:
				[pages,error] = self.PWMScan(justDriveNoScan,travel_times,p0,p1)
			else:
				[pages,error] = self.PWMScan(justDriveNoScan,travel_times)
		else:
			if not justDriveNoScan:
				[pages,error] = self.TMCScan(justDriveNoScan,travel_times,p0,p1)
			else:
				[pages,error] = self.TMCScan(justDriveNoScan,travel_times)
		# End
		time.sleep(0.5)	
		if not justDriveNoScan:	
			p0.stdin.close()
			p1.stdin.close()
		return [pages,error]

	def PWMScan(self,justDriveNoScan,travel_times,p0='none',p1='none'):
		''' Book Scan in PiPWM Mode '''
		CurrentSliderPosition = 0        
		k = 0
		## For ever loop	
		while k<travel_times:
			if not justDriveNoScan:
				p0.stdin.write("\n") #Send ENTER to Scanner1
				p1.stdin.write("\n") #Send ENTER to Scanner2
			MMToGo = defs.SCANNER_START_POSITION					# Steps to start position of first scanner
			print ["Distance to go: @S1st_canner_Start_Position " + str(MMToGo)]
			StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.TRAVEL_MODE)
			print ["Steps done: " + str(StepsDone)]														
				
			CurrentSliderPosition = MMToGo
			MMToGo = 20								#Add MM to reach start position for second scanner
			print ["Distance to go: @2nd_Scanner_Start_Position " + str(MMToGo)]											
			StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE)
			print ["Steps done: " + str(StepsDone)]
			
			if not justDriveNoScan:
				GPIOFunc.setPinOutput(defs.SCANNER1_ENDSTOP_PORT,defs.HIGH)	# Give scanner #1 End Stop Signal
				GPIOFunc.setPinOutput(defs.SCANNER2_ENDSTOP_PORT,defs.HIGH)	# Give Scanner #2 End Stop Signal
				time.sleep (0.1)
				GPIOFunc.setPinOutput(defs.SCANNER1_ENDSTOP_PORT,defs.LOW) #Release ENDSTOP of Scanner1
				GPIOFunc.setPinOutput(defs.SCANNER2_ENDSTOP_PORT,defs.LOW) #Release ENDSTOP of Scanner2
				
			CurrentSliderPosition += MMToGo
			MMToGo = defs.COANDA_START_POSITION  - CurrentSliderPosition		 #Calculate MM to Coanda Start Position
			print ["Distance to go: @Coanda_Start_Position " + str(MMToGo)]
			StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE)
			print ["Steps done: " + str(StepsDone)]
			
			CurrentSliderPosition += MMToGo
			MMToGo = defs.COANDA_STOP_POSITION - CurrentSliderPosition	#Calculate MM to Coanda Stop Position
			print ["Distance to go: @Coanda_End_Position " + str(MMToGo)]
			StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE)
			print ["Steps done: " + str(StepsDone)]
			
			CurrentSliderPosition += MMToGo
			MMToGo = defs.SCANNER_END_POSITION - CurrentSliderPosition	#Calculate MM to Scanner End Position
			print ["Distance to go: @Coanda_End_Position " + str(MMToGo)]
			StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE)
			print ["Steps done: " + str(StepsDone)]
			
			CurrentSliderPosition += MMToGo
			MMToGo = defs.SLIDER_END_POSITION - CurrentSliderPosition		#Calculate MM to Scanner End Position
			print ["Distance to go: @Scanner_End_Position " + str(MMToGo)]
			StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.TRAVEL_MODE)
			print ["Steps done: " + str(StepsDone)]
			
		#	CurrentSliderPosition += StepsDone
			GPIOFunc.moveSliderToEndstop (defs.DIRECTION_TO_START,defs.TRAVEL_MODE) # go back to start
			CurrentSliderPosition = 0
			k += 1
		test = 1
		return [k,test]


	def TMCScan(self,justDriveNoScan,travel_times,p0='none',p1='none'):
		''' Book Scan continued with TMC5130 '''
		TMC5130.setHomePosition()
		GPIOFunc.addEventChannel(defs.TMC_POSITION_CMP) # start interrupt handling on Position Compare GPIO
		CurrentSliderPosition = 0        
		k = 0
		## For ever loop	
		while k<travel_times:
			if not justDriveNoScan:
				p0.stdin.write("\n") #Send ENTER to Scanner1
				p1.stdin.write("\n") #Send ENTER to Scanner2
			MMToGo = defs.SCANNER_START_POSITION					# Steps to start position of first scanner
			print ["Distance to go: @1st_Scanner_Start_Position: " + str(MMToGo) + 'mm']
			#StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.TRAVEL_MODE,TMC5130)
			GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,defs.SLIDER_END_POSITION,defs.SCAN_MODE,TMC5130)
			StepsDone = GPIOFunc.setNextStage(defs.SCAN_MODE,defs.SCANNER_START_POSITION,TMC5130)
			test = GPIOFunc.waitForStageComplete()
			if not test:
				break
			print ["Steps done: " + str(StepsDone)]															
			CurrentSliderPosition = MMToGo
			MMToGo = 20								#Add MM to reach start position for second scanner
			print ["Distance to go: @2nd_Scanner_Start_Position " + str(MMToGo)]		
			#StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE,TMC5130)
			StepsDone = GPIOFunc.setNextStage(defs.SCAN_MODE,MMToGo,TMC5130)
			test = GPIOFunc.waitForStageComplete()
			if not test:
				break
			print ["Steps done: " + str(StepsDone)]
			
			if not justDriveNoScan:
				GPIOFunc.setPinOutput(defs.SCANNER1_ENDSTOP_PORT,defs.HIGH)	# Give scanner #1 End Stop Signal
				GPIOFunc.setPinOutput(defs.SCANNER2_ENDSTOP_PORT,defs.HIGH)	# Give Scanner #2 End Stop Signal
				time.sleep (0.1)
				GPIOFunc.setPinOutput(defs.SCANNER1_ENDSTOP_PORT,defs.LOW) #Release ENDSTOP of Scanner1
				GPIOFunc.setPinOutput(defs.SCANNER2_ENDSTOP_PORT,defs.LOW) #Release ENDSTOP of Scanner2
				
			CurrentSliderPosition += MMToGo
			MMToGo = defs.COANDA_START_POSITION  - CurrentSliderPosition		 #Calculate MM to Coanda Start Position
			print ["Distance to go: @Coanda_Start_Position " + str(MMToGo)]
			#StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE,TMC5130)
			StepsDone = GPIOFunc.setNextStage(defs.SCAN_MODE,MMToGo,TMC5130)
			test = GPIOFunc.waitForStageComplete()
			if not test:
				break
			print ["Steps done: " + str(StepsDone)]
			
			CurrentSliderPosition += MMToGo
			MMToGo = defs.COANDA_STOP_POSITION - CurrentSliderPosition	#Calculate MM to Coanda Stop Position
			print ["Distance to go: @Coanda_End_Position " + str(MMToGo)]
			#StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE,TMC5130)
			StepsDone = GPIOFunc.setNextStage(defs.SCAN_MODE,MMToGo,TMC5130)
			test = GPIOFunc.waitForStageComplete()
			if not test:
				break
			print ["Steps done: " + str(StepsDone)]
			
			CurrentSliderPosition += MMToGo
			MMToGo = defs.SCANNER_END_POSITION - CurrentSliderPosition	#Calculate MM to Scanner End Position
			print ["Distance to go: @Coanda_End_Position " + str(MMToGo)]
			#StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.SCAN_MODE,TMC5130)
			StepsDone = GPIOFunc.setNextStage(defs.SCAN_MODE,MMToGo,TMC5130)
			test = GPIOFunc.waitForStageComplete()
			if not test:
				break
			print ["Steps done: " + str(StepsDone)]
			
			CurrentSliderPosition += MMToGo
			MMToGo = defs.SLIDER_END_POSITION - CurrentSliderPosition		#Calculate MM to Scanner End Position
			print ["Distance to go: @Scanner_End_Position " + str(MMToGo)]
			#StepsDone = GPIOFunc.moveSliderSteps(defs.DIRECTION_TO_END,MMToGo,defs.TRAVEL_MODE,TMC5130)
			StepsDone = GPIOFunc.setNextStage(defs.TRAVEL_MODE,MMToGo-2,TMC5130)
			test = GPIOFunc.waitForStageComplete()
			if not test:
				break
			print ["Steps done: " + str(StepsDone)]
			
		#	CurrentSliderPosition += StepsDone
			GPIOFunc.moveSliderToEndstop (defs.DIRECTION_TO_START,defs.TRAVEL_MODE,TMC5130) # go back to start
			CurrentSliderPosition = 0
			k += 1
		return [k,test]

		
#Initialize
StepperMode = {0:"Pi HW PWM", 1: 'TMC5130'}		
while 1:
	Choice = input('Chose Step Signal Generation: \n [0] - Pi PWM / [1] - TMC5130 Driver\n')
	if Choice == 0:
		import wPiGPIOFunc as GPIOFunc
		TMC5130 = 'none'
		break
	elif  Choice == 1:
		import rPiGPIOFunc as GPIOFunc
		import TMC
		try:
			TMC5130 = TMC.TMC5130(defs.SPIBus,defs.SPIDev_TMC5130)
			break
		except TypeError :
			print '\nSPI Communication with TMC5130 Motor Controller failed!!!\n'
	else:
		print 'Not a valid mode!!!'
StepperMode = StepperMode [Choice]
GPIOFunc.initializeGPIOs()

# Start GUI
root = Tk()
root.title("Mäqädat Book Scanner GUI")
root.geometry ("540x400")


app = Application(root,StepperMode,TMC5130)

root.mainloop()

print ''
GPIOFunc.cleanupGPIOs()
try:
	TMC5130.destroy()
	print 'Motor stopped...'
except AttributeError:
	pass
print "Program End"

