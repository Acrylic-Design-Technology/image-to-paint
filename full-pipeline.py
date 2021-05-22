import math
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces

# Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
# how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
gcode_compiler = Compiler(interfaces.Gcode, movement_speed=5000, cutting_speed=1500, pass_depth=0)

curves = parse_file('C:/Users/12269/Documents/GitHub/image-to-paint/lauren3_OUTPUT_63.svg') # Parse an svg file into geometric curves

gcode_compiler.append_curves(curves) 
gcode_compiler.compile_to_file('C:/Users/12269/Documents/GitHub/image-to-paint/lauren3_OUTPUT_63.gcode', passes=1)

file_name = 'C:/Users/12269/Documents/GitHub/image-to-paint/lauren3_OUTPUT_63.gcode'  # put your filename here
paintbrush_len = 20 # paintbrush len in cm
angle = 45 # angle of paintbrush to page

with open(file_name, 'r+') as f:
    new_code = ""
    coordinates = []
    content = f.readlines()

    for line in content:
        if 'G1' in line:
            gcode = line.strip('\n')
            gcode = gcode.replace(';','')
            coordinate_set = {}
            for num in gcode.split()[1:]:
                if len(num) > 1:
                    coordinate_set[num[:1]] = float(num[1:])
            coordinates.append(coordinate_set)

    i = 0
    for line in content:
        if 'G1' in line:
            gcode = line.strip('\n')
            if i < len(coordinates) - 1:
                gcode = line.replace('\n','')
                gcode = gcode.replace(';','')
                x_0 = coordinates[i].get('X')
                y_0 = coordinates[i].get('Y')
                x_1 = coordinates[i+1].get('X')
                y_1 = coordinates[i+1].get('Y')
                i = i + 1
                if x_1 - x_0 == 0:
                    pz = 0
                else:
                    pz = math.atan((y_1-y_0)/(x_1-x_0)) * 156.75
                new_code += gcode + ' Z' + str(pz) + ';' + '\n'
            else:
                new_code += gcode + '\n'
            
        else:
            gcode = line.strip('\n')
            new_code += gcode + '\n'

    print(new_code)
    f.seek(0)
    f.write(new_code)