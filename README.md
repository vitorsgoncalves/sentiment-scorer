# Sentiment Scorer

This software aims at allowing researchers who aren't familiar with programming languages and environments, or aren't from techinical fields at all, to perform sentiment anaysis on textual data.

Sentiment Scores is designed to be user-friendly and accessible for non-technical people who need to assign sentiment scores to textual data. In this regard, the software has a simplified interface, with as fewer buttons and inputs as possible, labeled and documented, and a one-click approach for processing the data. The file format used is the CSV, which most researchers are familiar with, and allows for pre and post-processing using spreadsheet tools. The results are written in a selected destination folder, preserving the format and structure of the input, but adding a score column with the calculated values,

This project was created as a thecnical product in my thesis for the [PROFNIT](https://profnit.org.br/) master’s degree program. The original repository was archived, and can be accessed at (https://github.com/vitorsgoncalves/tcc-profnit). The published thesis can be accessed at: http://bd.centro.iff.edu.br/jspui/handle/123456789/4213

This tool uses the [VADER](https://github.com/cjhutto/vaderSentiment) methodology for scoring the sentiment in textual inputs. Thi method was chosen dued to its generally good results and low computational requirements.

## Features

 - Working with CSV data: The software works with data in CSV format, due to its practicality and popularity in scientific applications. The user can choose to either provide a single CSV file or several CSV ones for sentiment scoring.
 - Exporting in CSV format: The software exports the sentiment score data to a new CSV file, without modifying the source, containing the structure of the original file, with a new column added, with the calculated score. An auxiliary CSV file is also exported, containing one line for each input CSV and the average intensity of the texts in each of them, to facilitate obtaining averages for cases when the data is organized into multiple CSVs separated by time periods.
 - Selection of the column to be analyzed: The user can choose which column of the CSV will be analyzed so that the software will analyze only the text contained in the selected column, ignoring the others.
 - Filtering by keywords: The user can choose one or more keywords to filter the data. Only lines that contain at least one of the selected keywords will be analyzed. This functionality helps to analyze data with little or no pre-processing.

### Installing

Se você utiliza sistemas operacionais Windows ou Linux em arquitetura X64, foram criados executáveis que podem ser baixados e executados diretamente, a partir do link abaixo, sem a necessidade de conhecimentos técnicos específicos:

https://github.com/vitorsgoncalves/tcc-profnit/releases/tag/v0.1-alpha

Na página acima, você deve baixar o arquivo identificado no nome com sua plataforma. Junto da do software, é fornecido um arquivo zip contendo alguns arquivos de exemplo, para facilitar a realização de testes.

Caso utilize um sistema diferente, ou o procedimento acima não funcione, siga as instruções abaixo:

1. Instale o Python em sua máquina, se não estiver disponível, a partir das instruções do site oficial:

	[Página de instruções de instalação do Python](https://www.python.org/about/gettingstarted/)

1. Baixe ou clone o repositório do software a partir do comando:  

	` git clone https://github.com/vitorsgoncalves/tcc-profnit` 

2. Entre no diretório do software:

	` cd tcc-profnit/produto` 

3. Instale os pacotes Python necessários usando o comando 

	`pip install -r requirements.txt`

4. Execute o software a partir do comando abaixo:

	`python analise_sentimento.py`

### Usage

Ao iniciar o software, será exibida uma tela como essa:

![Tela principal do software, exibindo as opções disponíveis](https://github.com/vitorsgoncalves/tcc-profnit/blob/main/produto/imagens/tela%20principal.png?raw=true "Tela principal do software")

A tela principal consiste de dois campos de seleção de diretório, dois campos para inserção de parâmetros textuais, e os botões para iniciar e cancelar o processo.

No campo de "Entrada", deve ser definido o diretório no qual se encontram os arquivos CSV a serem analisados. É importante destacar que todos os CSVs dentro desse diretório serão lidos, e que estes devem conter campos padronizados. Recomenda-se que este diretório contenha apenas os arquivos desejados para o estudo.

No campo de "Saída", deve ser definido o caminho para gravação dos arquivos CSV gerados pelo software. Recomenda-se que não seja o mesmo diretório de entrada, para evitar que estes sejam lidos como entrada ao se executar novamente o procedimento.

O campo "Nome da coluna" deve ser preenchido com o nome da coluna do arquivo CSV que contenha os dados textuais a serem analisados. 

Já o campo "Palavras-chave" é opcional, e deve ser preenchido com as palavras-chave desejadas nos casos em que nem todas as linhas do arquivo CSV deverão ser analisadas. Ao se utilizar esse recurso, serão consideradas apenas as linhas que contenham pelo menos uma das palavras-chave inseridas e o arquivo de saída conterá apenas as linhas classificadas.

Um exemplo de preenchimento dos campos pode ser visto na figura abaixo:

![Imagem da tela principal com os dados preenchidos](https://github.com/vitorsgoncalves/tcc-profnit/blob/main/produto/imagens/dados%20inseridos.png?raw=true "Imagem da tela principal com os dados preenchidos")

Após preencher os dados, pressione o botão "Iniciar e aguarde a execução em uma nova tela. Dependendo do tamanho dos arquivos de entrada, o processo pode levar muito tempo. Após o término, será exibido um diálogo indicando o fim da operação.

Os resultados podem ser encontrados na pasta definida como saída. O arquivo gerado é uma cópia do arquivo original, com uma nova coluna referente ao valor calculado como intensidade de sentimento. Um exemplo de arquivos gerados pode ser visto nas imagens abaixo:

Exemplo de saída de dados:

![Imagem demonstrando um exemplo de saída de dados](https://github.com/vitorsgoncalves/tcc-profnit/blob/main/produto/imagens/resultado.png?raw=true "Exemplo de arquivo de saída")

Exemplo do segundo arquivo de saída, com os números de comentários de cada tipo e as médias calculadas para cada arquivo de entrada:

![Exemplo do segundo arquivo de saída, com os números de comentários de cada tipo e as médias calculadas para cada arquivo de entrada](https://github.com/vitorsgoncalves/tcc-profnit/blob/main/produto/imagens/resultado2.png?raw=true "Exemplo do segundo arquivo de saída, com os números de comentários de cada tipo e as médias calculadas para cada arquivo de entrada")


## Limitações e observações

- O léxico utilizado pelo método VADER é baseado no idioma inglês e pode não gerar resultados aceitáveis para outros idiomas.
- A metodologia não é livre de falhas, e o valor calculado pode não corresponder adequadamente com o texto analisado em alguns casos.


## Possibilidades futuras

- Adaptar a metodologia para outros idiomas.
- Permitir a inserção de palavras-chave com operadores lógicos.
- Permitir escolher a metodologia utilizada dentre outras opções populares.

