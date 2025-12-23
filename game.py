import tkinter as tk
import random

COR_FUNDO = "#DCF8A6"
COR_COBRA = "#4F5152"
COR_BOTAO = "#4A4A4A"
COR_TEXTO_BOTAO = "#FFFFFF"
LARGURA = 600
ALTURA = 400
TAMANHO_BLOCO = 20         
VELOCIDADE = 100           

class JogoCobra:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Snake Minimalista Pro")
        self.janela.configure(bg=COR_FUNDO)
        
        self.canvas = tk.Canvas(self.janela, bg=COR_FUNDO, width=LARGURA, height=ALTURA, highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # frame para os Botões
        self.frame_controles = tk.Frame(self.janela, bg=COR_FUNDO)
        self.frame_controles.pack(fill="x", pady=10)

        self.btn_iniciar = tk.Button(self.frame_controles, text="INICIAR", command=self.iniciar_partida, 
                                     bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, font=("Arial", 10, "bold"), width=10)
        self.btn_iniciar.pack(side="left", padx=20)

        self.btn_resetar = tk.Button(self.frame_controles, text="REINICIAR", command=self.resetar_jogo, 
                                     bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, font=("Arial", 10, "bold"), width=10)
        self.btn_resetar.pack(side="right", padx=20)

        # estado Inicial
        self.direcao = "Right"
        self.cobra = [(100, 100), (80, 100), (60, 100)] 
        self.rodando = False
        self.jogo_iniciado = False
        self.pontos = 0
        
        self.texto_score = self.canvas.create_text(
            LARGURA/2, 20, text=f"SCORE: {self.pontos}", 
            fill=COR_COBRA, font=("Courier New", 16, "bold")
        )
        
        self.gerar_comida()
        self.desenhar() 
        
        self.janela.bind("<Key>", self.mudar_direcao)
        self.janela.mainloop()

    def iniciar_partida(self):
        if not self.jogo_iniciado:
            self.rodando = True
            self.jogo_iniciado = True
            self.mover()

    def resetar_jogo(self):
        self.rodando = False
        self.jogo_iniciado = False
        self.direcao = "Right"
        self.cobra = [(100, 100), (80, 100), (60, 100)] 
        self.pontos = 0
        
        self.canvas.delete("all")
        self.texto_score = self.canvas.create_text(
            LARGURA/2, 20, text=f"SCORE: {self.pontos}", 
            fill=COR_COBRA, font=("Courier New", 16, "bold")
        )
        self.gerar_comida()
        self.desenhar()

    def gerar_comida(self):
        x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
        y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
        self.comida = (x, y)

    def desenhar(self):
        self.canvas.delete("cobra")
        self.canvas.delete("comida")
        
        cx, cy = self.comida
        self.canvas.create_oval(cx, cy, cx + TAMANHO_BLOCO, cy + TAMANHO_BLOCO, fill="#E93131", tags="comida")
        
        for x, y in self.cobra:
            self.canvas.create_rectangle(x, y, x + TAMANHO_BLOCO, y + TAMANHO_BLOCO, fill=COR_COBRA, outline=COR_FUNDO, tags="cobra")

    # def mover(self):
    #     if not self.rodando: return

    #     x_cabeca, y_cabeca = self.cobra[0]
    #     if self.direcao == "Up": y_cabeca -= TAMANHO_BLOCO
    #     elif self.direcao == "Down": y_cabeca += TAMANHO_BLOCO
    #     elif self.direcao == "Left": x_cabeca -= TAMANHO_BLOCO
    #     elif self.direcao == "Right": x_cabeca += TAMANHO_BLOCO

    #     # Colisões
    #     if x_cabeca < 0 or x_cabeca >= LARGURA or y_cabeca < 0 or y_cabeca >= ALTURA or (x_cabeca, y_cabeca) in self.cobra:
    #         self.game_over()
    #         return

    #     self.cobra.insert(0, (x_cabeca, y_cabeca))

    #     if x_cabeca == self.comida[0] and y_cabeca == self.comida[1]:
    #         self.pontos += 10
    #         self.canvas.itemconfig(self.texto_score, text=f"SCORE: {self.pontos}")
    #         self.gerar_comida()
    #     else:
    #         self.cobra.pop()

    #     self.desenhar()
    #     self.janela.after(VELOCIDADE, self.mover)

    def mover(self):
        if not self.rodando: return

        x_cabeca, y_cabeca = self.cobra[0]

        if self.direcao == "Up": y_cabeca -= TAMANHO_BLOCO
        elif self.direcao == "Down": y_cabeca += TAMANHO_BLOCO
        elif self.direcao == "Left": x_cabeca -= TAMANHO_BLOCO
        elif self.direcao == "Right": x_cabeca += TAMANHO_BLOCO

        nova_posicao = (x_cabeca, y_cabeca)

        if x_cabeca < 0 or x_cabeca >= LARGURA or y_cabeca < 0 or y_cabeca >= ALTURA or nova_posicao in self.cobra:
            self.game_over()
            return

        self.cobra.insert(0, nova_posicao)

        if x_cabeca == self.comida[0] and y_cabeca == self.comida[1]:
            self.pontos += 10
            self.canvas.itemconfig(self.texto_score, text=f"SCORE: {self.pontos}")
            self.gerar_comida()
        else:
            self.cobra.pop()

        self.desenhar()
        self.janela.after(VELOCIDADE, self.mover)


    def mudar_direcao(self, event):
        tecla = event.keysym
        opostos = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if tecla in opostos and tecla != opostos.get(self.direcao):
            self.direcao = tecla

    def game_over(self):
        self.rodando = False
        self.jogo_iniciado = False
        self.canvas.create_text(LARGURA/2 + 3, ALTURA/2 + 3, text="GAME OVER", fill="#570606", font=("Courier New", 40, "bold"))
        self.canvas.create_text(LARGURA/2, ALTURA/2, text="GAME OVER", fill="#B90707", font=("Courier New", 40, "bold"))

JogoCobra()
