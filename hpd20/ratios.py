
for u in range(1,100):
    for d in range(1,100):
        rat = float(u)/float(d)
        if rat >= 1.0 and rat <=2.0:
            print(u, d, rat*1200-1200, rat)


