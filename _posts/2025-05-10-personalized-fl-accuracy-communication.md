---
title: "Understanding the Statistical Accuracy-Communication Trade-off in Personalized Federated Learning with Minimax Guarantees"
date: 2025-05-10
venue: "ICML 2025"
paper_url: "https://proceedings.mlr.press/v267/yu25h.html"
permalink: /posts/2025/05/personalized-fl-accuracy-communication/
tags:
  - Paper Review
  - Federated Learning
---

<div class="paper-meta" markdown="1">

- **논문명**: Understanding the Statistical Accuracy-Communication Trade-off in Personalized Federated Learning with Minimax Guarantees
- **저자**: Xin Yu, Zelin He, Ying Sun, Lingzhou Xue, Runze Li
- **학회**: ICML 2025
- **링크**: [PMLR](https://proceedings.mlr.press/v267/yu25h.html)

</div>

## Introduction

Personalized Federated Learning(PFL)은 client 간 data heterogeneity를 고려하여 global model과 local model을 함께 학습하려는 접근입니다. 일반적인 FL은 하나의 global model을 모든 client가 공유하는 것을 목표로 하지만, client distribution이 크게 다르면 하나의 모델이 모든 client에 최적인 해가 되기 어렵습니다. 반대로 각 client가 자기 데이터만으로 local model을 학습하면 personalization은 되지만, 데이터가 적은 client는 충분한 성능을 얻기 어렵습니다.

PFL의 핵심 질문은 “얼마나 공유하고, 얼마나 개인화할 것인가”입니다. Local training은 communication cost가 없지만 shared knowledge를 활용하지 못하고, collaborative learning은 accuracy를 높일 수 있지만 communication cost가 발생합니다. 이 논문은 PFL에서 statistical accuracy와 communication 사이의 trade-off를 이론적으로 분석합니다.

이 연구가 중요한 이유는 personalization이 실제 FL에서 자주 필요한데도, 많은 방법이 heuristic에 의존하기 때문입니다. 어떤 상황에서 collaboration이 얼마나 필요한지, communication을 줄이면 accuracy가 얼마나 손해를 보는지, client 간 similarity가 있을 때 어떤 이득을 얻을 수 있는지를 이론적으로 설명하려고 합니다.

## Framework

### Personalization Degree

논문은 personalization degree가 sample efficiency와 algorithmic efficiency에 어떤 영향을 주는지 정량화합니다. Purely local model과 fully global model 사이에는 다양한 중간 형태가 존재합니다. 일부 parameter는 global하게 공유하고 일부는 client-specific하게 둘 수도 있고, global representation 위에 local head를 둘 수도 있으며, client similarity에 따라 cluster를 나눌 수도 있습니다.

Personalization degree가 높아지면 각 client의 특수한 distribution에 더 잘 맞출 수 있지만, 다른 client로부터 얻는 statistical benefit은 줄어들 수 있습니다. 반대로 sharing이 강해지면 data efficiency는 좋아질 수 있지만, client-specific bias를 충분히 반영하지 못합니다. 이 논문은 이러한 균형을 statistical accuracy와 communication 관점에서 분석합니다.

### Minimax Guarantees

저자들은 널리 사용되는 PFL formulation에 대해 minimax optimality 관점의 statistical accuracy guarantee를 제시합니다. Minimax guarantee는 최악의 경우에도 어떤 error rate를 달성할 수 있는지를 설명하는 이론적 기준입니다. 이를 통해 특정 algorithm이 단순히 실험적으로 잘 되는지뿐 아니라, 주어진 문제 class에서 근본적으로 어느 정도 성능이 가능한지 볼 수 있습니다.

이 관점은 PFL에서 중요합니다. Client 간 distribution이 비슷하면 collaboration의 이득이 크고, 서로 매우 다르면 personalization의 필요성이 커집니다. Minimax analysis는 이러한 client similarity와 heterogeneity가 accuracy bound에 어떻게 들어가는지 설명합니다. 따라서 personalization을 단순 heuristic이 아니라 이론적으로 해석할 수 있게 합니다.

## Experiments

이론적 결과는 synthetic dataset과 real-world dataset에서 검증됩니다. Synthetic setting은 client heterogeneity와 communication condition을 통제할 수 있기 때문에, 이론이 예측하는 trade-off가 실제로 나타나는지 확인하기 좋습니다. Real-world dataset은 실제 데이터 분포에서 personalization과 collaboration이 어떻게 작동하는지 보여줍니다.

또한 논문은 non-convex setting에서도 결과가 어느 정도 일반화될 수 있음을 확인합니다. 실제 deep learning 기반 FL은 대부분 non-convex optimization이기 때문에, 이론이 convex assumption에만 머물면 적용 범위가 제한됩니다. 실험은 이론적 insight가 실제 PFL algorithm 설계에도 의미가 있음을 보완합니다.

## Conclusion

이 논문은 PFL에서 communication을 줄이는 것과 statistical accuracy를 높이는 것이 별개의 목표가 아니라 trade-off 관계에 있음을 명확히 보여줍니다. Non-IID client 환경에서 personalization 정도를 어떻게 선택할지에 대한 이론적 기준을 제공한다는 점이 중요합니다.

제가 이 논문에서 중요하게 본 부분은 FL의 성능 문제를 단순히 “더 많이 통신하면 좋아진다” 또는 “더 개인화하면 좋아진다”로 보지 않는다는 점입니다. Client heterogeneity, sample size, communication budget이 함께 결정하는 trade-off를 이해해야 실제 시스템에서 적절한 PFL strategy를 선택할 수 있습니다.
