# zoomers

##  Описание 

Сегодня утром разведка перехватила секретное сообщение с планеты zoom. У нас в архивах также завалялся старенький шифратор. Сможешь узнать, что передавали `зумляне`?

## Решение

По коду шифратора можно заметить, что каждый из ключей является числом, меньшим чем 6. 

Вот пример эксплойта, перебираюшего ключи: 

```
earth_alhpabet = 'abcdefghijklmnopqrstuvwxyz{}_ '
zoom_alphabet = 'zoumna'

encrypted = 'mamuuomonmonznoooouzzoomuuoooouzoznounzooooomuuouzzmmuuzoooomaoznoooouzmuzzzuzuuooooznmznooaumaouzzznmmaoooozumunumaomamooooazznoznouzmuuooomzzuooouzoznounzoomooooozmonuzzzznooounuzzuooomaouuouzzznmmamuuooomznmmaooozznnoazznoznouzmuuuoazznoznouzmuuuoazznoznouzmuuooomzzummmooommuznoooooauznomaoooooozznooomzznuuomaoooouzzoanznounzmaoooooozmonuzzzznooooozznooomuzmuzzmaoooooanuzouuo'
encrypted = [encrypted[i:i+3] for i in range(0, len(encrypted), 3)]


def gen_translation(keys):
    a, b, c = keys
    translated_zoom_alphabed = [(zoom_alphabet[(len(earth_alhpabet) - i) % a] + zoom_alphabet[(len(earth_alhpabet) - i) %
                                                                                              b] + zoom_alphabet[(len(earth_alhpabet) - i) % c]) for i in range(len(earth_alhpabet))]
    translation = {translated_zoom_alphabed[i]
        : earth_alhpabet[i] for i in range(30)}
    return translation


err = True
keys = [0, 0, 0]
for keys[0] in range(1, 7):
    for keys[1] in range(1, 7):
        for keys[2] in range(1, 7):
            if not err:
                exit(0)
            trans = gen_translation(keys)
            try:
                res = ''
                for enc in encrypted:
                    res += trans[enc]
                print('[ OK ] [%i, %i, %i]' % (keys[0], keys[1], keys[2]))
                print(res)
                err = False
            except:
                print('[FAIL] [%i, %i, %i]' % (keys[0], keys[1], keys[2]))

```

 ### Флаг
 TeacherCTF{zoom_zoom_zoomers}