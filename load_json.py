import json, pprint

def open_file():
	file_pointer = open("map.json")

	map_data = json.load(file_pointer)

	for k, v in map_data.items():
		print(k, v)




#pprint.pprint(map_data)