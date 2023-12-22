import json

result = {}
index = "hello"
index2 = "goodbye"
result.update({index: index2})
result.update({"test2": "test2"})

print(json.dumps(result))