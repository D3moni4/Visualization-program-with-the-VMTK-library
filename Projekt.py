# #!/usr/bin/env python
# noinspection PyUnresolvedReferences
import glob
import vtkmodules.vtkInteractionStyle
import os
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
# from vtk.util.colors import tomato
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor
)
from vtkmodules.vtkCommonDataModel import (
    vtkPlane
)
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkTextRepresentation,
    vtkTextWidget
)
import vtk
import tkinter as tk
from tkinter import Entry, Tk, Frame, Button
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox 
from PIL import Image, ImageTk
from tkinter import simpledialog
#from mayavi import mlab
from vmtk import pypes
from vmtk import vmtkscripts
from vmtk import vmtkcontribscripts
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtGui import QColor
import csv



def create_labels_and_save_file(label_array, filename):
        #Load the VTP file
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata = reader.GetOutput()

    # Get the scalars and lookup table
    scalars = polydata.GetPointData().GetScalars()
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(256)
    lut.SetRange(scalars.GetRange())
    lut.SetScaleToLinear()
    lut.SetHueRange(0.90,0)
    lut.SetSaturationRange(1,1)
    lut.Build()


    # Set the number of table values to match the number of unique scalar values
    unique_color_values = set(scalars.GetTuple(i)[0] for i in range(scalars.GetNumberOfTuples()))
    lut.SetNumberOfTableValues(len(unique_color_values))

    # Build the lookup table
    lut.Build()


    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetScalarRange(min(unique_color_values), max(unique_color_values))
    mapper.SetLookupTable(lut)
    mapper.SetScalarModeToUsePointData()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)


    text_widgets = [] # create empty list to hold the text widgets

    # Create the TextActor and TextWidget in a for loop
    for i in range(len(label_array)):
        text_actor = vtkTextActor()
        text_actor.SetInput(label_array[i])
        r, g, b, _ = lut.GetTableValue(i)
        text_actor.GetTextProperty().SetColor(r,g,b)

        text_representation = vtkTextRepresentation()
        if(i%2):
            text_representation.GetPositionCoordinate().SetValue(0.15, 0.15+((i/2)*0.1))
        else: 
            text_representation.GetPositionCoordinate().SetValue(0.55, 0.15+((i/2)*0.1))    
        text_representation.GetPosition2Coordinate().SetValue(0.3, 0.1)

        text_widget = vtkTextWidget()
        text_widget.SetRepresentation(text_representation)
        text_widget.SetInteractor(interactor)
        text_widget.SetTextActor(text_actor)
        text_widget.SelectableOff()
        
        text_widgets.append(text_widget)  # append the new text widget to the list




    interactor.Initialize()
    for tw in text_widgets:  # turn on all the text widgets
        tw.On()


    interactor.Start()

