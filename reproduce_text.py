import re


# 从文本中提取日期和对话
def extract_dialogues(text):
    dialogue_dict = {}
    matches = re.findall(r"————— (\d{4}-\d{2}-\d{2}) —————\n\n([\s\S]*?)(?=————— \d{4}-\d{2}-\d{2} —————|\Z)", text)
    print(matches)
    for match in matches:
        date = match[0]
        print(f"Date: {date}")
        dialogue = match[1]
        print(f"Dialogue: {dialogue}")
        dialogue_dict[date] = dialogue.strip()
    return dialogue_dict


if __name__ == '__main__':
    # 读取文本文件
    import os
    text_list = ['./data/text06.txt', './data/text12.txt', './data/text16.txt']
    for textpath in text_list:
        with open(textpath, 'r', encoding='utf-8') as file:
            text = file.read()

        # 提取对话
        dialogues = extract_dialogues(text)

        # 保存为对应日期的txt文件
        for date, dialogue_list in dialogues.items():
            filename = date + ".txt"
            output_path = os.path.join("./data/dialogues/", filename)
            with open(output_path, 'w', encoding="gb18030") as file:
                file.write(dialogue_list)
