###Render a population map using pygal & pygal_maps_world modules
###2017 world population sourced from Data.World (https://data.world/edmadrigal/world-population-json)

import json
#Leverages 'pygal' and 'pygal_maps_world' modules
import pygal, pygal.maps.world as pygmaps

from country_code import get_country_code

#Data sourced from Data world (https://data.world/edmadrigal/world-population-json)
filename = 'worldpopulation2017.json'
with open(filename, encoding='utf-8') as f:
	pop_data = json.load(f)


#Build a dictionary of population data
cc_populations = {}
for pop_dict in pop_data:
	country_name = pop_dict['country']
	population = int(float(pop_dict['population']))

	#Get country code (lookup based on name); store as key if found
	code = get_country_code(country_name)
	if code:
		cc_populations[code] = population

#Group countries into 3 population levels
cc_pops_1, cc_pops_2, cc_pops_3 = {}, {}, {}
for cc, pop in cc_populations.items():
	if pop < 10**7:
		cc_pops_1[cc] = pop
	elif pop < 10**9: 
		cc_pops_2[cc] = pop
	else:
		cc_pops_3[cc] = pop


print(
	"<10,000,000: "+str(len(cc_pops_1))+'\n' +
	">10,000,000 & <1,000,000,000: "+str(len(cc_pops_2))+'\n' +
	">1,000,000,000: "+str(len(cc_pops_3))+'\n' +
	"Total countries: "+str(len(cc_populations)))
#Check
print(len(cc_pops_1)+len(cc_pops_2)+len(cc_pops_3) == len(cc_populations))

wm = pygmaps.World()
wm.title = 'World Population in 2017, by Country'
wm.add('0-10m', cc_pops_1)
wm.add('10-1bn', cc_pops_2)
wm.add('>1bn', cc_pops_3)


outfile = 'world_population2017.svg'
wm.render_to_file(outfile)
