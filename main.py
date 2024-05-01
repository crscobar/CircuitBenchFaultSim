from yachalk import chalk
# Class used to store information for a wire
class Node(object):
    def __init__(self, name, value, gatetype, innames):
        self.name = name         # string
        self.value = value        # char: '0', '1', 'U' for unknown
        self.gatetype = gatetype    # string such as "AND", "OR" etc
        self.interms = []     # list of nodes (first as strings, then as nodes), each is a input wire to the gatetype
        self.innames = innames  # helper string to temperarily store the interms' names, useful to find all the interms nodes and link them
        self.is_input = False    # boolean: true if this wire is a primary input of the circuit
        self.is_output = False   # boolean: true if this wire is a primary output of the circuit

    def set_value(self, v):
        self.value = v 

    def display(self):     # print out the node nicely on one line
        if self.is_input:
            nodeinfo = f"input:\t{str(self.name):5} = {self.value:^4}" 
            print(nodeinfo)
            return 
        elif self.is_output:
            nodeinfo = f"output:\t{str(self.name):5} = {self.value:^4}"
        else:               # internal nodes   
            nodeinfo = f"wire:  \t{str(self.name):5} = {self.value:^4}"

        interm_str = " "
        interm_val_str = " "
        for i in self.interms:
            interm_str += str(i.name)+" "
            interm_val_str += str(i.value)+" "

        nodeinfo += f"as {self.gatetype:>5}"
        nodeinfo += f"  of   {interm_str:20} = {interm_val_str:20}"

        print(nodeinfo)
        return 

    # calculates the value of a node based on its gate type and values at interms
    def calculate_value(self):
        u_inp = 0
        d_inp = 0
        d_prime_inp = 0

        for i in self.interms:  # skip calculating unless all interms have specific values 1 or 0
            if i.value != "0" and i.value !="1" and i.value != "U" and i.value != "D" and i.value != "D'":
                return "NV"

        if self.gatetype == "AND":
            val = "1"

            for i in self.interms:
                if i.value == "U":
                    u_inp = 1
                if i.value == "D":
                    d_inp = 1
                if i.value == "D'":
                    d_prime_inp = 1
                if i.value == "0":
                    val = "0"
                    self.value = str(val)
                    return str(val)
                elif u_inp == 1:
                    val = "U"
                elif d_inp == 1:
                    val = "D"
                elif d_prime_inp == 1:
                    val = "D'"

            self.value = str(val)
            return str(val)

        elif self.gatetype == "NAND":
            flag = "1"

            for i in self.interms:
                if i.value == "U":
                    u_inp = 1
                if i.value == "D":
                    d_inp = 1                
                if i.value == "D'":
                    d_prime_inp = 1
                if i.value == "0":
                    flag = "0"
                    val = str(1-int(flag))
                    
                    self.value = val
                    return val
                elif u_inp == 1:
                    flag = "U"

                elif d_inp == 1:
                    flag = "D'"     # inverse b/c NAND
                elif d_prime_inp == 1:
                    flag = "D"      # inverse b/c NAND
            if flag.isnumeric():
                val = str(1-int(flag))
            else:
                val = str(flag)

            self.value = str(val)
            return str(val)

        elif self.gatetype == "OR":
            val = "0"
            
            for i in self.interms:                
                if i.value == "U":
                    u_inp = 1
                if i.value == "D":
                    d_inp = 1
                if i.value == "D'":
                    d_prime_inp = 1
                if i.value == '1':
                    val = "1"
                    
                    self.value = val
                    return val
                elif u_inp == 1:
                    val = "U"
                elif d_inp == 1:
                    val = "D"
                elif d_prime_inp == 1:
                    val = "D'"

            self.value = val
            return val

        elif self.gatetype == "NOR":
            flag = "0"

            for i in self.interms:
                if i.value == "U":
                    u_inp = 1
                if i.value == "D":
                    d_inp = 1
                if i.value == "D'":
                    d_prime_inp = 1
                if i.value == "1":
                    flag = "1"

                    val = str(1-int(flag))
                    self.value = val
                    return val
                elif u_inp == 1:
                    flag = "U"
                elif d_inp == 1:
                    flag = "D'"         # inverse b/c NOR
                elif d_prime_inp == 1:
                    flag = "D"          # inverse b/c NOR
            
            if flag.isnumeric():
                val = str(1-int(flag))
            else:
                val = str(flag)

            self.value = str(val)
            return str(val)

        elif self.gatetype == "NOT":
            val = str(self.interms[0].value)

            if val.isnumeric():
                val = str(1-int(val))
            elif val == "D":
                val = "D'"
            elif val == "D'":
                val = "D"
            else:
                val = "U"

            self.value = str(val)
            return str(val)

        elif self.gatetype == "XOR":
            newVal = "NULL"

            for i in self.interms:
                oldVal = str(newVal)
                newVal = str(i.value)

                if oldVal != "NULL":
                    if oldVal == "0":
                        newVal = newVal     # XOR w/ 0 (oldVal) outputs the other inputs (newVal) value 

                    elif oldVal == "1":
                        if newVal == "0":
                            newVal = "1"
                        elif newVal == "1":
                            newVal = "0"
                        elif newVal == "U":
                            newVal = "U"
                        elif newVal == "D":
                            newVal = "D'"
                        elif newVal == "D;":
                            newVal = "D"
                        else:
                            print("XOR error 1")

                    elif oldVal == "D":
                        if newVal == "0":
                            newVal = "D"
                        elif newVal == "1":
                            newVal = "D'"
                        elif newVal == "U":
                            print("XOR(D, U) not possible")
                        elif newVal == "D":
                            newVal = "0"
                        elif newVal == "D'":
                            newVal = "1"
                        else:
                            print("XOR error 2")

                    elif oldVal == "D'":
                        if newVal == "0":
                            newVal = "D'"
                        elif newVal == "1":
                            newVal = "D"
                        elif newVal == "U":
                            print("XOR(D', U) not possible")
                        elif newVal == "D":
                            newVal = "1"
                        elif newVal == "D'":
                            newVal = "0"
                        else:
                            print("XOR error 3")

                    elif oldVal == "U":
                        if newVal == "D":
                            print("XOR(U, D) not possible")
                        elif newVal == "D'":
                            print("XOR(U, D') not possible")
                        else:
                            newVal = "U"

            self.value = newVal
            return newVal
            
        elif self.gatetype == "XNOR":
            newVal = "NULL"

            for i in self.interms:
                oldVal = newVal
                newVal = i.value

                if oldVal != "NULL":
                    if oldVal == "0":
                        newVal = newVal     # XOR w/ 0 (oldVal) outputs the other inputs (newVal) value 

                    elif oldVal == "1":
                        if newVal == "0":
                            newVal = "1"
                        elif newVal == "1":
                            newVal = "0"
                        elif newVal == "U":
                            newVal = "U"
                        elif newVal == "D":
                            newVal = "D'"
                        elif newVal == "D;":
                            newVal = "D"
                        else:
                            print("XNOR error 1")

                    elif oldVal == "D":
                        if newVal == "0":
                            newVal = "D"
                        elif newVal == "1":
                            newVal = "D'"
                        elif newVal == "U":
                            print("XNOR(D, U) not possible")
                        elif newVal == "D":
                            newVal = "0"
                        elif newVal == "D'":
                            newVal = "1"
                        else:
                            print("XNOR error 2")

                    elif oldVal == "D'":
                        if newVal == "0":
                            newVal = "D'"
                        elif newVal == "1":
                            newVal = "D"
                        elif newVal == "U":
                            print("XNOR(D', U) not possible")
                        elif newVal == "D":
                            newVal = "1"
                        elif newVal == "D'":
                            newVal = "0"
                        else:
                            print("XNOR error 3")

                    elif oldVal == "U":
                        if newVal == "D":
                            print("XNOR(U, D) not possible")
                        elif newVal == "D'":
                            print("XNOR(U, D') not possible")
                        else:
                            newVal = "U"

            if newVal == "0":         # invert the outputs here
                newVal = "1"
            elif newVal == "1":
                newVal = "0"
            elif newVal == "D":
                newVal = "D'"
            elif newVal == "D'":
                newVal = "D"
            elif newVal == "U":
                newVal = "U"
            else:
                print("INVALID INPUT XNOR")

            self.value = newVal
            return newVal

        elif self.gatetype == "BUFF":
            val = self.interms[0].value

            self.value = val
            return val



