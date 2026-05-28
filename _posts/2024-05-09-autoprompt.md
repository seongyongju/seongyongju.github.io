---
title: "AutoPrompt: Eliciting Knowledge from Language Models with Automatically Generated Prompts"
date: 2024-05-09
venue: "EMNLP 2020"
paper_url: "https://aclanthology.org/2020.emnlp-main.346/"
permalink: /posts/2024/05/autoprompt/
tags:
  - Paper Review
  - LLM Security
---

<div class="paper-meta" markdown="1">

- **논문명**: AutoPrompt: Eliciting Knowledge from Language Models with Automatically Generated Prompts
- **저자**: Taylor Shin, Yasaman Razeghi, Robert L. Logan IV, Eric Wallace, Sameer Singh
- **학회**: EMNLP 2020
- **링크**: [ACL Anthology](https://aclanthology.org/2020.emnlp-main.346/)

</div>

## Introduction

Pretrained language model이 어떤 지식을 학습했는지 평가하기 위해 cloze-style prompt를 사용하는 방법이 널리 쓰였습니다. 예를 들어 문장 중 일부를 `[MASK]`로 비워 두고, 모델이 어떤 token을 예측하는지 확인하면 모델 내부에 저장된 factual knowledge나 task capability를 간접적으로 볼 수 있습니다. 하지만 이 방식은 prompt wording에 매우 민감합니다. 같은 의미의 질문이라도 어떤 단어를 쓰는지, mask 앞뒤에 어떤 문맥을 두는지에 따라 모델의 예측이 크게 달라질 수 있습니다.

기존에는 이런 prompt를 사람이 직접 설계했습니다. 연구자가 여러 문장을 시도하고, validation 성능이 좋은 prompt를 고르는 방식입니다. 문제는 이 과정이 비체계적이고 재현성이 낮다는 점입니다. Prompt engineering 능력에 따라 결과가 달라지고, 사람이 직관적으로 좋은 prompt가 실제 모델에는 최적이 아닐 수 있습니다.

AutoPrompt는 gradient-guided search를 이용해 prompt를 자동으로 생성하는 방법입니다. 모델 parameter를 fine-tuning하지 않고, 입력 문장에 삽입할 trigger token을 탐색하여 pretrained model의 잠재 능력을 끌어냅니다. 이 논문은 prompt가 단순한 자연어 질문이 아니라, 모델 행동을 제어하는 interface라는 점을 명확하게 보여줍니다.

## Framework

### Trigger Token Search

AutoPrompt는 입력 문장에 trigger token을 삽입하고, masked language model의 prediction이 원하는 label에 가까워지도록 token을 탐색합니다. 예를 들어 sentiment classification task라면 입력 sentence와 `[MASK]` 사이에 여러 trigger token을 넣고, `[MASK]` 위치에서 positive 또는 negative label word가 나오도록 trigger를 조정합니다.

문제는 token이 discrete하기 때문에 일반적인 gradient descent로 직접 업데이트할 수 없다는 점입니다. AutoPrompt는 현재 trigger token의 embedding에 대한 gradient를 계산하고, 그 gradient 방향으로 loss를 줄일 가능성이 높은 vocabulary token 후보를 찾습니다. 이후 후보 token을 실제로 대입해 보며 성능이 좋은 trigger를 선택합니다. 즉 gradient는 token을 직접 바꾸는 값이 아니라, 어떤 token을 시도할지 안내하는 search signal로 사용됩니다.

이 과정은 여러 trigger position에 대해 반복됩니다. 한 위치의 token을 바꾸고, 다시 다른 위치를 바꾸며, validation objective가 좋아지는 방향으로 prompt를 개선합니다. 사람이 만든 자연스러운 문장과 달리 AutoPrompt가 찾은 trigger는 문법적으로 부자연스러울 수 있지만, 모델 내부 representation을 효과적으로 자극할 수 있습니다.

### Parameter-free Probing

모델 parameter를 fine-tuning하지 않고 prompt만 자동 생성한다는 점이 특징입니다. 이 때문에 AutoPrompt는 pretrained model 안에 이미 존재하는 knowledge나 capability를 probing하는 도구로 볼 수 있습니다. Fine-tuning을 하면 downstream data가 모델 parameter를 바꾸기 때문에, 모델이 원래 무엇을 알고 있었는지와 fine-tuning 과정에서 무엇을 배웠는지를 분리하기 어렵습니다. AutoPrompt는 parameter를 고정한 채 입력 interface만 바꾸므로 이 구분이 비교적 명확합니다.

논문은 sentiment analysis, natural language inference, relation extraction 등 여러 task에서 AutoPrompt를 적용합니다. 특히 relation extraction에서는 entity pair와 mask를 포함한 prompt를 만들어, 모델이 관계를 나타내는 label word를 예측하도록 합니다. 이는 language model이 pretraining 과정에서 얼마나 많은 relational knowledge를 획득했는지 보는 방식입니다.

이 구조는 이후 prompt attack이나 jailbreak 연구와도 연결됩니다. 모델 parameter를 바꾸지 않고 입력 token만 조작해 행동을 크게 바꿀 수 있다면, prompt는 강력한 control surface입니다. AutoPrompt는 이를 성능 향상과 probing 목적으로 사용했지만, 같은 원리는 adversarial prompt search에도 적용될 수 있습니다.

## Experiments

논문은 AutoPrompt가 manually designed prompt보다 더 나은 factual knowledge elicitation 성능을 보이고, 일부 task에서는 fine-tuning 없이도 강한 성능을 낼 수 있음을 보입니다. 중요한 점은 결과가 “자동 prompt가 사람이 만든 prompt보다 항상 자연스럽다”는 의미가 아니라는 것입니다. 오히려 AutoPrompt가 찾은 trigger는 사람이 보기에는 이상한 token sequence일 수 있습니다. 하지만 모델이 학습한 embedding space에서는 그 token들이 원하는 label prediction을 강하게 유도할 수 있습니다.

이 결과는 pretrained language model의 능력이 표면적인 자연어 prompt와 완전히 일치하지 않을 수 있음을 보여줍니다. 모델은 사람이 직관적으로 이해하는 방식과 다르게 token pattern에 반응할 수 있고, 따라서 capability evaluation도 prompt choice에 크게 의존합니다. AutoPrompt는 이 prompt sensitivity를 체계적으로 탐색하는 방법을 제공합니다.

## Conclusion

AutoPrompt는 prompt가 단순한 입력 문장이 아니라 model behavior를 강하게 제어하는 interface임을 보여줍니다. 특히 모델 parameter를 전혀 바꾸지 않고도 trigger token만으로 downstream behavior를 바꿀 수 있다는 점은 LLM security 관점에서도 중요합니다.

제가 이 논문에서 중요하게 본 부분은 자동화된 prompt search의 가능성입니다. 사람이 직접 jailbreak prompt를 만드는 방식은 한계가 있지만, gradient나 search signal을 이용하면 모델이 취약하게 반응하는 입력 패턴을 체계적으로 찾을 수 있습니다. AutoPrompt 자체는 harmful attack 논문은 아니지만, prompt optimization이 모델 행동을 얼마나 강하게 바꿀 수 있는지 보여준 초기 연구로서 이후 jailbreak mechanism analysis를 이해하는 데 기반이 됩니다.
