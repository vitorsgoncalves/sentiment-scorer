#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import re
import sys

from argparse import ArgumentParser
from gooey import Gooey, GooeyParser

import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()



@Gooey(
    program_name="Análise de sentimento",
    language="portuguese",
    program_description="Análise de sentimento utilizando a metodologia Vader",
    image_dir=".",
    default_size=(610, 660),
)
def main():
    
    parser = GooeyParser()
    
    required = parser.add_argument_group(
        'Parâmetros',
        gooey_options={
            'show_border': False,
            'columns': 2,
        }
    )
    
    required2 = parser.add_argument_group(
        '',
        gooey_options={
            'show_border': False,
            'columns': 1,
        }
    )
            
    required.add_argument(
        "-i",
        "--input", 
        required=True,
        metavar="Entrada",
        help="Caminho onde se encontram os CSVs de entrada",
        widget="DirChooser"
    )
    required.add_argument(
        "-o",
        "--output",
        required=True,
        metavar="Saída",
        help="Caminho a serem gravados os CSVs resultantes",
        widget="DirChooser"        
    )
    required2.add_argument(
        "-c",
        "--column",
        required=True,
        metavar="Nome da coluna",
        help="Nome da coluna com o texto a ser analisado",
    )    
    required2.add_argument(
        "-k",
        "--keywords",
        required=False,
        metavar="Palavras-chave",
        help="Palavras-chave a serem consideradas na seleção dos trechos (separadas por espaço)",
    )    
    
    args = parser.parse_args()    
      
    caminho_entrada = args.input
    caminho_saida = args.output
    if args.keywords is not None:
        palavras = args.keywords.split(' ')
    else: palavras = None
    coluna = args.column

    
    historico = []

    for files in os.listdir(caminho_entrada):
        if files.endswith(".csv"):
            ano = files.replace(".csv","")
            
            caminho = open(caminho_entrada + "/" + files, "r")
            arquivo = csv.DictReader(caminho)
            
            nbom = 0
            nruim = 0
            nneutro = 0
            soma_sentimento = 0
            
            with open(caminho_saida + "/" + files[:-4] +'_sentimento.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, arquivo.fieldnames + ["vader"])
                writer.writeheader()
                
                for row in arquivo:
                    
                    tex_original = row[coluna]
                    
                    a = tex_original.split('\n')
                    

                    if palavras is not None:
                    
                        b = []
                        for trecho in a:
                            if any(palavra in trecho.lower() for palavra in palavras):
                                b += [trecho]
                    else:
                        b = a
                            
                    
                    if len(''.join(b).strip('\n').strip(' ')) == 0:
                        continue
                    else:
                        tex = '\n'.join(b) 

                        ss = sia.polarity_scores(tex)
                        valor_vader = ss["compound"]
                        
                        row.update({"vader": valor_vader})

                        #print(valor_vader)
                        if valor_vader > 0.05:
                            nbom += 1

                        elif valor_vader < -0.05:
                            nruim += 1
        
                        else:
                            nneutro += 1


                        soma_sentimento += valor_vader
                        
                        writer.writerow(row)

            media = soma_sentimento / (nneutro+nruim+nbom) if (nneutro+nruim+nbom) else 0
            historico.append({'ano': ano, 'nbom': nbom, 'nneutro': nneutro, 'nruim': nruim , 'media': media})

        
    with open(caminho_saida + '/sentimento_mes.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ano','nbom', 'nneutro', 'nruim', 'media' ])
        writer.writeheader()
        writer.writerows(historico)


if __name__ == "__main__":
    main()
