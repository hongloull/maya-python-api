# -----------------------------------------------------------------------------------
# rt4x4MatrixToTRS Version 1.0
# Author:  Ryan Trowbridge
# Contact: admin@rtrowbridge.com 
#
# Please give credit where credit is due this is written by Ryan Trowbridge
# with lots of experamentation to try to get python to work correctly.
# 
# This node is similar to a combination of two nodes that ship with Maya called fourByFourMatrix and the decomposeMatrix
# It also has the attributes parentInverseMatrix, normalize, and offset TRS attributes
# You can technicaly do what this node does with only Maya nodes but you would have to use several to mimic this one node
#
# To use this node:
# Load this script as a plugin using the tool under the Main Menu Window\Settings Preferences\Plug-in Manager
# Open the hypershade and navigate to general utilities
# Select the rt4x4MatrixToTRS utility node in the menu to create it
#
# The user can connect, drive, or use expressions to create the 16 floats of a matrix for the input
# The output of this node is the 16 floats turned into a matrix and converted into translate, euler rotation, and scale
# There is a normalize option also that forces the matrix rotation vectors to be of unit length
# -----------------------------------------------------------------------------------	

import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

debug = False

# -----------------------------------------------------------------------------------
# define the node type name
# define the node class
# define the node unique id ( use: cmds.getClassification( 'nodeName' ) to find a nodes class)
# -----------------------------------------------------------------------------------
kMatrixUtilNodeTypeName = "rt4x4MatrixToTRS"
kMatrixUtilNodeClassify = "utility/general"
kMatrixUtilNodeId = OpenMaya.MTypeId(0x87105)
#this is a non commercial plugin id, I might release one with a commercial id if requested


