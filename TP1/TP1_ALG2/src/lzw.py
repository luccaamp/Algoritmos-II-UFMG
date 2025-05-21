import matplotlib.pyplot as plt
import time
import sys
import os

class Prefix_Trie_Node:
    def __init__(self):
        self.children = {}
        self.value = None

class Prefix_Trie:
    def __init__(self):
        self.root = Prefix_Trie_Node()

    def insert(self, key, value):
        node = self.root
        i = 0
        while i < len(key):
            # Encontrar o maior prefixo compartilhado entre o nó atual e a chave
            found_prefix = False
            for child_key in node.children:
                common_length = self._common_prefix_length(child_key, key[i:])
                if common_length > 0:
                    found_prefix = True
                    # Dividir o nó existente, se necessário
                    if common_length < len(child_key):
                        new_child = Prefix_Trie_Node()
                        new_child.children[child_key[common_length:]] = node.children[child_key]
                        new_child.value = node.children[child_key].value
                        node.children[child_key[:common_length]] = new_child
                        del node.children[child_key]
                    # Avançar para o próximo nó
                    node = node.children[child_key[:common_length]]
                    i += common_length
                    break
            # Se não houver prefixo comum, criar um novo nó
            if not found_prefix:
                node.children[key[i:]] = Prefix_Trie_Node()
                node = node.children[key[i:]]
                i = len(key)
        node.value = value

    def search(self, key):
        node = self.root
        i = 0
        while i < len(key):
            found_prefix = False
            for child_key in node.children:
                if key[i:].startswith(child_key):
                    found_prefix = True
                    node = node.children[child_key]
                    i += len(child_key)
                    break
            if not found_prefix:
                return None
        return node.value

    def _common_prefix_length(self, s1, s2):
        # Encontra o tamanho do prefixo comum entre duas strings
        min_length = min(len(s1), len(s2))
        for i in range(min_length):
            if s1[i] != s2[i]:
                return i
        return min_length
    
    def delete(self, key):
        def _delete(node, key, depth):
            # Caso base: se o fim da chave foi alcançado
            if depth == len(key):
                # Se o valor não existe, a chave não está na árvore
                if node.value is None:
                    return False
                # Remove o valor do nó
                node.value = None
                # Verifica se o nó pode ser removido (sem filhos)
                return len(node.children) == 0

            # Pega o próximo prefixo da chave
            prefix_found = None
            for child_key in node.children:
                if key[depth:].startswith(child_key):
                    prefix_found = child_key
                    break

            if prefix_found is None:
                # Chave não encontrada na árvore
                return False

            # Recursivamente remove a chave do filho
            should_delete_child = _delete(node.children[prefix_found], key, depth + len(prefix_found))

            # Se o nó filho deve ser removido, faça isso
            if should_delete_child:
                del node.children[prefix_found]

            # Retorna True se este nó não tiver mais filhos e nenhum valor
            return len(node.children) == 0 and node.value is None

        # Inicia a deleção recursiva a partir da raiz
        _delete(self.root, key, 0)


