#Author-Autodesk Inc.
#Description-Demo command input examples
import adsk.core, adsk.fusion, traceback
import math


_app = None
_ui  = None
_rowNumber = 0

# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

app = adsk.core.Application.get()
ui  = app.userInterface
des = app.activeProduct
root = des.rootComponent

linesk = root.sketches.itemByName('line')
bLine = linesk.sketchCurves.sketchLines.item(0)
bVect = bLine.geometry.startPoint.vectorTo(bLine.geometry.endPoint)
tLine = linesk.sketchCurves.sketchLines.item(1)
tVect = tLine.geometry.startPoint.vectorTo(tLine.geometry.endPoint)
angle = math.degrees(bVect.angleTo(tVect))

widthSk = root.sketches.itemByName('width')
width = widthSk.sketchCurves.sketchLines.item(0).length/2.54
angleFormat = str(round(180 - angle))
widthFormat = str(round(width,2)) + ' in'


# Adds a new row to the table.
def addRowToTable(tableInput):
    global _rowNumber
    # Get the CommandInputs object associated with the parent command.
    cmdInputs = adsk.core.CommandInputs.cast(tableInput.commandInputs)
    
    # Create three new command inputs.
    valueInput = cmdInputs.addValueInput('TableInput_value{}'.format(_rowNumber), 'Value', 'cm', adsk.core.ValueInput.createByReal(_rowNumber))
    stringInput =  cmdInputs.addStringValueInput('TableInput_string{}'.format(_rowNumber), 'String', str(_rowNumber))
    spinnerInput = cmdInputs.addIntegerSpinnerCommandInput('spinnerInt{}'.format(_rowNumber), 'Integer Spinner', 0 , 100 , 2, int(_rowNumber))
    
    # Add the inputs to the table.
    row = tableInput.rowCount
    tableInput.addCommandInput(valueInput, row, 0)
    tableInput.addCommandInput(stringInput, row, 1)
    tableInput.addCommandInput(spinnerInput, row, 2)
    
    # Increment a counter used to make each row unique.
    _rowNumber = _rowNumber + 1

def updateSliders(sliderInputs):
    global displacement
    global oaType
    """
    Populate 'slider_configuration' group with as many sliders as set in 'slider_controller'.
    Delete previous ones and create new sliders.
    """
    spinner = sliderInputs.itemById("slider_controller")
    value = spinner.value
    # # check ranges
    # if value > spinner.maximumValue or value < spinner.minimumValue:
    #     return
    weightInput = sliderInputs.itemById('BW')
    weight = weightInput.text

    oa = sliderInputs.itemById('dd2')
    oaType = oa.selectedItem.name


    angleInput = sliderInputs.itemById('angle')
    angle = int(angleInput.text)
    angleFormat = str(round(angle)) + '°'
    if oaType == 'Medial':
        finalPercentage = round((0.65 + (0.05*(angle))) * 100, 2)
    else:
        finalPercentage = round((0.35 + (0.05*(angle))) * 100, 2)

    activityInput = sliderInputs.itemById('dd3')
    activity = activityInput.selectedItem.name
    if activity == 'Moderate (4-7)':
        co = 2.66
    elif activity == 'Low (0-3)':
        co = 2.0
    elif activity == 'High (8-10)':
        co = 3.25

    # delete all sliders we have
    toRemove = []
    for i in range(sliderInputs.count):
        input = sliderInputs.item(i)
        if input.objectType == adsk.core.TextBoxCommandInput.classType():
            if input.id != 'BW' and input.id != 'angle' and input.id != 'width':
                toRemove.append(input)
    
    for input in toRemove:
        input.deleteMe()

    # create new ones with range depending on total number
    for i in range(1, value+1):
        id = str(i)
        axialForce = co*int(weight)/2
        medialForce = round(axialForce * (finalPercentage/100), 2)
        medialTorque = round((axialForce * (finalPercentage/100)) * (width/2), 2)
        appliedForce = round((axialForce * (finalPercentage/100)) * (width/2) * 0.15 / 8, 2)
        displacement = round(((axialForce * (finalPercentage/100)) * (width/2) * 0.15 / 8) *0.022, 4)
        A3displacement = round(((axialForce * (finalPercentage/100)) * (width/2) * 0.15 / 8) *0.022*2.9, 4)
        # pressure = round(((axialForce * (finalPercentage/100)) * (width/2) * 0.15 / 8)/4.85, 2)
        if i == 1:
        #     #sliderInputs.addTextBoxCommandInput('axial load equation', '<li style="font-size:25px;">Font</li>', '<li style="font-size:25px;">some text here</li>' , 5, True )
        #     sliderInputs.addTextBoxCommandInput('axial load equation', 'Peak Axial Force =', str(co) + '*' + weight + ' lbs' + '/2  = ' + str(axialForce) + ' lbs' , 2, True )
        # elif i == 2:
        #     sliderInputs.addTextBoxCommandInput('load share', 'Medial Load Share = ', '70% + (5% * ' + angleFormat + ')' + ' = ' + str(finalPercentage) + '%', 2, True)
        # elif i == 3:
        #     sliderInputs.addTextBoxCommandInput('Medial Force', 'Medial Condyle Force = ', str(axialForce) + ' lbs * ' + str(round(finalPercentage/100,4)) + ' = ' + str(medialForce) + ' lbs', 2, True)
        # elif i == 4:
        #     sliderInputs.addTextBoxCommandInput('Medial Torque', 'Medial Condyle Torque = ', str(medialForce) + ' lbs * (' + widthFormat + ' /2)' + ' = ' + str(medialTorque) + ' in*lbs', 2, True)
        # elif i == 5:
        #     sliderInputs.addTextBoxCommandInput('Moment Reduction', 'To achieve a 15% reduction in moment: ', 'Applied Brace Force * Brace Height = ' +  str(medialTorque) + ' in*lbs  * 0.15 ', 1, True)
        #     sliderInputs.addTextBoxCommandInput('Applied Force', 'Applied Brace Force = ',  str(medialTorque) + ' in*lbs  * 0.15  /  8 in  =  ' + str(appliedForce) + ' lbs', 2, True ) 
        # elif i == 6:                                   
            sliderInputs.addTextBoxCommandInput('Displacement', 'Frame Displacement = ', str(displacement) + ' in', 2, True)
            #sliderInputs.addTextBoxCommandInput('A Displacement', 'A3.0 Frame Displacement = ', str(A3displacement) + ' in', 2, True)
        # elif i == 7:
        #     sliderInputs.addTextBoxCommandInput('Pressure', 'Frame Pressure = ', str(pressure) + ' lbs/in^2', 2, True)
        #     if pressure > 1.75:
        #         sliderInputs.addTextBoxCommandInput('PressureLimit', 'PRESSURE ALERT: ', '<b>Frame pressure exceeds limit of 1.75 lbs/in^2.  Please Increase surface area factor to decrease pressure value</b>', 2, True)
        #         floatValueList = [0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5]
        #         sliderInputs.addFloatSliderListCommandInput('floatSlider2', 'Surface Area Multiplier', '', floatValueList)
                