def create_labels_from_loaded_file(filenameVTP, filenameCSV):
        #Load the VTP file

    label_name = []
    R_value = []
    G_value = []
    B_value = []

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            label_name.append(row[0])
            R_value.append(row[1])
            G_value.append(row[2])
            B_value.append(row[3]) 

    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filenameVTP)
    reader.Update()
    polydata = reader.GetOutput()



    # Get the scalars and lookup table
    scalars = polydata.GetPointData().GetScalars()
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(256)
    lut.SetRange(scalars.GetRange())
    lut.SetScaleToLinear()
    lut.SetHueRange(0.90,0)
    lut.SetSaturationRange(1,1)
    lut.Build()


    # Set the number of table values to match the number of unique scalar values
    unique_color_values = set(scalars.GetTuple(i)[0] for i in range(scalars.GetNumberOfTuples()))
    lut.SetNumberOfTableValues(len(unique_color_values))

    # Build the lookup table
    lut.Build()


    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetScalarRange(min(unique_color_values), max(unique_color_values))
    mapper.SetLookupTable(lut)
    mapper.SetScalarModeToUsePointData()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)


    text_widgets = [] # create empty list to hold the text widgets

    # Create the TextActor and TextWidget in a for loop
    for i in range(len(label_name)):
        text_actor = vtkTextActor()
        text_actor.SetInput(label_name[i])
        r = float(R_value[i])
        g = float(G_value[i])
        b = float(B_value[i])
        text_actor.GetTextProperty().SetColor(r,g,b)

        text_representation = vtkTextRepresentation()
        if(i%2):
            text_representation.GetPositionCoordinate().SetValue(0.15, 0.15+((i/2)*0.1))
        else: 
            text_representation.GetPositionCoordinate().SetValue(0.55, 0.15+((i/2)*0.1))    
        text_representation.GetPosition2Coordinate().SetValue(0.3, 0.1)

        text_widget = vtkTextWidget()
        text_widget.SetRepresentation(text_representation)
        text_widget.SetInteractor(interactor)
        text_widget.SetTextActor(text_actor)
        text_widget.SelectableOff()
        
        text_widgets.append(text_widget)  # append the new text widget to the list




    interactor.Initialize()
    for tw in text_widgets:  # turn on all the text widgets
        tw.On()


    interactor.Start()    

def save_label_value(label, R, G ,B):
    data = []

    for label, R, G, B in zip(label, R, G, B):
        data.append([label, R, G, B])

    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
        



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, filename, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.filepath = filename
        self.setWindowTitle("VTK Annotation")
        
        # Create a QVTKRenderWindowInteractor
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.vtk_widget.Initialize()
        self.vtk_widget.Start()

                    # # Load the VTP file
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(filename)
        reader.Update()
        polydata = reader.GetOutput()

        # Get the scalars and lookup table
        scalars = polydata.GetPointData().GetScalars()
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(256)
        lut.SetRange(scalars.GetRange())
        lut.SetScaleToLinear()
        lut.SetHueRange(0.90,0)
        lut.SetSaturationRange(1,1)
        lut.Build()


        # Set the number of table values to match the number of unique scalar values
        unique_color_values = set(scalars.GetTuple(i)[0] for i in range(scalars.GetNumberOfTuples()))
        lut.SetNumberOfTableValues(len(unique_color_values))

        # Build the lookup table
        lut.Build()

        number_of_unique_colors = len(unique_color_values)
        #print(len(unique_color_values))    



        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        mapper.SetScalarRange(min(unique_color_values), max(unique_color_values))
        mapper.SetLookupTable(lut)
        mapper.SetScalarModeToUsePointData()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)

        # Set the VTK renderer to the QVTKRenderWindowInteractor
        self.vtk_widget.GetRenderWindow().AddRenderer(renderer)