def lzw_fixo_codificacao(input_file, output_file, max_bits=12):
    max_dict_size = 2 ** max_bits 
    start_time = time.time()  # Marca o início da execução

    # Variáveis para rastrear estatísticas
    estatisticas = {
        "tempo": [],
        "tamanho_dicionario": [],
        "dados_processados": [],
    }
    
    # Inicializa a árvore de prefixo com caracteres ASCII, representados como strings
    dicionario = Prefix_Trie()
    for i in range(256):
        dicionario.insert(chr(i), i)  # Insere o caractere como string

    codigo = 256  # Próximo código disponível após caracteres ASCII
    resultado = []  # Lista para armazenar os códigos da compressão

    # Lê o arquivo de entrada como binário
    with open(input_file, "rb") as f:
        dados = f.read()

    p = ""  # Prefixo inicial (string)
    bytes_processados = 0
    for c in dados:
        c = chr(c)  # Converte caractere para string
        pc = p + c  # Concatena prefixo e caractere
        # Se pc está no dicionário, atualiza p para pc
        if dicionario.search(pc) is not None:
            p = pc
        else:
            # Adiciona o código do prefixo atual ao resultado
            resultado.append(dicionario.search(p))

            # Se o dicionário ainda não alcançou o tamanho máximo, adiciona pc a ele
            if codigo < max_dict_size:
                dicionario.insert(pc, codigo)
                codigo += 1

            # Atualiza o prefixo p para o caractere atual
            p = c

        # Atualiza estatísticas a cada 1000 bytes processados
        bytes_processados += 1
        if bytes_processados % 1000 == 0:
            tempo_decorrido = time.time() - start_time
            estatisticas["tempo"].append(tempo_decorrido)
            estatisticas["tamanho_dicionario"].append(codigo)
            estatisticas["dados_processados"].append(bytes_processados)

    # Adiciona o código do último prefixo, se existir
    if p:
        resultado.append(dicionario.search(p))

    # Escreve os códigos comprimidos no arquivo de saída em formato binário (12 bits por código)
    with open(output_file, "wb") as f:
        buffer = 0
        buffer_bits = 0

        for code in resultado:
            buffer |= code << buffer_bits
            buffer_bits += 12

            # Quando o buffer tiver mais de 8 bits, escrevemos no arquivo
            while buffer_bits >= 8:
                byte = buffer & 0xFF
                f.write(bytes([byte]))
                buffer >>= 8
                buffer_bits -= 8

        # Escreve qualquer dado restante que não tenha sido escrito
        if buffer_bits > 0:
            f.write(bytes([buffer & 0xFF]))

    end_time = time.time()  # Marca o fim da execução
    execution_time = end_time - start_time  # Calcula o tempo total
    print(f"Tempo de execução da codificação: {execution_time:.4f} segundos")

    return estatisticas


def lzw_fixo_decodificacao(input_file, output_file, max_bits=12):
    max_dict_size = 2 ** max_bits
    start_time = time.time()  # Marca o início da execução

    # Variáveis para rastrear estatísticas
    estatisticas = {
        "tempo": [],
        "tamanho_dicionario": [],
        "dados_processados": [],
    }
    
    # Inicializa a árvore de prefixo invertida com caracteres ASCII
    dicionario = Prefix_Trie()
    for i in range(256):
        dicionario.insert(str(i), bytes([i]))

    codigo = 256  # Próximo código disponível após caracteres ASCII

    # Lê o arquivo de entrada comprimido como binário
    with open(input_file, "rb") as f:
        dados_comprimidos = f.read()

    # Recupera os códigos (12 bits cada) do arquivo comprimido
    codigos = []
    buffer = 0
    buffer_bits = 0
    for byte in dados_comprimidos:
        buffer |= byte << buffer_bits
        buffer_bits += 8

        while buffer_bits >= 12:
            codigos.append(buffer & 0xFFF)  # Extrai 12 bits
            buffer >>= 12
            buffer_bits -= 12

    # Decodifica os códigos
    resultado = bytearray()
    if not codigos:
        return  # Arquivo vazio

    # Pega o primeiro código e escreve no resultado
    codigo_anterior = codigos[0]
    resultado += dicionario.search(str(codigo_anterior))

    # Estatísticas iniciais
    bytes_processados = len(resultado)
    estatisticas["tempo"].append(0)  # Tempo inicial
    estatisticas["tamanho_dicionario"].append(codigo)
    estatisticas["dados_processados"].append(bytes_processados)

    for i, codigo_atual in enumerate(codigos[1:], start=1):
        if dicionario.search(str(codigo_atual)) is not None:
            entrada = dicionario.search(str(codigo_atual))
        else:
            # Caso especial: quando o código atual ainda não está no dicionário
            entrada = dicionario.search(str(codigo_anterior)) + dicionario.search(str(codigo_anterior))[0:1]

        # Adiciona a entrada decodificada ao resultado
        resultado += entrada

        # Adiciona o novo código ao dicionário, se houver espaço
        if codigo < max_dict_size:
            nova_entrada = dicionario.search(str(codigo_anterior)) + entrada[0:1]
            dicionario.insert(str(codigo), nova_entrada)
            codigo += 1

        # Atualiza o código anterior
        codigo_anterior = codigo_atual

        # Atualiza estatísticas a cada 1000 códigos processados
        if i % 1000 == 0:
            tempo_decorrido = time.time() - start_time
            estatisticas["tempo"].append(tempo_decorrido)
            estatisticas["tamanho_dicionario"].append(codigo)
            estatisticas["dados_processados"].append(len(resultado))

    # Escreve os dados decodificados no arquivo de saída
    with open(output_file, "wb") as f:
        f.write(resultado)

    end_time = time.time()  # Marca o fim da execução
    execution_time = end_time - start_time  # Calcula o tempo total
    print(f"Tempo de execução da decodificação: {execution_time:.4f} segundos")

    return estatisticas


