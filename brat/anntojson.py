import os
import json


# ann 和 txt 文件目录
ann_document_path = './sample_ann'
txt_document_path = './sample_data'


# 返回文件名称，即id
def files_name(file_dir):
    name_list = []
    files = [files for root, dirs, files in os.walk(file_dir)]
    id_list =[file.split('.')[0] for file in files[-1]]
    # print(id_list)
    return id_list


def json_file(id_list):
    json_list = []
    for id in id_list:
        json_one = {}
        with open(txt_document_path + '/' + id + '.txt', 'r') as fid:
            json_one['text'] = fid.read()
        json_one['id'] = id
        json_one['event_list'] = []
        with open(ann_document_path+'/' + id + '.ann', 'r') as fann:
            json_one_first = {}
            content_list = fann.readlines()
            event_content = content_list[0]
            event_type_content = content_list[-1]
            arguments_content = content_list[1:-1]
            event_type = event_type_content.split('\t')[1].split(':')[0]
            class1 = event_content.split('\t')[1].split(' ')[0]
            trigger = event_content.split('\t')[-1].strip()
            print(class1)

            arguments = []
            for arg in arguments_content:
                argument = {}
                argument['argument_start_index'] = arg.split('\t')[1].split(' ')[1]
                print(argument['argument_start_index'])
                argument['role'] = arg.split('\t')[1].split(' ')[0]
                argument['argument'] = arg.split('\t')[-1].strip()
                argument['alias'] = []
                arguments.append(argument)

            json_one_first['event_type'] = event_type
            json_one_first['trigger'] = trigger
            json_one_first['class'] = class1
            json_one_first['trigger_start_index'] = event_content.split('\t')[2]
            json_one_first['arguments'] = arguments
            json_one['event_list'].append(json_one_first)
        # print(json_one)
        with open('aa.json', 'a+', encoding='utf-8') as f:
            json_one_content = json.dumps(json_one, ensure_ascii=False)
            f.write(json_one_content)
            f.write('\n')


if __name__ == "__main__":
    id_list = files_name(ann_document_path)
    json_file(id_list)