# Create a list of text inputs

        self.text_inputs = []
        self.R = []
        self.G = []
        self.B = []
        for i in range(number_of_unique_colors):
            text_input = QtWidgets.QLineEdit()
            label = QtWidgets.QLabel(f"        ", self)
            color_values = [float(val) for val in lut.GetTableValue(i)]
            color_values = [val*255 for val in lut.GetTableValue(i)][:3]
            label.setStyleSheet("QLabel { background-color: rgba("+','.join([str(val) for val in color_values])+"); }")
            #print("QFrame { background-color: rgba("+','.join([str(val) for val in color_values])+"); }")
            self.text_inputs.append((text_input, label))
            self.R.append(lut.GetTableValue(i)[0])
            self.G.append(lut.GetTableValue(i)[1])
            self.B.append(lut.GetTableValue(i)[2])




        # Create a button
        button = QtWidgets.QPushButton("Utwórz etykiety!")
        button.clicked.connect(self.on_button_clicked)

        # button2 = QtWidgets.QPushButton("Load data!(First VTP, Second CSV")
        # button2.clicked.connect(self.on_button_clicked2)

        button3 = QtWidgets.QPushButton("Zapisz dane!")
        button3.clicked.connect(self.on_button_clicked3)

            
        

        # Create a layout and add the VTK widget and button to it
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.vtk_widget)    

        for text_input, label in self.text_inputs:
            input_layout = QtWidgets.QHBoxLayout()
            input_layout.addWidget(text_input)
            input_layout.addWidget(label)
            layout.addLayout(input_layout)
        
        layout.addWidget(button)
        layout.addWidget(button3)
        # layout.addWidget(button2)
        

        # Set the layout to the central widget
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.values = []
        self.R_value = []
        self.G_value = []
        self.B_value = []


    def on_button_clicked(self):
        print("Labeled!")
        for text_input, label in self.text_inputs:
            self.values.append(text_input.text())
        create_labels_and_save_file(self.values, self.filepath)

    def on_button_clicked2(self):
        print("Data loaded!")
        vtp_filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
        csv_filepath = filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])

        create_labels_from_loaded_file(vtp_filepath, csv_filepath)    


    def on_button_clicked3(self):
        print("Data saved!")
        for text_input, label in self.text_inputs:
            self.values.append(text_input.text())
        for R in self.R:
            self.R_value.append(R)
        for G in self.G:
            self.G_value.append(G)
        for B in self.B:
            self.B_value.append(B)    
   
        save_label_value(self.values, self.R_value, self.G_value, self.B_value)    

        

botton = 0
top = 0
front = 0
back = 0
left = 0
right = 0

