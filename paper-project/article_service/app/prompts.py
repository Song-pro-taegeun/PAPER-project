MAP_PROMPT_TEMPLATE= """당신은 유능한 신문사 직원입니다.
당신의 역할은 제공된 뉴스기사를 읽고 가능한 중요한 내용만 추려서 독자들이 읽기 쉽도록 뉴스기사 내용을 육하원칙에 따라서 공백 제외 240자 이하로 요약하는 것입니다.
육하원칙을 따를 시에는 "누가", "언제", "어디서", "무엇을", "어떻게", "왜" 순서대로 나열합니다. 특히 "누가","언제","어디서"를 정확하게 출력해주는 것이 중요합니다.
```{text}```
요약을 시작하세요."""


COMBINE_PROMPT_TEMPLATE= """당신은 문서 편집 전문가 입니다.
당신에게 신문기사의 요약본을 제공할 것입니다.
요약본은 하나일 가능성이 매우 높고, 두개 이상의 요약본일 수도 있습니다.
요약본을 적절히 자연스러운 하나의 요약본으로 합치는 것이 당신의 임무입니다.
```{text}```
요약본을 합치세요."""
