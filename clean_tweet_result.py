# To Run: python3 clean_tweet_result.py 2010_10_14/tweet_result_0_.txt > '2010_10_14/tweet_result_0_cleaned.txt'

import sys

filename = sys.argv[1]

with open(filename) as f:
    l = f.readline()
    i = 0
    j = 0
    j_end = -1
    link_types = []
    links = []
    l_no = 0
    while(l):
        l_no += 1
        print(i, l_no, l, file=sys.stderr)
        if(j == 7):
            j_end = j + int(l.strip())

        if(j == j_end):
            if(j_end == 7):
                print(l.strip() + "\t", end = "")
                print("{}"+"\t"+"{}")
            else:
                # print(l.strip())
                l_split = l.strip().split()
                # print(len(l_split), file=sys.stderr)
                if(len(l_split) < 3):
                    link_types.append("-")
                    links.append("-")
                else:
                    link_types.append(l_split[1].replace(',', ''))
                    links.append(l_split[2].replace(',', ''))
                print("{", end = "")
                k = 0
                for link_type in link_types:
                    k += 1
                    if(k == len(link_types)):
                        print(link_type, end = "")
                    else: 
                        print(link_type + ",", end = "")
                print("}" + "\t", end = "")
                print("{", end = "")
                k = 0
                for link in links:
                    k += 1
                    if(k == len(links)):
                        print(link, end = "")
                    else: 
                        print(link + ",", end = "")
                print("}")
            i += 1
            j = -2
            j_end = -10 ** 10
            link_types = []
            links = []
            # print("test")
        else:
            if(j != -1):
                if (j > 7):
                    # print(l.strip())
                    l_split = l.strip().split()
                    # print(len(l_split), file=sys.stderr)
                    if(len(l_split) < 3):
                        link_types.append("-")
                        links.append("-")
                    else:
                        link_types.append(l_split[1].replace(',', ''))
                        links.append(l_split[2].replace(',', ''))
                elif (j == 2):
                    l_split = l.strip().split()
                    print(l_split[1] + "-" + l_split[2] + "-" + l_split[5] + "\t", end = "")
                    print(l_split[3] + "\t", end ="")
                elif (j == 5):
                    if(l.strip() == "-1"):
                        print("-1" + "\t", end = "")
                        print("-1" + "\t", end = "")
                    else:
                        print(l.strip().split()[0] + "\t", end = "")
                        print(l.strip().split()[1] + "\t", end = "")
                elif (j == 6):
                    print("{", end = "")
                    l_split = l.strip().split()
                    k = 0
                    for num in l_split:
                        k+=1
                        if(k<len(l_split)):
                            print(num, end = ",")
                        else:
                            print(num, end = "")
                    print("}" + "\t", end = "")
                else:
                    print(l.strip() + "\t", end = "")
            
        
        l = f.readline()
        j+=1
        # if (i == 1000000):
        #     break
        
        