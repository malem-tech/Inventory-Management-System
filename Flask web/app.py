data = {
    'a'=10,
    'b'=20
}

count = sum(1 for key, value in data.items() if value is None)
print(count)

count = 0
for key, value in data.item():
    if value is None:
        count += 1

print(count)

In dictionary key: int, sum all values.
Find average of values.
Return key with maximum value.


average = sum(data.values()) /len (data)

max_key = None
max_val = None

for key, value in data.items():
    if max_val is None or value > max_value:
        max_value = value
        max_key = key

print(max_key)
