##house generator  random 
import random
attr_livingroom = {'public':True, 'dimprange':(10,25), 'value':None,
                   'dimratiorange':(.75,.9)}
attr_diningroom = {'public':True, 'dimprange':(5,10), 'value':None,
                   'dimratiorange':(.75,.9)}
attr_kitchen = {'public':True, 'dimprange':(5,10), 'value':None,
                'dimratiorange':(.65,.9)}
attr_officestudy = {'public':False, 'dimprange':(5,10), 'value':None,
                    'dimratiorange':(.65,.9)}
attr_bath = {'public':True, 'dimprange':(3,7), 'value':None,
             'dimratiorange':(.5,.9)}
attr_hall = {'public':True, 'dimprange':(0,3), 'value':None,
             'dimratiorange':(.3,.35)}
attr_bedroom = {'public':False, 'dimprange':(5,10), 'value':None,
                'dimratiorange':(.75,.9)}
attr_masterbedroom = {'public':False, 'dimprange':(8,13), 'value':None,
                      'dimratiorange':(.75,.9)}
attr_masterbath = {'public':False, 'dimprange':(5,10), 'value':None,
                   'dimratiorange':(.5,.9)}
attr_closet = {'public':False, 'dimprange':(0,2), 'value':None,
               'dimratiorange':(.75,.9)}

nodes = {'livingroom':attr_livingroom, 'diningroom':attr_diningroom,
         'kitchen':attr_kitchen, 'officestudy':attr_officestudy,
         'bath':attr_bath, 'hall':attr_hall,
         'bedroom':attr_bedroom, 'masterbedroom':attr_masterbedroom,
         'masterbath':attr_masterbath, 'closet':attr_closet
         }

totalnodes = len(nodes)
nodekeylist = list(nodes.keys())
modnodes = {}
bal = 0
while ( len(nodekeylist) > 0):
    nlen = len(nodekeylist)
    i = random.randint(0,nlen-1)
    nkey = nodekeylist[i]
    attrs = nodes[nkey]
    val1, val2 = attrs['dimprange']
    j = random.randint(val1, val2+bal)
    bal = val2+bal - j
    attrs['value'] = j
    modnodes[nkey] = attrs
    del nodekeylist[i]
sumval = 0
for node in modnodes:
    sumval += modnodes[node]['value']

print("Total percentage: ", sumval)
nodekeylist = list(nodes.keys())
nlen = len(nodekeylist)
i = random.randint(0,nlen-1)
nkey = nodekeylist[i]
attrs = nodes[nkey]
attrs['value'] = 100-sumval
nodes[nkey] = attrs

## fully constrained space and contrained space are two model types.
## Fully constrained space model first uses a specified overall area.
##  From this area a randomly assigned size is given for a node, followed
## by its position.

## For either model:
##  There attribute 'public' defines position locus centrality.
##  Conversely 'non public' defines compliment position locus centrality.
## Non fully constrained models use nucleus approach methods for modeling.
##  In the 'nucleus' approach a seed 'public' node established the basis
## for the graph construction.
##  In constrained models:  we can instead opt also for non nucleus seeding
## where instead defining 'non public' node position on a give boundary,or
##alternately the rigidly overall spatial area can be defined as
## the nucleus.
## In constrained space model:
## In the fully constrained model user specified area is more rigidly conformed
## in so far as room design and space optimization, and thus we need to solve
## this problem where tracking not only the amount of space relative to
##overall space occupied, but also by the position and area taken for each
##node, while tracking this relative to its occupation in such overall
##space.  
