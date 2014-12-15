#!/usr/bin/python

from os import listdir
from os.path import isfile, join

onlyfiles = sorted([ f for f in listdir(".") if isfile(join(".", f)) ])


outputdatastruct = {}


def clean_number(num):
    return num.replace("\n", "")



def powerline_to_arr(line):
    line = line.strip()
    line = line.split()
    return [line[0], {"Switch": line[-5], "Int": line[-4], "Leak": line[-3], "Total": line[-2], "%": line[-1], "sub": []}]


# processes power data
# only handles up to 2 inner levels (4 space prefix)
def processpower(datarray, start_index):
    start_index += 2
    dataret = []
    top = powerline_to_arr(datarray[start_index])
    i = 1
    while True:
        currentline = datarray[start_index+i]
        if currentline == "1\n":
            break
        if currentline.startswith("  ") and not currentline.startswith("   "):
            dataret.append(powerline_to_arr(currentline))
        if currentline.startswith("    ") and not currentline.startswith("     "):
            dataret[-1][1]["sub"].append(powerline_to_arr(currentline))
        i += 1
    top[1]["sub"] = dataret
    return top



### round 1: get data out of the file
def process_file_r1(filename):
    pdat = {}


    f = open(filename)
    g = f.readlines()
    f.close()


    ready_for_area = False
    ready_for_power = False 

    arealabels = ["Combinational area", "Buf/Inv area", "Noncombinational area", "Net Interconnect area", "Total cell area", "Total area"]

    ### loop over the file, handling cases as we go
    for x in range(len(g)):

        ### "readies" - these determine if we're allowed to collect some piece of data
        if "redirect -file $REPORTS_DIR/$ICC_CHIP_FINISH_CEL.area.rpt {report_area -nosplit -hierarchy}" in g[x]:
            ready_for_area = True
        if "Hierarchical area distribution" in g[x]:
            print("triggered")
            ready_for_area = False

        #### be sure to get the ICC power report
        if "Report : power" in g[x] and "ICC" in g[x+4]:
            ready_for_power = True


        # get config data
        if "class DSEConfig" in g[x]:
            pdat["config"] = "".join(g[x:x+5])

        # area
        if ready_for_area:
            for label in arealabels:
                if label in g[x]:
                    #print("setting " + label)
                    #print(g[x])
                    pdat[label] = clean_number(g[x].strip().split(" ")[-1])

        # power
        if ready_for_power:
            if "Hierarchy                              Power    Power    Power    Power    %" in g[x]:
                pdat['power'] = processpower(g, x)

        # timing







    return pdat


### round 2: postprocess data
def process_file_r2(dat):
    return dat



stuff = process_file_r2(process_file_r1(onlyfiles[0]))
print(stuff)