def display_window_with_key_event(filepath):
    
    filename = filepath

    # Read all the data from the file
    reader = vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()

        # Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    mapper.SetScalarModeToUseCellData()

    colors = vtkNamedColors()
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('NavajoWhite'))

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('DarkOliveGreen'))
    renderer.GetActiveCamera().Pitch(90)
    renderer.GetActiveCamera().SetViewUp(0, 0, 1)
    renderer.ResetCamera()



    # Create a slider widget and representation
    sliderRep = vtk.vtkSliderRepresentation2D()
    sliderRep.SetMinimumValue(-20)
    sliderRep.SetMaximumValue(20)
    sliderRep.SetValue(0)
    sliderRep.SetTitleText("clip botton")
    sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep.GetPoint1Coordinate().SetValue(0.1, 0.2)
    sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep.GetPoint2Coordinate().SetValue(0.3, 0.2)
    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetInteractor(renderWindow.GetInteractor())
    sliderWidget.SetRepresentation(sliderRep)

    # Create a slider widget and representation
    sliderRep2 = vtk.vtkSliderRepresentation2D()
    sliderRep2.SetMinimumValue(-20)
    sliderRep2.SetMaximumValue(20)
    sliderRep2.SetValue(0)
    sliderRep2.SetTitleText("clip top")
    sliderRep2.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep2.GetPoint1Coordinate().SetValue(0.1, 0.1)
    sliderRep2.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep2.GetPoint2Coordinate().SetValue(0.3, 0.1)
    sliderWidget2 = vtk.vtkSliderWidget()
    sliderWidget2.SetInteractor(renderWindow.GetInteractor())
    sliderWidget2.SetRepresentation(sliderRep2)

    # Create a slider widget and representation
    sliderRep3 = vtk.vtkSliderRepresentation2D()
    sliderRep3.SetMinimumValue(-20)
    sliderRep3.SetMaximumValue(20)
    sliderRep3.SetValue(0)
    sliderRep3.SetTitleText("clip front")
    sliderRep3.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep3.GetPoint1Coordinate().SetValue(0.4, 0.2)
    sliderRep3.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep3.GetPoint2Coordinate().SetValue(0.6, 0.2)
    sliderWidget3 = vtk.vtkSliderWidget()
    sliderWidget3.SetInteractor(renderWindow.GetInteractor())
    sliderWidget3.SetRepresentation(sliderRep3)

    # Create a slider widget and representation
    sliderRep4 = vtk.vtkSliderRepresentation2D()
    sliderRep4.SetMinimumValue(-20)
    sliderRep4.SetMaximumValue(20)
    sliderRep4.SetValue(0)
    sliderRep4.SetTitleText("clip back")
    sliderRep4.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep4.GetPoint1Coordinate().SetValue(0.4, 0.1)
    sliderRep4.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep4.GetPoint2Coordinate().SetValue(0.6, 0.1)
    sliderWidget4 = vtk.vtkSliderWidget()
    sliderWidget4.SetInteractor(renderWindow.GetInteractor())
    sliderWidget4.SetRepresentation(sliderRep4)

    # Create a slider widget and representation
    sliderRep5 = vtk.vtkSliderRepresentation2D()
    sliderRep5.SetMinimumValue(-20)
    sliderRep5.SetMaximumValue(20)
    sliderRep5.SetValue(0)
    sliderRep5.SetTitleText("clip left")
    sliderRep5.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep5.GetPoint1Coordinate().SetValue(0.7, 0.2)
    sliderRep5.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep5.GetPoint2Coordinate().SetValue(0.9, 0.2)
    sliderWidget5 = vtk.vtkSliderWidget()
    sliderWidget5.SetInteractor(renderWindow.GetInteractor())
    sliderWidget5.SetRepresentation(sliderRep5)

    # Create a slider widget and representation
    sliderRep6 = vtk.vtkSliderRepresentation2D()
    sliderRep6.SetMinimumValue(-20)
    sliderRep6.SetMaximumValue(20)
    sliderRep6.SetValue(0)
    sliderRep6.SetTitleText("clip right")
    sliderRep6.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep6.GetPoint1Coordinate().SetValue(0.7, 0.1)
    sliderRep6.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep6.GetPoint2Coordinate().SetValue(0.9, 0.1)
    sliderWidget6 = vtk.vtkSliderWidget()
    sliderWidget6.SetInteractor(renderWindow.GetInteractor())
    sliderWidget6.SetRepresentation(sliderRep6)

    # Define the callback function for the slider
    def sliderCallback(obj, event):
        global botton
        botton = obj.GetRepresentation().GetValue()
        
    
    def sliderCallback2(obj, event):
        global top
        top = obj.GetRepresentation().GetValue()
        

    def sliderCallback3(obj, event):
        global front
        front = obj.GetRepresentation().GetValue()


    def sliderCallback4(obj, event):
        global back
        back = obj.GetRepresentation().GetValue()


    def sliderCallback5(obj, event):
        global left
        left = obj.GetRepresentation().GetValue()


    def sliderCallback6(obj, event):
        global right
        right = obj.GetRepresentation().GetValue()
                       
    # Set the callback function for the slider widget
    sliderWidget.AddObserver("InteractionEvent", sliderCallback)
    sliderWidget2.AddObserver("InteractionEvent", sliderCallback2)
    sliderWidget3.AddObserver("InteractionEvent", sliderCallback3)
    sliderWidget4.AddObserver("InteractionEvent", sliderCallback4)
    sliderWidget5.AddObserver("InteractionEvent", sliderCallback5)
    sliderWidget6.AddObserver("InteractionEvent", sliderCallback6)

    # Add key press event
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    def keypress(obj, event):
        key = obj.GetKeySym()
        if key == "u":
            display_vtk_file(filename)
    iren.AddObserver("KeyPressEvent", keypress)
    sliderWidget.SetInteractor(iren)
    sliderWidget2.SetInteractor(iren)
    sliderWidget3.SetInteractor(iren)
    sliderWidget4.SetInteractor(iren)
    sliderWidget5.SetInteractor(iren)
    sliderWidget6.SetInteractor(iren)
    iren.Initialize()


    text_actor = vtkTextActor()
    text_actor.SetInput("Press u for Update")
    text_representation = vtkTextRepresentation() 
    text_representation.GetPositionCoordinate().SetValue(0.15, 0.85)
    text_representation.GetPosition2Coordinate().SetValue(0.3, 0.1)
    text_widget = vtkTextWidget()
    text_widget.SetRepresentation(text_representation)
    text_widget.SetInteractor(iren)
    text_widget.SetTextActor(text_actor)
    text_widget.SelectableOff()

    # Render the window
    renderWindow.Render()
    renderWindow.SetWindowName("Clipper")
    sliderWidget.EnabledOn()
    sliderWidget2.EnabledOn()
    sliderWidget3.EnabledOn()
    sliderWidget4.EnabledOn()
    sliderWidget5.EnabledOn()
    sliderWidget6.EnabledOn()
    text_widget.On()
    iren.Start()

