## Name: Shreshth Nawander 
## EQ Works Data Role

import pandas as pd
import math
import matplotlib.pyplot as plt
## ------------------------------------------------------------------------------------
## 1) Cleanup 

data1 = "DataSample.csv"
subset_lst1 = [' TimeSt', 'Latitude', 'Longitude']
# the Columns that are the parameters whose contents need to be cleaned, 
# if they're duplicates

def clean_data(csv_file, subset_lst):
    df = pd.read_csv(csv_file)
    cleaned_df = (df[~df.duplicated(subset = subset_lst)]) # selecting the inverse of the subset
                                                           # that has all duplicates
    return cleaned_df

data_df = clean_data(data1, subset_lst1) #cleaned data
print("1) Cleaned Data:")
print(data_df)
print("##############################################################################")

## ------------------------------------------------------------------------------------
## 2) Label

data2 = "POIList.csv"
subset_lst2 = [' Latitude', 'Longitude']
groups_df = clean_data(data2, subset_lst2) # cleaned dataset since POI2 = POI1
groups_long = groups_df['Longitude']
groups_lat = groups_df[' Latitude']

def make_distances(df,Longitudes, Latitudes): #returns a list containing all distances of each request
    zipped_lst = zip(Longitudes, Latitudes)
    distances = []
    for (item1, item2) in zipped_lst:
        distance = math.sqrt((item1)**2 + (item2)**2) #used pythagorean's theorem to calculate distance
        distances.append(distance)
    df['Distance'] = distances
    return df


distance_df = (make_distances(groups_df, groups_long, groups_lat))
distance_series = distance_df['Distance']
data_long = data_df['Longitude']
data_lat = data_df['Latitude']
updated_data_df = make_distances(data_df, data_long, data_lat)

# from POIList.csv, we now have seperated data for the distance of each POI
POI1 = distance_series[0]
POI3 = distance_series[2]
POI4 = distance_series[3]


# categorize(df) essentially assigns each request one of three values: POI1, POI2, POI3
# depending on which it is closest to. (smallest distance)
def categorize(df):
    df_dist_series = df['Distance']
    df_dist_list = [];
    for elem in df_dist_series:
        first = abs(POI1 - elem)
        second = abs(POI3 - elem)
        third = abs(POI4 - elem)
        dist_lst = [first, second, third]
        min_val = min(dist_lst)
        if min_val == first:
            df_dist_list.append('POI1')
        elif min_val == second:
            df_dist_list.append('POI3')
        else: 
            df_dist_list.append('POI4')
    return df_dist_list

dist_lst = categorize(updated_data_df)
cleaned_data = clean_data(data1, subset_lst1)
cleaned_data['POI'] = dist_lst

# following line gives the required info: 
print("\n2) Labeled Data:")
print(cleaned_data)
print("##############################################################################")
## ------------------------------------------------------------------------------------
## 3a) Analysis

df_distances = categorize(updated_data_df)
updated_data_df['POI'] = df_distances

# seperating the data into three sub-dataframes that have their assigned POI values
POI1_df = updated_data_df[updated_data_df.values  == 'POI1']
POI3_df = updated_data_df[updated_data_df.values  == 'POI3']
POI4_df = updated_data_df[updated_data_df.values  == 'POI4']

# returns the mean, standard deviation, and a list of the values that contain the difference
# between the distance of the POI and each of its request.
def avg_dist(POI_df, POI_val):
    my_lst = []
    for dist in POI_df['Distance']:
        difference = abs(POI_val - dist)
        my_lst.append(difference)
    pop_size = len(my_lst)
    mean = (sum(my_lst) / pop_size)
    summation = 0
    for dist in POI_df['Distance']: 
        summation += (dist - mean)**2
    sd = math.sqrt(summation/pop_size) #sd is the standard deviation
    return [mean, sd, my_lst]; # returns list containing the three elements as stated above

POI1_mean_sd = avg_dist(POI1_df, POI1)
POI3_mean_sd = avg_dist(POI3_df, POI3)
POI4_mean_sd = avg_dist(POI4_df, POI4)

POI1_mean = POI1_mean_sd[0]
POI3_mean = POI3_mean_sd[0]
POI4_mean = POI4_mean_sd[0]

POI1_sd = POI1_mean_sd[1]
POI3_sd = POI3_mean_sd[1]
POI4_sd = POI4_mean_sd[1]

print("3) i) \n")
print("The average and standard deviation of the distance between POI1 to each of its assigned requests is: ")
print("  Average Distance: " + str(POI1_mean))
print("  Standard Deviation: " + str(POI1_sd) + "\n")

