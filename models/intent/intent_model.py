# 의도 분류 모듈
# train_model로 핛브한 의도 분류 모델 파일을 활용

import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

class IntentModel:
    def __init__(self, model_name, proprocess):
        # self.labels = {0: '인사', 1: '욕설', 2: '주문', 3: '예약', 4: '기타'}
        self.labels = {0: '감정/감정조절이상', 1: '감정/감정조절이상/화', 2: '감정/걱정', 3: '감정/걱정/건강문제',
                       4: '감정/걱정/건강염려', 5: '감정/걱정/경제적문제', 6: '감정/걱정/미래', 7: '감정/걱정/불면',
                       8: '감정/걱정/암', 9: '감정/걱정/자녀', 10: '감정/걱정/주변평가', 11: '감정/걱정/증상재발',
                       12: '감정/고독감', 13: '감정/곤혹감', 14: '감정/공포', 15: '감정/공포/새', 16: '감정/공허감',
                       17: '감정/과민반응', 18: '감정/괴로움', 19: '감정/기분저하', 20: '감정/기시감', 21: '감정/긴장',
                       22: '감정/눈물', 23: '감정/답답', 24: '감정/답답/사람많은곳', 25: '감정/당황', 26: '감정/두려움',
                       27: '감정/두려움/운전', 28: '감정/두려움/자동차', 29: '감정/멍함', 30: '감정/모호함', 31: '감정/무력감',
                       32: '감정/무미건조', 33: '감정/무서움', 34: '감정/미안함/자녀', 35:	'감정/미움', 36: '감정/배신감',
                       37: '감정/부정적사고', 38:	'감정/분노', 39:	'감정/불만', 40:	'감정/불신', 41:	'감정/불안감',
                       42: '감정/불안감/긴장', 43:	'감정/불안감/미래', 44: '감정/불안감/증상재발', 45: '감정/불안감/초조함',
                       46: '감정/불쾌감', 47:	'감정/불편감', 48: '감정/비관적', 49: '감정/살인욕구', 50: '감정/생각',
                       51: '감정/서운함', 52:	'감정/속상함', 53: '감정/슬픔', 54: '감정/신경쓰임', 55: '감정/심란',
                       56: '감정/억울함', 57:	'감정/예민함', 58: '감정/외로움', 59: '감정/우울감', 60: '감정/우울감/눈물',
                       61: '감정/우울감/증상재발', 62: '감정/우울감/증상지속', 63: '감정/의기소침', 64: '감정/의기소침/자격지심',
                       65: '감정/의욕상실', 66: '감정/의욕상실/무기력', 67: '감정/자괴감', 68: '감정/자살충동',
                       69: '감정/자신감저하', 70: '감정/자존감저하', 71:	'감정/절망감', 72: '감정/좌절', 73: '감정/죄책감',
                       74: '감정/즐거움', 75:	'감정/짜증', 76: '감정/창피함', 77: '감정/초조함', 78: '감정/충격',
                       79: '감정/통제력상실', 80: '감정/허무함', 81: '감정/화', 82: '감정/후회', 83: '감정/후회/결혼',
                       84: '감정/힘듦', 85: '감정/힘듦/스트레스', 86: '감정/힘듦/지침', 87: '내원이유/상담',
                       88: '내원이유/의사소견', 89: '내원이유/치료', 90: '모호함', 91: '배경/가족', 92: '배경/가족/갈등',
                       93: '배경/가족/무관심', 94:	'배경/건강문제', 95: '배경/건강문제/갑상선', 96: '배경/건강문제/다이어트',
                       97: '배경/건강문제/다이어트/스트레스', 98: '배경/건강문제/생리불순', 99: '배경/건강문제/수술',
                       100: '배경/건강문제/알레르기', 101: '배경/건강문제/항암', 102: '배경/결혼', 103: '배경/결혼/미혼',
                       104: '배경/경제적문제', 105: '배경/경제적문제/가난', 106: '배경/경제적문제/빚', 107: '배경/공부',
                       108: '배경/공부/부진', 109: '배경/군대/군입대', 110: '배경/귀국', 111: '배경/남자친구',
                       112: '배경/남자친구/고민/없음', 113: '배경/남자친구/동경', 114: '배경/남자친구/없음',
                       115: '배경/남자친구/이별', 116: '배경/남자친구/집착', 117: '배경/남자친구/짧은교제', 118: '배경/남편',
                       119: '배경/남편/갈등', 120: '배경/남편/경제적문제', 121: '배경/남편/과음', 122: '배경/남편/관계소원',
                       123: '배경/남편/관계양호', 124: '배경/남편/다툼', 125: '배경/남편/무관심', 126: '배경/남편/바람',
                       127: '배경/남편/사업', 128: '배경/남편/소통불가', 129: '배경/남편/의심', 130: '배경/남편/의지',
                       131: '배경/남편/폭력', 132: '배경/대인관계', 133: '배경/대인관계/갈등', 134: '배경/대인관계/양호',
                       135: '배경/대인관계/협소', 136: '배경/대학', 137: '배경/대학/실패', 138: '배경/대학/실패/재수',
                       139: '배경/대학/입학', 140: '배경/대학/재수', 141: '배경/대학/휴학', 142: '배경/문제',
                       143: '배경/문제/과음', 144: '배경/문제/머리카락/털뽑기', 145: '배경/문제/불면', 146: '배경/문제/불안감/소변',
                       147: '배경/문제/불편감/옷', 148: '배경/문제/소변', 149: '배경/문제/알코올의존', 150: '배경/부모',
                       151: '배경/부모/가출/아버지', 152: '배경/부모/갈등', 153: '배경/부모/갈등/아버지', 154: '배경/부모/관계소원',
                       155: '배경/부모/무관심', 156: '배경/부모/싸움', 157: '배경/부모/아버지', 158: '배경/부모/아버지/죽음',
                       159: '배경/부모/아버지/폭력', 160: '배경/부모/어머니/죽음', 161: '배경/부모/이혼', 162: '배경/부모/죽음',
                       163: '배경/사고', 164: '배경/사고/교통사고', 165: '배경/사업', 166: '배경/사업/경제적문제/실패',
                       167: '배경/사업/남편/동업자', 168: '배경/사업/실패', 169: '배경/생활', 170: '배경/생활/불가능/운전',
                       171: '배경/생활/스트레스', 172: '배경/생활/양호', 173: '배경/생활/여행/해외', 174: '배경/생활/운동',
                       175: '배경/생활/자연소멸/증상', 176: '배경/생활/취미', 177: '배경/생활/폭행/피해', 178: '배경/생활/해외',
                       179: '배경/생활/혼자', 180: '배경/생활/휴식', 181: '배경/성격', 182: '배경/성격/극단적',
                       183: '배경/성격/급함', 184: '배경/성격/내성적', 185: '배경/성격/소심', 186: '배경/성격/예민함',
                       187: '배경/성격/완벽추구', 188: '배경/성격/욕심많음', 189: '배경/성격/자기중심적', 190: '배경/성격/자립적',
                       191: '배경/시댁', 192: '배경/시댁/갈등', 193: '배경/시댁/갈등/시어머니', 194: '배경/시댁/경제적문제',
                       195: '배경/아르바이트', 196: '배경/애완동물', 197: '배경/애완동물/가족/갈등', 198: '배경/어린시절',
                       199: '배경/어린시절/가난', 200: '배경/여자친구', 201: '배경/여자친구/관계소원', 202: '배경/여자친구/동거',
                       203: '배경/여자친구/이별', 204: '배경/연애', 205: '배경/연애/이별', 206: '배경/유학',
                       207: '배경/육아/힘듦', 208: '배경/음주', 209: '배경/음주/과음', 210: '배경/음주/알코올의존',
                       211: '배경/음주/애주가', 212: '배경/음주/자주', 213: '배경/이사', 214: '배경/이혼', 215: '배경/임신',
                       216: '배경/임신/낙태', 217: '배경/자각/우울증', 218: '배경/자각/정신질환', 219: '배경/자녀',
                       220: '배경/전연인', 221: '배경/종교', 222: '배경/직장', 223: '배경/직장/고민/퇴사',
                       224: '배경/직장/과도한업무', 225: '배경/직장/반복/이직', 226: '배경/직장/복직', 227: '배경/직장/불만',
                       228: '배경/직장/불만/업무', 229: '배경/직장/스트레스', 230: '배경/직장/양호', 231: '배경/직장/없음/흥미',
                       232: '배경/직장/이직', 233: '배경/직장/퇴사', 234: '배경/직장/휴직', 235: '배경/진로', 236: '배경/취업',
                       237: '배경/취업/준비', 238: '배경/취업/힘듦', 239: '배경/친구', 240: '배경/친구/관계소원',
                       241: '배경/친구/배신', 242: '배경/친구/없음', 243: '배경/타인/갈등', 244: '배경/학교',
                       245: '배경/학교/갈등/선생님', 246: '배경/학교/결석', 247: '배경/학교/따돌림', 248: '배경/학교/자퇴',
                       249: '배경/학업', 250: '배경/학업/부진', 251: '배경/학업/양호', 252: '배경/학업/우수', 253: '부가설명',
                       254: '상태/양호', 255: '상태/증상감소', 256: '원인/없음', 257: '일반대화', 258: '자가치료/심리조절',
                       259: '자가치료/심리조절/증상지속', 260: '자가치료/운동', 261: '자가치료/충분한휴식', 262: '증상/가슴답답',
                       263: '증상/가슴떨림', 264: '증상/가슴통증', 265: '증상/건강염려', 266: '증상/공격적성향',
                       267: '증상/공황발작', 268: '증상/과대망상', 269: '증상/과수면', 270: '증상/기억력저하',
                       271: '증상/기억력저하/집중력저하', 272: '증상/기억상실', 273: '증상/기절', 274: '증상/기절예기',
                       275: '증상/대인기피', 276: '증상/두근거림', 277: '증상/두근거림/불면', 278: '증상/두통',
                       279: '증상/두통/불면', 280: '증상/떨림', 281: '증상/만성피로', 282: '증상/메스꺼움', 283: '증상/무기력',
                       284: '증상/무기력/은둔', 285: '증상/무기력/의욕상실', 286: '증상/반복사고', 287: '증상/반복사고/트라우마',
                       288: '증상/반복행동', 289: '증상/반복행동/대화', 290: '증상/반복행동/문단속', 291: '증상/반복행동/손씻기',
                       292: '증상/반복행동/확인', 293: '증상/발작', 294: '증상/불면', 295: '증상/불면/불안감',
                       296: '증상/불면/생각많음', 297: '증상/불면/스트레스', 298: '증상/불면/예민함', 299: '증상/불면/증상지속',
                       300: '증상/불면/피로', 301: '증상/생리불순', 302: '증상/성격변화', 303: '증상/성욕상승',
                       304: '증상/소화불량', 305: '증상/속쓰림', 306: '증상/시력저하', 307: '증상/식욕저하',
                       308: '증상/식욕저하/불면', 309: '증상/식욕저하/체중감소', 310: '증상/신체이상/목', 311: '증상/악몽',
                       312: '증상/알코올의존', 313: '증상/어지러움', 314: '증상/은둔', 315: '증상/이명', 316: '증상/이인감',
                       317: '증상/인지기능저하', 318: '증상/자살기도', 319: '증상/자해', 320: '증상/저림현상/발/손',
                       321: '증상/죽음공포', 322: '증상/죽음공포/호흡곤란', 323: '증상/집중력저하', 324: '증상/체력저하',
                       325: '증상/체중감소', 326: '증상/체중증가', 327: '증상/컨디션저조', 328: '증상/통증', 329: '증상/통증/목',
                       330: '증상/통증/전신', 331: '증상/통증/허리', 332: '증상/편두통', 333: '증상/폭식',
                       334: '증상/폭식/스트레스/해소', 335: '증상/피로', 336: '증상/피로/불면', 337: '증상/피해망상',
                       338: '증상/피해망상/감시', 339: '증상/피해망상/감시/남편', 340: '증상/피해망상/남편',
                       341: '증상/피해망상/도청', 342: '증상/호흡곤란', 343: '증상/호흡곤란/가슴답답', 344: '증상/환각',
                       345: '증상/환청', 346: '증상/힘빠짐', 347: '치료이력/검사', 348: '치료이력/검사/이상없음',
                       349: '치료이력/병원내원', 350: '치료이력/병원내원/검사/이상없음', 351: '치료이력/병원내원/복약',
                       352: '치료이력/병원내원/이상없음', 353: '치료이력/응급실', 354: '현재상태/증상감소', 355: '현재상태/증상악화',
                       356: '현재상태/증상지속', 357: '인사', 358: '예약'}
        self.model = load_model(model_name)
        self.p = proprocess

    def predict_class(self, query):
        pos = self.p.pos(query)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        from config.globalparams import MAX_SEQ_LEN
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]
