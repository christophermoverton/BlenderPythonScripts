
import math
import mathutils
import bpy
from math import radians

TOLERANCE = .005
SCALE = (1,1) # 1 actual ft to 1 drawn ft
STEP_WIDTH = 15/12
STEP_RISER = 10/12
STEPS = 12
STYLES = ('stone', 'industrial')
IBCROSSLENGTH = 1
IBTHICKNESS = .1
RAIL_AP = 32
LEN_AP = 2 # Minimum 2 
SPIRAL_RAD = 2  #This radius for spiral curvature
SPIRAL_STEP_DIV = 20 #For building spiral step curvature.  Low values create higher curvature aliasing.

class Spiralbuild:

	def computeriserandwidth(self):
		global STEP_RISER
		self.steps = round(self.z/STEP_RISER)
		STEP_RISER = self.z / self.steps
		global STEP_WIDTH
		STEP_WIDTH = STEP_RISER / self.slope

	def slope(self):
		self.slope = STEP_RISER/STEP_WIDTH
	def zsubincf(self):
		self.zinc = STEP_RISER
		self.zsubinc = STEP_RISER/SPIRAL_STEP_DIV
	def thetasubincf(self):
		thetainc = STEP_WIDTH/(SPIRAL_RAD + self.stepwidth)
		self.thetasubinc = thetainc/SPIRAL_STEP_DIV 
	

	def polarcoords(self, radius, theta):
		x = (radius)*math.cos(theta)
		y = (radius)*math.sin(theta)
		return x,y

	def buildfaces(self):
		nincs = SPIRAL_STEP_DIV * self.steps
		nrange = range(0,nincs-1)	
		a = 0
		b = 1
		c = 2
		d = 3
		e = 4
		f = 5
		g = 6
		h = 7
		faces = []
		for n in nrange:
			f1 = [[a,e,h,d], [b,f,g,c], [a,b,c,d],[e,f,g,h],
			     [a,b,f,e], [d,c,g,h]]
			faces += f1
			if (n + 1) % SPIRAL_STEP_DIV == 0 and not n == 0:
				c = g + 2
				d = h + 2
				a = e
				b = f
				e += 6
				f += 6
				g += 6
				h += 6
			else:
				c = g
				d = h
				a = e
				b = f
				e += 4
				f += 4
				g += 4
				h += 4	
		return faces
			

	def buildverts(self):
		nincs = SPIRAL_STEP_DIV * self.steps
		nrange = range(0,nincs)
		outerradius = SPIRAL_RAD + self.stepwidth
		innerradius = SPIRAL_RAD
		thetapos = 0
		zpos = 0 
		uzpos = self.zinc
		vertices = []
		for n in nrange:
			x,y = self.polarcoords(innerradius, thetapos)
			vertices += [[x,y,zpos]]
			x1,y1 = self.polarcoords(outerradius, thetapos)
			vertices += [[x1,y1,zpos],[x1,y1, uzpos],[x,y,uzpos]]
			vertices = vertices[0:len(vertices)]
			if n % SPIRAL_STEP_DIV == 0 and not n == 0:
				vertices += [[x1,y1, uzpos + self.zinc],[x,y, uzpos + self.zinc]]
			if n < 5:
				thetapos += self.thetasubinc
			else:
				thetapos += self.thetasubinc
				zpos += self.zsubinc
				if n % SPIRAL_STEP_DIV == 0:
					uzpos += self.zinc
		self.nincs = nincs
		self.outerradius = outerradius
		self.innerradius = innerradius
		self.thetatotal = thetapos
		print(self.zsubinc)
		return vertices		
				
			
	def construct(self):
		self.slope()
		self.computeriserandwidth()
		self.zsubincf()
		self.thetasubincf()
		verts = self.buildverts()
		faces = self.buildfaces()
		return verts, faces
		
	def __init__(self, z, stepwidth):
		self.z = z
		self.stepwidth = stepwidth

