---
title: "GPU Travelling: Efficient Confidential Collaborative Training with TEE-Enabled GPUs"
date: 2026-05-10
venue: "CCS 2025"
paper_url: "https://research.ibm.com/publications/gpu-travelling-efficient-confidential-collaborative-training-with-tee-enabled-gpus"
permalink: /posts/2026/05/gpu-travelling/
tags:
  - Paper Review
  - Hardware Security
---

<div class="paper-meta" markdown="1">

- **논문명**: GPU Travelling: Efficient Confidential Collaborative Training with TEE-Enabled GPUs
- **저자**: Shixuan Zhao, Zhongshu Gu, Md Salman Ahmed, Ray Valdez, Hani Jamjoom, Zhiqiang Lin
- **학회**: CCS 2025
- **링크**: [IBM Research](https://research.ibm.com/publications/gpu-travelling-efficient-confidential-collaborative-training-with-tee-enabled-gpus)

</div>

## Introduction

GPU Travelling은 여러 데이터 소유자가 서로의 데이터를 직접 공개하지 않고 공동으로 ML model을 학습하는 confidential collaborative training 문제를 다룹니다. Collaborative training에서는 각 data holder가 자신의 데이터를 외부에 공개하지 않으면서도, 전체 데이터의 이점을 활용해 더 좋은 모델을 만들고 싶어합니다.

기존 방식은 데이터나 모델을 반복적으로 전송해야 하므로, 모델과 데이터셋 규모가 커질수록 communication overhead가 커집니다. 특히 foundation model이나 large-scale training에서는 model parameter와 intermediate state도 크고, raw dataset은 더 클 수 있습니다. 따라서 무엇을 이동시킬지 결정하는 것이 성능과 비용에 큰 영향을 줍니다.

## Framework

### TEE-enabled GPU 이동

이 논문은 TEE-enabled GPU를 데이터가 있는 위치로 이동시키는 방식의 설계를 제안합니다. 여기서 “GPU가 이동한다”는 것은 물리적 장치를 계속 옮긴다는 의미라기보다, confidential training을 수행하는 trusted GPU execution environment가 각 data holder의 site에서 순차적으로 학습을 수행하도록 구성한다는 의미로 이해할 수 있습니다.

GPU가 각 data holder의 환경에서 protected memory로 데이터를 직접 적재한 뒤 학습을 수행하면, 대용량 raw data를 중앙 서버로 보내지 않아도 됩니다. Data holder는 자신의 data를 외부에 공개하지 않고, GPU TEE는 학습 중 data와 model state를 보호합니다. 이후 필요한 protected model update만 다음 단계로 전달됩니다.

### Communication Overhead 감소

핵심은 데이터를 중앙으로 모으는 대신, 보호된 GPU execution environment를 데이터 소유자 쪽으로 이동시키는 것입니다. 이는 “data moves to compute”가 아니라 “trusted compute moves to data”에 가까운 설계입니다.

이 방식은 communication overhead를 줄이는 동시에 privacy requirement를 만족하려고 합니다. 각 site는 raw data를 자신의 trust boundary 안에 유지하고, GPU TEE는 remote attestation을 통해 올바른 confidential environment에서 실행 중임을 증명합니다. Data holder는 attestation을 확인한 뒤에만 자신의 데이터를 GPU protected memory로 제공할 수 있습니다.

또한 collaborative training에서는 model state가 여러 site를 거치며 업데이트되기 때문에, state integrity와 confidentiality도 중요합니다. GPU Travelling은 단순 data protection이 아니라 training workflow 전체의 trust chain을 설계하는 문제입니다.

## Experiments

논문은 collaborative training 환경에서 기존 방식과 GPU Travelling의 communication cost 및 training overhead를 비교합니다. 특히 모델과 데이터셋 크기가 커질수록 데이터 이동을 줄이는 설계가 중요해진다는 점을 보여줍니다.

평가에서 중요한 관점은 보안 기능 자체의 비용뿐 아니라 시스템 배치가 만드는 비용입니다. Confidential computing을 사용하더라도, 매번 대용량 데이터를 암호화해 전송하면 communication bottleneck이 생깁니다. GPU Travelling은 데이터가 있는 곳에서 protected computation을 수행하여 이 병목을 줄이려는 architecture-level optimization입니다.

## Conclusion

제가 이 논문에서 본 핵심은 confidential computing을 단순히 "계산을 보호하는 기술"로 보지 않고, 시스템 배치와 데이터 이동 비용을 함께 최적화하는 architecture-level mechanism으로 본다는 점입니다. 보안 기능을 넣었을 때 생기는 overhead를 줄이려면, 암호화나 격리 기술만이 아니라 데이터가 어디에서 이동하고 어디에서 처리되는지도 함께 설계해야 합니다.

이 관점은 SDV controller architecture에도 연결됩니다. TEE를 어느 controller에 둘지, sensitive data를 어디까지 이동시킬지, attestation을 어느 boundary에서 수행할지에 따라 overhead와 security property가 달라집니다.
