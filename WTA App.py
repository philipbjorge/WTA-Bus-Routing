from graph_tool.all import *
from sets import Set
import random
from geopy import geocoders, distance
from decimal import *


def randomize(iterable, bufsize=1000):
   ''' generator that randomizes an iterable. space: O(bufsize). time: O(n+bufsize). '''
   buf = [None] * bufsize
   for x in iterable:
      i = random.randrange(bufsize)
      if buf[i] is not None: yield buf[i]
      buf[i] = x
   for x in buf:
      if x is not None: yield x

g = Graph()
g = load_graph("finalNodes.dot", "dot")

vprop_name = g.vertex_properties["nameP"] #new_vertex_property("string")
vprop_gps = g.vertex_properties["gpsP"] #g.new_vertex_property("vector<float>")

g.edge_properties["busP"] = g.new_edge_property("string")
g.edge_properties["departureP"] = g.new_edge_property("int")
g.edge_properties["travelTimeP"] = g.new_edge_property("int")

eprop_bus = g.edge_properties["busP"] #g.new_edge_property("string")
eprop_departure = g.edge_properties["departureP"] #g.new_edge_property("vector<int>")
eprop_travelTime = g.edge_properties["travelTimeP"] #g.new_edge_property("int") #"Weight"

## Todo: User interface

startAddress = raw_input('What is your starting destination? ')
endAddress = raw_input('What is your ending destination? ')
leaveTime = raw_input('What is your departure time (in 24-h format? ')
lt = leaveTime.split(':')
finalTime = int(lt[0]*60) + int(lt[1])

geo = geocoders.Google('ABQIAAAAvaUMwifr0cnMnRZBCTqakRQ3CNZRIJSQeL6Igs3rwxcD1MUFWRQ5kLVLY8Rw6NfrZ-DkmklP0dA0AA')
sPlace, sGPS = geo.geocode(startAddress)
ePlace, eGPS = geo.geocode(endAddress)


closestS = -1
closestE = -1
shortestS = 1000.0
shortestE = 1000.0
for v in g.vertices():
	coord = vprop_gps[v].split(', ')
	sDist = distance.distance(sGPS, [float.fromhex(coord[0]), float.fromhex(coord[1])]).miles
	eDist = distance.distance(eGPS, [float.fromhex(coord[0]), float.fromhex(coord[1])]).miles
	if sDist < shortestS:
		shortestS = sDist
		closestS = v
	if eDist < shortestE:
		shortestE = eDist
		closestE = v

print vprop_name[closestS]
print vprop_name[closestE]

START_TIME = finalTime
END_TIME = START_TIME+120
START_NODE = closestS
END_NODE = closestE

#TODO: Better way to add edges
# Specifically, read the file myself

f = open("busEdgesData.txt", "r")
d = f.readlines()

for line in d:
	line = line.split("  ")
	vData = line[0].split("->")
	newSplit = line[1].split("\"")
	
	bus = newSplit[1] # Bus number
	times = newSplit[3]
	travelTime = newSplit[5]
	times = eval('['+times+']')
	for t in times:
		if t >= START_TIME and t <= END_TIME:
			newE = g.add_edge(g.vertex(vData[0]), g.vertex(vData[1]))
			eprop_bus[newE] = bus
			eprop_departure[newE] = t
			eprop_travelTime[newE] = int(travelTime)

successRoutes = []
	
for rider in range(150):
	currentNode = g.vertex(START_NODE)
	currentBus = "-1"
	currentRoute = []
	currentRoute.append([vprop_name[currentNode], "", START_TIME, 0])
	print "Trial " + str(rider)
	for choice in range(100):
		if currentNode == g.vertex(END_NODE):
			currentRoute.append(vprop_name[currentNode])
			successRoutes.append(currentRoute)
			break
		else:
			coin = random.randint(0,1)
			if coin == 0 and currentBus != "-1":
				# continue on bus
				for e in currentNode.out_edges():
					lastTry = currentRoute.pop()
					currentRoute.append(lastTry)
					#print eprop_bus[e] + " vs " + currentBus
					#print str(eprop_departure[e]) + " vs " + str(lastTry[2] + lastTry[3])
					if eprop_bus[e] == currentBus and eprop_departure[e] == (lastTry[2] + lastTry[3]):
						currentNode = e.target()
						currentRoute.append([vprop_name[currentNode], eprop_bus[e], eprop_departure[e], eprop_travelTime[e]])
						break
			else:
				# try a different bus
				found = -1
				for e in randomize(currentNode.out_edges(), 1000):
					lastTry = currentRoute.pop()
					currentRoute.append(lastTry)
					if eprop_departure[e] >= (lastTry[2] + lastTry[3]):
						newE = e
						found = 1
				if found != -1:
					currentBus = eprop_bus[newE]
					currentNode = newE.target()
					currentRoute.append([vprop_name[currentNode], eprop_bus[newE], eprop_departure[newE], eprop_travelTime[newE]])

#print currentRoute
threeShortest = []
thirdShortest = 10000			
for r in successRoutes:
	end = r.pop()
	next = r.pop()
	length = int(next[2])
	r.append(next)
	r.append(end)
	if length < thirdShortest:
		thirdShortest = length
		if len(threeShortest) == 3:
			threeShortest.pop()
			threeShortest.append(r)
		else:
			threeShortest.append(r)
for r in threeShortest:
	print "Attempt:"
	print r

print str(len(successRoutes)) + "/" + str(100)
