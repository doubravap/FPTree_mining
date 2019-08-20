#input the minimum support threshold for an itemset to be frequent
min_sup = int(input())

#input the dataset to be mined for frequent pattern and store each unique transaction within the dataset in a database
database = {}
while True:
    try:
        transaction = frozenset(input().split())
        #record the frequency of each transaction in the database
        database[transaction] = database.get(transaction, 0) + 1
    except EOFError:
        break

#The FPTree class which will be used to create the Frequent Pattern Growth Tree 
class FPTree:
    def __init__(self, node, count, parent):
        self.node = node
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None
        
    def increment(self, val):
        self.count += val


def print_FPTree(FPT, level):
    if FPT.node:
        print('\t' * level + FPT.node + ' ' + str(FPT.count))
        
    for child in FPT.children.values():
        print_FPTree(child, level+1)


def growFPTree(FPT, data, freq_items_dict, num_data):
    if data[0] in FPT.children:
        FPT.children[data[0]].increment(num_data)
    else:
        FPT.children[data[0]] = FPTree(data[0], num_data, FPT)
        
        if freq_items_dict[data[0]][1] == None:
            freq_items_dict[data[0]][1] = FPT.children[data[0]]
        else:
            FPTree_node =  freq_items_dict[data[0]][1]
            while FPTree_node.node_link != None:
                FPTree_node = FPTree_node.node_link
                
            FPTree_node.node_link = FPT.children[data[0]]
            
    if len(data) > 1:
        growFPTree(FPT.children[data[0]], data[1::], freq_items_dict, num_data)


def create_FPTree(database, min_support):
    freq_items = {}
    for data, count in database.items():
        for item in data:
            freq_items[item] = freq_items.get(item, 0) + count
            
    for item in list(freq_items):
        if freq_items[item] < min_support:
            del(freq_items[item])
        else:
            freq_items[item] = [freq_items[item], None]
            
    if not freq_items:
        return None, None
    
    FPT = FPTree({}, 1, None)
    
    for data, count in database.items():
        relevant_data = list(filter(lambda item: item in data, freq_items))
        
        #relevant_data.sort()
        relevant_data.sort(key=lambda item: freq_items[item][0], reverse=True)
        
        growFPTree(FPT, relevant_data, freq_items, count)
        
    return FPT, freq_items


def mine_FPTree(FPT, freq_items_dict, min_support, prev_itemset, freq_itemsets):
    #temp_freq_itemlist = sorted(freq_items_dict.items(), key=lambda item: item[0])
    #sorted_freq_itemlist = [sorted_item[0] for sorted_item in sorted(temp_freq_itemlist, key=lambda item: item[1][0], reverse=True)]
    
    for item in freq_items_dict:
        curr_itemset = prev_itemset.copy()
        curr_itemset.append(item)
        curr_itemset.sort()
            
        freq_itemsets.append((curr_itemset, freq_items_dict[item][0]))
        
        cond_database = {}
        
        FPTree_node = freq_items_dict[item][1]
        while FPTree_node != None:
            prefix_path = []
            
            prefix_node = FPTree_node.parent
            while prefix_node.parent != None:
                prefix_path.append(prefix_node.node)
                prefix_node = prefix_node.parent
                
            if prefix_path:
                cond_database[frozenset(prefix_path)] = FPTree_node.count
                
            FPTree_node = FPTree_node.node_link
            
        cond_FPT, cond_freq_items = create_FPTree(cond_database, min_support)
        
        if cond_freq_items:
            mine_FPTree(cond_FPT, cond_freq_items, min_support, curr_itemset, freq_itemsets)

FPT, freq_items_dict = create_FPTree(database, min_sup)

prev_itemset = []
freq_itemsets = []
mine_FPTree(FPT, freq_items_dict, min_sup, prev_itemset, freq_itemsets)

freq_itemsets.sort(key=lambda item: item[0][0])
freq_itemsets.sort(key=lambda item: item[1], reverse=True)

print(freq_itemsets)
