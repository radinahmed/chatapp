userconn={
  "k" : "wwwwww",
  "T": "dasdgcvv"
}

thisdict={
  "ru": "pppppw"
}
for key, value in userconn.items():
  if(key=="ru"):
    userconn["ru"]= thisdict["ru"]

if(userconn.get("ru")==None):
  userconn["ru"]= thisdict["ru"]

 

print(userconn)