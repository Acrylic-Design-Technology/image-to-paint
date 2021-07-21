import math

file_name = 'C:/Users/12269/Downloads/gcode/shark.gcode'  # put your filename here
# paintbrush_len = 146 # paintbrush len in mm
# angle = 45 # angle of paintbrush to page

scale_rate_x = 0.67777777777  # hardcoded variable calc for above 2
scale_rate_y = 0.77065767285

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
            if i < len(coordinates):
                gcode = line.replace('\n','')
                gcode = gcode.replace(';','')

                # parameters to calculate angle of each brush stroke
                x = (coordinates[i].get('X') * scale_rate_x)
                y = (coordinates[i].get('Y') * scale_rate_y)
                i = i + 1

                # Add Gcode to new file
                new_code += 'G1 X' + str(round(x, 1)) + ' Y' + str(round(y, 1)) + ';' + '\n'
            else:
                print("done")
            
        else:
            gcode = line.strip('\n')
            new_code += gcode + '\n'

    # write Gcode to new file
    print(new_code)
    f.seek(0)
    f.write(new_code)