import sys

import matplotlib.pyplot as plt

freqs = {}
total = 0
for line in sys.stdin:
    count, freq = map(int, line.strip().split())
    freqs[count] = freq
    total += freq

max_n = int(sys.argv[1])

labels = list(range(1, max_n)) + [f'>={max_n}']

sizes = [0] * max_n

for count, freq in freqs.items():
    if count == 0:
        continue
    elif count < max_n:
        sizes[count - 1] = freq
    else:
        sizes[-1] += freq

# explode = (0.1,) * len(labels)
explode = (0.0,) * len(labels)
# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

print('sizes:', sizes)
print('labels:', labels)

print('total freq:', total)

fig1, ax1 = plt.subplots(figsize=(4.8, 4.8))
ax1.pie(
    sizes, explode=explode, labels=labels, startangle=90, autopct="%1.1f%%"
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

# plt.show()
plt.savefig(sys.argv[2])