def display_vtk_file(filepath):
    colors = vtkNamedColors()

    filename = filepath

    # Read all the data from the file
    reader = vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    #Cutting botton side of volume, bigger value makes bigger cut
    plane = vtkPlane()
    origin = reader.GetOutput().GetCenter()
    origin = [origin[0], origin[1], origin[2]+botton]
    plane.SetOrigin(origin)
    plane.SetNormal(0, 0, 1)

    clipper = vtkClipPolyData()
    clipper.SetInputConnection(reader.GetOutputPort())
    clipper.SetClipFunction(plane)
    clipper.SetValue(-1)
    clipper.Update()
    #Cutting top side of volume, bigger value makes smaller cut
    plane2 = vtkPlane()
    origin2 = clipper.GetOutput().GetCenter()
    origin2 = [origin2[0], origin2[1], origin2[2]+top]
    plane2.SetOrigin(origin2)
    plane2.SetNormal(0, 0, -1)

    clipper2 = vtkClipPolyData()
    clipper2.SetInputConnection(clipper.GetOutputPort())
    clipper2.SetClipFunction(plane2)
    clipper2.SetValue(1)
    clipper2.Update()
    #Cutting front side of volume, bigger value makes bigger cut
    plane3 = vtkPlane()
    origin3 = clipper2.GetOutput().GetCenter()
    origin3 = [origin3[0], origin3[1]+front, origin3[2]]
    plane3.SetOrigin(origin3)
    plane3.SetNormal(0, 1, 0)

    clipper3 = vtkClipPolyData()
    clipper3.SetInputConnection(clipper2.GetOutputPort())
    clipper3.SetClipFunction(plane3)
    clipper3.SetValue(-1)
    clipper3.Update()
    #Cutting back side of volume, bigger value makes smaller cut
    plane4 = vtkPlane()
    origin4 = clipper3.GetOutput().GetCenter()
    origin4 = [origin4[0], origin4[1]+back, origin4[2]]
    plane4.SetOrigin(origin4)
    plane4.SetNormal(0, -1, 0)

    clipper4 = vtkClipPolyData()
    clipper4.SetInputConnection(clipper3.GetOutputPort())
    clipper4.SetClipFunction(plane4)
    clipper4.SetValue(1)
    clipper4.Update()
    #Cutting left side of volume, bigger value makes bigger cut
    plane5 = vtkPlane()
    origin5 = clipper4.GetOutput().GetCenter()
    origin5 = [origin5[0]+left, origin5[1], origin5[2]]
    plane5.SetOrigin(origin5)
    plane5.SetNormal(1, 0, 0)

    clipper5 = vtkClipPolyData()
    clipper5.SetInputConnection(clipper4.GetOutputPort())
    clipper5.SetClipFunction(plane5)
    clipper5.SetValue(-1)
    clipper5.Update()
    #Cutting right side of volume, bigger value makes smaller cut
    plane6 = vtkPlane()
    origin6 = clipper5.GetOutput().GetCenter()
    origin6 = [origin6[0]+right, origin6[1], origin6[2]]
    plane6.SetOrigin(origin6)
    plane6.SetNormal(-1, 0, 0)

    clipper6 = vtkClipPolyData()
    clipper6.SetInputConnection(clipper5.GetOutputPort())
    clipper6.SetClipFunction(plane6)
    clipper6.SetValue(1)
    clipper6.Update()


    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(clipper6.GetOutputPort())
    mapper.SetScalarModeToUseCellData()


    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('NavajoWhite'))

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    def keypress(obj, event):
        key = obj.GetKeySym()
        if key == "s":
            print("Saved")
            writer = vtk.vtkXMLPolyDataWriter()

            # Set the input data
            writer.SetInputConnection(clipper6.GetOutputPort())

            # Set the file name for the output VTK file
            writer.SetFileName('myDICOMclipped.vtp')

            # Write the VTK file
            writer.Write()
    iren.AddObserver("KeyPressEvent", keypress)

    text_actor = vtkTextActor()
    text_actor.SetInput("Press s for Save")
    text_representation = vtkTextRepresentation() 
    text_representation.GetPositionCoordinate().SetValue(0.15, 0.85)
    text_representation.GetPosition2Coordinate().SetValue(0.3, 0.1)
    text_widget = vtkTextWidget()
    text_widget.SetRepresentation(text_representation)
    text_widget.SetInteractor(renderWindowInteractor)
    text_widget.SetTextActor(text_actor)
    text_widget.SelectableOff()
    text_widget.On()

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('DarkOliveGreen'))
    renderer.GetActiveCamera().Pitch(90)
    renderer.GetActiveCamera().SetViewUp(0, 0, 1)
    renderer.ResetCamera()

    renderWindow.SetSize(600, 600)
    renderWindow.Render()
    renderWindow.SetWindowName('Clipped')
    renderWindowInteractor.Start()


