import os
import json
from collections import Counter

def gerar_packs_json():
    packs = []
    extensoes = ['webm', 'webp', 'jpg', 'png', 'jpeg', 'WEBM', 'WEBP', 'JPG', 'PNG', 'JPEG']
    
    ultimo_pack = 1
    if os.path.exists('ultimo.txt'):
        try:
            with open('ultimo.txt', 'r', encoding='utf-8') as f:
                ultimo_pack = int(f.read().strip())
        except:
            pass

    if os.path.exists('pack'):
        pastas = os.listdir('pack')
        numeros = []
        for p in pastas:
            if p.isdigit():
                numeros.append(int(p))
        
        max_num = max(numeros) if numeros else ultimo_pack

        for i in range(max_num, 0, -1):
            pasta_pack = os.path.join('pack', str(i))
            if os.path.isdir(pasta_pack):
                info_path = os.path.join(pasta_pack, 'info.txt')
                link_path = os.path.join(pasta_pack, 'link.txt')
                tag_path = os.path.join(pasta_pack, 'tag.txt')
                
                if os.path.exists(info_path) and os.path.exists(link_path):
                    try:
                        with open(info_path, 'r', encoding='utf-8') as f:
                            title = f.read().strip()
                        
                        with open(link_path, 'r', encoding='utf-8') as f:
                            link = f.read().strip()
                        
                        # Lê as tags do arquivo tag.txt (se houver vírgulas, separa em lista)
                        tags_pack = ["geral"]
                        if os.path.exists(tag_path):
                            with open(tag_path, 'r', encoding='utf-8') as f:
                                conteudo_tag = f.read().strip()
                                if conteudo_tag:
                                    # Separa por vírgula e limpa os espaços de cada tag
                                    tags_pack = [t.strip().lower() for t in conteudo_tag.split(',') if t.strip()]
                        
                        if not title or not link:
                            continue
                            
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
                                "link": link,
                                "tags": tags_pack # Agora salva uma lista de tags por pack
                            })
                    except Exception as e:
                        print(f"Erro ao ler o pack {i}: {e}")

    # Salva o packs.json
    with open('packs.json', 'w', encoding='utf-8') as f:
        json.dump(packs, f, ensure_ascii=False, indent=4)

    # Conta todas as ocorrências de cada tag individualmente em todos os packs
    todas_as_tags = []
    for p in packs:
        todas_as_tags.extend(p["tags"])

    tag_counts = Counter(todas_as_tags)
    tags_list = [{"name": tag, "count": count} for tag, count in tag_counts.most_common()]
    
    # Salva o tags.json com a contagem exata de cada tag
    with open('tags.json', 'w', encoding='utf-8') as f:
        json.dump(tags_list, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! packs.json e tags.json atualizados ({len(packs)} packs).")

if __name__ == '__main__':
    gerar_packs_json()