def variavel_codificacao(input_file, output_file, max_bits=12):
    start_time = time.time()  # Marca o início da execução
    # Inicializa a árvore de prefixo com caracteres ASCII
    dicionario = Prefix_Trie()
    for i in range(256):
        dicionario.insert(bytes([i]), i)

    codigo = 256  # Próximo código disponível após caracteres ASCII
    resultado = []  # Lista para armazenar os códigos da compressão

    # Parâmetros de controle de tamanho de código
    tamanho_codigo = 9
    max_dict_size = 2 ** tamanho_codigo  # Tamanho máximo do dicionário para o tamanho atual de código

    estatisticas = {
        "tempo": [],
        "tamanho_dicionario": [],
        "dados_processados": [],
    } 

    # Lê o arquivo de entrada como binário
    with open(input_file, "rb") as f:
        dados = f.read()

    bytes_processados = 0

    p = b""  # Prefixo inicial (binário)
    for c in dados:
        c = bytes([c])  # Converte caractere para bytes
        pc = p + c
        # Se pc está no dicionário, atualiza p para pc
        if dicionario.search(pc) is not None:
            p = pc
        else:
            # Adiciona o código do prefixo atual ao resultado
            resultado.append(dicionario.search(p))

            # Se o dicionário ainda não alcançou o tamanho máximo, adiciona pc a ele
            if codigo < (2 ** max_bits):
                dicionario.insert(pc, codigo)
                codigo += 1

                # Verifica se precisa aumentar o tamanho do código
                if codigo >= max_dict_size and tamanho_codigo < max_bits:
                    tamanho_codigo += 1
                    max_dict_size = 2 ** tamanho_codigo

            # Atualiza o prefixo p para o caractere atual
            p = c

        # Atualiza estatísticas a cada 1000 bytes processados
        bytes_processados += 1
        if bytes_processados % 1000 == 0:
            tempo_decorrido = time.time() - start_time
            estatisticas["tempo"].append(tempo_decorrido)
            estatisticas["tamanho_dicionario"].append(codigo)
            estatisticas["dados_processados"].append(bytes_processados)

    # Adiciona o código do último prefixo, se existir
    if p:
        resultado.append(dicionario.search(p))

    # Escreve os códigos comprimidos no arquivo de saída
    with open(output_file, "wb") as f:
        buffer = 0
        buffer_bits = 0

        for code in resultado:
            buffer |= code << buffer_bits
            buffer_bits += tamanho_codigo

            # Quando o buffer tiver mais de 8 bits, escrevemos no arquivo
            while buffer_bits >= 8:
                byte = buffer & 0xFF
                f.write(bytes([byte]))
                buffer >>= 8
                buffer_bits -= 8

        # Escreve qualquer dado restante que não tenha sido escrito
        if buffer_bits > 0:
            f.write(bytes([buffer & 0xFF]))
    
    end_time = time.time()  # Marca o fim da execução
    execution_time = end_time - start_time  # Calcula o tempo total
    #print(f"Tempo de execução da codificação: {execution_time:.4f} segundos")
    return tamanho_codigo, execution_time, estatisticas