class Railbuild:

	def joinobjects(self):
		bpy.ops.object.join()

	def selectobjects(self, objnamelist):
		objlist = []
		for objectname in objnamelist:
			obj = bpy.data.objects[objectname]
			obj.select = True
			

	def initcursorlocation(self):
		bpy.context.scene.cursor_location = [0.0, 0.0, 0.0]

	def rotateobject(self, objectname, axis, rt_amt):
		obj = bpy.data.objects[objectname]
		bpy.context.scene.objects.active = obj
		rt_amt = self.degtorad(rt_amt)
		if axis == 'x':
			bpy.context.object.rotation_euler.x = rt_amt
		elif axis == 'y':
			bpy.context.object.rotation_euler.y = rt_amt
		elif axis == 'z':
			bpy.context.object.rotation_euler.z = rt_amt

	def translate(self, objectname, axis, tr_amt):
		obj = bpy.data.objects[objectname]
		bpy.context.scene.objects.active = obj
		if axis == 'x':
			bpy.context.object.location.x = tr_amt
		elif axis == 'y':
			bpy.context.object.location.y = tr_amt
		elif axis == 'z':
			bpy.context.object.location.z = tr_amt		
	
	def addingMeshobj(self, meshname, objectname, coords, faces):
		me = bpy.data.meshes.new(meshname)   # create a new mesh  
 
		ob = bpy.data.objects.new(objectname, me)          # create an object with that mesh
		ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
		bpy.context.scene.objects.link(ob)                # Link object to scene
 
		# Fill the mesh with verts, edges, faces 