# Take a line from the circuit file which represents a gatetype operation and returns a node that stores the gatetype

def parse_gate(rawline):
    # example rawline is: a' = NAND(b', 256, c')
    # should return: node_name = a',  node_gatetype = NAND,  node_innames = [b', 256, c']

    # get rid of all spaces
    line = rawline.replace(" ", "")
    # now line = a'=NAND(b',256,c')

    name_end_idx = line.find("=")
    node_name = line[0:name_end_idx]
    # now node_name = a'

    gt_start_idx = line.find("=") + 1
    gt_end_idx = line.find("(")
    node_gatetype = line[gt_start_idx:gt_end_idx]
    # now node_gatetype = NAND

    # get the string of interms between ( ) to build tp_list
    interm_start_idx = line.find("(") + 1
    end_position = line.find(")")
    temp_str = line[interm_start_idx:end_position]
    tp_list = temp_str.split(",")
    # now tp_list = [b', 256, c]

    node_innames = [i for i in tp_list]
    # now node_innames = [b', 256, c]

    return node_name, node_gatetype, node_innames


# Create circuit node list from input file
def construct_nodelist():
    o_name_list = []

    for line in input_file_values:
        if line == "\n":
            continue

        if line.startswith("#"):
            continue

        if line.startswith("INPUT"):
            index = line.find(")")
            name = str(line[6:index])
            n = Node(name, "U", "PI", [])
            n.is_input = True
            node_list.append(n)


        elif line.startswith("OUTPUT"):
            index = line.find(")")
            name = line[7:index]
            o_name_list.append(name)


        else:   # majority of internal gates processed here
            node_name, node_gatetype, node_innames = parse_gate(line)
            n = Node(node_name, "U", node_gatetype, node_innames)
            node_list.append(n)

    # now mark all the gates that are output as is_output
    for n in node_list:
        if n.name in o_name_list:
            n.is_output = True

    # link the interm nodes from parsing the list of node names (string)
    # example: a = AND (b, c, d)
    # thus a.innames = [b, c, d]
    # node = a, want to search the entire node_list for b, c, d
    for node in node_list:
        for cur_name in node.innames:
            for target_node in node_list:
                if target_node.name == cur_name:
                    node.interms.append(target_node)

    return 

