line = "-0.40,1.26,9.63,-0.03,-0.02,-0.02"
print(type(line))
# Step 1: Split the string by comma
a = line.split(',')
b = [float(i) for i in a]
print(b)