##		me.from_pydata(coords,[],faces)   # edges or faces should be [], or you ask for problems
##		me.update(calc_edges=True) 


	def degtorad(self, deg):
		return ((2 * math.pi)/360)*deg
	
	def radtodeg(self, rad):
		return (360/ (2*math.pi)) * rad

	def buildendvertsonmiter(self, zpos, div = False, inv = False, ct = False,
				 zspiral = False, nincs = 0,
			  	 thetasubinc = 0, zsubinc = 0, radius = 0):
		vertices = []
		arcinc = 360/RAIL_AP
		arcincrad = self.degtorad(arcinc)
		arcradpos = 0
		irange = range(0, RAIL_AP)
		if div:
			if inv:
				if ct:
					theta = -((90 -self.angle)/2)
				else:
					theta = -(self.angle/2)
			else:
				if ct:
					theta = (90 - self.angle)/2
				else:
					theta = (self.angle/2)
		else:
			if inv:
				if ct:
					theta = -(90 - self.angle)
				else:
					theta = -(self.angle)
			else:
				if ct:
					theta = (90 - self.angle)
				else:
					theta = self.angle
		for i in irange:
			x = self.radius*math.cos(arcradpos)
			y = self.radius*math.sin(arcradpos)
			yatrdist = self.radius + y
			z = yatrdist*math.tan(self.degtorad(theta))
			z += zpos
			if zspiral:
				z -= zpos
				phi = math.atan(zsubinc/(radius))
				thetapos = 0
				if not zpos == 0:
					thetapos += thetasubinc * nincs
				eul = mathutils.Euler((phi + 90, 0.0, thetapos), 'XYZ')
				vec = mathutils.Vector((x,y,z))
				vec.rotate(eul)
				x, y, z = (vec.x, vec.y, vec.z)
				
			vertices.append([x,y,z])
			arcradpos += arcincrad
		return vertices

	def builbodyverts(self, length, lcheck = False, zspiral = False, nincs = 0,
			  thetasubinc = 0, zsubinc = 0, radius = 0):
		print('thetasubinc: ',thetasubinc)
		print('zsubinc: ',zsubinc)
		print('radius: ',radius)
		vertices = []
		if zspiral:
			nrange = range(0,nincs-1)
			phi = math.atan(zsubinc/(radius))
			thetapos = 0
			zpos = 0 
			irange = range(0, RAIL_AP)
			arcinc = 360/RAIL_AP
			arcincrad = self.degtorad(arcinc)
			arcradpos = 0			
			vertices = []
			for n in nrange:
				arcradpos = 0
				eul = mathutils.Euler((phi + 90, 0.0, thetapos), 'XYZ')
				for i in irange:
					x = self.radius*math.cos(arcradpos)
					y = self.radius*math.sin(arcradpos)
					vec = mathutils.Vector((x,y,0))
					vec.rotate(eul)
					#if zspiral:
					vertices.append([vec.x,vec.y,vec.z])
					#else:
					#	vertices.append([x,y,zpos])
					arcradpos += arcincrad
				thetapos += thetasubinc
				
		else:			
			
			global LEN_AP
			if length > self.z and not lcheck:
				LEN_AP = int(length/1.5)
			zinc = length/(LEN_AP)
			zpos = zinc
			irange = range(0, RAIL_AP)
			arcinc = 360/RAIL_AP
			arcincrad = self.degtorad(arcinc)
			arcradpos = 0
			zrange = range(0, LEN_AP-1)
			for z in zrange:
				arcradpos = 0
				for i in irange:
					x = self.radius*math.cos(arcradpos)
					y = self.radius*math.sin(arcradpos)
					if zspiral:
						vertices.append([x,y,0])
					else:
						vertices.append([x,y,zpos])
					arcradpos += arcincrad
				zpos += zinc
		
		return vertices

	def buildfaces(self):
		faces = []
		zrange = range(0, LEN_AP)
		irange = range(0, RAIL_AP)
		vert1 = 0
		vert2 = 1
		vert4 = vert1 + RAIL_AP
		vert3 = vert2 + RAIL_AP
		for z in zrange:
			for i in irange:
				if not i == RAIL_AP-1:
					faces.append([vert1, vert2, vert3, vert4])
					vert1 = vert2
					vert2 += 1
					vert4 = vert3
					vert3 += 1
				else:
					vert3 = vert4 - (RAIL_AP - 1)
					vert2 = vert1 - (RAIL_AP - 1)
					faces.append([vert1, vert2, vert3, vert4])
					if z == LEN_AP-1:
						break
					vert1 += 1
					vert2 = vert1 + 1
					vert4 += 1 
					vert3 = vert4 + 1
		print('rail faces: ', faces[0:33])
		return faces

 
	def doublemiteredend(self, bottom = [], top = [], tangle = None):
		if not len(bottom) == 0:
			bdiv, binv, bct = bottom
		else:
			bdiv = False
			binv = False
			bct = False
		if not len(top) == 0:
			tdiv, tinv, tct = top
		else:
			tdiv = True
			tinv = True
			tct = True 
		
		vertices = self.buildendvertsonmiter(0, bdiv, binv, bct)
		vertices += self.builbodyverts(self.z)
		zinc = self.z/(LEN_AP)
		zpos = zinc
		zpos += zinc
		if tangle == None:
			tangle = self.angle
		anglecpy = self.angle
		self.angle = tangle 
		vertices += self.buildendvertsonmiter(zpos, tdiv, tinv, tct)
		faces = self.buildfaces()
		self.angle = anglecpy
		return vertices, faces

	def dmiteredrail(self, lcheck = False, zspiral = False, nincs = 0,
			 thetasubinc = 0, zsubinc = 0, radius = 0):
		global LEN_AP
		lenapcopy = LEN_AP
		vertices = self.buildendvertsonmiter(0,True, False, True,
						     zspiral, nincs,
					       	     thetasubinc, zsubinc, radius )
		vertices += self.builbodyverts(self.beamlength, lcheck, zspiral, nincs,
					       thetasubinc, zsubinc, radius)

		#if self.beamlength > self.z:
		#	LEN_AP = int(self.beamlength/1.5)
		#zinc = self.beamlength/(LEN_AP)
		#zinc = self.z/(LEN_AP)
		zpos = self.beamlength
		#zpos += zinc
		angle1 = self.angle
		self.angle -= (90-angle1)
		vertices += self.buildendvertsonmiter(zpos, True, True, True,
						      zspiral, nincs,
					       	      thetasubinc, zsubinc, radius)
		faces = self.buildfaces()
		self.angle = angle1
		LEN_AP = lenapcopy
		return vertices, faces

	def sprotverts(self, verts, thetainc, zinc, radius):
		thetapos = 0
		zpos = 0
		#phi in radians
		phi = math.atan(zinc/(radius))
		phi_mat_rot = mathutils.Matrix.Rotation(phi, 4, 'Y') 
		count = 0
		rsprotverts = []
		for vert in verts:
			x,y,z = vert
			vec = mathutils.Vector((x, y, z))
			if count % RAIL_AP == 0:
				#if not thetapos % 90 == 0: 
					#theta1 = math.atan((math.tan(radians(thetapos)))**-1)
				theta1 = thetapos
				tx = radius * math.cos(thetapos)
				ty = radius * math.sin(thetapos)
				tz = zpos
				if count == 0:
					self.spiralarcleninc = (tx**2 + ty**2 + tz**2)**.5
					
				tvec = mathutils.Vector((tx,ty,tz))
				trmat = mathutils.Matrix.Translation(tvec)
				
				#else:
				#	value = thetapos/90
				#	intval = int(value)
				
				#	remainder = value - intval
				#	angle = remainder*360
				#	if angle == 0:
				#		theta1 = radians(90)
				#	elif angle == 90:
				#		theta1 = radians(0)
				#	elif angle == 180:
				#		theta1 = radians(-90)
				#	elif angle == 270:
				#		theta1 = radians(0)
			
				theta_mat_rot = mathutils.Matrix.Rotation(theta1, 4, 'Z')
				eul = mathutils.Euler((phi, 0.0, theta1+180), 'XYZ')
				mat_rot = eul.to_matrix()
			#RAIL_AP
			translated_vec = trmat*vec
			#rot_vec = translated_vec.rotate(eul)
			rsprotverts.append([translated_vec.x, translated_vec.y, translated_vec.z])
			if (count+1) % RAIL_AP == 0 and not count == 0:
				#print(thetapos)
				thetapos += thetainc
				#print(thetapos) 
				zpos += zinc
			count += 1
		return rsprotverts

	
	
	def constructspiralrail(self, nincs, thetainc, zinc, oradius, iradius):
		global LEN_AP
		lenapcopy = LEN_AP
		LEN_AP = nincs
		phi = math.atan(zinc/(oradius))		
		vdmr, fdmr = self.dmiteredrail(lcheck = True, zspiral = True, nincs = nincs,
						thetasubinc = thetainc, zsubinc = zinc, radius = oradius)
		rvdmr = self.sprotverts(vdmr, thetainc, zinc, oradius)
		self.addingMeshobj('rail', 'Rail', rvdmr, fdmr)
		vdmr, fdmr = self.dmiteredrail(lcheck = True, zspiral = True, nincs = nincs,
						thetasubinc = thetainc, zsubinc = zinc, radius = oradius)
		rvdmr = self.sprotverts(vdmr, thetainc, zinc, oradius)
		self.addingMeshobj('rail2', 'Rail2', rvdmr, fdmr)
		ivdmr, ifdmr = self.dmiteredrail(lcheck = True, zspiral = True, nincs = nincs,
						thetasubinc = thetainc, zsubinc = zinc, radius = iradius)
		irvdmr = self.sprotverts(ivdmr, thetainc, zinc, iradius)
		self.addingMeshobj('rail3', 'Rail3', irvdmr, ifdmr)
		LEN_AP = lenapcopy
		self.spiralarclen = self.spiralarcleninc * nincs
		self.totalarcangle = thetainc * nincs
		self.totalz = zinc * nincs
		vdm, fdm = self.doublemiteredend()
		self.addingMeshobj('post', 'Post', vdm, fdm)
		xinc = oradius*math.cos(0.0)
		yinc = oradius*math.sin(0.0)
		self.translate('Post', 'x', xinc)
		self.translate('Post', 'y', yinc -.04)
		self.translate('Post', 'z', .04)
		self.translate('Rail', 'z', 3.0)
		top1 = [False, False, False]
		tangle1 = 90 - (90-self.angle)/2
		vdm2, fdm2 = self.doublemiteredend(top = top1, tangle = tangle1)
		xinc = oradius*math.cos(self.totalarcangle)
		yinc = oradius*math.sin(self.totalarcangle)
		
		self.addingMeshobj('post2', 'Post2', vdm2, fdm2)
		self.translate('Post2', 'z', self.totalz - 0.38001 + .26989)
		self.translate('Post2', 'y', yinc - 0.19997 + 0.3183)
		self.translate('Post2', 'x', xinc -0.00385)
		self.rotateobject('Post2', 'z', 8.0)
		nposts = int (self.spiralarclen / 15 )
		
		npostdivz = self.totalz / nposts
		npostdivarcangle = self.totalarcangle / nposts
		postrange = range(1, nposts)

		objectnamelist = []
		for n in postrange:
			
			xinc = oradius*math.cos(npostdivarcangle*n)
			yinc = oradius*math.sin(npostdivarcangle*n)
			zinc = npostdivz * n
			top1 = [False, False, False]
			tangle1 = 90-self.angle
			vdm2, fdm2 = self.doublemiteredend(top = top1, tangle = tangle1)
			self.addingMeshobj('post' + str(n + 2), 'Post' + str(n + 2), vdm2, fdm2)
			self.translate('Post' + str(n+2), 'z', zinc - 0.38001 + .24)
			self.translate('Post' + str(n+2), 'y', yinc - 0.04)
			self.translate('Post' + str(n+2), 'x', xinc)
			self.rotateobject('Post' + str(n+2), 'z', self.radtodeg(npostdivarcangle * n))
			objectnamelist += ['Post' + str(n+2)]
			objectnamelist = objectnamelist[0:len(objectnamelist)]	
		print('nposts: ', nposts)
		objectnamelist += ['Post','Post2','Rail','Rail2']
		print(objectnamelist)
		self.selectobjects(objectnamelist)	
		self.joinobjects()

	def construct(self):
		vdm, fdm = self.doublemiteredend()
		self.addingMeshobj('post', 'Post', vdm, fdm)
		vdmr, fdmr = self.dmiteredrail()		
		self.addingMeshobj('rail', 'Rail', vdmr, fdmr)
		self.rotateobject('Rail', 'x', -(90-self.angle))
		yinc = self.beamlength*math.cos(self.degtorad(self.angle))
		zinc = self.beamlength*math.sin(self.degtorad(self.angle))
		self.translate('Rail', 'z', self.z - .09)
		self.translate('Rail', 'y', -.04)
		top1 = [False, False, False]
		tangle1 = 90 - (90-self.angle)/2
		vdm2, fdm2 = self.doublemiteredend(top = top1, tangle = tangle1)
		self.addingMeshobj('post2', 'Post2', vdm2, fdm2)
		self.translate('Post2', 'z', zinc - 0.38001)
		self.translate('Post2', 'y', yinc - 0.19997)
		nposts = int (self.beamlength / 5 )
		npostdiv = self.beamlength / nposts
		postrange = range(1, nposts)
		objectnamelist = []
		for n in postrange:
			
			yinc = n*npostdiv*math.cos(self.degtorad(self.angle))
			zinc = n*npostdiv*math.sin(self.degtorad(self.angle))
			top1 = [False, False, False]
			tangle1 = (90-self.angle)
			vdm2, fdm2 = self.doublemiteredend(top = top1, tangle = tangle1)
			self.addingMeshobj('post' + str(n + 2), 'Post' + str(n + 2), vdm2, fdm2)
			self.translate('Post' + str(n+2), 'z', zinc - 0.38001)
			self.translate('Post' + str(n+2), 'y', yinc - 0.19997)
			objectnamelist += ['Post' + str(n+2)]
			objectnamelist = objectnamelist[0:len(objectnamelist)]	
		vdmr, fdmr = self.dmiteredrail()		
		self.addingMeshobj('rail2', 'Rail2', vdmr, fdmr)
		self.rotateobject('Rail2', 'x', -(90-self.angle))
		self.translate('Rail2', 'z', self.z/2 - .09)
		self.translate('Rail2', 'y', -.04)
		objectnamelist += ['Post','Post2','Rail','Rail2']
		print(objectnamelist)
		self.selectobjects(objectnamelist)	
		self.joinobjects()	
		
		

	def __init__(self, radius, z, angle, beamlength):
		self.radius = radius
		self.z = z 
		self.angle = angle
		self.beamlength = beamlength