print("The average and standard deviation of the distance between POI3 to each of its assigned requests is: ")
print("  Average Distance: " + str(POI3_mean))
print("  Standard Deviation: " + str(POI3_sd) + "\n")

print("The average and standard deviation of the distance between POI4 to each of its assigned requests is: ")
print("  Average Distance: " + str(POI4_mean))
print("  Standard Deviation: " + str(POI4_sd) + "\n")
print("##############################################################################")
# ------------------------------------------------------------------------------------
# 3b) Analysis - Circle

# finds the radius given the dataframe, the difference list, and a string which contains the name of the POI
def get_radius(df, diff_lst, group_num):
    # the point with the greatest distance from the POI (the greatest value of the diff_lst)
    # is the one that will be on the circumfrence of the circle. Therefore, it will be the radius of the circle
    max_val = max(diff_lst)
    index_max_val = diff_lst.index(max_val)    
    outer = df.iloc[index_max_val]
    outer_latitude = outer['Latitude']
    outer_longitude = outer['Longitude']
    POI_latitude = (groups_df.loc[group_num][' Latitude'])
    POI_longitude = (groups_df.loc[group_num]['Longitude'])

    # using the distance formula to calculate the distance between two points: The outter-most request, and the coordinates
    # of the POI
    radius = math.sqrt(((outer_latitude - POI_latitude) ** 2) + ((outer_longitude - POI_longitude) ** 2))
    return radius

# getting the radius of each POI's circle, and its density:
POI1_df = updated_data_df[updated_data_df.values  == 'POI1']
POI1_diff_lst = POI1_mean_sd[2]
POI1_radius = get_radius(POI1_df, POI1_diff_lst, 0)
POI1_denisty = POI1_radius/(math.pi * (POI1_radius**2))

POI3_df =  updated_data_df[updated_data_df.values  == 'POI3']
POI3_diff_lst = POI3_mean_sd[2]
POI3_radius = get_radius(POI3_df, POI3_diff_lst, 2)
POI3_denisty = POI3_radius/(math.pi * (POI3_radius**2))

POI4_df = updated_data_df[updated_data_df.values  == 'POI4']
POI4_diff_lst = POI4_mean_sd[2]
POI4_radius = get_radius(POI4_df, POI4_diff_lst, 3)
POI4_denisty = POI4_radius/(math.pi * (POI4_radius**2))

print("3) ii) \n")
print("POI1:")
print("  Radius: " + str(POI1_radius))
print("  Density: " + str(POI1_denisty))

print("POI3:")
print("  Radius: " + str(POI3_radius))
print("  Density: " + str(POI3_denisty))

print("POI4:")
print("  Radius: " + str(POI4_radius))
print("  Density: " + str(POI4_denisty))

# these coordinates will be the center of the circle, latitude being the "x" and longitude being the "y"
POI1_latitude = (groups_df.loc[0][' Latitude'])
POI3_latitude = (groups_df.loc[2][' Latitude'])
POI4_latitude = (groups_df.loc[3][' Latitude'])

POI1_longitude = (groups_df.loc[0]['Longitude'])
POI3_longitude = (groups_df.loc[2]['Longitude'])
POI4_longitude = (groups_df.loc[3]['Longitude'])

# creating each cricle
circle1 = plt.Circle((POI1_latitude, POI1_latitude), POI1_radius, alpha = 0.5, color = 'r')
circle3 = plt.Circle((POI3_latitude, POI3_latitude), POI3_radius, alpha = 0.5, color = 'b')
circle4 = plt.Circle((POI4_latitude, POI4_latitude), POI4_radius, alpha = 0.5, color='g')
circles = [circle1, circle3, circle4]

# plotting the circles
fig, ax = plt.subplots()
plt.xlim(-75,200)
plt.ylim(-75,200)
plt.grid(linestyle='--')
ax.set_aspect(1)
ax.add_artist(circle1)
ax.add_artist(circle3)
ax.add_artist(circle4)
ax.legend(circles, ['POI1', 'POI3', 'POI4'])
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Circles')
plt.show()


# ------------------------------------------------------------------------------------
# 4 a) i) Model

# The following Model maps the popularity of each POI ranging from a scale of -10 to 10
#   where -10 is the least popular and 10 is the most popular

# The intuition behind the "popularity" of a POI can be related with its density

# Step 1:
# Given the radius of the POI, divide the radius into 20 intervals of equal length

# Step 2:
# The popularity rating of each request in the POI can be assigned as follows:
#   The firt interval [0, radius/20) has a rating of 10
#   The second interval [radius/20, 2*radius/20) has a rating of 9
#   The third interval [2*radius/20, 3*radius/20) has a rating of 8
#   ...The twentieth interval [19*radius/20, radius] has a rating of -10

