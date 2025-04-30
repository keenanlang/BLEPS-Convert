#! /APSshare/anaconda3/x86_64/bin/python3

import os
import json
import xlrd
import pathlib
import argparse
import subprocess

script_dir = str(pathlib.Path(__file__).resolve().parent.resolve())
curr_dir = str(pathlib.Path(os.getcwd()).resolve())

parser = argparse.ArgumentParser(prog="BLEPS-convert", usage='%(prog)s [OPTIONS] inpath [outpath]')

parser.add_argument("inpath", metavar="inpath", type=str, help="BLEPS Excel file")
parser.add_argument("outpath", nargs="?", metavar="outpath", type=str, help="Folder to hold output files")

parser.add_argument("-t", "-w", "--to", "--write",
	metavar="FORMAT",
	dest="out_format",
	action="store",
	help="Type of conversion, based on output file. Either xls->substutions or xls->ui/css. Recognized values are ['substitutions', 'subs', 'templates', 'ui', 'qt', 'css', 'bob']",
	type=str,
	default="substitutions",
	choices=['substitutions', 'subs', 'templates', 'ui', 'qt', 'css', 'bob'])


def ai_header(output):
	output.write('file "$(TOP)/db/bleps_ai.db"\n')
	output.write("{\n")
	output.write("pattern\n")
	output.write("{N\t\t\tTAG\t\tSCAN\t\tPREC\t\tEGU\t\tHIHI\t\tHIGH\t\tLOW\t\tLOLO\t\tHHSV\t\tHSV\t\tLSV\t\tLLSV\t\tDESC}\n")
	
def bi_header(output):
	output.write('file "$(TOP)/db/bleps_bi.db"\n')
	output.write("{\n")
	output.write("pattern\n")
	output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
	
def bo_header(output):
	output.write('file "$(TOP)/db/bleps_bo.db"\n')
	output.write("{\n")
	output.write("pattern\n")
	output.write("{N\t\t\tTAG\t\tHIGH\t\tZNAM\t\tONAM\t\tDESC}\n")

	
def parse_row(row):
	row[3].ctype = 1
	
	used = row[0].value
	typ  = row[1].value
	name = row[2].value
	
	tag  = row[4].value
	desc = row[5].value
	
	pv = name.upper()
	desc = desc.lstrip("0123456789 ")
	
	return { 
		"used" : used, 
		"type" : typ, 
		"name" : name, 
		"pv"   : pv, 
		"tag"  : tag,
		"desc" : desc
	}
	
def write_basic(output, worksheet, title, header, format):
	output.write("# BLEPS {title}\n\n".format(title=title))
	header(output)
	
	for index in range(worksheet.nrows):
		info = parse_row(worksheet.row(index))
			
		if info["used"] and info["used"] == "X":
			output.write(format.format(name=info["pv"], tag=info["tag"], desc=info["desc"]))
			
	output.write("}\n\n\n")
	
		
def EPICS_to_substitution(output, worksheet):
	output.write("# BLEPS EPICS Inputs\n\n")
	bo_header(output)
	
	for index in range(worksheet.nrows):
		info = parse_row(worksheet.row(index))
			
		onam = "CLOSE"
		high = "0.5"
		
		if "open" in info["pv"].lower():
			onam = "OPEN"
		
		if "reset" in info["pv"].lower():
			high = "1.0"
		
		if info["used"] and info["used"] == "X":
			output.write('{{"BLEPS:{name}",\t"{tag}",\t"{high}",\t"",\t"{onam}",\t"{desc}"}}\n'.format(name=info["pv"], high=high, onam=onam, tag=info["tag"], desc=info["desc"]))
				
	output.write("}\n\n\n")
		