class Stairbuild:
	def scaleconverttoactual(self):
		adist, ddist = SCALE
		c1 = adist == 1
		c2 = ddist == 1
		if not c1 or not c2:
			#convert input drawn distances
			self.x = self.x * (adist / ddist)
			self.y = self.y * (adist / ddist)
			self.z = self.z * (adist / ddist)

	def scaleconverttodrawn(self):
		adist, ddist = SCALE
		c1 = adist == 1
		c2 = ddist == 1
		if not c1 or not c2:
			#convert input drawn distances
			self.x = self.x * (ddist / adist)
			self.y = self.y * (ddist / adist)
			self.z = self.z * (ddist / adist)

	def calcSteps(self, localy, localz):
		global STEPS
		stepsw = localy / STEP_WIDTH
		stepsr = localz / STEP_RISER
		if stepsw < stepsr:
			steps = stepsr
		else:
			steps = stepsw

		STEPS = int(steps)	
		print ('steps: ', STEPS)

	def approxY(self):
		return STEPS * STEP_WIDTH 	

	def degtorad(self, deg):
		return ((2 * math.pi)/360)*deg
	
	def radtodeg(self, rad):
		return (360/ (2*math.pi)) * rad

	def estimaterange(self, value):
		return (value - value*TOLERANCE, value + value*TOLERANCE)

	def calcincrement(self, lenvalue):
		return lenvalue/STEPS
	
	def initcursorlocation(self):
		bpy.context.scene.cursor_location = [0.0, 0.0, 0.0]

	def rotateobject(self, objectname, axis, rt_amt):
		obj = bpy.data.objects[objectname]
		bpy.context.scene.objects.active = obj
		rt_amt = self.degtorad(rt_amt)
		if axis == 'x':
			bpy.context.object.rotation_euler.x = rt_amt
		elif axis == 'y':
			bpy.context.object.rotation_euler.y = rt_amt
		elif axis == 'z':
			bpy.context.object.rotation_euler.z = rt_amt

	def translate(self, objectname, axis, tr_amt):
		obj = bpy.data.objects[objectname]
		bpy.context.scene.objects.active = obj
		if axis == 'x':
			bpy.context.object.location.x = tr_amt
		elif axis == 'y':
			bpy.context.object.location.y = tr_amt
		elif axis == 'z':
			bpy.context.object.location.z = tr_amt		
	
	def addingMeshobj(self, meshname, objectname, coords, faces):
		me = bpy.data.meshes.new(meshname)   # create a new mesh  
 
		ob = bpy.data.objects.new(objectname, me)          # create an object with that mesh
		ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
		bpy.context.scene.objects.link(ob)                # Link object to scene
 
		# Fill the mesh with verts, edges, faces 
		me.from_pydata(coords,[],faces)   # edges or faces should be [], or you ask for problems
		me.update(calc_edges=True) 

	def buildIbeamfaces(self):
		faces = []
		
		a = [0, 12, 13, 1]    
		b = [17, 5, 3, 15]
		c = [2, 14, 12, 0]
		d = [1, 13, 15, 3]
		e = [14, 2, 4, 16]
		f = [12, 6, 11, 13]
		g = [14, 7, 6, 12]
		h = [13, 11, 10, 15]
		i = [14, 7, 8, 16]
		j = [17, 9, 10, 15]
		k = [4, 16, 8, 4]
		l = [5, 17, 9, 5]
		setone = [a, b, c, d, e, f, g,
			  h, i, j, k, l]
