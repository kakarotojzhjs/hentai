import os
import json

def gerar_packs_json():
    packs = []
    # Extensões de imagem/vídeo suportadas para a capa
    extensoes = ['webm', 'webp', 'jpg', 'png', 'jpeg', 'WEBM', 'WEBP', 'JPG', 'PNG', 'JPEG']
    
    # Lê o número do último pack se o arquivo ultimo.txt existir, ou assume um valor alto
    ultimo_pack = 1
    if os.path.exists('ultimo.txt'):
        try:
            with open('ultimo.txt', 'r', encoding='utf-8') as f:
                ultimo_pack = int(f.read().strip())
        except:
            pass

    # Varre a partir do último pack até o 1 (ou você pode ajustar para varrer a pasta pack/)
    if os.path.exists('pack'):
        # Pega todas as pastas dentro de 'pack/'
        pastas = os.listdir('pack')
        numeros = []
        for p in pastas:
            if p.isdigit():
                numeros.append(int(p))
        
        if numeros:
            max_num = max(numeros)
        else:
            max_num = ultimo_pack

        for i in range(max_num, 0, -1):
            pasta_pack = os.path.join('pack', str(i))
            if os.path.isdir(pasta_pack):
                info_path = os.path.join(pasta_pack, 'info.txt')
                link_path = os.path.join(pasta_pack, 'link.txt')
                
                # Verifica se info.txt e link.txt existem
                if os.path.exists(info_path) and os.path.exists(link_path):
                    try:
                        with open(info_path, 'r', encoding='utf-8') as f:
                            title = f.read().strip()
                        
                        with open(link_path, 'r', encoding='utf-8') as f:
                            link = f.read().strip()
                        
                        if not title or not link:
                            continue
                            
                        # Procura pela capa com qualquer extensão válida
                        capa_encontrada = None
                        for ext in extensoes:
                            caminho_capa = os.path.join(pasta_pack, f'capa.{ext}')
                            if os.path.exists(caminho_capa):
                                capa_encontrada = f'pack/{i}/capa.{ext}'
                                break
                        
                        if capa_encontrada:
                            packs.append({
                                "numero": i,
                                "title": title,
                                "image": capa_encontrada,
                                "link": link
                            })
                    except Exception as e:
                        print(f"Erro ao ler o pack {i}: {e}")

    # Salva o resultado no arquivo packs.json
    with open('packs.json', 'w', encoding='utf-8') as f:
        json.dump(packs, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! Arquivo packs.json atualizado com {len(packs)} packs.")

if __name__ == '__main__':
    gerar_packs_json()
                          