def variavel_decodificacao(input_file, output_file, bits_por_codigo, max_bits=12):
    max_dict_size = 2 ** max_bits # 4096
    start_time = time.time()  # Marca o início da execução

    # Inicializa a árvore de prefixo invertida com caracteres ASCII
    dicionario = Prefix_Trie()
    for i in range(256):
        dicionario.insert(str(i), bytes([i]))

    codigo = 256  # Próximo código disponível após caracteres ASCII

    # Estatísticas
    estatisticas = {
        "tempo": [],
        "tamanho_dicionario": [],
        "dados_processados": [],
    }

    # Lê o arquivo de entrada comprimido como binário
    with open(input_file, "rb") as f:
        dados_comprimidos = f.read()

    # Recupera os códigos (bits_por_codigo bits cada) do arquivo comprimido
    codigos = []
    buffer = 0
    buffer_bits = 0
    mascara = (1 << bits_por_codigo) - 1  # Máscara para extrair os bits necessários

    for byte in dados_comprimidos:
        buffer |= byte << buffer_bits
        buffer_bits += 8

        while buffer_bits >= bits_por_codigo:
            codigos.append(buffer & mascara)  # Extrai os bits de acordo com bits_por_codigo
            buffer >>= bits_por_codigo
            buffer_bits -= bits_por_codigo

    # Decodifica os códigos
    resultado = bytearray()
    if not codigos:
        return  # Arquivo vazio

    # Pega o primeiro código e escreve no resultado
    codigo_anterior = codigos[0]
    resultado += dicionario.search(str(codigo_anterior))
    bytes_processados = len(resultado)

    for idx, codigo_atual in enumerate(codigos[1:], start=1):
        if dicionario.search(str(codigo_atual)) is not None:
            entrada = dicionario.search(str(codigo_atual))
        else:
            # Caso especial: quando o código atual ainda não está no dicionário
            entrada = dicionario.search(str(codigo_anterior)) + dicionario.search(str(codigo_anterior))[0:1]

        # Adiciona a entrada decodificada ao resultado
        resultado += entrada

        # Adiciona o novo código ao dicionário, se houver espaço
        if codigo < max_dict_size:
            nova_entrada = dicionario.search(str(codigo_anterior)) + entrada[0:1]
            dicionario.insert(str(codigo), nova_entrada)
            codigo += 1

        # Atualiza o código anterior
        codigo_anterior = codigo_atual

        # Atualiza estatísticas a cada 1000 códigos processados
        bytes_processados += len(entrada)
        if idx % 1000 == 0:
            tempo_decorrido = time.time() - start_time
            estatisticas["tempo"].append(tempo_decorrido)
            estatisticas["tamanho_dicionario"].append(codigo)
            estatisticas["dados_processados"].append(bytes_processados)

    # Escreve os dados decodificados no arquivo de saída
    with open(output_file, "wb") as f:
        f.write(resultado)
    
    end_time = time.time()  # Marca o fim da execução
    execution_time = end_time - start_time  # Calcula o tempo total
    #print(f"Tempo de execução da decodificação: {execution_time:.4f} segundos")
    return execution_time, estatisticas


def verificar_taxa_compressao_porcentagem(input_file, compressed_file):
    # Obtém o tamanho do arquivo original em bytes
    tamanho_original = os.path.getsize(input_file)

    # Obtém o tamanho do arquivo comprimido em bytes
    tamanho_comprimido = os.path.getsize(compressed_file)

    # Calcula a taxa de compressão em porcentagem
    if tamanho_original > 0:
        taxa_compressao_percent = ((tamanho_original - tamanho_comprimido) / tamanho_original) * 100
    else:
        taxa_compressao_percent = 0

    # Exibe os resultados em porcentagem
    print(f"Tamanho original: {tamanho_original} bytes")
    print(f"Tamanho comprimido: {tamanho_comprimido} bytes")
    print(f"Taxa de compressão: {taxa_compressao_percent:.2f}%")