# Event handler that reacts to any changes the user makes to any of the command inputs.
class MyCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            inputs = eventArgs.inputs
            cmdInput = eventArgs.input
            # onInputChange for slider controller
            if cmdInput.id == "slider_controller":
                sliderGroup = adsk.core.GroupCommandInput.cast(cmdInput.parentCommandInput)
                sliderInputs = sliderGroup.children
                updateSliders(sliderInputs)
            else:
                tableInput = inputs.itemById('table')
                if cmdInput.id == 'tableAdd':
                    addRowToTable(tableInput)
                elif cmdInput.id == 'tableDelete':
                    if tableInput.selectedRow == -1:
                        _ui.messageBox('Select one row to delete.')
                    else:
                        tableInput.deleteRow(tableInput.selectedRow)
          
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler that reacts to when the command is destroyed. This terminates the script.            
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            # This will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler that reacts when the command definitio is executed which
# results in the command being created and this event being fired.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)

            # Connect to the command destroyed event.
            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)

            # Connect to the input changed event.           
            onInputChanged = MyCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)    

            # Get the CommandInputs collection associated with the command.
            inputs = cmd.commandInputs

            # Create a tab input.
            tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Patient Info')
            tab1ChildInputs = tabCmdInput1.children

            # Create a read only textbox input.
            dropdown1 = tab1ChildInputs.addDropDownCommandInput('dd', 'orientation', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
            dd1items = dropdown1.listItems
            dd1items.add('left', False,'')
            dd1items.add('right', True,'')


            # Create an editable textbox input.        

            # groupCmdInput = tab1ChildInputs.addGroupCommandInput('axial load', 'Peak Axial Load')
            # groupCmdInput.isExpanded = True
            # groupChildInputs = groupCmdInput.children


            #groupChildInputs.addTextBoxCommandInput('axial load equation', 'Peak Axial Load Equation', 'Peak load = 2.66 * ' + weight + ' lbs', 2, True )
            sliderGroup = tab1ChildInputs.addGroupCommandInput("slider_configuration", "Medial Condyle Load")
            sliderInputs = sliderGroup.children

            dropdown2 = sliderInputs.addDropDownCommandInput('dd2', 'OA Type', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
            dd2items = dropdown2.listItems
            dd2items.add('Medial', True,'')
            dd2items.add('Lateral', False,'')


            sliderInputs.addTextBoxCommandInput('BW', 'Weight (lbs)', '0', 1, False)
            dropdown3 = sliderInputs.addDropDownCommandInput('dd3', 'Activity Level/Pain Score', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
            dd3items = dropdown3.listItems
            dd3items.add ('Low (0-3)', False, '')
            dd3items.add ('Moderate (4-7)', True, '')
            dd3items.add ('High (8-10)', False, '')

            sliderInputs.addTextBoxCommandInput('angle','Degrees of malalignment (°) = ', angleFormat, 1, False)
            sliderInputs.addTextBoxCommandInput('width','Condyle Width = ', widthFormat, 1, True)
            sliderInputs.addIntegerSpinnerCommandInput('slider_controller', 'calculate', 0,7,1,0)
            updateSliders(sliderInputs)


            # loadGroup = tab1ChildInputs.addGroupCommandInput('load', ' ')
            # loadInputs = loadGroup.children
            # loadInputs.addTextBoxCommandInput('blank', ' ', ' ', 20, True)

            onExecute = A2CommandExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
            
        
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def ip_mover(i,transform, bip=False):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    root = design.rootComponent
#function to move all IPs and BIPs with their CSs

    skList = []
    if bip:
        skList.append(root.sketches.itemByName('BIP-' + str(i)))
    else:
        skList.append(root.sketches.itemByName('IP-' + str(i)))
    
    if i == 5:
        skList.append(root.sketches.itemByName('IP-4.5'))
        skList.append(root.sketches.itemByName('IP-5.5'))

    for sk in skList:
        group = adsk.core.ObjectCollection.create()
        #add all sketch components to group
        for crv in sk.sketchCurves:
            group.add(crv)
        for pnt in sk.sketchPoints:
            group.add(pnt)

        sk.move(group, transform) 

    if not bip:
        railSk = root.sketches.itemByName('Pipe-rail-1')
        railGrp = adsk.core.ObjectCollection.create()
        if 1 <= i <= 4:
            railPt = railSk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i-1)
        elif i == 5:
            railPt = railSk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i-1)
            railPt2 = railSk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i)
            railPt3 = railSk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i+1)
            railGrp.add(railPt2)
            railGrp.add(railPt3)
        else:
            railPt = railSk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i+1)
        railGrp.add(railPt)

        railSk.move(railGrp, transform)
    