# Main function starts
# Step 1: get circuit file name from command line
wantToInputCircuitFile = str(
    input(chalk.green("Provide a benchfile name (return to accept circuit.bench by default):\n")))

if len(wantToInputCircuitFile) != 0:
    circuitFile = wantToInputCircuitFile
    try:
        f = open(circuitFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting circuit file to default')
        circuitFile = "circuit.bench"
else:
    circuitFile = "circuit.bench"

print("\n---------------")

# Constructing the circuit netlist
file1 = open(circuitFile, "r")
input_file_values = file1.readlines()
file1.close()
node_list = []
construct_nodelist()
# printing list of constructed nodes
for n in node_list:
    n.display()

print("---------------")

while True:

    # makes the list of input names and their respective values
    input_list = [i.name for i in node_list if i.is_input and i.name != "0" and i.name != "1" and i.name != "U"]
    input_val = [i.value for i in node_list if i.is_input and i.name != "0" and i.name != "1" and i.name != "U"]

    listlen = len(input_list)

    print(chalk.green("\nSimulation - provide a " + str(listlen) +  "-bit vector for input nodes "), end="")
    print(chalk.green_bright(*input_list), end = "")
    print(chalk.green(" (return to exit):"))

    line_of_val = input()

    u_input = 0
    fault_node = "none"

    for i in line_of_val:
        if i == "U":
            u_input = 1

    if u_input != 1:
        fault_node = input(chalk.green("Which node should be faulty? (Type 'none' for no faults):\n"))

        if(fault_node.lower() != "none"):
            fault_num = input(chalk.green("Stuck at 0 or 1?\n"))
            print("\n--- With the following fault: " + str(fault_node) + "-SA-" + str(fault_num) + " ---\n")
    
    if len(line_of_val)==0:
        break

    # Clear all nodes values to U in between simulation runs
    for node in node_list:
        node.set_value("U")

    strindex = 0

    # Set value of input node
    for node in node_list:
        if node.is_input:
            if strindex > len(line_of_val)-1:
                break
            node.set_value(line_of_val[strindex])
            strindex = strindex + 1

    print("simulating with the following input values:")

    for node in node_list:
        if node.is_input:
            node.display()
    
    print("--- Begin simulation: ---")

    # simulation by trying calculating each node's value in the list
    updated_count = 1       #initialize to 1 to enter while loop at least once
    iteration = 0
    while updated_count > 0:
        updated_count = 0
        iteration += 1
        for n in node_list:
            if n.name == fault_node:
                if fault_num == "1":
                    n.value = "D'"
                else:
                    n.value = "D"

            if n.value == "U":
                n.calculate_value()
                if n.value == "0" or n.value == "1":
                    updated_count +=1
            n.display()
        print (f'--- iteration {iteration} finished: updated {updated_count} values--- ')

    input_list = [i.name for i in node_list if i.is_input and i.name != "0" and i.name != "1" and i.name != "U"]
    input_val = [i.value for i in node_list if i.is_input and i.name != "0" and i.name != "1" and i.name != "U"]

    print(chalk.cyan("\n--- Simulation results: ---"))

    print("input: \t", end="")

    print(*input_list, end = "")
    print("\t = \t", end = "")
    print(*input_val)
    print("")

    output_list = [i.name for i in node_list if i.is_output]
    output_val = [i.value for i in node_list if i.is_output]

    print("output:\t", end="")
    print(*output_list, end = "")
    print("\t = \t", end = "")
    print(*output_val)
    print("\n")

    if fault_node.lower() != "none":
        d_prop = 0
        d_prop_nodes = []
        d_prop_val = []
        j = 1

        for i in node_list:
            if (i.value == "D" and i.is_output) or (i.value == "D'" and i.is_output):
                d_prop = 1
                d_prop_nodes.append(str(i.name))
                d_prop_val.append(str(i.value))

        if d_prop == 1:
            print(chalk.magenta("Fault " + fault_node + "-SA-" + fault_num + " detected with input " + line_of_val + ", at output nodes:"), end=" ")

            for i in range(len(d_prop_nodes)):
                if len(d_prop_nodes) > 1:
                    print(d_prop_nodes[i] + " = " + d_prop_val[i], end= ", ")
                else:
                    print(d_prop_nodes[i] + " = " + d_prop_val[i])
        else:
            print(chalk.magenta("Fault " + fault_node + "-SA-" + fault_num + " undetected with input " + line_of_val + "\n\n"))
    print("\n")
print("Finished - bye!")