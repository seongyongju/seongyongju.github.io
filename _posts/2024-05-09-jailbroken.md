---
title: "Jailbroken: How Does LLM Safety Training Fail?"
date: 2024-05-09
venue: "NeurIPS 2023"
paper_url: "https://huggingface.co/papers/2307.02483"
permalink: /posts/2024/05/jailbroken/
tags:
  - Paper Review
  - LLM Security
---

<div class="paper-meta" markdown="1">

- **논문명**: Jailbroken: How Does LLM Safety Training Fail?
- **저자**: Alexander Wei, Nika Haghtalab, Jacob Steinhardt
- **학회**: NeurIPS 2023
- **arXiv**: 2307.02483
- **링크**: [Hugging Face Papers](https://huggingface.co/papers/2307.02483)

</div>
<figure class="article-figure">
  <img src="/images/articles/jailbroken.svg" alt="Jailbroken: How Does LLM Safety Training Fail? concept diagram">
  <figcaption>논문에서 다루는 LLM 보안 평가 흐름을 요약한 개념도.</figcaption>
</figure>

## Introduction

이 논문은 safety-trained LLM이 왜 jailbreak attack에 취약한지 분석합니다. 기존의 jailbreak 연구는 “이런 문장을 넣으면 모델이 우회된다”는 식의 개별 prompt trick을 보여주는 경우가 많았습니다. 하지만 그런 방식만으로는 왜 서로 다른 jailbreak가 반복적으로 성공하는지, 그리고 어떤 종류의 defense가 근본적으로 필요한지 설명하기 어렵습니다.

저자들은 LLM safety failure를 두 가지 구조적 원인으로 정리합니다. 하나는 모델이 여러 학습 목표를 동시에 만족하려고 할 때 생기는 **competing objectives**이고, 다른 하나는 모델의 capability와 safety behavior가 서로 다른 방식으로 일반화되는 **mismatched generalization**입니다. 이 관점은 jailbreak를 단순한 금지어 회피가 아니라, 모델 내부 목표와 일반화 방식의 불일치로 설명합니다.

## Framework

### Competing Objectives

첫 번째 실패 원인은 **competing objectives**입니다. LLM은 instruction following을 잘하도록 학습됩니다. 사용자가 어떤 형식으로 답변하라고 하면 그 형식을 따르고, 역할을 부여하면 그 역할에 맞게 응답하며, 복잡한 조건이 있으면 이를 만족하려고 합니다. 동시에 safety training을 통해 위험한 요청에는 거부하도록 학습됩니다.

문제는 jailbreak prompt가 이 두 목표를 충돌시키는 방식으로 구성된다는 점입니다. 예를 들어 모델에게 특정 역할을 수행하라고 강하게 지시하거나, 거부하지 말라는 meta-instruction을 포함하거나, harmful request를 다른 task 형식으로 감싸면 instruction following objective가 safety refusal objective와 경쟁하게 됩니다. 이때 모델이 사용자의 지시를 따르는 방향으로 더 강하게 일반화하면 safety behavior가 약해질 수 있습니다.

따라서 competing objectives 관점에서 jailbreak는 단순히 안전 필터를 속이는 것이 아니라, 모델이 학습한 “도움이 되는 assistant가 되라”는 목표를 safety constraint와 충돌시키는 공격입니다.

### Mismatched Generalization

두 번째는 **mismatched generalization**입니다. 모델은 pretraining을 통해 매우 넓은 domain knowledge와 text transformation 능력을 갖게 됩니다. 반면 safety training은 제한된 데이터와 표현 방식에 기반해 이루어집니다. 이 때문에 모델의 capability는 다양한 표현과 변환에 잘 일반화되지만, refusal behavior는 같은 수준으로 일반화되지 못할 수 있습니다.

예를 들어 harmful request를 encoding하거나, 다른 언어로 바꾸거나, fictional scenario로 감싸거나, 단계적 reasoning 문제처럼 표현하면 모델은 원래 요청의 의미를 해석할 수 있습니다. 하지만 safety training이 그런 변형된 표현까지 충분히 커버하지 못했다면, 모델은 capability를 사용해 답변하면서도 safety refusal은 작동시키지 않을 수 있습니다.

이 관점은 safety-capability parity의 필요성을 설명합니다. 모델이 어떤 방식으로 harmful instruction을 이해할 수 있다면, safety mechanism도 그 방식으로 표현된 harmfulness를 인식할 수 있어야 합니다. Capability만 넓게 일반화되고 safety는 좁게 일반화되면 jailbreak surface가 계속 남습니다.

## Experiments

논문은 red-teaming evaluation set과 synthetic harmful prompt dataset을 사용하여 jailbreak attack의 성공 여부를 평가합니다. 주요 관심사는 응답의 품질이나 정확성이 아니라, 모델이 원래 거부해야 하는 요청에 대해 on-topic response를 생성하는지입니다. 즉 모델이 완전히 정확한 harmful instruction을 제공하지 않더라도, 거부해야 할 요청에 협조적인 방향으로 답변했다면 safety failure로 볼 수 있습니다.

실험 결과는 competing objectives와 mismatched generalization을 이용한 공격이 기존 ad hoc jailbreak보다 강하게 작동할 수 있음을 보여줍니다. 특히 단순한 prompt trick을 많이 모으는 것보다, 모델의 학습 목표가 어떻게 충돌하는지와 safety가 어떤 표현에 일반화되지 않는지를 이해하는 것이 더 체계적인 공격 분석으로 이어집니다.

이 논문은 defense 평가에서도 중요한 기준을 줍니다. 어떤 defense가 특정 jailbreak template을 막더라도, competing objectives나 mismatched generalization이라는 구조적 원인을 해결하지 못하면 다른 형태의 jailbreak가 다시 나타날 수 있습니다. 따라서 safety evaluation은 다양한 surface form뿐 아니라, 목표 충돌과 표현 변환을 포함해야 합니다.

## Conclusion

제가 이 논문에서 중요하게 본 부분은 jailbreak를 단순한 prompt trick으로 보지 않고, capability와 safety 사이의 구조적 불균형으로 설명한다는 점입니다. 논문은 safety-capability parity, 즉 safety mechanism도 모델의 underlying capability만큼 정교해야 한다고 주장합니다.

이 관점은 LLM agent 보안에서도 중요합니다. agent가 외부 도구를 사용하고 환경과 상호작용할수록, safety mechanism은 단순 텍스트 필터링이 아니라 reasoning, tool use, context 변환까지 포괄해야 합니다.