def create_centerline_and_branch(filepath):

    inputfile = filepath
    # create the command
    myArguments = 'vmtksurfacereader -ifile ' + inputfile + ' --pipe vmtkcenterlines --pipe vmtkbranchextractor --pipe vmtkbranchclipper -ofile CenterlinesExtractor.vtp'
    myPype = pypes.PypeRun(myArguments)


def create_centerline_and_voronoi(filepath):
    
    inputfile = filepath
    # create the command 
    arguments = 'vmtksurfacereader -ifile ' + inputfile + ' --pipe vmtkcenterlines --pipe vmtkrenderer --pipe vmtksurfaceviewer -opacity 0.25 --pipe vmtksurfaceviewer  -i @vmtkcenterlines.voronoidiagram -array MaximumInscribedSphereRadius -ofile CenterlinesRadius.vtp --pipe vmtksurfaceviewer -i @vmtkcenterlines.o'
    myPype = pypes.PypeRun(arguments)


def create_centerline(filepath):

    inputfile = filepath
    # create the command
    arguments = 'vmtksurfacereader -ifile ' + inputfile + ' --pipe vmtkcenterlines -ofile Centerlines.vtp'
    myPype = pypes.PypeRun(arguments)


def cutting_out_fragments(filepath):

    inputfile = filepath
    # create the command
    arguments = 'vmtksurfacereader -ifile ' + inputfile + ' --pipe vmtksurfaceclipper -ofile modifiedModel.vtp'
    myPype = pypes.PypeRun(arguments)


def handle_data_selection():
    entryString = tk.StringVar()

    sub_window = tk.Toplevel(root)
    sub_window.geometry("450x250")
    sub_window.title("Prowadzanie ID gałęzi do usunięcia") 
    label_sub_window = tk.Label(sub_window, text= "Wprowadz liczbę")
    label_sub_window.pack(fill="x", side="top")
    entry_branch_number = tk.Entry(sub_window, textvariable=entryString)
    entry_branch_number.pack(fill="x", pady=30, padx=50) 

    button_save = tk.Button(sub_window, text="Zapisz", command=lambda: save_branch_number(entryString.get(), sub_window))
    button_save.pack(pady=30, padx=50, side="bottom", fill="x")


