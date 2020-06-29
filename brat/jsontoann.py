import json


# json 转为单个txt 文本
def json_txt(f):
    with open(f) as f:
        content = f.readlines()
    for line in content:
        # line = json.loads(line)
        l = json.loads(line)
        with open("./train/" + l['id'] + ".txt", "a+") as fs:
            fs.write(l['text'])
        # print(l['text'])


# json_txt('train.json')


# # json 转为单个ann 文本
def json_ann(f):
    with open(f) as f:
        content = f.readlines()
    for line in content:
        # line = json.loads(line)
        l = json.loads(line)
        arguments_length = len(l['event_list'][0]['arguments'])
        t_list = []
        t_list.append("T1" + "\t" + l['event_list'][0]['class'] + " "  + str(l['event_list'][0]['trigger_start_index']) +  " "  + \
            str(int(l['event_list'][0]['trigger_start_index']) + len(l['event_list'][0]['trigger'])) +  "\t" + l['event_list'][0]['trigger'] )
        e = "E1" + "\t" + l['event_list'][0]['event_type'] + ":T1" + " "
        for i in range(int(arguments_length)):
            t_string = "T" + str(i+2) + "\t" + l['event_list'][0]['arguments'][i]['role'] + " " + \
                       str(l['event_list'][0]['arguments'][i]['argument_start_index']) +  " " +  \
                       str(int(l['event_list'][0]['arguments'][i]['argument_start_index']) + int(len(l['event_list'][0]['arguments'][i]['argument']))) + "\t" + \
                       l['event_list'][0]['arguments'][i]['argument']
            e = e + l['event_list'][0]['arguments'][i]['role'] + ":"+ "T" + str(i+2) + " "
            # with open("./sample_ann/" + l['id'] + ".ann", "w") as fs:
            t_list.append(t_string)
            # print(t_string)

        t_list.append(e)
        with open("./train_ann/" + l['id'] + ".ann", "w") as fs:
            for t in t_list:
                fs.write(t)
                fs.write('\n')

        # print(arguments_length)
        # with open("./sample_ann/"+ l['id'] + ".ann", "w") as fs:
        #    arguments_length = len(l['event_list'][0]['arguments'])

json_ann('train.json')