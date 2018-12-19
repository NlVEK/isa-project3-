from pyspark import SparkContext
# assuming my input file has format like
#user_id item_id1, item_id2
sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/myinput_file.log", 2)     # each worker loads a piece of the data file

a = [1,2]

pairs = data.map(lambda line: line.split())   # tell each worker to split each line of it's partition
# pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id

def compact(pair):
    a = pair.split(',')
    a.sort()
    pointer = 1
    list_of_pairs = []
    # c = dict()
    for i in range(0, len(a)):
        for j in range(pointer, len(a)):
            list_of_pairs.append((a[i], a[j]))
        #     try :
        #         b = c[(a[i],a[j])]
        #     except KeyError:
        #         c[(a[i], a[j])] = 1
        #     else:
        #         c[(a[i], a[j])] = b + 1
        pointer += 1
    return (list_of_pairs)

item_coview = pairs.map(lambda pair: compact(pair[1]))
x = dict()
for i in item_coview.collect():
    if len(i)> 1:
        for all_pairs in i:
            try:
                if x[all_pairs]:
                    x[all_pairs] += 1
            except KeyError:
                x[all_pairs] = 1
    else:
        try:
            if x[i[0]]:
                x[i[0]] += 1
        except KeyError:
            x[i[0]] = 1
for key, value in x.items():
    print(key)
    print("\n")
    print(value)
    print("\n")

recommend = dict()
for key, value in x.items():
    if value >= 3:
        #add key and value to recommendation
        if key[0] in recommend.keys():
            recommend[key[0]] += key[1] #concat?
        else:
            recommend[key[0]] = key[1]
        if key[1] in recommend.keys():
            recommend[key[1]] += key[0] #concat?
        else:
            recommend[key[1]] = key[0]

for key, value in recommend.items():
    print("key: " + key)
    print("\t")
    print("value: " +value)
    print("\t")
# count = user__item.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
#                                                   # and then reduce all the values by adding them together
#
# output = count.collect()                          # bring the data back to the master node so we can print it out
# for page_id, count in output:
#     if count >= 3:
#         print ("userid %s count %d" % (page_id, count))
# print ("Popular items done")
# output = freq.collect()
# for everything in output:
#     print(ev