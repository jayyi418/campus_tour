
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY") 

client = OpenAI(api_key=api_key) 
# 장소 요약 목록
place_list = """- 정문: 연세대학교의 정문은 캠퍼스를 상징하는 대표적인 입구입니다
- 공학원: 공학대학의 중심 건물로, 여러 공학 계열 연구실이 위치해 있습니다
- 제1공학관: 정문에 들어가자마자 백양로 왼쪽으로 보이는 공학관입니다
- 제2공학관: 실험실, 연구실이 배치되어 있는 첨단 공학 교육 공간입니다
- 제3공학관: 공과대학 교수 연구실과 일부 전공 강의실이 혼합된 건물입니다
- 제4공학관: 최신 실험장비가 구비된 공학 실험 중심 공간입니다
- 대운동장: 연세대학교 내 최대 야외 운동 시설로, 축제나 체육 행사에 자주 활용됩니다
- 야구장: 야구부 및 동아리 활동이 활발히 이루어지는 체육 공간입니다
- 과학원: 연세대학교의 기초과학 교육 중심 건물로, 물리, 화학, 생물 실험과 강의가 이루어집니다
- GS칼텍스산학협력관: 산학협력 프로그램과 연구 프로젝트가 진행되는 공간입니다
- 백양누리: 학생 복지 및 활동 공간으로 다양한  카페, 샐러디, 마호가니 카페, 스타벅스 카페, 연세 굿즈샵 등이 있습...
- 백주년기념관: 연세대학교 100주년을 기념하여, 지어진 건물로 각종 공식 행사가 열립니다
- 학생회관: 학생 복지를 위한 주요 공간으로, 식당(맛나샘, 고를샘, 부를샘) 과 편의시설이 있습니다
- 중앙도서관: 연세대학교의 주요 도서관으로 다양한 자료를 보유하고 있습니다
- 연세삼성학술정보관: 중앙도서관과 연결된 최첨단 학술 정보 공간으로 ‘신중도’라고 불립니다
- 과학관: 자연계열 기초과학 수업이 이루어지는 강의동입니다
- 삼성관: 삼성그룹의 지원으로 지어진 생활과학계열 강의동입니다
- 광복관: 강의실 중심 건물이며, 사회과학 계열 전공 수업이 많이 열리는 곳입니다
- 백양관: 연세대학교의 상징적인 건물로, 인문사회계열 수업이 주로 이루어집니다
- 대강당: 입학식, 졸업식 등 주요 행사가 열리는 중앙 강당입니다
- 루스채플: 예배 및 종교 활동이 이루어지는 연세대의 대표 채플 건물입니다
- 노천극장: 야외 공연과 아카라카 행사 등 대형 이벤트가 열리는 공연장입니다
- 음악관: 음악대학 강의 및 실습 공간으로, 연습실과 공연장이 갖춰져 있습니다
- 언더우드관: 언더우드 선교사를 기념한 건물로, 고전 건축 양식이 특징입니다
- 신학관: 신학과 관련된 강의가 이루어지는 고전적인 분위기의 건물입니다
- 한경관: 점심/저녁에 뷔페 식 학식을 제공합니다
- 외솔관: 국문학과 관련된 강의 및 연구가 이루어지는 공간입니다
- 교육과학관: 교육학 및 과학교육 관련 전공 수업이 열리는 공간입니다
- 연희관: 다양한 전공 강의가 진행되는 중형 강의동입니다
- 대우관: 대형 강의실과 세미나실이 배치된 건물입니다
- 청송대: 사시사철 푸른 소나무 숲이 우거진 연세인들의 뒷뜰입니다. 산책과 피크닉을 즐길 수 있습니다. """

# 프롬프트 생성 함수
def build_gpt_prompt(user_input: str) -> str:
    prompt = f"""너는 연세대학교 캠퍼스를 잘 아는 GPT 챗봇이야.
사용자의 질문에 어울리는 장소를 아래 장소 목록 중에서 3개 골라서 추천해줘.
각 장소 이름과 추천 이유를 한 줄로 설명해줘.

[장소 목록]
{place_list}

질문: {user_input}
답변 형식 예시:
1. 장소명 - 이유
2. 장소명 - 이유
3. 장소명 - 이유
"""
    return prompt


def recommend_place_with_gpt(user_input):
    prompt = build_gpt_prompt(user_input)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "너는 연세대학교 캠퍼스를 잘 아는 친절한 장소 추천 챗봇이야."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content.strip()

# 실행 예시
if __name__ == "__main__":
    question = input("어디가 좋을까? ▶ ")
    print("\n[GPT 추천 결과]")
    print(recommend_place_with_gpt(question))
