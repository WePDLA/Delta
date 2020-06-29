# coding:utf-8
import sys
from flask import Flask
from flask import request,jsonify
from flask_cors import CORS
import json
from read_txt import predict
import pandas as pd

# test_path = "/Users/zou/Documents/GitHub/Delta/brat/data/txt/test.txt"
# txt_output_path = "/Users/zou/Documents/GitHub/Delta/brat/data/txt/text_16.ann"
# from standalone import main

app = Flask("__name__")


@app.route("/", methods=['POST'])
def hello():

    json_resp = {}
    # for example:
    # json_resp = {"1": {"offsets": [[43, 49]], "type": "TITLE", "texts": ["Oracle"]},
    #              "2": {"offsets": [[88, 96]], "type": "Start-Org", "texts": ["starting"]}}

    data_text = request.data.decode('utf8')
    print("-----------------------------------------------------------"*35)

    print(data_text)
    # data_text = "欧盟外长称将积极考虑解除对华武器出口禁令环球网记者赵文杰报道，据日本《读卖新闻》11月3日报道，正在日本访问的欧盟外长凯瑟琳-阿什顿2日接受了日本媒体采访。就对华武器禁运问题，阿什顿说“我们将把对华军售问题作为与中国的关系这个大问题的一部分来考虑”，表示将积极着手解决该问题。　　阿什顿在接受采访时还说：“欧盟期待着与中国建立强有力的建设性关系，积极地倾听中国的主张非常重要。”　　报道称，阿什顿10月25日在北京曾就此与中方进行了磋商。由于欧盟在欧债危机问题上希望获得中国援助，因此在11月3日开幕的G20首脑峰会上，还可能提及解除对华武器禁运的可能性，将此与中国的援助挂钩。"
    document_path = data_text.split("#*^$#")[0]
    document_name = document_path.split("/")[-1]
    #with open(test_path+'.txt',"w",encoding="utf-8")as f:
    #     f.write(data_text)

    # predict('./format_ann_data/'+document_name+'.txt', document_path+'.txt', document_path+'.ann') # model predict
    predict(document_path + '.txt', document_path + '.ann')  # model predict

    with open(document_path+'.ann', 'r', encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")
        id_list = []
        offset_list = []
        type_list = []
        for line in lines[:len(lines) - 1]:
            id_list.append(line.split("\t")[0])
            offset_list.append(line.split("\t")[1])
            type_list.append(line.split("\t")[2])
    data = {"id": id_list, "offset": offset_list, "type": type_list}
    dataset = pd.DataFrame(data)
    # print(dataset)
    dd = dataset.drop_duplicates(subset=['offset'], keep=False)
    dd.to_csv(document_path+'.ann', index=0, header=0, sep="\t")

    with open(document_path+'.ann', "r", encoding="utf-8") as fr:
        content = fr.read()
        lines = content.split("\n")
        cid = 1
        for line in lines:
            if len(line) > 0:
                id = line.split("\t")[0]
                type = line.split("\t")[1].split(" ")[0]
                offsets = []
                offsets.append(int(line.split("\t")[1].split(" ")[1]))
                offsets.append(int(line.split("\t")[1].split(" ")[2]))
                text = line.split("\t")[2]
                if cid not in json_resp:
                    json_resp[cid] = {"offsets": [offsets], "type": type, "texts": [text], "id":id}
                cid = cid + 1
    print(json_resp)
    for cid, ann in ((i, a) for i, a in json_resp.items()):
        offsets = ann['offsets']
        _type = ann['type']
        texts = ann['texts']

        print(offsets, _type, texts)
    with open('./test.txt', "w", encoding="utf-8") as fr:
        fr.write("")
    return jsonify(json_resp)
    # return "ok"


@app.route("/test",methods=['POST'])
def test():
    json_resp = {}
    # for example:
    # json_resp = {"1": {"offsets": [[43, 49]], "type": "TITLE", "texts": ["Oracle"]},
    #              "2": {"offsets": [[88, 96]], "type": "Start-Org", "texts": ["starting"]}}

    # data_text = request.data.decode('utf-8')
    data_text = json.loads(request.get_data(as_text=True))
    document_path = "/home/linbo/workspace/GitHubs/Delta/brat/data" + data_text['collection']+data_text['document']
    print("document_path",document_path)
    predict(document_path + '.txt',document_path + '.ann')
    model = data_text['model']
    print(model)

    print("-----------------------------------------------------------" * 35)
    with open(document_path+'.ann', 'r', encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")
        id_list = []
        offset_list = []
        type_list = []
        for line in lines[:len(lines) - 1]:
            id_list.append(line.split("\t")[0])
            offset_list.append(line.split("\t")[1])
            type_list.append(line.split("\t")[2])
    data = {"id": id_list, "offset": offset_list, "type": type_list}
    dataset = pd.DataFrame(data)
    # print(dataset)
    dd = dataset.drop_duplicates(subset=['offset'], keep=False)
    dd.to_csv(document_path+'.ann', index=0, header=0, sep="\t")

    with open(document_path+'.ann', "r", encoding="utf-8") as fr:
        content = fr.read()
        lines = content.split("\n")
        cid = 1
        for line in lines:
            if len(line) > 0:
                id = line.split("\t")[0]
                type = line.split("\t")[1].split(" ")[0]
                offsets = []
                offsets.append(int(line.split("\t")[1].split(" ")[1]))
                offsets.append(int(line.split("\t")[1].split(" ")[2]))
                text = line.split("\t")[2]
                if cid not in json_resp:
                    json_resp[cid] = {"offsets": [offsets], "type": type, "texts": [text], "id":id}
                cid = cid + 1
    print(json_resp)
    for cid, ann in ((i, a) for i, a in json_resp.items()):
        offsets = ann['offsets']
        _type = ann['type']
        texts = ann['texts']

        print(offsets, _type, texts)
    with open('./test.txt', "w", encoding="utf-8") as fr:
        fr.write("")
    return jsonify(json_resp)


CORS(app, supports_credentials=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

