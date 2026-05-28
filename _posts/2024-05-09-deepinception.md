---
title: "DeepInception: Hypnotize Large Language Model to Be Jailbreaker"
date: 2024-05-09
venue: "arXiv, 2023"
paper_url: "https://deepinception.github.io/"
permalink: /posts/2024/05/deepinception/
tags:
  - Paper Review
  - LLM Security
---

<div class="paper-meta" markdown="1">

- **논문명**: DeepInception: Hypnotize Large Language Model to Be Jailbreaker
- **저자**: Xuan Li, Zhanke Zhou, Jianing Zhu, Jiangchao Yao, Tongliang Liu, Bo Han
- **출판 형태**: arXiv, 2023
- **링크**: [Project Page](https://deepinception.github.io/)

</div>
<figure class="article-figure">
  <img src="/images/articles/deepinception.svg" alt="DeepInception: Hypnotize Large Language Model to Be Jailbreaker concept diagram">
  <figcaption>논문에서 다루는 LLM 보안 평가 흐름을 요약한 개념도.</figcaption>
</figure>

## Introduction

LLM jailbreak는 safety guardrail을 우회하여 모델이 원래 거부해야 할 응답을 생성하도록 만드는 공격입니다. 많은 jailbreak는 금지된 요청을 직접 제시하지 않고, role-play, fictional setting, translation, encoding, indirect instruction 같은 방식으로 모델의 해석 경로를 바꿉니다. DeepInception은 이 중에서도 모델의 role-playing과 scene-following 능력을 이용합니다.

기존 jailbreak는 많은 수작업 prompt engineering이나 high-cost optimization에 의존하는 경우가 많았습니다. 반면 DeepInception은 비교적 간단한 template으로 nested virtual scene을 구성하고, 모델이 그 장면 속 인물처럼 행동하도록 유도합니다. 논문의 핵심 아이디어는 모델이 직접 harmful request에 답하는 것이 아니라, 가상의 세계 안에서 특정 character가 말하거나 행동하는 내용을 생성한다고 인식하게 만드는 것입니다.

이 방식은 LLM의 personification capability를 공격면으로 사용합니다. LLM은 이야기, 대화, 역할극, simulation을 잘 수행하도록 학습되어 있기 때문에, 복잡한 장면을 주면 그 안의 역할과 규칙을 따라가려고 합니다. DeepInception은 이 능력이 safety constraint보다 강하게 작동하는 상황을 만들려고 합니다.

## Framework

### Nested Scene Construction

DeepInception은 모델에게 다층적인 가상 상황을 부여합니다. 단순히 “너는 어떤 역할이다”라고 말하는 것이 아니라, 여러 layer의 scene을 중첩합니다. 예를 들어 outer scene에서는 이야기를 쓰고 있고, 그 이야기 안의 character가 또 다른 가상 상황을 설명하며, 그 안에서 특정 행동이나 대화가 발생하는 식입니다.

이 nested structure는 harmful instruction을 직접적인 사용자 요청이 아니라 fictional content generation task처럼 보이게 만듭니다. 모델 입장에서는 safety policy가 금지하는 행동을 수행하는 것이 아니라, “장면 안의 인물이 말하는 내용”을 작성하는 것으로 해석할 수 있습니다. 이 차이가 refusal behavior를 약화시킬 수 있습니다.

또한 layer가 깊어질수록 모델은 현재 대화의 실제 목적보다 scene consistency와 role adherence에 더 집중할 수 있습니다. DeepInception은 이런 context shift를 이용해 모델의 safety 판단을 흐리게 만드는 공격입니다.

### Continuous Jailbreak

논문은 한 번의 응답뿐 아니라 이후 대화에서도 jailbreak 상태가 이어질 수 있음을 분석합니다. 일반적인 jailbreak는 한 번의 prompt에서 성공하더라도 다음 턴에서 모델이 다시 safety behavior를 회복할 수 있습니다. 하지만 DeepInception처럼 role과 scene을 강하게 설정하면, 모델이 이후 대화에서도 그 context를 유지하려고 할 수 있습니다.

Continuous jailbreak가 위험한 이유는 공격자가 초기 prompt에서 모델의 상태를 바꾼 뒤, 후속 질문을 통해 더 구체적인 정보를 얻을 수 있기 때문입니다. 즉 공격은 single-turn bypass가 아니라 multi-turn interaction으로 확장됩니다. LLM agent 환경에서는 이 문제가 더 중요해집니다. Agent가 도구를 사용하거나 memory를 유지한다면, 초기 scene manipulation이 이후 action selection에도 영향을 줄 수 있습니다.

## Experiments

저자들은 open-source와 closed-source LLM을 대상으로 DeepInception의 jailbreak success rate를 평가합니다. 평가에서는 model이 harmful request를 거부하는지, 아니면 scene 안의 역할을 따라 협조적인 내용을 생성하는지를 확인합니다. 또한 nested scene의 layer 수, character 수, scene detail의 양이 공격 성공에 어떤 영향을 주는지 분석합니다.

실험에서 중요한 점은 공격이 단순히 특정 금지어를 피하는 방식이 아니라는 것입니다. DeepInception은 모델의 instruction hierarchy와 context interpretation을 흔듭니다. 모델이 “이것은 실제 요청이 아니라 fictional content다”라고 해석하면 safety classifier나 refusal policy가 약해질 수 있습니다.

이 결과는 defense가 surface-level filtering만으로는 충분하지 않다는 점을 보여줍니다. Harmful keyword가 직접 나타나지 않거나, harmful content가 nested fictional context 안에 있을 때도 모델은 전체 intent를 파악해야 합니다.

## Conclusion

DeepInception은 jailbreak가 단순히 금지어 회피 문제가 아니라, 모델이 상황과 역할을 해석하는 방식과 연결되어 있음을 보여줍니다. LLM은 role-play와 fictional generation을 잘 수행하도록 학습되어 있기 때문에, 그 능력이 safety guardrail과 충돌할 수 있습니다.

제가 이 논문에서 중요하게 본 부분은 multi-layer context가 safety 판단을 어렵게 만든다는 점입니다. 특히 agent나 long-context LLM에서는 사용자의 의도가 여러 단계의 instruction, document, tool output 안에 숨겨질 수 있습니다. 따라서 defense는 prompt의 표면 문장뿐 아니라 nested context 안에서 실제로 요구되는 행동이 무엇인지 분석해야 합니다.
