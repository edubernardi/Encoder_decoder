# Informações Básicas e Uso
Esse projeto se trata de um trabalho de implementação realizado na disclipina de Teoria da Informação: Compressão e Criptografia.

Foram construídos, na linguagem python, scripts responsáveis pela codificação e decodificação de arquivos através dos algoritmos Golomb, Elias-Gamma, Fibonacci, Unária e Delta, com o objetivo de compressão.

Também foi empregado o uso de técnicas de tratamento de ruído e correção de erro (ECC), nas formas de CRC-8 para os headers e Hamming para o bloco de dados.

Ao executar o programa na função encode são gerados dois arquivos, um arquivo com a extensão .cod apenas com a codificação, e outro com a extensão .ecc, que se trata do arquivo .cod incrementado com o tratamento de ruído. Isso é útil pois permite comparar o taxa de compressão entre os diferentes arquivos e algoritmos, além de perceber o acréscimo de tamanho ao utilizar a correção de erro.

Para a decoficação, é possível fornecer tanto o arquivo .cod quanto .ecc, o decoder realizara as operações necessárias de acordo com a extensão do documento. É interessante também comperar o tempo de execução necessário, tanto entre algoritmos diferentes quanto utilizando ou não ECC.

O uso da aplicação é feito através de parametros fornecidos na execução pela linha de comando. O arquivo principal a ser executado é encoder.py. O uso é descrito a seguir:

Para codificar um arquivo:
```
encoder.py [encode] [input file name] [output file name] [method]"
```

Para decodificar um arquivo:
```
encoder.py [decode] [input file name] [output file name]"
```

O primeiro argumento se trata da operação encode/decode, o segundo é o arquivo de entrada e o terceiro o arquivo de saída. No caso da função encode, também é necessário um quarto parâmetro, que corresponde ao algoritmo a ser empregado. Esse algoritmo pode ser informado através dos valores [1-5], de acordo com a relação:
1. Golomb
2. Elias-Gamma
3. Fibonacci
4. Unary
5. Delta

Exemplo de uso:
```
python encoder.py encode alice29.txt alice_fibonacci 3
```
O comando acima irá codificar o arquivo alice29.txt com o algoritmo Fibonacci. Como resultado, serão gerados os arquivos alice_fibonacci.cod e alice_fibonacci.ecc.

Em seguida pode ser realizado o decode dos arquivos gerados:

```
python encoder.py decode alice_golomb.ecc alice_fibonacci.txt
```
Ou
```
python encoder.py decode alice_golomb.cod alice_fibonacci.txt
```

# Detalhes da implmentação

As operações de leitura e escrita dos arquivos são realizadas byte a byte. Os cálculos realizados pelos algoritmos são realizados com auxilio da biblioteca numpy, que facilita a manipulação de sequência de bits com funções como unpackbits(), que converte um byte em um array de 8 bits.

No caso da codificação binária, foi optado por representar valores através de sequências de bits 0, separados por stop-bits 1. Os demais algoritmos não possuem diferenças consideráveis da sua proposta básica.

Para a realização das operações, é utilizado um buffer de bits que é escrito no arquivo alvo sempre que seu comprimento é divisível por 8 com resto 0 (formando um byte completo), ou quando o arquivo de entrada chega a seu fim.

Vários dos algoritmos empregados possuem eficiência maior quando trabalhando com valores menores, especialmente a codificação em Unário. Porém os caracteres ascii minúsculos, os mais usados, se iniciam no valor decimal 97. Para aumentar a eficiência na compressão nesses casos, é feita uma validação se o valor ascii médio do arquivo é maior do que 65. Se isso for verdade, é empregada um soma nos valores dos caracteres, fazendo com que os de valor entre 97 e 123 sofram uma subtração de 95, e os entre 1 e 28 uma adição de 95. Dessa forma, caracteres que são pouco usados são efetivamente trocados pelos carateres de maior uso no documento. A informação se o arquivo original se trata de um arquivo de texto é passada através de um header, assim o decoder pode realizar a operação contrária caso necessário.

No caso de falha na validação dos headers através do crc-8, o erro é apontado e o processo de decodificação é abortado. No caso de detecção de erros no corpo do arquivo, o usuário é notificado e o erro é corrigido usando as propriedades da codificação Hamming.