def save_branch_number(entry_string: str, window: tk.Toplevel):
    global branch_number 
    try:
        branch_number = int(entry_string)
        messagebox.showinfo("Sukces", "Liczba została zapisana pomyślnie.")
        window.destroy()
        filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
        if bool(filepath):
            branch_splitting(filepath)
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawną liczbę.")
    pass

def branch_splitting(filepath):
    
    inputfile = filepath
    # create the command
    arguments = ' vmtksurfacereader -ifile ' + inputfile + ' --pipe vmtkcenterlines --pipe vmtkbranchextractor --pipe vmtkbranchclipper -groupids '+ str(branch_number) +' -ofile oneBranch.vtp '
    print(arguments)
    myPype = pypes.PypeRun(arguments)


def show_labeled_image(filepath):
    inputfile = filepath

    # create the command
    myArguments = 'vmtksurfaceviewer -ifile ' + inputfile + ' -array GroupIds -ofile Branches.vtp'
    
    # run the command
    myPype = pypes.PypeRun(myArguments)



def show_file(filename):
    # Read the VTP file
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()

    # Map the data to geometry
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor to represent the geometry
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a renderer and add the actor to it
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    # Create a render window and add the renderer to it
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Create an interactor and set the render window as the input
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Start the interaction
    interactor.Initialize()
    render_window.Render() 
    interactor.Start()


def show_file_with_labels(filename):
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(filename)
    window.show()
    sys.exit(app.exec_())



# Konwertowanie pliku DICOM
def convert_DICOM_to_VTK(filepath):

    file_out = 'myDICOM.vtk'
    file_path = os.path.join(os.getcwd(), file_out)

    reader=vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(filepath)
    reader.Update()

    writer=vtk.vtkDataSetWriter()
    writer.SetInputData(reader.GetOutput())
    writer.SetFileName(file_path)
    writer.Write()

# Konwrtowanie vtp.to ASCII
def convert_VTP_to_ASCII(filepath):

    file_out = 'ASCII.csv'
    file_path = os.path.join(os.getcwd(), file_out)
    
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filepath)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(file_path)
    writer.SetInputConnection(reader.GetOutputPort())
    writer.SetDataModeToAscii()
    writer.Write()

# Tworzenie z zdjęcia 3D modelu z geometrycznej powierzchni
# Ta funkacja przyjduje jedyni pliki .vtk lyb .vti  
def extract_veselss_marchingcubes(filepath):

    myArguments = 'vmtkmarchingcubes -ifile ' + filepath + ' -l 1200 --pipe vmtksurfaceviewer'
    myPype = pypes.PypeRun(myArguments)
    mySurface = myPype.GetScriptObject('vmtkmarchingcubes','0').Surface

    mySmoother = vmtkscripts.vmtkSurfaceSmoothing()
    mySmoother.Surface= mySurface
    mySmoother.PassBand = 0.2
    mySmoother.NumberOfIterations = 30
    mySmoother.Execute()

    myConnectivity = vmtkscripts.vmtkSurfaceConnectivity()
    myConnectivity.Surface = mySmoother.Surface
    myConnectivity.Execute()

    if filepath.endswith('.xml') or filepath.endswith('.vtk'):
        writer = vmtkscripts.vmtkSurfaceWriter()
    else:
        writer = vtk.vtkPolyDataWriter()

    file_out = 'myDICOMVessels.vtp'
    file_path = os.path.join(os.getcwd(), file_out)
    writer.Surface = myConnectivity.Surface
    writer.OutputFileName = file_path
    writer.Execute()
        

# Creating functions for buttons
def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        display_window_with_key_event(filepath)    

def browse_file2():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        create_centerline_and_branch(filepath)

def browse_file9():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        create_centerline_and_voronoi(filepath)