# Step 3:
# The popularity rating of each request in the POI can be assigned as follows:
#   The firt interval [0, radius/20) has a rating of 10
#   The second interval [radius/20, 2*radius/20) has a rating of 9
#   The third interval [2*radius/20, 3*radius/20) has a rating of 8
#   ...The twentieth interval [19*radius/20, radius] has a rating of -10

# Step 4:
# Find the mean popularity rating of all the requests. This is the popularity rating
#   of the POI
# Round the popularity rating to the nearest whole number.


def popularity(POI_df, radius, diff_lst):
    interval_length = radius/21
    intervals = []
    for i in range(0,22):
        val = i * interval_length
        intervals.append(val) # dividing the radius into 20 equal intervals
    rating = 10
    
    rated_dict = {}
    for i in range(21):
        c_int = [intervals[i] , intervals[i + 1], 0]
        rated_dict.update({rating : c_int}) 
        #created a dictionary witch the key as a rating between -10 to 10, and its corresponding value
        #being the interval that it matches with. The value is a list, with its third element correspoinding
        #to the number of requests that are within the interval defined
        rating -= 1

    interval_lsts = rated_dict.values() #get a list of all values of the rated_dict
    total = 0
    pop_size = len(diff_lst) #the number of requests we're dealing with
    
    for dist in diff_lst:
        if dist == radius: #if the request's distance is exactly the length of the radius of the circle
            total += -10 #then we give it a rating of -10
        else:
            for val in interval_lsts: #providing rating of all other points within the circle
                first = val[0]
                second = val[1]
                if (dist >= first) and (dist < second):
                    my_key = list(rated_dict.keys())[list(rated_dict.values()).index(val)]
                    total += my_key
                    val[2] += 1 #updating the total number of requests that fall in that interval

    final_rating = round(total/float(pop_size)) 
    # the final POI rating is the average of the sum of all ratings, divided by the population size.
    # we then round the rating to the nearest whole number
    for i in range(-10, 11):
        vals = rated_dict[i]
        count_val = vals[2]
        rated_dict.update({i : count_val})

        # we dont require the dictionary to contain the interval anymore, only the number of requests associated
        # with each rating

    return [rated_dict, final_rating] # return a list containing the dictionary, which is our data
    # and the final_rating correspdonign with the POI

def show_POI_plot(histdata, name): #creates a bar-plot, similar to a histogram to 
                                   # show the distribution of ratings vs numbeer of requests
    
    histx = histdata.keys()
    histy = histdata.values()
    plt.scatter(histx,histy, s = 75)
    plt.xticks(histx)
    plt.xlabel("Popoularity")
    plt.ylabel("Number of Requests")
    plt.title(name)
    plt.show()

def show_pie_plot(histdata, name): # creates a Pie-chart to show the distribution of requests
                                   # of each rating
    requests = histdata.values()
    ratings = histdata.keys()
    this = 21 * [0.15]
    figureObject, axesObject = plt.subplots()
    axesObject.pie(requests,
        explode = this,
        labels=ratings, 
        autopct='%.2f', 

        startangle=0,
        
        )
    axesObject.axis('equal')
    plt.title(name)
    plt.show()


#extracting each POI's dictionary or "histogram data" and its final rating

POI1_popularity_histdata = popularity(POI1_df, POI1_radius, POI1_diff_lst)
POI1_histdata = POI1_popularity_histdata[0]
POI1_popularity = POI1_popularity_histdata[1]

POI3_popularity_histdata = popularity(POI3_df, POI3_radius, POI3_diff_lst)
POI3_histdata = POI3_popularity_histdata[0]
POI3_popularity = POI3_popularity_histdata[1]

POI4_popularity_histdata = popularity(POI4_df, POI4_radius, POI4_diff_lst)
POI4_histdata = POI4_popularity_histdata[0]
POI4_popularity = POI4_popularity_histdata[1]

print("\nUsing the described model, the popularity of POI1 is: " + str(POI1_popularity))
print("Using the described model, the popularity of POI3 is: " + str(POI3_popularity))
print("Using the described model, the popularity of POI4 is: " + str(POI4_popularity))

show_POI_plot(POI1_histdata, "POI1 visualization: populartiy of requests")
show_pie_plot(POI1_histdata, "POI1 Pie Chart Distribution")

show_POI_plot(POI3_histdata, "POI3 visualization: populartiy of requests")
show_pie_plot(POI3_histdata, "POI3 Pie Chart Distribution")

show_POI_plot(POI4_histdata, "POI4 visualization: populartiy of requests")
show_pie_plot(POI4_histdata, "POI4 Pie Chart Distribution")
























