from experts.models import CategoryChoices

CATEGORY_CHOICES = {
    'APPLIANCE': {
        'label': '가전/수리',
        'subcategories': [
            '조명·전등 수리', '가구 조립 및 수리', '방충망·창문 보수', '욕실 타일 보수', '도어락 교체',
            '에어컨 설치 및 수리', 'TV·가전 설치 및 수리', '문 손잡이·경첩 수리', '수도꼭지/샤워기 수리'
        ]
    },
    'HEALTH': {
        'label': '헬스/스포츠',
        'subcategories': [
            '다이어트 코칭', '운동·식단관리 코칭', '등산·러닝·사이클', '복싱·격투기',
            '산전·산후 운동', '체형·거북목 교정', '필라테스·요가', '수영·아쿠아로빅·다이빙'
        ]
    },
    'BUSINESS': {
        'label': '컨설팅/비즈니스',
        'subcategories': [
            '여성 창업 컨설팅', '이력서·자기소개서 코칭', '여성 CEO 멘토링', '워킹맘 멘토링',
            '경력단절여성 컨설팅', 'SNS 브랜딩 및 운영', '여성 리더십·자기계발', '여성 프리랜서 멘토링'
        ]
    },
    'LIFESTYLE': {
        'label': '생활/라이프',
        'subcategories': [
            '인테리어·셀프시공', '반려동물 케어·펫시터', '홈카페·베이킹', '호신술·경호술',
            '방문청소·정리', '육아·베이비시터', '요리·살림·자취'
        ]
    },
}

CATEGORY_ENUM_MAP = {
    'appliance': (CategoryChoices.APPLIANCE, '가전/수리'),
    'health': (CategoryChoices.HEALTH, '헬스/스포츠'),
    'business': (CategoryChoices.BUSINESS, '컨설팅/비즈니스'),
    'lifestyle': (CategoryChoices.LIFESTYLE, '생활/라이프'),
}