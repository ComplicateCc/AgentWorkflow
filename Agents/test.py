import os


def compose_promt():
    directory_path = "./Datas/"
    reference_content = ""
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    reference_content += f"<{filename}>\n{file_content}\n</{filename}>\n\n"
    except Exception as e:
        print(f"发生错误: {e}")
    print(reference_content)

compose_promt()