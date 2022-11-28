import requests
import vk_api
from KEY.key import API_KEY_FRIENDS
import json
import networkx as nx
import matplotlib.pyplot as plt

#1 level
USER_IDs1 = [185215592, 181948702, 154308430, 152087036, 143779216, 161594007, 472583599, 113001678, 183648122, 196404046, 85770676, 355133495, 137872152, 102711908, 126568936, 507184348, 458357505, 131765293, 323208790, 173792332, 343410069, 346034855, 255053910, 338686058, 312616596]  
USER_IDs2 = []
USER_IDs3 = []
g = nx.Graph()

#2 level
for USER_ID in USER_IDs1 :
    #avoid accounts without access to friend list 
    try:
        #get friends
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "user_id": USER_ID,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": API_KEY_FRIENDS,
            "v": 5.122
        }).json()["response"]["items"]
        USER_IDs2 += r
        #make edges
        for j in r:
            g.add_edge(USER_ID, j)
    except (KeyError):
        pass

#3 level
for USER_ID in USER_IDs2 :
    #avoid accounts without access to friend list
    try:
        #get friends
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "user_id": USER_ID,
            "order": "name",
            "count": 10000,
            "offset": 0,
           "access_token": API_KEY_FRIENDS,
            "v": 5.122
        }).json()["response"]["items"]
        USER_IDs3 += r
        #make edges
        for j in r:
            g.add_edge(USER_ID, j)
    except (KeyError):
        pass


#make edges for 3th row
for i in USER_IDs3:
    try:
        r = requests.get("https://api.vk.com/method/friends.get", params={
                "user_id": i,
                "order": "name",
                "count": 10000,
                "offset": 0,
                "access_token": API_KEY_FRIENDS,
                "v": 5.122
            }).json()["response"]["items"]
        for j in USER_IDs3:
            if j in r:
                g.add_edge(i, j)
    except ( KeyError):
        pass

#show info + graph
print(nx.info(g))
plt.figure(figsize =(15, 15))
nx.draw_networkx(g, with_labels = True)
plt.show()

count = 0
#closeness centrality
print("Winner of closeness centrality:")
close_centrality = nx.closeness_centrality(g)
#sort 
close_c = dict(sorted(close_centrality.items(), key=lambda item: item[1], reverse=True))
#get list of ids 
close_keys = list(close_c.keys())
#find top3 ids from our group
for i in close_keys:
    if i in USER_IDs1:
        r = requests.get("https://api.vk.com/method/users.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": API_KEY_FRIENDS,
            "v": 5.122
        }).json()["response"]
        print(r[0]["first_name"])
        print(r[0]["last_name"])
        count += 1
        if count > 2:
            break

count = 0
#betweenness centrality
print("Winner of betweenness centrality:")
bet_centrality = nx.betweenness_centrality(g, normalized = True, endpoints = False)
bet_c = dict(sorted(bet_centrality.items(), key=lambda item:item[1], reverse=True))
bet_keys = list(bet_c.keys())
for i in bet_keys:
    if i in USER_IDs1:
        r = requests.get("https://api.vk.com/method/users.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": API_KEY_FRIENDS,
            "v": 5.122
        }).json()["response"]
        print(r[0]["first_name"])
        print(r[0]["last_name"])
        count += 1
        if count > 2:
            break
    
count = 0
#eigenvector centrality
print("Winner of eigenvector centrality:")
pr = nx.pagerank(g, alpha = 0.8)
pr_sorted = dict(sorted(pr.items(), key=lambda item:item[1], reverse=True))
pr_keys = list(pr_sorted.keys())
for i in pr_keys:
    if i in USER_IDs1:
        r = requests.get("https://api.vk.com/method/users.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": API_KEY_FRIENDS,
            "v": 5.122
        }).json()["response"]
        print(r[0]["first_name"])
        print(r[0]["last_name"])
        count += 1
        if count > 2:
            break
