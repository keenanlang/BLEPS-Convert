#! /usr/bin/env python3

import argparse
import xlrd

parser = argparse.ArgumentParser(prog="BLEPS-convert", usage='%(prog)s [OPTIONS] TABLE')

parser.add_argument("table", metavar="TABLE", type=str, help="BLEPS Transfer Table")


def convert_fifo(worksheet):
	with open("bleps_fifo.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_ai.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tPREC\t\tEGU\t\tHIHI\t\tHIGH\t\tLOW\t\tLOLO\t\tHHSV\t\tHSV\t\tLSV\t\tLLSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"0"\t"",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")


def convert_faults(worksheet):
	with open("bleps_faults.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bi.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"0.5",\t""\t"Present",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")

def convert_trips(worksheet):
	with open("bleps_trips.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bi.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"NO FAULT"\t"TRIP",\t"NO ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")

		
def convert_warnings(worksheet):
	with open("bleps_warnings.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bi.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"NO FAULT"\t"TRIP",\t"NO ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")		

		
def convert_flows(worksheet):
	with open("bleps_flows.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_ai.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tPREC\t\tEGU\t\tHIHI\t\tHIGH\t\tLOW\t\tLOLO\t\tHHSV\t\tHSV\t\tLSV\t\tLLSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"1"\t"gpm",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")

def convert_temps(worksheet):
	with open("bleps_temps.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_ai.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tPREC\t\tEGU\t\tHIHI\t\tHIGH\t\tLOW\t\tLOLO\t\tHHSV\t\tHSV\t\tLSV\t\tLLSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"1"\t"degC",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")

		
def convert_inputs(worksheet):
	with open("bleps_inputs.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bi.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"GOOD"\t"BAD",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")
		
		
def convert_outputs(worksheet):
	with open("bleps_outputs.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bi.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"GOOD"\t"BAD",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")

		
def convert_EPICS(worksheet):
	with open("bleps_EPICS.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bo.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tHIGH\t\tZNAM\t\tONAM\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			onam = "CLOSE"
			high = "0.5"
			
			if "open" in pv.lower():
				onam = "OPEN"
			
			if "reset" in pv.lower():
				high = "1.0"
			
			if used and used == "X":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"{high}"\t"",\t"{onam}",\t"{desc}"}}\n'.format(name=pv, high=high, onam=onam, tag=tag, desc=desc))
				
		output.write("}\n")
		

def convert_display(worksheet):
	with open("bleps_display.substitutions", "w") as output:
		output.write('file "$(TOP)/db/bleps_bi.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tZNAM\t\tONAM\t\tZSV\t\tOSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X" and typ == "Bool":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"GOOD"\t"BAD",\t"NO_ALARM",\t"MAJOR",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n\n\n")
		output.write('file "$(TOP)/db/bleps_ai.db"\n')
		output.write("{\n")
		output.write("pattern\n")
		output.write("{N\t\t\tTAG\t\tSCAN\t\tPREC\t\tEGU\t\tHIHI\t\tHIGH\t\tLOW\t\tLOLO\t\tHHSV\t\tHSV\t\tLSV\t\tLLSV\t\tDESC}\n")
		
		for index in range(worksheet.nrows):
			row = worksheet.row(index)
			
			used = row[0].value
			typ  = row[1].value
			name = row[2].value
			pv   = row[3].value
			tag  = row[4].value
			desc = row[5].value
			
			pv = pv[pv.rfind(":") + 1:]
			desc = desc.lstrip("0123456789 ")
			
			if used and used == "X" and typ == "Int":
				output.write('{{"BLEPS:{name}",\t"{tag}",\t"2.0",\t"0"\t"",\t"",\t"",\t""\t"",\t"",\t"",\t""\t"",\t"{desc}"}}\n'.format(name=pv, tag=tag, desc=desc))
				
		output.write("}\n")
		
		

sheet_functions = {
	"FIFOs"        : convert_fifo,
	"Faults"       : convert_faults,
	"Trips"        : convert_trips,
	"Warnings"     : convert_warnings,
	"Info"         : None,
	"Flows"        : convert_flows,
	"Temps"        : convert_temps,
	"Inputs"       : convert_inputs,
	"Outputs"      : convert_outputs,
	"Sheet1"       : None,
	"Display"      : convert_display,
	"EPICS_Inputs" : convert_EPICS,
}



if __name__ == "__main__":
	args = parser.parse_args()
	
	data = xlrd.open_workbook(args.table)
	
	for sheet in data.sheets():
		if sheet.name in sheet_functions and sheet_functions[sheet.name]:
			sheet_functions[sheet.name](sheet)
