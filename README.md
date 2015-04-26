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

I have also two different Mondrian 2d subdivision scripts.  The first is more lengthy and quite a bit more complex in implementation, and producing different geometric results relative to the second script which is simpler in terms of code implementation.  

Prim's random maze generator was a short fairly easy to implement script, and generates a 3d maze.  User's can specify wall and cell(floor) spatial sizes here alongside the number of nodes (or floor cell tiles given) for the maze's overall dimensions.  

Gabriel Graph generator (work in progress at the moment) generates a Gabriel graph of specified dimensions into a given 3d mesh object in blender.  A Gabriel Graph is I believe mentioned as a Voronoi dual graph, or with some computational geometric methods you can convert this likewise to a Voronoi graph.  
