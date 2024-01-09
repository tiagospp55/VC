from dict import letters


def translate(list_bin):

    maxlen = 0
    for i in range(0, len(list_bin)):
        if len(list_bin[i]) > maxlen:
            maxlen = len(list_bin[i])

    for i in range(0, len(list_bin)):
        if len(list_bin[i]) < maxlen:
            list_bin[i] = list_bin[i] + [0]*(maxlen - len(list_bin[i]))

    if len(list_bin) % 3 != 0:
        list_bin.append([0]*maxlen)

     
    letters_non_translated = []

    if len(list_bin) > 3:
        for i in range(0,len(list_bin)-3, 3): # Andas pelas listas
            first_column = 0
            second_column = 0

            for j in range(0, maxlen, 2): # andar pelas colunas
                    first_column = 32 * list_bin[i][j] + 8 * list_bin[i+1][j] + 2 * list_bin[i+2][j]
                    second_column = 16 * list_bin[i][j+1] + 4 * list_bin[i+1][j+1] + list_bin[i+2][j+1]
                    letters_non_translated.append(first_column + second_column)
    else:
            first_column = 0
            second_column = 0
            i = 0
            for j in range(0, maxlen, 2): # andar pelas colunas
                    first_column = 32 * list_bin[i][j] + 8 * list_bin[i+1][j] + 2 * list_bin[i+2][j]
                    second_column = 16 * list_bin[i][j+1] + 4 * list_bin[i+1][j+1] + list_bin[i+2][j+1]
                    letters_non_translated.append(first_column + second_column)
    letters_translated = []

    print('------------')   
    print(letters_non_translated)
    print('------------') 

    for i in range(0, len(letters_non_translated)):
        for key, value in letters.items():
            if key == letters_non_translated[i]:
                letters_translated.append(value)

    for i in range(1, len(letters_translated)-1):
        if letters_translated[i-1] == '#':
            letters_translated[i] = letters_translated[i].upper()
    
    print(letters_translated)

    return [letters_translated[i] for i in range(len(letters_translated)) if letters_translated[i] != '#']


