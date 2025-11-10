with open("context_map.json", "rb") as f:
    data = f.read()

# Remove UTF-8 BOM if it exists
if data.startswith(b'\xef\xbb\xbf'):
    data = data[3:]

with open("context_map.json", "wb") as f:
    f.write(data)

print("Context map cleaned successfully.")
