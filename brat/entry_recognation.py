"""
    操作说明：
        1. pip install spacy
        2. python -m spacy download en_core_web_sm
"""

import spacy

# 加载 English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")
#
# 处理文档
# text = ("When Sebastian Thrun started working on self-driving cars at "
#         "Google in 2007, few people outside of the company took him "
#         "seriously. “I can tell you very senior CEOs of major American "
#         "car companies would shake my hand and turn away because I wasn’t "
#         "worth talking to,” said Thrun, in an interview with Recode earlier "
#         "this week.")
# doc = nlp(text)

# 分析
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# 查找命名实体、短语和概念
# for entity in doc.ents:
#    print(entity.text, entity.label_)


def entity_rec(input_file):
    entity_list_data = []
    text = ''
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            text+=line
    doc = nlp(text)
    for entity in doc.ents:
        entity_data = {}
        entity_data['entity_name'] = entity.text
        entity_data['entity_type'] = entity.label_
        entity_list_data.append(entity_data)
    return entity_list_data


print(entity_rec('test.txt'))

"""
结果如下：
[{'entity_name': 'Sebastian Thrun', 'entity_type': 'PERSON'}, {'entity_name': '2007', 'entity_type': 'DATE'}, {'entity_name': 'American', 'entity_type': 'NORP'}, {'entity_name': 'Thrun', 'entity_type': 'PERSON'}, {'entity_name': 'Recode', 'entity_type': 'ORG'}, {'entity_name': 'this week', 'entity_type': 'DATE'}]

"""
