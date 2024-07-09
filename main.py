from tkinter import *
from tkinter import ttk
import sqlite3

janela = Tk()
class Funcao():
    def limpa_tela(self):
        self.codigo_input.delete(0, END)
        self.nome_input.delete(0, END)
        self.telefone_input.delete(0, END)
        self.cidade_input.delete(0, END)
    def conecta_bd(self):
        self.conecta = sqlite3.connect("clientes.bd")
        self.cursor = self.conecta.cursor(); print('Conectando ao banco de dados')
    def desconecta_bd(self):
        self.conecta.close(); print("Desconectando banco de dados")
    def criar_tabela(self):
        self.conecta_bd()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade char (40)          
            );                       
        """)
        self.conecta.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_input.get()
        self.nome = self.nome_input.get()
        self.telefone = self.telefone_input.get()
        self.cidade = self.cidade_input.get()

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd() 
        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, telefone, cidade)
            VALUES (?,?,?)""", (self.nome, self.telefone, self.cidade))
        self.conecta.commit()
        self.desconecta_bd()
        self.atualiza_lista()
        self.limpa_tela()
    def atualiza_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=(i))
        self.desconecta_bd()
    def duplo_clique(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for i in self.listaCli.selection():
            col1,col2,col3,col4 = self.listaCli.item(i,'values')
            self.codigo_input.insert(END, col1)
            self.nome_input.insert(END, col2)
            self.telefone_input.insert(END, col3)
            self.cidade_input.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conecta.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.atualiza_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente =?, telefone = ?, cidade = ? WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo,))
        self.conecta.commit()
        self.desconecta_bd()
        self.atualiza_lista()
        self.limpa_tela()
    
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_input.insert(END, '%')
        nome = self.nome_input.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" %nome)
        buscarnomeCli = self.cursor.fetchall()
        for i in buscarnomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()
class Aplication(Funcao):
    def __init__(self) -> None:
        self.janela = janela
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.criar_tabela()
        self.atualiza_lista()
        janela.mainloop()
    def tela(self):
        self.janela.configure(background="#1458a6")
        self.janela.title("Cadastro de Clientes")
        self.janela.geometry("700x500")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=400, height=300)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.janela, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#05058a', highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame_2 = Frame(self.janela, bd=4, bg= '#dfe3ee'
                             , highlightbackground= '#05058a', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        self.bt_limpar = Button(self.frame_1, text= 'Limpar',
                                bg = '#05058a', fg = 'white', font= ("verdana", 10, "bold"), command= self.limpa_tela)
        self.bt_limpar.place(relx=0.14, rely=0.17, relwidth=0.1, relheight=0.14)

        self.bt_buscar = Button(self.frame_1, text='Buscar' , bg = '#05058a',
                                fg = 'white', font= ("verdana", 10, "bold"), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.24, rely=0.17, relwidth=0.1, relheight=0.14)

        self.bt_novo = Button(self.frame_1, text='Novo' , bg = '#05058a',
                              fg = 'white', font= ("verdana", 10, "bold"), command= self.add_cliente)
        self.bt_novo.place(relx=0.5, rely=0.17, relwidth=0.1, relheight=0.14)

        self.bt_alterar = Button(self.frame_1, text='Alterar' , bg = '#05058a',
                                 fg = 'white', font= ("verdana", 10, "bold"), command= self.altera_cliente)
        self.bt_alterar.place(relx=0.6, rely=0.17, relwidth=0.1, relheight=0.14)

        self.bt_apagar = Button(self.frame_1, text='Apagar' , bg = '#05058a',
                                fg = 'white', font= ("verdana", 10, "bold"), command= self.deleta_cliente)
        self.bt_apagar.place(relx=0.7, rely=0.17, relwidth=0.1, relheight=0.14)

        self.lb_codigo = Label(self.frame_1, text = "Código")
        self.lb_codigo.place(relx = 0.03, rely = 0.05)
        
        self.codigo_input = Entry(self.frame_1)
        self.codigo_input.place(relx=0.03, rely=0.17, relwidth=0.1, relheight=0.15)

        self.lb_nome = Label(self.frame_1, text = "Nome")
        self.lb_nome.place(relx = 0.03, rely = 0.35)
        
        self.nome_input = Entry(self.frame_1)
        self.nome_input.place(relx=0.03, rely=0.45, relwidth=0.78, relheight=0.15)

        self.lb_telefone = Label(self.frame_1, text = "Telefone")
        self.lb_telefone.place(relx = 0.03, rely = 0.65)
        
        self.telefone_input = Entry(self.frame_1)
        self.telefone_input.place(relx=0.03, rely=0.75, relwidth=0.4, relheight=0.15)

        self.lb_cidade = Label(self.frame_1, text = "Cidade")
        self.lb_cidade.place(relx = 0.5, rely = 0.65)
        
        self.cidade_input = Entry(self.frame_1)
        self.cidade_input.place(relx=0.5, rely=0.75, relwidth=0.32, relheight=0.15)
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height= 3, columns=("col1", "col2","col3", "col4"))
        self.listaCli.heading("#0", text='')
        self.listaCli.heading("#1", text='Código')
        self.listaCli.heading("#2", text='Nome')
        self.listaCli.heading("#3", text='Telefone')
        self.listaCli.heading("#4", text='Cidade')
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx= 0.02, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll = self.scrollLista.set)
        self.scrollLista.place(relx= 0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.duplo_clique)

Aplication()