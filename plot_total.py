from matplotlib import pyplot as plt

#heap memory usage for uxb containers

with open('heap_uxb_total.txt') as f:
    totals = f.readlines()

totals_int = map(int, totals)
for total in totals_int:
    print total

plt.plot(totals_int, 'rx')

print max(totals_int), min(totals_int)

plt.show()