import csv

def add_line(file, line):
    for process in line['Processes'].split(';'):
        file.write("%s\t%s\n" % (line['Seconds'],
                                process.split(" ")[-1]))

def get_csv_lines(file_name):
    lines = csv.DictReader(open(file_name, 'rU'), 
                           delimiter='\t', 
                           skipinitialspace=True)
    return lines
    
def parse_long(version):
    file = open("intermediate/seconds_program_%s.txt" % version, 'w')
    file.write("Seconds\tprogram\n")
    lines = get_csv_lines("input/execute_%s.log" % version)
    for line in lines:
        add_line(file, line)
    file.close()
        
if __name__ == "__main__":
    parse_long("3")
