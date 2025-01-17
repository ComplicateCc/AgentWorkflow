

def compose_promt():
    file_path = "./Datas/"
    #读取file_path路径下的所有文件 并整合成字符串
    with open(file_path, 'r', encoding='utf-8') as f:
        reference_content = f.read()
    print(reference_content)
    
    pass

compose_promt()