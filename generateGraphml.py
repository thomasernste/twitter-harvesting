import sqlite3, json

conn = sqlite3.connect("./rettiwt.db")
curse = conn.cursor()
base = curse.execute("select uid, following, followers, targetinfo from gotcha")
dupedges = set([])
dupnodes = set([])
nodes = ""
edges = ""
edgeID = ""
for user in base:
    uid = user[0];
    name = json.loads(user[3])[0]["screen_name"]
    if(str(uid) in dupnodes):
        print "argh"
    nodes += "<node id=\""+uid+"\"><data key=\"name\">"+name+"</data></node>\n"
    dupnodes.add(str(uid))
    
base = curse.execute("select uid, following, followers, targetinfo from gotcha")
for user in base:
    uid = user[0];
    following = json.loads(user[1])
    followers = json.loads(user[2])
    for toid in following:
        edgeID = str(uid)+"."+str(toid)
        if(edgeID not in dupedges):
            edges += "<edge  source=\""+str(uid)+"\" target=\""+str(toid)+"\"/>\n" #id=\"e"+edgeID+"\"
            dupedges.add(edgeID)
            if(str(toid) not in dupnodes):
                nodes += "<node id=\""+str(toid)+"\"/>\n"
                dupnodes.add(str(toid))
    for fromid in followers:
        edgeID = str(fromid)+"."+str(uid)
        if(edgeID not in dupedges):
            edges += "<edge  source=\""+str(fromid)+"\" target=\""+str(uid)+"\"/>\n" #id=\"e"+edgeID+"\"
            dupedges.add(edgeID)
            if(str(fromid) not in dupnodes):
                nodes += "<node id=\""+str(fromid)+"\"/>\n"
                dupnodes.add(str(fromid))
        
graphml = "<graphml edgedefault=\"directed\">\n  <key id=\"name\" for=\"edge\" attr.name=\"name\" attr.type=\"string\"/> <graph edgedefault=\"directed\">\n" + nodes + edges + "</graph>\n</graphml>";
print graphml