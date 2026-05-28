---
title: "Synthetic Data from Diffusion Models Improves ImageNet Classification"
date: 2025-05-10
venue: "arXiv, 2023"
paper_url: "https://arxiv.org/abs/2304.08466"
permalink: /posts/2025/05/synthetic-data-diffusion-imagenet/
tags:
  - Paper Review
  - Machine Learning
---

<div class="paper-meta" markdown="1">

- **논문명**: Synthetic Data from Diffusion Models Improves ImageNet Classification
- **저자**: Shekoofeh Azizi, Simon Kornblith, Chitwan Saharia, Mohammad Norouzi, David J. Fleet
- **출판 형태**: arXiv, 2023
- **링크**: [arXiv](https://arxiv.org/abs/2304.08466)

</div>
<figure class="article-figure">
  <img src="/images/articles/synthetic-data-diffusion-imagenet.svg" alt="Synthetic Data from Diffusion Models Improves ImageNet Classification concept diagram">
  <figcaption>모델 학습 및 평가 파이프라인의 핵심 구성 요소.</figcaption>
</figure>

## Introduction

Diffusion model은 고품질 이미지를 생성할 수 있게 되었지만, 생성 이미지가 discriminative task의 학습 성능을 실제로 높일 수 있는지는 별도의 문제입니다. 이미지가 사람 눈에 자연스러워 보인다고 해서 classifier 학습에 도움이 되는 것은 아닙니다. 생성 데이터가 너무 단순하거나, 실제 데이터 분포와 다르거나, label과 맞지 않는 artifact를 포함하면 오히려 성능을 해칠 수 있습니다.

이 논문은 diffusion model로 생성한 synthetic data가 ImageNet classification 성능을 개선할 수 있는지 분석합니다. 핵심 질문은 “생성 모델의 품질이 충분히 높아지면 synthetic data가 supervised classifier의 generalization을 실제로 개선할 수 있는가”입니다.

## Framework

### Class-conditional Diffusion Data

저자들은 large-scale text-to-image diffusion model을 ImageNet class 조건에 맞게 fine-tune하여 class-conditional synthetic image를 생성합니다. Class label에 맞는 prompt나 conditioning을 사용하여 특정 ImageNet category에 해당하는 이미지를 만들고, 이를 실제 ImageNet training set에 추가합니다.

중요한 점은 synthetic data가 실제 데이터를 대체하는 것이 아니라 보완한다는 것입니다. 실제 ImageNet은 이미 대규모 데이터셋이지만, class 내부 variation을 모두 포함하지는 못합니다. Diffusion model은 새로운 pose, background, lighting, texture variation을 생성하여 classifier가 더 다양한 visual pattern을 보게 할 수 있습니다.

### Synthetic Data Augmentation

핵심은 synthetic data가 단순히 이미지 수를 늘리는 것이 아니라, classifier가 generalization에 필요한 visual variation을 더 많이 보게 만든다는 점입니다. 만약 생성 이미지가 실제 training set과 거의 중복되는 형태라면 정보량이 적고, 너무 distribution 밖에 있으면 label noise가 됩니다. 따라서 좋은 synthetic data는 실제 class semantics를 유지하면서도 새로운 variation을 제공해야 합니다.

논문은 ResNet과 Vision Transformer 계열 모델에서 augmentation 효과를 평가합니다. 서로 다른 architecture에서 효과를 확인하는 이유는 synthetic data의 이점이 특정 모델 구조에만 의존하지 않는지 보기 위해서입니다.

## Experiments

논문은 diffusion model이 생성한 ImageNet sample의 FID, Inception Score, Classification Accuracy Score를 측정하고, synthetic data를 추가했을 때 classification accuracy가 향상되는지 평가합니다. Generative quality metric은 이미지가 얼마나 자연스러운지 보는 데 유용하지만, downstream task 성능과 완전히 같은 것은 아닙니다.

따라서 이 논문에서 중요한 평가는 최종 classifier accuracy입니다. Synthetic data를 추가했을 때 validation accuracy가 올라간다면, 생성 이미지가 실제로 discriminative learning에 도움이 되었다고 볼 수 있습니다. 또한 synthetic data의 양과 실제 데이터와의 비율도 중요합니다. 너무 많은 synthetic data는 distribution bias를 만들 수 있고, 너무 적으면 효과가 작을 수 있습니다.

## Conclusion

이 논문은 synthetic data가 generative model의 품질 평가를 넘어서 downstream classifier 학습에 실질적인 도움을 줄 수 있음을 보여줍니다. Federated Learning이나 low-data setting에서도 synthetic data augmentation을 활용할 가능성을 생각해볼 수 있습니다.

제가 이 논문에서 중요하게 본 부분은 synthetic data를 “보기 좋은 이미지 생성”이 아니라 “학습에 필요한 variation 제공”이라는 관점에서 평가했다는 점입니다. Non-IID Federated Learning에서도 client별 부족한 class나 feature variation을 synthetic data로 보완할 수 있기 때문에, 이 논문은 data augmentation 기반 FL 연구를 이해하는 데 연결됩니다.
