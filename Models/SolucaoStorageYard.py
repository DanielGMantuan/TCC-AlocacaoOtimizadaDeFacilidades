class SolucaoStorageYard:
    patios: list[int] = []
    volumes: list[float] = []
    distanciaTotal = 0.0
    FO = 0.0
    tempoSol = 0.0
    tempo = 0.0
    numIteracoes = int(0)
    numViaveis = int(0)
    numInviaveis = int(0)
    viavel = True
    arvores = [[] for _ in range(14)]
    
    # teste de tempo
    tempoCalculoFO_Total = 0.0
    tempoCalculoFO_SA = 0.0
    tempoCalculoFO_Heuristica = 0.0
    tempoSA = 0.0
    tempoHeuristica = 0.0
    tempoTotal = 0.0
    t = 0.0
    tempoDjisktra = 0.0

    def fileWritter(self, index: int, restVolSup:float, path: str):
        caminho = fr"{path}\patios.txt"
        with open(caminho, "w") as arquivo:
            arquivo.write("distanciaTotal: " + str(self.distanciaTotal) + "\n")
            arquivo.write("FO: " + str(self.FO) + "\n")
            arquivo.write("tempoSol: " + str(self.tempoSol) + "\n")
            arquivo.write("tempo: " + str(self.tempo) + "\n")
            arquivo.write("numIteracoes: " + str(self.numIteracoes) + "\n")
            arquivo.write("numViaveis: " + str(self.numViaveis) + "\n")
            arquivo.write("numInviaveis: " + str(self.numInviaveis) + "\n")
            arquivo.write("viavel: " + str(self.viavel) + "\n\n")


            arquivo.write(f"Tempo total de execucao do sistema (leitura/escrita dos shapefiles): {str(self.tempoTotal)}\n")
            arquivo.write(f"Tempo total do calculo FO (construtiva e SA): {str(self.tempoCalculoFO_Heuristica + self.tempoCalculoFO_SA)}\n")
            arquivo.write(f"% Tempo total do calculo FO (construtiva e SA) no tempo total do sistema (leitura/escrita dos shapefiles): {str( ( (self.tempoCalculoFO_Heuristica + self.tempoCalculoFO_SA) / self.tempoTotal ) * 100 )}%\n")

            if(self.tempoSA != 0):
                arquivo.write(f" --- Estimativas SA --- \n")
                arquivo.write(f"\t Tempo total do SA: {str(self.tempoSA)} \n")
                arquivo.write(f"\t Tempo total da do calculo FO no SA: {str(self.tempoCalculoFO_SA)} \n")
                arquivo.write(f"\t % Tempo do SA no tempo das heuristicas: {str( (self.tempoSA / self.tempo) * 100 )}% \n")
                arquivo.write(f"\t % Tempo do calculo da FO no SA : {str( (self.tempoCalculoFO_SA / self.tempoSA) * 100 )}% \n")
                arquivo.write(f"\t % Tempo do SA no tempo total do sistema (leitura/escrita dos shapefiles): {str( (self.tempoSA / self.tempoTotal) * 100 )}% \n")

            if(self.tempoHeuristica != 0):
                arquivo.write(f" --- Estimativas Heuristica --- \n")
                arquivo.write(f"\t Tempo total da construtiva: {str(self.tempoHeuristica)} \n")
                arquivo.write(f"\t Tempo total do calculo FO na construtiva: {str(self.tempoCalculoFO_Heuristica)} \n")
                arquivo.write(f"\t % Tempo da construtiva no tempo das heuristicas: {str( (self.tempoHeuristica / self.tempo) * 100 )}% \n")
                arquivo.write(f"\t % Tempo do calculo da FO na construtiva : {str( (self.tempoCalculoFO_Heuristica / self.tempoHeuristica) * 100 )}% \n")
                arquivo.write(f"\t % Tempo da construtiva no tempo total do sistema (leitura/escrita dos shapefiles): {str( (self.tempoHeuristica / self.tempoTotal) * 100 )}% \n")

            arquivo.write(f" --- Outras estimativas --- \n")
            arquivo.write(f"\t Tempo total do Djkistra: {str(self.tempoDjisktra)} \n")
            arquivo.write(f"\t % Tempo do Djkistra no tempo das heuristicas: {str( (self.tempoDjisktra / self.tempo) * 100 )}% \n")
            arquivo.write(f"\t % Tempo do Djkistra no tempo total do sistema (leitura/escrita dos shapefiles): {str( (self.tempoDjisktra / self.tempoTotal) * 100 )}% \n")
            
            tempoSobra = self.tempoTotal - self.tempo - self.tempoDjisktra
            arquivo.write(f"\t Tempo da leitura/escrita dos arquivos e criacao dos grafos: {str(tempoSobra)} \n")
            arquivo.write(f"\t % Tempo da leitura/escrita dos arquivos e criacao dos grafos no tempo total do sistema (leitura/escrita dos shapefiles): {str((tempoSobra / self.tempoTotal) * 100)}% \n\n")

            arquivo.write("+----------------RESULTADO----------------+\n")
            volumeTotal = 0
            arquivo.write("Patio\t N_Arvores\t Volume" + "\n")
            for i in range(len(self.patios)):
                if(self.volumes[i] >= restVolSup):
                    arquivo.write(str(self.patios[i]) + "\t " + str(len(self.arvores[i])) + "\t " + str(self.volumes[i]) + "\t PENALIZADO \n") 
                else:
                    arquivo.write(str(self.patios[i]) + "\t " + str(len(self.arvores[i])) + "\t " + str(self.volumes[i]) + "\n")
                volumeTotal += self.volumes[i]
            arquivo.write("Volume Total:" + str(volumeTotal) + "\n")
            arquivo.write("RestVolSup:" + str(restVolSup) + "\n")
            arquivo.write("+-------------- Relacao patio x arvores ------------------+\n")
            for i in range(len(self.arvores)):
                arquivo.write("Patio\tId_arvore\tNum_Arvores\n")
                for j in range(len(self.arvores[i])):
                    arquivo.write(str(self.patios[i]) +"\t"+ str(self.arvores[i][j]['id']) + "\t" + str(self.arvores[i][j]['numero']) + "\n")
    