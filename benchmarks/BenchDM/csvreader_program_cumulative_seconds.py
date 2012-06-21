import csv

def add_line(file, line):
    file.write("%s\t%s\n" % (line['process'],
                             line['cumulative_seconds']))

def get_csv_lines(file_name):
    lines = csv.DictReader(open(file_name, 'rU'), 
                           delimiter='\t', 
                           skipinitialspace=True)
    return lines
    
def parse_long(version):
    file = open("intermediate/process_cumulative_seconds_%s.txt" % version, 'w')
    file.write("process\tcumulative_seconds\n")
    lines = get_csv_lines("input/execute_%s.log" % version)
    cumulative = {}
    for line in lines:
        for process in line['Processes'].split(';'):
            process_name = process.split(' ')[-1]
            if process_name in cumulative:
                cumulative[process_name] += 1
            else:
                cumulative[process_name] = 1
    processes = cumulative.keys()
    processes.sort()
    for process in processes:
        line = {'process':process,
                'cumulative_seconds':cumulative[process]}
        add_line(file, line)
    file.close()
        
if __name__ == "__main__":
    parse_long("3")