def verificar_igualdade_arquivos(original_file, decoded_file):
    # Lê o arquivo original
    with open(original_file, 'rb') as f1:
        original_data = f1.read()

    # Lê o arquivo decodificado
    with open(decoded_file, 'rb') as f2:
        decoded_data = f2.read()

    # Compara os conteúdos dos arquivos
    if original_data == decoded_data:
        print("Os arquivos são iguais.")
    else:
        print("Os arquivos são diferentes.")


def plot_estatisticas(estatisticas, file_label, output_dir="stats"):
    # Cria a pasta se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Define o caminho completo para o arquivo com base no nome do arquivo de entrada/saída
    output_file = os.path.join(output_dir, f"estatisticas_{file_label}.png")
    
    # Configuração do gráfico
    plt.figure(figsize=(12, 6))
    
    # Gráfico 1: Crescimento do dicionário ao longo do tempo
    plt.subplot(1, 2, 1)
    plt.plot(estatisticas["tempo"], estatisticas["tamanho_dicionario"], label="Tamanho do Dicionário")
    plt.xlabel("Tempo Decorrido (s)")
    plt.ylabel("Tamanho do Dicionário")
    plt.title("Crescimento do Dicionário")
    plt.legend()
    
    # Gráfico 2: Dados processados ao longo do tempo
    plt.subplot(1, 2, 2)
    plt.plot(estatisticas["tempo"], estatisticas["dados_processados"], label="Dados Processados (bytes)")
    plt.xlabel("Tempo Decorrido (s)")
    plt.ylabel("Bytes Processados")
    plt.title("Dados Processados ao Longo do Tempo")
    plt.legend()
    
    plt.tight_layout()
    
    # Salva o gráfico na pasta especificada
    plt.savefig(output_file)
    plt.close()  # Fecha o gráfico para liberar memória

    print(f"Gráficos de estatísticas salvos em: {output_file}")


def salvar_informacoes(output_file, tempo_execucao, tamanho_original, tamanho_comprimido, taxa_compressao, output_dir="stats"):
    # Cria a pasta 'stats' se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Extrai o nome base do arquivo de saída
    base_name = os.path.splitext(os.path.basename(output_file))[0]
    
    # Define o caminho completo para o arquivo de informações
    info_file = os.path.join(output_dir, f"{base_name}.txt")

    # Cria o conteúdo do arquivo de informações
    conteudo = (
        f"Tempo total de execução: {tempo_execucao:.4f} segundos\n"
        f"Tamanho original: {tamanho_original} bytes\n"
        f"Tamanho comprimido: {tamanho_comprimido} bytes\n"
        f"Taxa de compressão: {taxa_compressao:.2f}%\n"
    )

    # Salva o conteúdo no arquivo
    with open(info_file, "w") as f:
        f.write(conteudo)

    print(f"Informações salvas em: {info_file}")