##		setone = [a,f]
		settwo = []
		for i in setone:
			newface = []
			for vert in i:
				newface.append(vert + 18)
			settwo.append(newface)
		m = [11, 6, 24, 29]
		n = [1, 0, 18, 19]
		o = [6, 7, 25, 24]
		p = [10, 11, 29, 28]
		q = [2, 0, 18, 20]
		r = [1, 3, 21, 19]
		s = [3, 5, 23, 21]
		t = [2, 4, 22, 20]
		u = [9, 10, 28, 27]
		v = [8, 7, 25, 26]
		w = [4, 22, 26, 8]
		x = [5, 28, 27, 9] 
		setthree = [m, n, o, p, q, r, s, t,
			    u, v, w, x]
		faces = setone + settwo + setthree
##		faces = setone + settwo
		return faces


	def buildIbeamverts(self, bnormtozinc, bnormtoz):
		phi = 90 - self.pickangle
		bprime = bnormtozinc * math.cos(self.degtorad(self.pickangle))
		self.bprime = bprime
		IBTHICKNESS = .1 * bprime
		IBCROSSLENGTH = bprime
		bprime += 4*IBTHICKNESS 
		midpointcrosslen = IBCROSSLENGTH/2
		mh = IBTHICKNESS/2
		beamlen = (bnormtoz**2 + self.z**2)**.5	
		vertices = []

		# should post a sketch of the model in terms of diagram here
		#for clarity. 
	
		a = [0,0,0]
		b = [IBCROSSLENGTH, 0, 0]
		c = [0, IBTHICKNESS, 0]
		d = [IBCROSSLENGTH, IBTHICKNESS, 0]
		e = [midpointcrosslen-mh, IBTHICKNESS, 0]
		ex, ey, ez = e
		f = [midpointcrosslen+mh, IBTHICKNESS, 0]
		fx, fy, fz = f
		g = [0,bprime, 0]
		h = [0,bprime-IBTHICKNESS, 0]
		i = [midpointcrosslen - mh, bprime - IBTHICKNESS, 0]
		j = [midpointcrosslen + mh, bprime - IBTHICKNESS, 0]
		k = [IBCROSSLENGTH, bprime - IBTHICKNESS, 0]
		l = [IBCROSSLENGTH, bprime, 0]
		ta = [0, bprime*math.cos(self.degtorad(phi))**2, 
              	      -bprime*math.cos(self.degtorad(phi))*math.sin(self.degtorad(phi))]
		tax, tay, taz = ta
		tb = [IBCROSSLENGTH, tay, taz]
		tbx, tby, tbz = tb
		tc = [0, tay, taz + IBTHICKNESS]
		tcx, tcy, tcz = tc
		td = [tbx, tay, taz + IBTHICKNESS]
		te = [ex, tcy, tcz]
		tf = [fx, tcy, tcz]
		setone = [a,b,c,d,e,f,g,h,i,j,k,l]
		
		settwo = []
		for i in setone:
			ix,iy,iz = i 
			settwo.append([ix,iy,beamlen])
		pta = [0, bprime*math.cos(self.degtorad(self.pickangle))**2, 
			beamlen + bprime*math.cos(self.degtorad(self.pickangle))*math.sin(self.degtorad(self.pickangle))]
		ptax, ptay, ptaz = pta
		ptb = [IBCROSSLENGTH, ptay, ptaz]
		ptbx, ptby, ptbz = ptb
		ptc = [0, ptay, ptaz - IBTHICKNESS]
		ptcx, ptcy, ptcz = ptc
		ptd = [ptbx, ptay, ptaz - IBTHICKNESS]
		pte = [ex, ptcy, ptcz]
		ptf = [fx, ptcy, ptcz]
		setthree = [ta, tb, tc, td, te, tf]
		setfour = [pta, ptb, ptc, ptd, pte, ptf]
		vertices += setone + setthree + settwo + setfour
		print(vertices)
		print(len(vertices))
		return vertices		

	def construct(self, zinc, bnormtoz, bnormtozinc, bplanenormlen):
		def genvertinds(vertinds):
			vertrange = range(0, 8)
			verts = []
			for i in vertrange:
				verts.append(vertinds + i)
			return verts

		def genfaces(vertinds):
			faces = []
			
			a,b,c,d,e,f,g,h = vertinds
			af = [a,e,g,c]
			bf = [a,e,f,b]
			cf = [c,g,h,d]
			df = [a,c,d,b]
			ef = [b,f,h,d]
			ff = [e,g,h,f]
			faces += [af,bf,cf,df,ef,ff]
			#faces = [af]				
			return faces

		def buildindsteps():
			vertices = []
			faces = []
			count = 0
			incrange = range(0, STEPS)
			ypos = 0
			nypos = 0
			nzpos = 0
			zpos = 0
			vertind = 0
			stepinc = .1*zinc
			for i in incrange:
				nypos += bnormtozinc
				nzpos += zinc
				nszpos = zpos
				nszpos -= stepinc
				verta = [0, ypos, nszpos]	
				vertb = [bplanenormlen, ypos, nszpos]
				vertc = [0, nypos, nszpos]
				vertd = [bplanenormlen, nypos, nszpos]
				verte = [0, ypos, zpos]
				vertf = [bplanenormlen, ypos, zpos]
				vertg = [0, nypos, zpos]
				verth = [bplanenormlen, nypos, zpos]
				vertices += [verta, vertb, vertc, vertd, verte, vertf,
					     vertg, verth]	
				vertices = vertices[0:len(vertices)]			
				newverts = genvertinds(vertind) 
				faces += genfaces(newverts)
