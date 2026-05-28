---
title: "Balancing Methods for Multi-label Text Classification with Long-Tailed Class Distribution"
date: 2025-05-10
venue: "EMNLP 2021"
paper_url: "https://aclanthology.org/2021.emnlp-main.643/"
permalink: /posts/2025/05/long-tailed-multilabel-balancing/
tags:
  - Paper Review
  - Machine Learning
---

<div class="paper-meta" markdown="1">

- **논문명**: Balancing Methods for Multi-label Text Classification with Long-Tailed Class Distribution
- **저자**: Yi Huang, Buse Giledereli, Abdullatif Koksal, Arzucan Ozgur, Elif Ozkirimli
- **학회**: EMNLP 2021
- **링크**: [ACL Anthology](https://aclanthology.org/2021.emnlp-main.643/)

</div>

## Introduction

Multi-label text classification은 하나의 문서가 여러 label에 동시에 속할 수 있기 때문에 label dependency를 고려해야 합니다. 예를 들어 하나의 biomedical abstract가 여러 topic에 동시에 해당하거나, 뉴스 문서가 정치와 경제 label을 동시에 가질 수 있습니다. 이 경우 label 간 co-occurrence pattern이 중요합니다.

여기에 long-tailed class distribution까지 존재하면 문제가 더 어려워집니다. Head label은 많은 sample을 가지고 있어 모델이 쉽게 학습하지만, tail label은 등장 빈도가 낮아 충분한 학습 신호를 얻기 어렵습니다. Multi-label setting에서는 tail label이 head label과 함께 등장하는 경우도 많기 때문에, 모델이 tail label을 독립적으로 학습하지 못하고 head label에 묻어버릴 수 있습니다.

이 논문은 long-tailed multi-label text classification에서 balancing method가 어떤 효과를 갖는지 분석합니다.

## Framework

### Long-tailed Multi-label Setting

Single-label classification과 달리 multi-label setting에서는 label frequency뿐 아니라 label co-occurrence도 중요합니다. Tail label은 단독으로 적게 등장할 뿐 아니라 head label과 함께 등장할 수 있어 imbalance correction이 더 복잡해집니다. 단순히 tail label sample을 oversampling하면 그 sample에 같이 붙어 있는 head label도 함께 늘어나기 때문에, 의도치 않게 head label의 영향도 다시 커질 수 있습니다.

또한 multi-label classifier는 각 label을 독립 binary classification처럼 처리하기도 하지만, 실제 label들은 서로 독립이 아닙니다. 특정 label 조합은 자주 등장하고, 어떤 label들은 거의 함께 등장하지 않습니다. 따라서 balancing method는 label별 frequency뿐 아니라 label dependency를 망가뜨리지 않는지도 고려해야 합니다.

### Balancing Methods

논문은 resampling, loss reweighting 등 class imbalance를 완화하기 위한 방법들을 multi-label text classification에 적용하고 비교합니다. Resampling은 rare label이 포함된 example을 더 자주 보게 하거나, head label 중심 sample의 비중을 줄이는 방식입니다. Loss reweighting은 tail label의 loss에 더 큰 weight를 부여하여 모델이 rare label을 무시하지 않도록 합니다.

목표는 tail label 성능을 개선하면서 전체 classification 성능을 유지하는 것입니다. Tail label만 과도하게 강조하면 head label 성능이 떨어질 수 있고, 전체 micro score는 높지만 tail label macro score는 낮은 모델이 나올 수도 있습니다. 따라서 평가 지표를 해석할 때 head-tail 성능 차이를 함께 봐야 합니다.

## Experiments

저자들은 long-tailed label distribution을 가진 multi-label text dataset에서 balancing method들을 평가합니다. 실험은 head label 중심으로 최적화된 모델이 tail label에서 성능 저하를 보일 수 있음을 보여줍니다. 특히 전체 accuracy나 micro-F1만 보면 head label 성능이 크게 반영되기 때문에 tail label 문제가 가려질 수 있습니다.

Balancing method들은 tail label recall을 개선할 수 있지만, 항상 모든 지표를 동시에 개선하는 것은 아닙니다. 따라서 어떤 application에서 tail label을 놓치는 것이 더 큰 문제인지, false positive를 늘리는 것이 더 큰 문제인지에 따라 적절한 balancing 전략이 달라집니다.

## Conclusion

이 논문은 multi-label text classification에서 imbalance 문제를 단순한 class frequency 보정으로만 다루기 어렵다는 점을 보여줍니다. Label dependency와 tail label 성능을 함께 고려하는 평가가 필요합니다.

제가 이 논문에서 중요하게 본 부분은 long-tailed distribution이 단순 데이터 수 부족 문제가 아니라 평가 지표와 label dependency 문제까지 포함한다는 점입니다. Federated Learning의 Non-IID 문제에서도 rare class나 rare label이 client별로 흩어져 있을 수 있으므로, imbalance를 어떻게 측정하고 보정할지 신중하게 봐야 합니다.