def main():
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Uso: python3 ./src/variado.py <f|v> <c|d> <arquivo_entrada> <arquivo_saida> [max_bits]")
        sys.exit(1)

    tipo = sys.argv[1]  # 'f' para fixo ou 'v' para variável
    operacao = sys.argv[2]  # 'c' para codificação ou 'd' para decodificação
    arquivo_entrada = sys.argv[3]
    arquivo_saida = sys.argv[4]
    max_bits = int(sys.argv[5]) if len(sys.argv) > 5 else 12

    base_name = os.path.splitext(os.path.basename(arquivo_entrada))[0]

    # Verificar se o diretório ./output existe, se não existir então criar ele
    output_dir = os.path.dirname(arquivo_saida)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if tipo not in ['f', 'v']:
        print("Erro: O tipo deve ser 'f' (fixo) ou 'v' (variável).")
        sys.exit(1)

    if operacao not in ['c', 'd']:
        print("Erro: A operação deve ser 'c' (codificação) ou 'd' (decodificação).")
        sys.exit(1)

    if tipo == 'f':
        print("LZW Tamanho Fixo:")
        if operacao == 'c':
            print(f"Comprimindo {arquivo_entrada} para {arquivo_saida} com max_bits={max_bits}...")
            f_estatisticas_c = lzw_fixo_codificacao(arquivo_entrada, arquivo_saida, max_bits)
            verificar_taxa_compressao_porcentagem(arquivo_entrada, arquivo_saida)
            plot_estatisticas(f_estatisticas_c, f"{base_name}Comp")
            # Verificar e calcular a taxa de compressão
            tamanho_original = os.path.getsize(arquivo_entrada)
            tamanho_comprimido = os.path.getsize(arquivo_saida)
            taxa_compressao_percent = ((tamanho_original - tamanho_comprimido) / tamanho_original) * 100
            # Salvar informações em um arquivo .txt
            salvar_informacoes(
                arquivo_saida,
                tempo_execucao=f_estatisticas_c["tempo"][-1],
                tamanho_original=tamanho_original,
                tamanho_comprimido=tamanho_comprimido,
                taxa_compressao=taxa_compressao_percent,
            )
        elif operacao == 'd':
            print(f"Descomprimindo {arquivo_entrada} para {arquivo_saida} com max_bits={max_bits}...")
            f_estatisticas_d = lzw_fixo_decodificacao(arquivo_entrada, arquivo_saida, max_bits)

            name = base_name.replace("_comprimido", "")
            plot_estatisticas(f_estatisticas_d, f"{name}Decomp")
        else:
            print("Opção inválida! Use 'c' para compressão ou 'd' para descompressão.")
            sys.exit(1)
    elif tipo == 'v':
        print("LZW Tamanho Variável:")
        if operacao == 'c':
            print(f"Comprimindo {arquivo_entrada} para {arquivo_saida} com max_bits={max_bits}...")
            bits, tempo, v_estatisticas_c = variavel_codificacao(arquivo_entrada, arquivo_saida, max_bits)
            print(f"Tempo de execução da codificação: {tempo:.4f} segundos")
            print(f"Cada código tem {bits} bits")
            verificar_taxa_compressao_porcentagem(arquivo_entrada, arquivo_saida)
            plot_estatisticas(v_estatisticas_c, f"{base_name}Comp")
            # Verificar e calcular a taxa de compressão
            tamanho_original = os.path.getsize(arquivo_entrada)
            tamanho_comprimido = os.path.getsize(arquivo_saida)
            taxa_compressao_percent = ((tamanho_original - tamanho_comprimido) / tamanho_original) * 100  
            # Salvar informações em um arquivo .txt
            salvar_informacoes(
                arquivo_saida,
                tempo_execucao=v_estatisticas_c["tempo"][-1],
                tamanho_original=tamanho_original,
                tamanho_comprimido=tamanho_comprimido,
                taxa_compressao=taxa_compressao_percent,
            )       
        elif operacao == 'd':
            print(f"Descomprimindo {arquivo_entrada} para {arquivo_saida} com max_bits={max_bits}...")
            # Identificar o nome original do arquivo
            nome_arquivo_saida = os.path.basename(arquivo_saida)
            nome_original = nome_arquivo_saida.replace("_descomprimido", "")
            # Extrair o formato do arquivo (assumindo que a extensão está no nome)
            formato = nome_original.split('.')[-1]
            # Montar o caminho do arquivo de entrada correspondente
            caminho_input = os.path.join("./input", formato, nome_original)
            # Chamar a função de codificação
            bits, t, v_estatisticas_c = variavel_codificacao(caminho_input, arquivo_saida, max_bits)

            tempo, v_estatisticas_d = variavel_decodificacao(arquivo_entrada, arquivo_saida, bits, max_bits)
            print(f"Tempo de execução da decodificação: {tempo:.4f} segundos")

            name = base_name.replace("_comprimido", "")
            plot_estatisticas(v_estatisticas_d, f"{name}Decomp")

            # Verificar se os arquivos são iguais após a descompressão
            verificar_igualdade_arquivos(caminho_input, arquivo_saida)
        else:
            print("Opção inválida! Use 'c' para compressão ou 'd' para descompressão.")
            sys.exit(1)

if __name__ == "__main__":
    main()
