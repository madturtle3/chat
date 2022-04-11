import socklib

client = socklib.Client()
client.custom_parameters["Username"]= "boba"
client.send("H(*")
print(client.recv())