def browse_file10():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        create_centerline(filepath)

def browse_file4():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        show_labeled_image(filepath)

def browse_file3():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        show_file(filepath)

def browse_file5():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        show_file_with_labels(filepath)    

def browse_file6():
    filepath = filedialog.askdirectory()
    if bool(filepath):
        print(filepath)
        convert_DICOM_to_VTK(filepath)  

def browse_file11():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        print(filepath)
        convert_VTP_to_ASCII(filepath)  

def browse_file7():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtk")])
    if bool(filepath):
        extract_veselss_marchingcubes(filepath)

def browse_file8():
    vtp_filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    csv_filepath = filedialog.askopenfilename(filetypes=[("Plik CSV", "*.csv")])
    if bool(vtp_filepath) and bool(csv_filepath):
        create_labels_from_loaded_file(vtp_filepath, csv_filepath)   

def browse_file12():
    filepath = filedialog.askopenfilename(filetypes=[("Plik VTP", "*.vtp")])
    if bool(filepath):
        cutting_out_fragments(filepath) 

def browse_file13():
    handle_data_selection()
    


             

root = tk.Tk()
root.title("Aplikacja do adnotacji naczyń krwionośnych")
root.geometry("800x380")

img = PhotoImage(file=os.path.join(os.getcwd(),"gifek.gif"))

# Create a label and set its image attribute
bg_label = tk.Label(root, image=img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create buttons to seach for files
browse_button6 = tk.Button(root, text="Konwersja plików DICOM w plik VTK (folder)", command=browse_file6)
browse_button6.grid(row=0, column=0, padx=5, pady=10)

browse_button11 = tk.Button(root, text="Konwersja plików VTP w plik ASCII (folder)", command=browse_file11)
browse_button11.grid(row=0, column=1, padx=5, pady=10)

browse_button7 = tk.Button(root, text="Wyodrębnianie naczyń kwionośnych z pliku VTK", command=browse_file7)
browse_button7.grid(row=1, column=1, padx=5, pady=10)

browse_button = tk.Button(root, text="Przeglądaj plik VTP w celu wycięcia danego obszaru", command=browse_file)
browse_button.grid(row=2, column=1, padx=5, pady=10)

browse_button2 = tk.Button(root, text="Wygeneruj szkielet i gałęzie(extractor)", command=browse_file2)
browse_button2.grid(row=3, column=0, padx=5, pady=10)

browse_button9 = tk.Button(root, text="Wygeneruj szkielet i gałęzie(voronoi)", command=browse_file9)
browse_button9.grid(row=3, column=1, padx=5, pady=10)

browse_button10 = tk.Button(root, text="Wygeneruj szkielet i gałęzie(C-lines)", command=browse_file10)
browse_button10.grid(row=3, column=2, padx=5, pady=10)
                                       
browse_button4 = tk.Button(root, text="Nadaj gałęziom identyfikator", command=browse_file4)
browse_button4.grid(row=4, column=1, padx=5, pady=10)

browse_button3 = tk.Button(root, text="Pokaż model powierzchniowy sieci naczyń", command=browse_file3)
browse_button3.grid(row=7, column=2, padx=5, pady=10)

browse_button5 = tk.Button(root, text="Nadaj etykiety", command=browse_file5)
browse_button5.grid(row=5, column=1, padx=5, pady=10)

browse_button8 = tk.Button(root, text="Wczytaj istniejące dane z etykietami (VTP, CSV)", command=browse_file8)
browse_button8.grid(row=6, column=1, padx=5, pady=10)

browse_button12 = tk.Button(root, text="Manualne wycinanie fragmentu", command=browse_file12)
browse_button12.grid(row=7, column=0, padx=5, pady=10)

browse_button13 = tk.Button(root, text="Wycinanie gałęzi", command=browse_file13)
browse_button13.grid(row=7, column=1, padx=5, pady=10)


root.mainloop()
