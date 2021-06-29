import math
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode import TOLERANCES
TOLERANCES['approximation'] = 0.9

# Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
# how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
'''
gcode_compiler = Compiler(interfaces.Gcode, movement_speed=5000, cutting_speed=1500, pass_depth=0)

curves = parse_file('C:/Users/12269/Documents/GitHub/image-to-paint/star_manual.svg') # Parse an svg file into geometric curves

gcode_compiler.append_curves(curves) 
gcode_compiler.compile_to_file('C:/Users/12269/Documents/GitHub/image-to-paint/star_manual.gcode', passes=1)
'''

file_name = 'C:/Users/12269/Documents/GitHub/image-to-paint/hype.gcode'  # put your filename here
# paintbrush_len = 146 # paintbrush len in mm
# angle = 45 # angle of paintbrush to page

offset_len = 84.175  # hardcoded variable calc for above 2

with open(file_name, 'r+') as f:
    new_code = ""
    coordinates = []
    content = f.readlines()

    for line in content:
        if 'G1' in line:
            # retrieve all XY pairs from GCode for manipulation
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

                # parameters to calculate angle of each brush stroke
                x_0 = coordinates[i].get('X')
                y_0 = coordinates[i].get('Y')
                x_1 = coordinates[i+1].get('X')
                y_1 = coordinates[i+1].get('Y')
                i = i + 1
                
                if (x_1 != x_0):
                    base_angle = math.atan(abs((y_1-y_0))/abs((x_1-x_0)))
                # 4 edge cases (straight lines) and 4 quadrant calculations
                if (x_1 == x_0) & (y_1 < y_0):
                    pz = 0
                elif (x_1 == x_0) & (y_1 > y_0):
                    pz = math.pi * offset_len
                elif (y_1 == y_0) & (x_1 < x_0):
                    pz = (math.pi / 2) * offset_len
                elif (y_1 == y_0) & (x_1 > x_0):
                    pz = ((3 * math.pi) / 2) * offset_len
                elif (x_1 > x_0) & (y_1 > y_0): # general angle calc q1
                    pz = (((3 * math.pi) / 2) - base_angle) * offset_len
                elif (x_1 < x_0) & (y_1 > y_0): # general angle calc q2
                    pz = ((math.pi / 2) + base_angle) * offset_len
                elif (x_1 < x_0) & (y_1 < y_0): # general angle calc q3
                    pz = ((math.pi / 2) - base_angle) * offset_len
                else: # general angle calc q4
                    pz = (((3 * math.pi) / 2) + base_angle) * offset_len
                
                # 4 straight lines and then 4 quadrant movement
                if (x_1 == x_0) & (y_1 > y_0):
                    y_0 += offset_len
                    y_1 +=  offset_len
                elif (x_1 == x_0) & (y_1 < y_0):
                    y_0 -= offset_len
                    y_1 -=  offset_len
                elif (y_1 == y_0) & (x_1 > x_0):
                    x_0 += offset_len
                    x_1 += offset_len
                elif (y_1 == y_0) & (x_1 < x_0):
                    x_0 -= offset_len
                    x_1 -= offset_len
                elif (x_1 > x_0) & (y_1 > y_0): # general offset calc q1
                    x_0 += math.cos(base_angle) * offset_len
                    x_1 += math.cos(base_angle) * offset_len
                    y_0 += math.sin(base_angle) * offset_len
                    y_1 += math.sin(base_angle) * offset_len
                elif (x_1 < x_0) & (y_1 > y_0): # general offset calc q2
                    x_0 -= math.cos(base_angle) * offset_len
                    x_1 -= math.cos(base_angle) * offset_len
                    y_0 += math.sin(base_angle) * offset_len
                    y_1 += math.sin(base_angle) * offset_len
                elif (x_1 < x_0) & (y_1 < y_0): # general offset calc q3
                    x_0 -= math.cos(base_angle) * offset_len
                    x_1 -= math.cos(base_angle) * offset_len
                    y_0 -= math.sin(base_angle) * offset_len
                    y_1 -= math.sin(base_angle) * offset_len
                else: # general offset calc q4
                    x_0 += math.cos(base_angle) * offset_len
                    x_1 += math.cos(base_angle) * offset_len
                    y_0 -= math.sin(base_angle) * offset_len
                    y_1 -= math.sin(base_angle) * offset_len

                # Add Gcode to new file
                # new_code += gcode + ' Z' + str(pz) + ';' + '\n'
                new_code += 'G1 F6500' + ' X' + str(round(x_0, 5)) + ' Y' + str(round(y_0, 5)) + ';' + '\n'
                new_code += 'G1 F6500' + ' A' + str(pz) + ';' + '\n'
                new_code += 'G1 F250' + ' Z' + '10' + ';' + '\n'
                new_code += 'G1 F6500' + ' X' + str(round(x_1, 5)) + ' Y' + str(round(y_1, 5)) + ';' + '\n'
                new_code += 'G1 F250' + ' Z' + '0' + ';' + '\n' + '\n'
            else:
                print("done")
            
        else:
            gcode = line.strip('\n')
            new_code += gcode + '\n'

    # write Gcode to new file
    print(new_code)
    f.seek(0)
    f.write(new_code)