# BlenderPythonScripts
Two files provided one an script executions instruction file for following in the python console interface in Blender
and the other providing script.  The script itself is for selection subdivision based batch inset extrusion operations.  You might find this script useful when needing to parse and subdivide a given selection area, into 
smaller selection areas that are iterated for operations.  I chose inset primarily because it is one of those 
operator functions where the function applied to a whole selection area is not the same as iterated subset selection
areas applied to the whole same selection area.

You can modify the general subdivision selection area MxN dimension size by modifying in script variables:
dimx

and 

dimy 

The script optimizes on the edge boundaries of given selection area a nearest fit selection area approximation 
otherwise to the specific MxN area.  
