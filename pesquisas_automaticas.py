import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import keyboard
import threading

class AutoPesquisaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Pesquisa")
        self.root.geometry("600x500")
        
        # Variável de controle
        self.executando = False
        self.thread_pesquisa = None
        
        # Lista de pesquisas
        self.pesquisas = [
            "O impacto das redes sociais no bem-estar mental.",
            "Técnicas de mindfulness para reduzir o estresse.",
            "A evolução da música eletrônica nas últimas décadas.",
            "Benefícios e desafios do trabalho remoto.",
            "A história da arquitetura moderna.",
            "Efeitos da dieta cetogênica na saúde.",
            "Tecnologia blockchain e suas aplicações além das criptomoedas.",
            "Como a IA está transformando a medicina.",
            "Curiosidades sobre a exploração espacial.",
            "O desenvolvimento de carros autônomos.",
            "Como as mudanças climáticas afetam os oceanos.",
            "Impacto das fake news em eleições recentes.",
            "A importância da biodiversidade nos ecossistemas.",
            "Como as teorias da conspiração se espalham online.",
            "A história dos jogos de tabuleiro.",
            "Técnicas de persuasão na publicidade.",
            "O efeito do jejum intermitente na perda de peso.",
            "A influência da cultura pop japonesa no Ocidente.",
            "O surgimento do cyberpunk na literatura e no cinema.",
            "A história do cinema mudo.",
            "Aplicações da impressão 3D na construção civil.",
            "Como a genética influencia a personalidade.",
            "A relação entre esportes e saúde mental.",
            "O papel das mulheres na Revolução Industrial.",
            "A psicologia das cores no design gráfico.",
            "O efeito da meditação na neuroplasticidade.",
            "Como os robôs estão mudando a agricultura.",
            "A evolução do design de videogames.",
            "A história do desenvolvimento das lentes de contato.",
            "O impacto dos plásticos no meio ambiente.",
            "A vida das abelhas e seu papel na polinização."
        ]
        
        # Configurar interface
        self.criar_interface()
        
        # Configurar tecla ESC para parar
        keyboard.add_hotkey('esc', self.parar_execucao)
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Auto Pesquisa", font=('Helvetica', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Descrição
        descricao = ttk.Label(main_frame, text="Este programa automatiza pesquisas no navegador.", wraplength=500)
        descricao.pack(pady=5)
        
        # Lista de pesquisas
        lista_frame = ttk.LabelFrame(main_frame, text="Pesquisas a serem realizadas", padding=10)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lista_pesquisas = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, height=10)
        for pesquisa in self.pesquisas:
            self.lista_pesquisas.insert(tk.END, pesquisa)
        self.lista_pesquisas.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_pesquisas.yview)
        
        # Controles
        controles_frame = ttk.Frame(main_frame)
        controles_frame.pack(fill=tk.X, pady=10)
        
        self.btn_iniciar = ttk.Button(controles_frame, text="Iniciar Pesquisas", command=self.iniciar_pesquisas)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        
        self.btn_parar = ttk.Button(controles_frame, text="Parar (ESC)", command=self.parar_execucao, state=tk.DISABLED)
        self.btn_parar.pack(side=tk.LEFT, padx=5)
        
        self.btn_adicionar = ttk.Button(controles_frame, text="Adicionar", command=self.adicionar_pesquisa)
        self.btn_adicionar.pack(side=tk.LEFT, padx=5)
        
        self.btn_remover = ttk.Button(controles_frame, text="Remover", command=self.remover_pesquisa)
        self.btn_remover.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para começar")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.pack(fill=tk.X, pady=(5,0))
    
    def adicionar_pesquisa(self):
        def salvar_pesquisa():
            nova_pesquisa = entrada.get()
            if nova_pesquisa:
                self.pesquisas.append(nova_pesquisa)
                self.lista_pesquisas.insert(tk.END, nova_pesquisa)
                janela.destroy()
        
        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Pesquisa")
        
        frame = ttk.Frame(janela, padding="10")
        frame.pack()
        
        ttk.Label(frame, text="Digite a nova pesquisa:").pack(pady=5)
        entrada = ttk.Entry(frame, width=50)
        entrada.pack(pady=5)
        
        btn_salvar = ttk.Button(frame, text="Salvar", command=salvar_pesquisa)
        btn_salvar.pack(pady=5)
        
        entrada.focus_set()
    
    def remover_pesquisa(self):
        selecionados = self.lista_pesquisas.curselection()
        
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione uma pesquisa para remover!")
            return
            
        for index in reversed(selecionados):
            self.lista_pesquisas.delete(index)
            self.pesquisas.pop(index)
    
    def iniciar_pesquisas(self):
        if not self.pesquisas:
            messagebox.showwarning("Aviso", "Não há pesquisas para realizar!")
            return
            
        resposta = messagebox.askyesno(
            "Confirmação", 
            "O programa irá começar a automatizar as pesquisas.\n"
            "Certifique-se de:\n"
            "1. Ter o navegador aberto\n"
            "2. Não mover o mouse durante a execução\n"
            "3. Pressione ESC para parar\n\n"
            "Deseja continuar?"
        )
        
        if resposta:
            self.executando = True
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_parar.config(state=tk.NORMAL)
            self.btn_adicionar.config(state=tk.DISABLED)
            self.btn_remover.config(state=tk.DISABLED)
            self.status_var.set("Preparando... (5 segundos para posicionar o navegador)")
            
            # Executar em uma thread separada para não travar a interface
            self.thread_pesquisa = threading.Thread(target=self.executar_pesquisas, daemon=True)
            self.thread_pesquisa.start()
    
    def executar_pesquisas(self):
        time.sleep(5)  # Tempo para o usuário preparar o ambiente
        
        for i, pesquisa in enumerate(self.pesquisas):
            if not self.executando:
                break
                
            self.status_var.set(f"Executando pesquisa {i+1}/{len(self.pesquisas)}: {pesquisa[:30]}...")
            self.root.update()  # Atualiza a interface
            
            try:
                # Abre uma nova guia
                pyautogui.hotkey('ctrl', 't')
                time.sleep(1)
                
                # Digita a pesquisa
                pyautogui.write(pesquisa)
                time.sleep(1)
                
                # Pressiona Enter
                pyautogui.press('enter')
                time.sleep(3)
                
                # Fecha a aba
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(1)
                
            except Exception as e:
                self.status_var.set(f"Erro: {str(e)}")
                self.executando = False
                break
        
        self.finalizar_execucao()
    
    def parar_execucao(self):
        if self.executando:
            self.executando = False
            self.status_var.set("Parando...")
    
    def finalizar_execucao(self):
        self.executando = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.btn_adicionar.config(state=tk.NORMAL)
        self.btn_remover.config(state=tk.NORMAL)
        
        if self.thread_pesquisa and self.thread_pesquisa.is_alive():
            self.thread_pesquisa.join()
        
        self.status_var.set("Execução concluída!" if not self.executando else "Execução interrompida pelo usuário")
        messagebox.showinfo("Concluído", "Processo de pesquisa finalizado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPesquisaApp(root)
    root.mainloop()