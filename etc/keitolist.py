import pickle

with open("test", "rb") as test_file:
    new = pickle.load(test_file)

for e in new:
    print(e)
