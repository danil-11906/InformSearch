line = []
for i in range (100):
    text = open("lemmas/lemmas_" + str(i+1) + ".txt", "r", encoding="utf-8")
    lines = text.read().split('\n')
    for m in lines:
        line.append(m)

finish = sorted(list(set(line)))
finish.remove('')
print(finish)

fine = open("lemma.txt", "w", encoding="utf-8")
for w in finish:
    fine.write(f"{w}\n")