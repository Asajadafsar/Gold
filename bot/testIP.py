import geocoder

g = geocoder.ip('me') 

print(f"IP Address: {g.ip}")
print(f"Country: {g.country}")
print(f"Location: {g.city}, {g.state}, {g.country}")