# define a new matrixUtilNode class derived from the MPxNode class
class rtMatrixUtilNode(OpenMayaMPx.MPxNode):

	# class variables
	
	parentInverseMatrix = OpenMaya.MObject()
	
	matrixIn = OpenMaya.MObject()
	
	in00 = OpenMaya.MObject()
	in01 = OpenMaya.MObject()
	in02 = OpenMaya.MObject()
	in03 = OpenMaya.MObject()
	
	in10 = OpenMaya.MObject()
	in11 = OpenMaya.MObject()
	in12 = OpenMaya.MObject()
	in13 = OpenMaya.MObject()
	
	in20 = OpenMaya.MObject()
	in21 = OpenMaya.MObject()
	in22 = OpenMaya.MObject()
	in23 = OpenMaya.MObject()
	
	in30 = OpenMaya.MObject()
	in31 = OpenMaya.MObject()
	in32 = OpenMaya.MObject()
	in33 = OpenMaya.MObject()
		
	out_t = OpenMaya.MObject()
	out_r = OpenMaya.MObject()
	out_s = OpenMaya.MObject()
	
	offset_t = OpenMaya.MObject()
	offset_r = OpenMaya.MObject()
	offset_s = OpenMaya.MObject()
	
	eulRotateOrder = OpenMaya.MObject()
	normalize = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		
	# arguments ( self, MPlug, MDataBlock) 
	def compute(self, plug, dataBlock):
		
		# if these attributes are requested, recompute their values
		if plug == rtMatrixUtilNode.out_t or \
			rtMatrixUtilNode.out_r or rtMatrixUtilNode.out_s:
		
			if debug:
				# print to the output window if in compute()
				sys.__stdout__.write( "##compute()\n" )

			# get MDataHandle's to attributes
			#
			
			try:
				pim_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.parentInverseMatrix )
			except:
				sys.stderr.write( "Failed to get inputValue parentInverseMatrix" )
				raise
			
			###vector X
			try:
				in00_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in00 )
			except:
				sys.stderr.write( "Failed to get inputValue in00" )
				raise
			try:
				in01_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in01 )
			except:
				sys.stderr.write( "Failed to get inputValue in01" )
				raise
			try:
				in02_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in02 )
			except:
				sys.stderr.write( "Failed to get inputValue in02" )
				raise
			try:
				in03_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in03 )
			except:
				sys.stderr.write( "Failed to get inputValue in03" )
				raise
			
			###vector Y
			try:
				in10_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in10 )
			except:
				sys.stderr.write( "Failed to get inputValue in10" )
				raise
			try:
				in11_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in11 )
			except:
				sys.stderr.write( "Failed to get inputValue in11" )
				raise
			try:
				in12_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in12 )
			except:
				sys.stderr.write( "Failed to get inputValue in12" )
				raise
			try:
				in13_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in13 )
			except:
				sys.stderr.write( "Failed to get inputValue in13" )
				raise
			
			###vector Z
			try:
				in20_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in20 )
			except:
				sys.stderr.write( "Failed to get inputValue in20" )
				raise
			try:
				in21_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in21 )
			except:
				sys.stderr.write( "Failed to get inputValue in21" )
				raise
			try:
				in22_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in22 )
			except:
				sys.stderr.write( "Failed to get inputValue in22" )
				raise
			try:
				in23_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in23 )
			except:
				sys.stderr.write( "Failed to get inputValue in23" )
				raise
			
			###vector T
			try:
				in30_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in30 )
			except:
				sys.stderr.write( "Failed to get inputValue in30" )
				raise
			try:
				in31_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in31 )
			except:
				sys.stderr.write( "Failed to get inputValue in31" )
				raise
			try:
				in32_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in32 )
			except:
				sys.stderr.write( "Failed to get inputValue in32" )
				raise
			try:
				in33_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.in33 )
			except:
				sys.stderr.write( "Failed to get inputValue in33" )
				raise
				
			###offset trs handles
			try:
				offset_t_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.offset_t )	
			except:
				sys.stderr.write( "Failed to get inputValue offset_t" )
				raise

			try:
				offset_r_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.offset_r )
			except:
				sys.stderr.write( "Failed to get inputValue offset_r" )
				raise

			try:
				offset_s_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.offset_s )
			except:
				sys.stderr.write( "Failed to get inputValue offset_s" )
				raise
				
			### user option attributes
			try:
				normalize_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.normalize)
			except:
				sys.stderr.write( "Failed to get inputValue normalize" )
				raise
			
			try:
				rotOrder_dataHandle = dataBlock.inputValue( rtMatrixUtilNode.eulRotateOrder )
			except:
				sys.stderr.write( "Failed to get inputValue eulRotateOrder" )
				raise
			
			###trs handles
			try:
				ot_dataHandle = dataBlock.outputValue( rtMatrixUtilNode.out_t )	
			except:
				sys.stderr.write( "Failed to get inputValue out_t" )
				raise
				
			try:
				or_dataHandle = dataBlock.outputValue( rtMatrixUtilNode.out_r )
			except:
				sys.stderr.write( "Failed to get inputValue out_r" )
				raise
				
			try:
				os_dataHandle = dataBlock.outputValue( rtMatrixUtilNode.out_s )
			except:
				sys.stderr.write( "Failed to get inputValue out_s" )
				raise
				
				
			# get values from dataHandles
			#
			pInvMatrix_value = pim_dataHandle.asMatrix()
			
			in00_value = in00_dataHandle.asFloat()
			in01_value = in01_dataHandle.asFloat()
			in02_value = in02_dataHandle.asFloat()
			in03_value = in03_dataHandle.asFloat()
			
			in10_value = in10_dataHandle.asFloat()
			in11_value = in11_dataHandle.asFloat()
			in12_value = in12_dataHandle.asFloat()
			in13_value = in13_dataHandle.asFloat()
			
			in20_value = in20_dataHandle.asFloat()
			in21_value = in21_dataHandle.asFloat()
			in22_value = in22_dataHandle.asFloat()
			in23_value = in23_dataHandle.asFloat()
			
			in30_value = in30_dataHandle.asFloat()
			in31_value = in31_dataHandle.asFloat()
			in32_value = in32_dataHandle.asFloat()
			in33_value = in33_dataHandle.asFloat()
			
			normalize_value = normalize_dataHandle.asBool()
			
			offset_t_value = offset_t_dataHandle.asFloatVector()
			offset_r_value = offset_r_dataHandle.asFloatVector()
			offset_s_value = offset_s_dataHandle.asFloatVector()

			
			# Note there is a Maya Python bug with enum attributes
			# you must use MDataHandle.asShort() to get the proper value
			rotOrder_value = rotOrder_dataHandle.asShort()
			
			# get the matrix as vectors
			x_vector = OpenMaya.MVector(in00_value, in01_value, in02_value)
			y_vector = OpenMaya.MVector(in10_value, in11_value, in12_value)
			z_vector = OpenMaya.MVector(in20_value, in21_value, in22_value)
			
			# user option for normalizing the matrix rotation vectors
			if normalize_value:
				x_vector.normalize()
				y_vector.normalize()
				z_vector.normalize()
			
			# create a matrix from the input values
			getMatrix = OpenMaya.MMatrix()
			matrixList = (x_vector.x, x_vector.y, x_vector.z, in03_value,
					y_vector.x, y_vector.y, y_vector.z, in13_value,
					z_vector.x, z_vector.y, z_vector.z, in23_value,
					in30_value, in31_value, in32_value, in33_value)
						
			OpenMaya.MScriptUtil().createMatrixFromList(matrixList, getMatrix)
			
			if debug:
				#print matrix values
				sys.__stdout__.write("matrix out: ( " + str(x_vector.x) + ", " + str(x_vector.y) + ", " + str(x_vector.z) + ", " + str(0.0) + ", \n" + \
								str(y_vector.x) + ", " + str(y_vector.y) + ", " + str(y_vector.z) + ", " + str(0.0) + ", \n" + \
								str(z_vector.x) + ", " + str(z_vector.y) + ", " + str(z_vector.z) + ", " + str(0.0) + ", \n" + \
								str(in30_value) + ", " + str(in31_value) + ", " + str(in32_value) + ", " + str(1.0) + " )\n" )
	
			# Multiply parentInverseMatrix by the matrix created by the user
			finalMatrix = ( getMatrix * pInvMatrix_value )
	
			# MTransformationMatrix
			mTM = OpenMaya.MTransformationMatrix( finalMatrix)
			
			# Get the translation
			trans = mTM.getTranslation( OpenMaya.MSpace.kTransform )
			
			# Get the rotation
			mquat = mTM.rotation()
			rot = mquat.asEulerRotation()
			rot.reorderIt( rotOrder_value )
			
			# Get the scale
			scaleDoubleArray = OpenMaya.MScriptUtil()
			scaleDoubleArray.createFromList( [0.0, 0.0, 0.0], 3 )
			scaleDoubleArrayPtr = scaleDoubleArray.asDoublePtr()
			
			mTM.getScale( scaleDoubleArrayPtr, OpenMaya.MSpace.kTransform)
						
			x_scale = OpenMaya.MScriptUtil().getDoubleArrayItem( scaleDoubleArrayPtr, 0 )
			y_scale = OpenMaya.MScriptUtil().getDoubleArrayItem( scaleDoubleArrayPtr, 1 )
			z_scale = OpenMaya.MScriptUtil().getDoubleArrayItem( scaleDoubleArrayPtr, 2 )
			
			if debug:
				# print to the output window the output values that are to be set
				sys.__stdout__.write( "rotate order: " + str( rotOrder_value ) + "\n" )
				sys.__stdout__.write( "normalize: " + str( normalize_value ) + "\n" )
				
				sys.__stdout__.write( "trans.x: " + str(trans.x) + "\n" )
				sys.__stdout__.write( "trans.y: " + str(trans.y) + "\n" )
				sys.__stdout__.write( "trans.z: " + str(trans.z) + "\n" )

				sys.__stdout__.write( "rot.x: " + str(math.degrees( rot.x )) + "\n" )
				sys.__stdout__.write( "rot.y: " + str(math.degrees( rot.y )) + "\n" )
				sys.__stdout__.write( "rot.z: " + str(math.degrees( rot.z )) + "\n" )
				
				sys.__stdout__.write( "x_scale: " + str(x_scale) + "\n" )
				sys.__stdout__.write( "y_scale: " + str(y_scale) + "\n" )
				sys.__stdout__.write( "z_scale: " + str(z_scale) + "\n" )

			# get the final result vectors as a MFloatVector
			resultTrans = OpenMaya.MFloatVector(trans.x, trans.y, trans.z)
			resultRot = OpenMaya.MFloatVector(math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z ))
			resultScale = OpenMaya.MFloatVector( x_scale, y_scale, z_scale)

			# set the output trs values
			ot_dataHandle.setMFloatVector( (resultTrans + offset_t_value) )
			or_dataHandle.setMFloatVector( (resultRot + offset_r_value) )
			os_dataHandle.setMFloatVector( (resultScale + offset_s_value) )
			
			# set the plug clean so maya knows it can update
			dataBlock.setClean(plug)
	
		else:
			return OpenMaya.kUnknownParameter
		
		return OpenMaya.MStatus.kSuccess
			
