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
            arquivo.write("viavel: " + str(self.viavel) + "\n")
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
    