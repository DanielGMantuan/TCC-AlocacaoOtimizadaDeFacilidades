def quickSort(v, vInd, vInd2, esquerda, direita):
    esq = esquerda
    dir = direita
    pivo = v[int((esq + dir) / 2)]
    while esq <= dir:
        while v[esq] < pivo:
            esq = esq + 1
        while v[dir] > pivo:
            dir = dir - 1
        if esq <= dir:
            #troca o valor do elemento
            troca = v[esq]
            v[esq] = v[dir]
            v[dir] = troca
            #trocando o elemento
            elemento =  vInd[esq]
            vInd[esq] = vInd[dir]
            vInd[dir] = elemento
            #trocando o segundo elemento
            elemento = vInd2[esq]
            vInd2[esq] = vInd2[dir]
            vInd2[dir] = elemento
            esq = esq + 1
            dir = dir - 1
    if(dir > esquerda):
        quickSort(v, vInd, vInd2, esquerda, dir)
    if(esq < direita):
        quickSort(v, vInd, vInd2, esq, direita)