def nodeCreator():

	return OpenMayaMPx.asMPxPtr( rtMatrixUtilNode() )

# create and initialize the attributes to the node
def nodeInitializer():

	nAttr = OpenMaya.MFnNumericAttribute()
	eAttr = OpenMaya.MFnEnumAttribute()
	nMAttr = OpenMaya.MFnMatrixAttribute()
	cAttr = OpenMaya.MFnCompoundAttribute()
	
	# create input attributes
	#
	
	rtMatrixUtilNode.parentInverseMatrix = nMAttr.create( "parentInverseMatrix", "pim", OpenMaya.MFnMatrixAttribute.kDouble )
	nMAttr.setWritable(True)
	nMAttr.setStorable(True)
	nMAttr.setReadable(True)
	nMAttr.setKeyable(True)
	
	# Vector X
	rtMatrixUtilNode.in00 = nAttr.create("in00", "i00", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.in01 = nAttr.create("in01", "i01", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.in02 = nAttr.create("in02", "i02", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.in03 = nAttr.create("in03", "i03", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	# Vector Y
	rtMatrixUtilNode.in10 = nAttr.create("in10", "i10", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtMatrixUtilNode.in11 = nAttr.create("in11", "i11", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtMatrixUtilNode.in12 = nAttr.create("in12", "i12", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.in13 = nAttr.create("in13", "i13", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	# Vector Z
	rtMatrixUtilNode.in20 = nAttr.create("in20", "i20", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtMatrixUtilNode.in21 = nAttr.create("in21", "i21", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtMatrixUtilNode.in22 = nAttr.create("in22", "i22", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.in23 = nAttr.create("in23", "i23", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	# Vector T
	rtMatrixUtilNode.in30 = nAttr.create("in30", "i30", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtMatrixUtilNode.in31 = nAttr.create("in31", "i31", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	rtMatrixUtilNode.in32 = nAttr.create("in32", "i32", OpenMaya.MFnNumericData.kFloat, 0.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.in33 = nAttr.create("in33", "i33", OpenMaya.MFnNumericData.kFloat, 1.0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	

	# create TRS offset attributes
	#
	rtMatrixUtilNode.offset_t = nAttr.createPoint("offsetTranslate", "oft" )
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.offset_r = nAttr.createPoint("offsetRotate", "ofr" )
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	rtMatrixUtilNode.offset_s = nAttr.createPoint("offsetScale", "ofs" )
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)
	
	
	# create TRS output attributes
	#
	rtMatrixUtilNode.out_t = nAttr.createPoint("outputTranslate", "ot" )
	nAttr.setWritable(False)
	nAttr.setStorable(False)
	nAttr.setReadable(True)
	
	rtMatrixUtilNode.out_r = nAttr.createPoint("outputRotate", "or" )
	nAttr.setWritable(False)
	nAttr.setStorable(False)
	nAttr.setReadable(True)
	
	rtMatrixUtilNode.out_s = nAttr.createPoint("outputScale", "os" )
	nAttr.setWritable(False)
	nAttr.setStorable(False)
	nAttr.setReadable(True)
	
	# create rotate order enum attribute
	rtMatrixUtilNode.eulRotateOrder = eAttr.create( "eulerRotateOrder", "ero", 0 )
	eAttr.addField("XYZ", 0)
	eAttr.addField("YZX", 1)
	eAttr.addField("ZXY", 2)
	eAttr.addField("XZY", 3)
	eAttr.addField("YXZ", 4)
	eAttr.addField("ZYX", 5)
	eAttr.setWritable(True)
	eAttr.setStorable(True)
	eAttr.setReadable(True)
	eAttr.setKeyable(False)
	
	# create normalize attribute
	rtMatrixUtilNode.normalize = nAttr.create("normalize", "n", OpenMaya.MFnNumericData.kBoolean , 0)
	nAttr.setWritable(True)
	nAttr.setStorable(True)
	nAttr.setReadable(True)
	nAttr.setKeyable(True)

	# create compound attribute
	#
	rtMatrixUtilNode.matrixIn = cAttr.create( "matrixIn", "mi" )
	
	cAttr.addChild( rtMatrixUtilNode.in00 )
	cAttr.addChild( rtMatrixUtilNode.in01 )
	cAttr.addChild( rtMatrixUtilNode.in02 )
	cAttr.addChild( rtMatrixUtilNode.in03 )
	
	cAttr.addChild( rtMatrixUtilNode.in10 )
	cAttr.addChild( rtMatrixUtilNode.in11 )
	cAttr.addChild( rtMatrixUtilNode.in12 )
	cAttr.addChild( rtMatrixUtilNode.in13 )
	
	cAttr.addChild( rtMatrixUtilNode.in20 )
	cAttr.addChild( rtMatrixUtilNode.in21 )
	cAttr.addChild( rtMatrixUtilNode.in22 )
	cAttr.addChild( rtMatrixUtilNode.in23 )
	
	cAttr.addChild( rtMatrixUtilNode.in30 )
	cAttr.addChild( rtMatrixUtilNode.in31 )
	cAttr.addChild( rtMatrixUtilNode.in32 )
	cAttr.addChild( rtMatrixUtilNode.in33 )


	# add attribues
	#
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.normalize )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.eulRotateOrder )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.parentInverseMatrix )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.matrixIn )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.offset_t )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.offset_r )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.offset_s )

	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.out_t )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.out_r )
	rtMatrixUtilNode.addAttribute( rtMatrixUtilNode.out_s )	
	
	# Setup which attributes affect each other	
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.matrixIn,  rtMatrixUtilNode.out_t )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.normalize,  rtMatrixUtilNode.out_t )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.eulRotateOrder,  rtMatrixUtilNode.out_t )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.parentInverseMatrix, rtMatrixUtilNode.out_t )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.offset_t, rtMatrixUtilNode.out_t )
	
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.matrixIn,  rtMatrixUtilNode.out_r )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.normalize,  rtMatrixUtilNode.out_r )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.eulRotateOrder,  rtMatrixUtilNode.out_r )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.parentInverseMatrix, rtMatrixUtilNode.out_r )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.offset_r, rtMatrixUtilNode.out_r )
	
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.matrixIn,  rtMatrixUtilNode.out_s )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.normalize,  rtMatrixUtilNode.out_s )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.eulRotateOrder,  rtMatrixUtilNode.out_s )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.parentInverseMatrix, rtMatrixUtilNode.out_s )
	rtMatrixUtilNode.attributeAffects ( rtMatrixUtilNode.offset_s, rtMatrixUtilNode.out_s )
	
	
# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
	try:
		mplugin.registerNode( kMatrixUtilNodeTypeName, kMatrixUtilNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kMatrixUtilNodeClassify)
	except:
		sys.stderr.write( "Failed to register node: %s" % kMatrixUtilNodeTypeName )
		raise


# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( kMatrixUtilNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % kMatrixUtilNodeTypeName )
		raise