def spline_mover(i, transform):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    root = design.rootComponent
    splineList = ['rail-1', 'rail-2', 'rail-3', 'rail-4', 'rail-5']

    for spline in splineList:
        #function to move a specific spline point i, from the spline inputted
        sk = root.sketches.itemByName(spline)

        group = adsk.core.ObjectCollection.create()
        #add all sketch components to group
        spoint = sk.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(i)
        group.add(spoint)

        sk.move(group, transform)

def hinge_mover(transform, medial=False):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    root = design.rootComponent
    if medial:
        occ = root.occurrences.itemByName('MedialHinge:1')
    else:
        occ = root.occurrences.itemByName('LateralHinge:1')
    features = occ.component.features
    moveFeats = features.moveFeatures

    bodies = adsk.core.ObjectCollection.create()
    for body in occ.component.bRepBodies:
        bodies.add(body)

    moveFeatureInput = moveFeats.createInput(bodies, transform)
    moveFeats.add(moveFeatureInput)   

def csMover(i, transform):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct
    root = design.rootComponent

    #add cross section curve and points to group and move together
    group = adsk.core.ObjectCollection.create()
    #Grab sketch based on i
    cs = root.sketches.itemByName('CS-'+ str(i))
    #add all sketch components to group
    for crv in cs.sketchCurves:
        group.add(crv)
    for pnt in cs.sketchPoints:
        group.add(pnt)

    #find inside point on CS as our fromPt
    csPt = cs.sketchCurves.sketchFittedSplines.item(0).fitPoints.item(1).worldGeometry

    #grab corresponding fitPt from list of nodes



    if i == 1:
        hinge_mover(transform, False)
    elif i == 13:
        hinge_mover(transform, True)
        
    cs.move(group, transform)
    spline_mover(i-1, transform)
    if 1 <= i <= 13:
        ip_mover(i, transform)
    elif i == 14 or i == 24:
        ip_mover(i, transform, True)

    


class A2CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        # Code to react to the event.
        app  :adsk.core.Application = adsk.core.Application.get()
        ui   :adsk.core.UserInterface = app.userInterface
        des  :adsk.fusion.Design = app.activeProduct
        root :adsk.fusion.Component = des.rootComponent

        occ = root.occurrences.itemByName('HINGE:1')
        occ2 = root.occurrences.itemByName('snap_caps:1')


        hinges = [1,2, 3, 23,24, 11,12,13,14,15]
        corners = [5,9,17,21]




        transform = adsk.core.Matrix3D.create()
        transform.translation = adsk.core.Vector3D.create(displacement, 0, 0)

        negTransform = adsk.core.Matrix3D.create()
        negTransform.translation = adsk.core.Vector3D.create(displacement*-1, 0, 0)
         
        if oaType == 'Medial':
            for i in hinges:
                csMover(i, transform)
            for n in corners:
                csMover(n, negTransform)
        else:
            for i in hinges:
                csMover(i, negTransform)
            for n in corners:
                csMover(n, transform)
    


def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = _ui.commandDefinitions.itemById('cmdInputsSample')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition('cmdInputsSample', 'Command Inputs Sample', 'Sample to demonstrate various command inputs.')

        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Execute the command definition.
        cmdDef.execute()

        # Prevent this module from being terminated when the script returns, because we are waiting for event handlers to fire.
        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))