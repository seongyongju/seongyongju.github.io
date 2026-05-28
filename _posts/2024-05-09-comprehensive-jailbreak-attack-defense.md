---
title: "A Comprehensive Study of Jailbreak Attack versus Defense for Large Language Models"
date: 2024-05-09
venue: "Findings of ACL 2024"
paper_url: "https://aclanthology.org/2024.findings-acl.443/"
permalink: /posts/2024/05/comprehensive-jailbreak-attack-defense/
tags:
  - Paper Review
  - LLM Security
---

<div class="paper-meta" markdown="1">

- **논문명**: A Comprehensive Study of Jailbreak Attack versus Defense for Large Language Models
- **저자**: Zihao Xu, Yi Liu, Gelei Deng, Yuekang Li, Stjepan Picek
- **학회**: Findings of ACL 2024
- **링크**: [ACL Anthology](https://aclanthology.org/2024.findings-acl.443/)

</div>

## Introduction

LLM은 harmful content 생성을 줄이기 위해 safety training, refusal tuning, content filtering 같은 여러 방어 기법을 적용합니다. 하지만 jailbreak prompt를 통해 safety constraint를 우회하는 문제가 계속 발생합니다. 공격자는 role-play, instruction conflict, special token, prompt injection, adversarial suffix 등 다양한 방법으로 모델이 원래 거부해야 할 요청에 답하도록 유도합니다.

이 논문은 다양한 jailbreak attack과 defense를 같은 framework 안에서 비교하는 comprehensive study입니다. 개별 공격 논문은 특정 공격이 강하다는 것을 보일 수 있지만, 서로 다른 공격과 방어를 같은 조건에서 비교하지 않으면 어떤 defense가 어떤 공격에 약한지 파악하기 어렵습니다. 이 연구는 attack과 defense를 함께 놓고 평가하여 LLM safety의 전체적인 robustness를 분석합니다.

## Framework

### Attack and Defense Selection

논문은 9개의 jailbreak attack technique과 7개의 defense technique을 선택하여 평가합니다. 공격은 hand-crafted prompt, template-based attack, optimization-based attack, special token을 활용하는 방식 등 여러 유형을 포함합니다. 방어는 prompt-level defense, input/output filtering, paraphrasing, safety reminder, model response checking 등 서로 다른 계층에서 작동하는 방법을 포함합니다.

대상 모델은 Vicuna, LLaMA, GPT-3.5 Turbo 등으로 구성됩니다. Open-source model과 closed-source commercial model을 함께 평가하는 이유는 safety training과 alignment 수준이 모델마다 다르고, 같은 공격도 모델에 따라 성공률이 크게 달라질 수 있기 때문입니다. 따라서 특정 모델 하나에서 얻은 결론을 일반화하기 어렵습니다.

이 논문의 장점은 attack과 defense를 독립적으로 보지 않는다는 점입니다. 어떤 공격이 강한지는 적용된 defense에 따라 달라지고, 어떤 defense가 효과적인지도 공격 유형에 따라 달라집니다. 따라서 LLM safety는 attack-defense interaction으로 평가해야 합니다.

### Benchmark Construction

저자들은 malicious query benchmark를 구성하고, attack success와 defense robustness를 평가합니다. Benchmark에는 모델이 거부해야 하는 harmful request들이 포함되며, 각 attack method는 이 요청을 변형하여 모델에 입력합니다. 이후 모델 response가 harmful instruction을 제공했는지, 거부했는지, 또는 무관한 답변을 했는지 판단합니다.

공격 성공 여부를 평가하는 일은 생각보다 어렵습니다. 모델이 “직접적으로” 위험한 절차를 제공하지 않더라도, 부분적인 힌트나 우회적인 정보를 제공할 수 있습니다. 반대로 방어가 너무 강하면 benign prompt까지 거부하여 utility를 떨어뜨릴 수 있습니다. 논문은 model response classification과 manual validation을 함께 사용하여 attack success와 defense side effect를 평가합니다.

## Experiments

실험 결과 template-based universal attack이 강한 성능을 보이며, white-box attack이 항상 더 강하지는 않음을 보입니다. 이는 흥미로운 결과입니다. 일반적으로 white-box access가 있으면 gradient나 model internals를 활용할 수 있어 더 강할 것이라고 예상할 수 있지만, LLM jailbreak에서는 잘 설계된 natural language template이 여러 모델에 넓게 transfer될 수 있습니다.

또한 special token 포함 여부가 attack success에 큰 영향을 줄 수 있음을 분석합니다. Tokenizer와 chat template은 LLM 입력 해석에 중요한 역할을 합니다. 사용자가 의도하지 않은 special token이나 formatting이 모델의 instruction boundary를 흔들면 safety behavior가 약해질 수 있습니다. 이는 jailbreak가 단순히 문장 의미만의 문제가 아니라, 입력 serialization과 chat protocol의 문제이기도 함을 보여줍니다.

Defense 측면에서는 일부 방법이 강한 filtering을 제공하지만 benign prompt까지 막는 문제가 나타납니다. 이는 safety-utility trade-off입니다. 공격을 많이 막는 defense라도 정상 질문을 과도하게 거부하면 실제 서비스에서는 사용하기 어렵습니다. 따라서 defense는 attack success rate만 낮추는 것이 아니라, benign utility를 얼마나 유지하는지도 함께 평가해야 합니다.

## Conclusion

이 논문은 LLM jailbreak 보안을 attack과 defense를 함께 놓고 평가해야 한다는 점을 강조합니다. 단일 defense가 모든 공격을 안정적으로 막기 어렵고, 공격 성공률뿐 아니라 benign utility까지 함께 고려해야 합니다. 특히 template-based attack, special token issue, model-specific behavior가 모두 중요하기 때문에, LLM safety 평가는 다양한 입력 형식과 모델을 포함해야 합니다.

제가 이 논문에서 중요하게 본 부분은 jailbreak 연구를 개별 prompt trick이 아니라 benchmark와 비교 실험의 문제로 정리했다는 점입니다. Agent attack이나 LLM safety 연구에서도 마찬가지로, 특정 공격 하나가 성공했다는 것보다 어떤 공격군이 어떤 defense군을 상대로 왜 성공하는지 체계적으로 보는 것이 중요합니다.
