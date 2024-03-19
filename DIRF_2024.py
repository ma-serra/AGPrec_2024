#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
from PIL import Image
import pandas as pd
import re
import time
#st.spinner(text="In progress...")
st.set_page_config(layout="centered", page_icon="⚖", page_title="Tribunal de Justiça do MA")
image = Image.open('logoTJMA.jpg')
st.image(image)
st.subheader("⚖ Tribunal de Justiça do MA")
st.write("Emissão de comprovante DIRF 2024.")


meio, left, right = st.columns(3)

meio.write(
    "Este App emite o comprovante de rendimentos referente ao recebimento de até 1 precatório no ano de 2024. Caso tenha recebido mais de um pagamento, por favor entrar em contato com a Assessoria de Gestão de Precatórios. Fone: (98) 2055-2426."
, style="text-align: justjy")

right.write("Este é o modelo que será emitido:")

right.image("Comprovante de rendimentos DIRF2024_2.png", width=180)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("Comprovante de rendimentos DIRF2024.html")

left.write("Informe os Dados:")
form = left.form("template_form")
CPF = form.text_input("CPF (sem pontos):", max_chars=11)
#student = form.text_input("Nome Completo:")
cpfPontuado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', CPF)

#grade = 'R$ 1.000.000,00'

submit = form.form_submit_button("Generate PDF")

DIRF2024 = pd.read_excel('DIRF2024.xlsx', dtype=str)
#DIRF2024 = pd.read_excel('C:/USERS/US NOTE/DOWNLOADS/JUPYTER/DIRF2024.xlsb', engine='pyxlsb')
#DIRF2024 = pd.read_excel('/DIRF2024.xlsb', engine='pyxlsb')

DIRF2024['VALOR'] = DIRF2024['VALOR'].astype(str)
#DIRF2024['VALOR'] = DIRF2024['VALOR'].str.replace('.', ',')
DIRF2024['PREVIDENCIA'] = DIRF2024['PREVIDENCIA'].astype(str)
#DIRF2024['PREVIDENCIA'] = DIRF2024['PREVIDENCIA'].str.replace('.', ',')
DIRF2024['IR'] = DIRF2024['IR'].astype(str)
#DIRF2024['IR'] = DIRF2024['IR'].str.replace('.', ',')
DIRF2024['QTD_MESES'] = DIRF2024['QTD_MESES'].astype(str)
DIRF2024['PROCESSO'] = DIRF2024['PROCESSO'].astype(str)
DIRF2024['PROCESSO'] = DIRF2024['PROCESSO'].str.replace(',', '.')

#CPF2 = {'CPF':{},'VALOR':{},'PREVIDENCIA':{},'IR':{}}
#CPF3 = pd.DataFrame(CPF2)
#TABELA = pd.merge(CPF3, DIRF2023, left_on=['CPF','VALOR'], right_on=['CPF','VALOR'], how='right')
#grade = DIRF2023.loc[DIRF2023.CPF == course,'VALOR'].values
#grade = DIRF2023.loc[DIRF2023['CPF'] == CPF,'VALOR'].values
#DIRF2023 = DIRF2023.set_index('CPF')
#DIRF2023.index.names = [None]
grade = DIRF2024.loc[DIRF2024['CPF'] == CPF,'VALOR'].values
student = DIRF2024.loc[DIRF2024['CPF_N_DUPLICADO'] == CPF,'NOME_N_DUPLICADO'].values
QTD_MESES = DIRF2024.loc[DIRF2024['CPF'] == CPF,'QTD_MESES'].values
PROCESSO = DIRF2024.loc[DIRF2024['CPF'] == CPF,'PROCESSO'].values
VALOR = DIRF2024.loc[DIRF2024['CPF'] == CPF,'VALOR'].values
PREVIDENCIA = DIRF2024.loc[DIRF2024['CPF'] == CPF,'PREVIDENCIA'].values
IR = DIRF2024.loc[DIRF2024['CPF'] == CPF,'IR'].values

#grade = re.search('02439232360', grade.decode('utf-8'))
#grade = grade.encode(encoding='utf-8')

#grade = re.sub("\[|\'|\]","",grade)

characters = "'[]"

grade = ''.join( x for x in grade if x not in characters)
student = ''.join( x for x in student if x not in characters)
#QTD_MESES =  ''.join( x for x in QTD_MESES if x not in characters)
#PROCESSO =  ''.join( x for x in PROCESSO if x not in characters)

try:
    if submit:
        with st.spinner('Aguarde'):
            PROCESSO = PROCESSO[0]
            QTD_MESES = QTD_MESES[0]
            VALOR = VALOR[0]
            PREVIDENCIA = PREVIDENCIA[0]
            IR = IR[0]
            VALOR = float(VALOR)
            VALOR = round(VALOR,2)
            VALOR = str(VALOR).replace('.', ',')
            html = template.render(
            course=cpfPontuado,
            student=student,
            date=date.today().strftime("%d / %m / %Y"),
            grade=grade,
            PROCESSO=PROCESSO,
            QTD_MESES=QTD_MESES,
            VALOR=VALOR,
            PREVIDENCIA=PREVIDENCIA,
            IR=IR
            )
            pdf = pdfkit.from_string(html, False)
            st.balloons()
            right.success("⚖ Comprovante Emitido com Sucesso!")
            right.download_button("⬇️ Download PDF",data=pdf,file_name="Comprovante de Rendimentos.pdf",mime="application/octet-stream")


#st.success('Gerado com Sucesso!')



        

except IndexError:
    right.write("CPF não encontrado! Entre em contato com a Coordenadoria de Precatórios. Fone:(98) 2055-2426.")

    


# In[2]:





# In[ ]:




