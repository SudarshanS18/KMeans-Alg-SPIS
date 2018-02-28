import csv

# input files and columns to filter
fileToBeCleaned = input("enter the name of the file to be cleaned: ")
latLocation = int(input("enter column of Latitude"))
longLocation = int(input("enter column of Longitude"))

# open the file as CSV
inp = open(fileToBeCleaned, 'r')
reader = csv.reader(inp)

# skip first line (header line)
next(reader)

# variable to store data in
data = []

#for each row
for row in reader:
    
    #if it is null
    if (((row[latLocation]) != "") or (row[longLocation] != "")):
        
        #if not out of bounds of the map of America
        if((float(row[latLocation]) > 24.005611) and (float(row[latLocation]) < 48.987386)):
            if((float(row[longLocation]) > -124.62608) and (float(row[longLocation]) < -62.361014)):
                #then and only then include the row
                data.append(row)
            else:
                print(row[latLocation], row[longLocation])
        else:
            print(row[latLocation], row[longLocation])
    else:
        print(row[latLocation], row[longLocation])
# if i dont include any row, im going to print it out so i can see what I'm
# not including.

# close the input file.
inp.close()


# open new file with write privileges and write the rows.
with open('new.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(data)
