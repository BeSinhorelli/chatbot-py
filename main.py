import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatbotCardapio:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Cardápio - Restaurante Python")
        self.root.geometry("700x550")
        
        # Configurar tema escuro
        self.cor_fundo = "#2b2b2b"
        self.cor_texto = "#ffffff"
        self.cor_botoes = "#3c3f41"
        self.cor_botoes_hover = "#4e5254"
        self.cor_entrada = "#3c3f41"
        self.cor_destaque = "#6a8759"
        
        self.root.configure(bg=self.cor_fundo)
        
        # Cardápio com numeração
        self.cardapio = {
            '1': {'descricao': 'Pizza Margherita', 'preco': 35.00},
            '2': {'descricao': 'Hambúrguer Artesanal', 'preco': 25.00},
            '3': {'descricao': 'Salada Caesar', 'preco': 20.00},
            '4': {'descricao': 'Combo Sushi 16 peças', 'preco': 45.00},
            '5': {'descricao': 'Lasanha à Bolonhesa', 'preco': 30.00},
            '6': {'descricao': 'Brownie com Sorvete', 'preco': 15.00},
            '7': {'descricao': 'Refrigerante 500ml', 'preco': 8.00}
        }
        
        self.pedido = []
        self.criar_interface()
        
        # Mensagem inicial
        self.adicionar_mensagem("Bot", "Bem-vindo ao nosso restaurante! 😊")
        self.adicionar_mensagem("Bot", "Digite 'ajuda' para ver os comandos disponíveis")
        self.adicionar_mensagem("Bot", "Ou digite 'cardapio' para ver nosso menu\n")
    
    def criar_interface(self):
        # Configurar estilo dos widgets
        estilo_botao = {
            'bg': self.cor_botoes,
            'fg': self.cor_texto,
            'activebackground': self.cor_botoes_hover,
            'activeforeground': self.cor_texto,
            'relief': 'flat',
            'border': 0,
            'padx': 10,
            'pady': 5
        }
        
        estilo_label = {
            'bg': self.cor_fundo,
            'fg': self.cor_texto
        }
        
        # Área de conversa
        self.conversa = scrolledtext.ScrolledText(
            self.root, 
            width=80, 
            height=20, 
            state='disabled',
            bg=self.cor_entrada,
            fg=self.cor_texto,
            insertbackground=self.cor_texto,
            relief='flat',
            font=('Arial', 10)
        )
        self.conversa.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Frame para entrada de dados
        frame_entrada = tk.Frame(self.root, bg=self.cor_fundo)
        frame_entrada.pack(pady=10, padx=10, fill='x')
        
        tk.Label(
            frame_entrada, 
            text="Digite o número do item ou comando:",
            **estilo_label
        ).pack(side=tk.LEFT)
        
        self.entrada = tk.Entry(
            frame_entrada, 
            width=30,
            bg=self.cor_entrada,
            fg=self.cor_texto,
            insertbackground=self.cor_texto,
            relief='flat'
        )
        self.entrada.pack(side=tk.LEFT, padx=5)
        self.entrada.bind('<Return>', lambda event: self.processar_comando())
        
        # Botões
        frame_botoes = tk.Frame(self.root, bg=self.cor_fundo)
        frame_botoes.pack(pady=10, padx=10)
        
        tk.Button(frame_botoes, text="Enviar", command=self.processar_comando, **estilo_botao).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Cardápio", command=self.mostrar_cardapio, **estilo_botao).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Pedido", command=self.mostrar_pedido, **estilo_botao).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Finalizar", command=self.finalizar_pedido, **estilo_botao).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Sair", command=self.root.quit, **estilo_botao).pack(side=tk.LEFT, padx=5)
        
        # Aplicar hover effects aos botões
        self.configurar_hover_effects()
    
    def configurar_hover_effects(self):
        # Configurar efeito hover para todos os botões
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.bind("<Enter>", lambda e, b=child: b.configure(bg=self.cor_botoes_hover))
                        child.bind("<Leave>", lambda e, b=child: b.configure(bg=self.cor_botoes))
    
    def adicionar_mensagem(self, remetente, mensagem):
        self.conversa.config(state='normal')
        
        # Configurar cor baseada no remetente
        if remetente == "Bot":
            tag_name = "bot_message"
            self.conversa.tag_config(tag_name, foreground=self.cor_destaque)
        else:
            tag_name = "user_message"
            self.conversa.tag_config(tag_name, foreground="#bbbbbb")
        
        self.conversa.insert(tk.END, f"{remetente}: ", tag_name)
        self.conversa.insert(tk.END, f"{mensagem}\n")
        
        self.conversa.config(state='disabled')
        self.conversa.see(tk.END)
    
    def mostrar_cardapio(self):
        cardapio_texto = "\n🍽️  **NOSSO CARDÁPIO** 🍽️\n"
        cardapio_texto += "=" * 60 + "\n"
        for num, info in self.cardapio.items():
            cardapio_texto += f"{num} - {info['descricao']:.<35} R$ {info['preco']:6.2f}\n"
        cardapio_texto += "=" * 60 + "\n"
        cardapio_texto += "Digite o número do item para adicionar ao pedido\n\n"
        self.adicionar_mensagem("Bot", cardapio_texto)
    
    def mostrar_pedido(self):
        if not self.pedido:
            self.adicionar_mensagem("Bot", "Seu pedido está vazio no momento.")
            return
        
        total = 0
        resposta = "\n🛒 **SEU PEDIDO** 🛒\n"
        resposta += "=" * 60 + "\n"
        
        for item in self.pedido:
            resposta += f"{item['descricao']:.<40} R$ {item['preco']:6.2f}\n"
            total += item['preco']
        
        resposta += "=" * 60 + "\n"
        resposta += f"TOTAL: {'R$':.<35} {total:6.2f}\n"
        resposta += "=" * 60
        self.adicionar_mensagem("Bot", resposta)
    
    def finalizar_pedido(self):
        if not self.pedido:
            self.adicionar_mensagem("Bot", "Seu pedido está vazio. Adicione itens antes de finalizar.")
            return
        
        total = sum(item['preco'] for item in self.pedido)
        resposta = "\n🎉 **PEDIDO FINALIZADO!** 🎉\n"
        resposta += "=" * 60 + "\n"
        
        for item in self.pedido:
            resposta += f"{item['descricao']:.<40} R$ {item['preco']:6.2f}\n"
        
        resposta += "=" * 60 + "\n"
        resposta += f"TOTAL: {'R$':.<35} {total:6.2f}\n"
        resposta += "=" * 60 + "\n"
        resposta += "Seu pedido foi enviado para a cozinha!\n"
        resposta += "Tempo estimado: 25-40 minutos\n"
        resposta += "Obrigado pela preferência! 😊\n\n"
        
        self.adicionar_mensagem("Bot", resposta)
        self.pedido = []  # Limpa o pedido
    
    def processar_comando(self):
        comando = self.entrada.get().strip()
        self.entrada.delete(0, tk.END)  # Limpa o campo de entrada
        
        if comando == '':
            return
        
        self.adicionar_mensagem("Você", comando)
        
        # Comandos especiais
        if comando.lower() == 'cardapio':
            self.mostrar_cardapio()
            return
        
        if comando.lower() == 'pedido':
            self.mostrar_pedido()
            return
        
        if comando.lower() == 'finalizar':
            self.finalizar_pedido()
            return
        
        if comando.lower() == 'ajuda':
            ajuda_texto = (
                "📋 **COMANDOS DISPONÍVEIS:**\n"
                "- Digite 'cardapio' para ver o menu\n"
                "- Digite 'pedido' para ver seu pedido atual\n"
                "- Digite 'finalizar' para finalizar o pedido\n"
                "- Digite o número do item para adicionar ao pedido\n\n"
            )
            self.adicionar_mensagem("Bot", ajuda_texto)
            return
        
        # Adicionar item ao pedido
        if comando in self.cardapio:
            item = self.cardapio[comando]
            self.pedido.append(item)
            self.adicionar_mensagem("Bot", f"✅ {item['descricao']} adicionado ao pedido!")
        else:
            self.adicionar_mensagem("Bot", "❌ Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis.")

# Executar o chatbot
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotCardapio(root)
    root.mainloop()