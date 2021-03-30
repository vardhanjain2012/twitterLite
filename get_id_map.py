# To Run: python3 get_id_map.py > user_list_w_newid.txt
i = 0
with open("user_list.txt", "r") as f:
    l = f.readline().strip()
    while(l):
        print(i, l)
        l = f.readline().strip()
        i+=1