# 엔진 전체 동작
# 전처리 -> 의도 분류 -> 개체명 인식 -> 답변 검색

from config.DB_Config import *
from utils.database import Database
from utils.preprocess import Preprocess

p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin', userdic='../utils/user_dic.tsv')

db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
)
db.connect()

# query = '오전에 탕수육 10개 주문합니다'
# query = '탕수육 주문'
query = '짜장면 주문'


from models.intent.intent_model import IntentModel
intent = IntentModel(model_name='../models/intent/intent_model.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]


from models.ner.nermodel import NerModel
ner = NerModel(model_name='../models/ner/ner_model.h5', proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print('질문 : ', query)
print('=' * 40)
print('의도 파악 : ', intent_name)
print('개체명 인식 : ', predicts)
print('답변 검색에 필요한 NER 태그 : ', ner_tags)
print('=' * 40)


from utils.findanswer import FindAnswer
try:
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = '죄송해요, 무슨 말인지 모르겠어요.'

print('답변 : ', answer)

db.close()