#				vertices += newverts
				vertind += 8
				ypos = nypos
				zpos = nzpos
			return vertices, faces 

		def buildonplane():
			vertices = []
			faces = []
			count = 0
			incrange = range(0, STEPS)
			ypos = 0

			zpos = 0
			vertind = 0
			for i in incrange:
				nypos += ypos + bnormtozinc
				nzpos += zpos + zinc
				verta = [0, ypos, 0]	
				vertb = [bplanenormlen, ypos, 0]
				vertc = [0, nypos, 0]
				vertd = [bplanenormlen, nypos, 0]
				verte = [0, ypos, zpos]
				vertf = [bplanenormlen, ypos, zpos]
				vertg = [0, nypos, zpos]
				verth = [bplanenormlen, nypos, zpos]
				vertices += [verta, vertb, vertc, vertd, verte, vertf,
					     vertg, verth]	
				vertices = vertices[0:len(vertices)]			
				newverts = genvertinds(vertind) 
				faces += genfaces(newverts)
				vertices += newverts
				vertind += 6
				ypos = nypos
				zpos = nzpos
			return vertices, faces

		if self.style == 'stone':
			verts, faces = buildonplane()
		elif self.style == 'industrial':
			#constructing Ibeam
			ibverts = self.buildIbeamverts(bnormtozinc, bnormtoz)
			ibfaces = self.buildIbeamfaces()
			meshname = 'Ibeammesh'
			objectname = 'Ibeam'
			self.initcursorlocation()
			self.addingMeshobj(meshname, objectname, ibverts, ibfaces)
			vertices, faces = buildindsteps()
			print('angle: ', self.pickangle)
			self.addingMeshobj('indsteps','Steps', vertices, faces)
			self.rotateobject(objectname, 'x', -self.pickangle)
			self.addingMeshobj('Ibeam1','Ibeam2', ibverts, ibfaces)
			self.rotateobject('Ibeam2', 'x', -self.pickangle)
			self.translate('Ibeam2', 'x', bplanenormlen)
			beamlen = (bnormtoz**2 + self.z**2)**.5	
			rb = Railbuild(.1, 3, 90-self.pickangle, beamlen)
			rb.construct()
		elif self.style == 'spiral':
			sb = Spiralbuild(self.z, bplanenormlen)
			verts, faces = sb.construct()
			self.initcursorlocation()
			self.addingMeshobj('spiralstairs', 'Spiralstairs', verts, faces[0:len(faces)])
			railrad = sb.outerradius
			arclen = (railrad**2 + (sb.zsubinc**2)/(railrad**2))**.5 * sb.thetatotal
			beamlen = (bnormtoz**2 + self.z**2)**.5	
			rb = Railbuild(.1, 3, 90-self.pickangle, arclen)
			rb.constructspiralrail(sb.nincs, sb.thetasubinc, sb.zsubinc, sb.outerradius, sb.innerradius)			

	def checktolerance(self, estrange, value):
		check = False
		lb, ub = estrange
		c1 = value < lb
		c2 = value > ub
		if not c1 or not c2:
			check = True
		return check 

	def recommends(self, bplaneangledeg, bnormtozaxis):
		bnormtoz = self.z*math.tan(self.degtorad(self.pickangle))**-1
		print('Specified parameters for building stairs are out of range./n')
		print('Changing the angle of stairs to: ', bplaneangledeg)
		print('or changing on the ', bnormtozaxis, ' length to: ', bnormtoz)
		print('provides adequate building parameters.')
	

	def checkreq(self):
		check = False
		if not self.buildplane == 'double':
			if self.buildplane == 'xz':
				bplaneanglerad = math.atan(self.z/self.x)
				bplaneangledeg = self.radtodeg(bplaneanglerad)
				estrange = self.estimaterange(bplaneangledeg)
				localz = self.z
				localy = self.x
				localx = self.y
				if self.checktolerance(estrange, self.pickangle):
					check = True
					self.pickangle = bplaneangledeg
                    
				else:
					self.recommends(bplaneangledeg, 'x')
			else:
				localz = self.z
				localy = self.y
				localx = self.x
				bplaneanglerad = math.atan(self.z/self.y)
				bplaneangledeg = self.radtodeg(bplaneanglerad)
				estrange = self.estimaterange(bplaneangledeg)
				if self.checktolerance(estrange, self.pickangle):
					check = True
					self.pickangle = bplaneangledeg
				else:
					self.recommends(bplaneangledeg, 'x')
		return check, localx, localy, localz

	def setup(self):
		
		cbool, localx, localy, localz = self.checkreq()
		if cbool:
			self.calcSteps(localy, localz)
			if self.approx:
				localy = self.approxY()
				bplaneanglerad = math.atan(localz/localy)
				bplaneangledeg = self.radtodeg(bplaneanglerad)
				self.pickangle = bplaneangledeg
			self.pickangle = 90 - self.pickangle
			zinc = localz/STEPS
			bnormtoz = localy
			bnormtozinc = localy/STEPS
			bplanenormlen = localx 
			self.construct(zinc, bnormtoz, bnormtozinc, bplanenormlen)
			#will need to rotate object once instantiated representing global axis
			#as opposed to local coord system build
			

	def __init__(self, x, y, z, style, buildplane, 
		     pickangle = 35.5, pangle = False, approx = False):
		self.x = x
		self.y = y
		self.z = z
		#builds are done either in a double or single plane.
		#specified either 'xz', 'yz' or 'double'
		#Will leave it up to a user to rotate the mesh object once constructed
        
		self.buildplane = buildplane
		
		self.pickangle = pickangle
		self.pangle = pangle 
		self.style = style
		self.approx = approx
		#if approx checked true, calculates on local y nearest y conforming 
		#to STEP_WIDTH boundaries, checked false implies STEP_WIDTH is variable

sb = Stairbuild(5, 20, 30, 'spiral', 'yz', approx = True)
sb.setup()
thetainc = 360/20
thetaincrad = math.radians(thetainc)
irange = range(0,20)
thetapos = 0
z = 0
verts = []
eul = mathutils.Euler((math.radians(45.0), 0.0, math.radians(45.0)), 'XYZ')
for i in irange:
	eul = mathutils.Euler((math.radians(45.0), 0.0, math.radians(45.0 + i)), 'XYZ')
	x = math.cos(thetapos)
	y = math.sin(thetapos)
	vec = mathutils.Vector((x,y,z))
	vec.rotate(eul)
	verts.append([vec.x,vec.y,vec.z])
	verts = verts[0:len(verts)]
	thetapos += thetainc


#sb.addingMeshobj('circledots', 'circledots', verts, [])