def display_to_substitution(output, worksheet):
	output.write("# BLEPS Display (Bools)\n")
	bi_header(output)
			
	for index in range(worksheet.nrows):
		info = parse_row(worksheet.row(index))
		
		if info["used"] and info["used"] == "X" and info["type"] == "Bool":
			output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"GOOD",\t"BAD",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=info["pv"], tag=info["tag"], desc=info["desc"]))
				
	output.write("}\n\n\n")
	output.write("# BLEPS Display (Ints)\n")
	ai_header(output)
	
	for index in range(worksheet.nrows):
		info = parse_row(worksheet.row(index))
		
		if info["used"] and info["used"] == "X" and info["type"] == "Int":
			output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"0",\t"",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n'.format(name=info["pv"], tag=info["tag"], desc=info["desc"]))
				
	output.write("}\n\n\n")
	

substitution_functions = {
	"FIFOs"        : (lambda f, s: write_basic(f, s, title="FIFO",     header=ai_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"0",\t"",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n')),
	"Faults"       : (lambda f, s: write_basic(f, s, title="Faults",   header=bi_header, format='{{"BLEPS:{name}",\t"{tag}",\t"0.5",\t"",\t"Present",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n')),
	"Trips"        : (lambda f, s: write_basic(f, s, title="Trips",    header=bi_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"NO_FAULT",\t"TRIP",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n')),
	"Warnings"     : (lambda f, s: write_basic(f, s, title="Warnings", header=bi_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"NO_FAULT",\t"TRIP",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n')),
	"Info"         : None,
	"Flows"        : (lambda f, s: write_basic(f, s, title="Flows",    header=ai_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"1",\t"gpm",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n')),
	"Temps"        : (lambda f, s: write_basic(f, s, title="Temps",    header=ai_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"1",\t"degC",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n')),
	"Inputs"       : (lambda f, s: write_basic(f, s, title="Inputs",   header=bi_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"BAD",\t"GOOD",\t"MAJOR",\t"NO_ALARM",\t"{desc}"}}\n')),
	"Outputs"      : (lambda f, s: write_basic(f, s, title="Outputs",  header=bi_header, format='{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"GOOD",\t"BAD",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n')),
	"Display"      : display_to_substitution,
	"EPICS_Inputs" : EPICS_to_substitution,
}


if __name__ == "__main__":
	args = parser.parse_args()
	
	if not args.outpath:
		args.outpath = curr_dir

	data = xlrd.open_workbook(args.inpath)
		
	if args.out_format == "css":
		args.out_format = "bob"
		
	if args.out_format == "qt":
		args.out_format = "ui"
	
	if args.out_format in ["substitutions", "subs", "templates"]:
		with open(args.outpath + "/bleps.substitutions", "w") as output:
			for sheet in data.sheets():
				if sheet.name in substitution_functions and substitution_functions[sheet.name]:
					substitution_functions[sheet.name](output, sheet)

	elif args.out_format in ["qt", "ui", "css", "bob"]:
		shutter_yaml = {"shutters" : [] }
		GV_yaml   = {"GVs"    : [], "aspect" : 1.6}
		Temp_yaml = {"num_Temps" : 0, "aspect" : 0.37}
		Flow_yaml = {"Flows" : [], "aspect" : 0.45}
		Extras_yaml = {"Gauges" : [], "Pumps" : [], "VS1" : [], "VS2" : []}
		
		for index in range(data.sheet_by_name("Outputs").nrows):
			info = parse_row(data.sheet_by_name("Outputs").row(index))
			
			if info["used"] and info["used"] == "X":
				if "Permit" in info["name"] and ".Permit" in info["tag"]:
					abbr = info["name"][0:3]
					
					cutoff = max(info["desc"].rfind("Valve"), info["desc"].rfind("Shutter"))
					
					label = info["desc"][0: cutoff].strip()
					
					shutter_yaml["shutters"].append({ "label" : label, "abbreviation" : abbr})
					
				if "GV" in info["name"] and "Open" in info["name"]:
					GV_yaml["GVs"].append({"ID" : info["name"].removesuffix("_Open_Command")})
					
		for index in range(data.sheet_by_name("Temps").nrows):
			info = parse_row(data.sheet_by_name("Temps").row(index))
			
			if info["used"] and info["used"] == "X":
				if "Current" in info["name"]:
					Temp_yaml["num_Temps"] += 1
					
		for index in range(data.sheet_by_name("Flows").nrows):
			info = parse_row(data.sheet_by_name("Flows").row(index))
			
			if info["used"] and info["used"] == "X":
				if "Current" in info["name"]:
					Flow_yaml["Flows"].append({"ID" : info["name"].removeprefix("Flow").removesuffix("_Current")})
					
		for index in range(data.sheet_by_name("Inputs").nrows):
			info = parse_row(data.sheet_by_name("Inputs").row(index))
			
			if info["used"] and info["used"] == "X":
				if "IP" in info["name"]:
					Extras_yaml["Pumps"].append({"ID" : info["name"].strip("IPStatus_")})
					
				if "IG" in info["name"]:
					Extras_yaml["Gauges"].append({"ID" : info["name"].strip("IGStatus_")})
					
		for index in range(data.sheet_by_name("Trips").nrows):
			info = parse_row(data.sheet_by_name("Trips").row(index))
			
			if info["used"] and info["used"] == "X":
				if "VS" in info["name"]:
					Extras_yaml["VS1"].append({"ID" : info["name"].strip("VSTrip_")})
					
		second_col = int(len(Extras_yaml["VS1"]) / 2)
		
		Extras_yaml["VS2"] = Extras_yaml["VS1"][second_col:]
		Extras_yaml["VS1"] = Extras_yaml["VS1"][0:second_col]
		
		
		All_yaml = {}
		All_yaml["shutters"] = shutter_yaml["shutters"]
		All_yaml["GVs"] = GV_yaml["GVs"]
		All_yaml["num_Temps"] = Temp_yaml["num_Temps"]
		All_yaml["Flows"] = Flow_yaml["Flows"]
		All_yaml["Gauges"] = Extras_yaml["Gauges"]
		All_yaml["Pumps"] = Extras_yaml["Pumps"]
		All_yaml["VS1"] = Extras_yaml["VS1"]
		All_yaml["VS2"] = Extras_yaml["VS2"]
		
		
		print("Generating Shutters Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{yaml}' --output {path}.{format} shutters.yml".format(format=args.out_format, yaml=json.dumps(shutter_yaml), path=args.outpath + "/shutters"), shell=True)

		print("Generating Gate Valve Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{yaml}' --output {path}.{format} bleps_valves.yml".format(format=args.out_format, yaml=json.dumps(GV_yaml), path=args.outpath + "/bleps_valves"), shell=True)
		
		print("Generating Temps Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{yaml}' --output {path}.{format} bleps_temps.yml".format(format=args.out_format, yaml=json.dumps(Temp_yaml), path=args.outpath + "/bleps_temps"), shell=True)
		
		print("Generating Flows Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{yaml}' --output {path}.{format} bleps_flows.yml".format(format=args.out_format, yaml=json.dumps(Flow_yaml), path=args.outpath + "/bleps_flows"), shell=True)
		
		print("Generating FIFO Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{{}}' --output {path}.{format} bleps_fifo.yml".format(format=args.out_format, path=args.outpath + "/bleps_fifo"), shell=True)
		
		print("Generating Extras Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{yaml}' --output {path}.{format} bleps_extras.yml".format(format=args.out_format, yaml=json.dumps(Extras_yaml), path=args.outpath + "/bleps_extras"), shell=True)
		
		print("Generating Everything Screen")
		subprocess.call("/APSshare/bin/gestalt --to {format} --from str --input '{yaml}' --output {path}.{format} bleps_all.yml".format(format=args.out_format, yaml=json.dumps(All_yaml), path=args.outpath + "/bleps_all"), shell=True)
