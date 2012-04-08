rt4x4MatrixToTRS Version 1.0
Author:  Ryan Trowbridge
Contact: admin@rtrowbridge.com

Description:
The rt4x4MatrixToTRS plugin "should" run correctly in Maya 2008 and all future versions.

A html file is included in the vain of every other Autodesk node html help file. It lists every attribute of the node and what it does.

Install:

Place the rt4x4MatrixToTRS script in this folder:
\Documents and Settings\user\My Documents\maya\version\scripts
 
In the main menus select Window\Settings\Preferences\Plug-in Manager

Select the Browse button and browse to the folder:
\Documents and Settings\user\My Documents\maya\version\scripts

Select the script to load the plug-in, drag the scroll bar to the bottom of the plugin manager to check if the rt4x4MatrixToTRS.py plugin is loaded. If it has an X on the Loaded checkbox and no errors popped up it should be good to go. 

Last you should try and load up the rt4x4MatrixToTRS_example.ma file to make sure everything is working fine. If it is you should be able to select the matrix_vector_mover nodes to influence the mesh spheres matrix. If the driven_matrix_sphere node is selected it will show the rt4x4MatrixToTRS1 as an input.

To create a new rt4x4MatrixToTRS node open the Hypershade editor. Select the Utilities tab. Now navigate to the menu Create\General Utilities\rt4x4MatrixToTRS This will create a new node of that type.

If an error popped up well Autodesk or Python changed something and either you can look at the source code and fix it yourself or look to see if I released a newer version.




