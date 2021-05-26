from pathlib import Path
from os import makedirs, listdir, rename
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from tkinter import Tk, Label, font, Button


# Função para converter os arquivos tipo pdf em txt.

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def fim():
    global lb1, lb2, bt
    lb1['text'] = 'Arquivos renomeados com sucesso!'
    lb2['text'] = 'Clique no botão "Encerrar" para finalizar.'
    bt['text'] = 'Encerrar'
    bt['command'] = lambda : janela.destroy()

#Função para listar os arquivos a serem listados, identificar o layout, renomear o arquivo e o excluir da lista.

def ler_pdf():

    #Criação da lista com os arquivos para identificar o layout.

    NFs = listdir(pasta)
    item = str(pasta) + '\\' + NFs[0]
    lb_controle2 = Label(janela, text=f'{len(NFs)} arquivo(s) para renomear.')
    lb_controle2.pack(side='top')
    conteudo = convert_pdf_to_txt(item)
    print(conteudo)

    #Condições para identificação e renomeação dos arquivos.

    if 'PREFEITURA MUNICIPAL DE SÃO JOSÉ DOS PINHAIS' in conteudo:
        nome = f'{conteudo[159:161]}-{conteudo[162:164]}-{conteudo[167:169]} - NFS {conteudo[132:138]}'
        if 'O BOTICÁRIO' in conteudo:
            nome += ' - O BOTICÁRIO - '
            if '00.856.186/0004-28' in conteudo:
                nome += 'DC'
                rename(item, str(pasta) + '\\' + nome + '.pdf')
    fim()

#Criação e configuração de interface.

janela = Tk()
janela.geometry('800x600+200+50')
janela.title('SAM - System Assistant Management')

font_titulo = font.Font(family='Lucida Grande', size=20)
font_texto = font.Font(family='Lucida Grande', size=12)

lb_titulo = Label(janela, font=font_titulo, text='RENOMEADOR DE NFS', height='5')
lb_titulo.pack(side='top')

#Criação e customização dos labels de instruções.

lb1 = Label(janela, font=font_texto, text=f'1 - Mova as NFs para a pasta "NFs" caminho - '
                                          f'{Path.home() / "Documents" / "NFs"}')
lb1.pack(side='top')
lb2 = Label(janela, font=font_texto, text='2 - Assim que os arquivos estiverem na pasta, clique no botão "Iniciar"'
                                          + ' '*16, height='5')
lb2.pack(side='top')

#Criação do botão "Iniciar" e marca d'água.

lb_bt = Label(janela, height='3')
lb_bt.pack(side='top')
bt = Button(janela, text='Iniciar', font=font_texto, command=ler_pdf, width='15')
bt.pack(side='top')
lb_marca = Label(janela, text='SAM - RNFv1.0.0 developed by Samuel Nunes')
lb_marca.pack(side='bottom', anchor='e')

# Criação do diretório de origem das NFs.

try:
    pasta = Path.home() / "Documents" / 'NFs'
    makedirs(pasta)
    teste = Path.home() / 'Desktop'
except:
    lb = Label(janela, height='2')
    lb.pack(side='top')
    lb_controle1 = Label(janela, text='Diretório OK')
    lb_controle1.pack(side='top')

janela.mainloop()