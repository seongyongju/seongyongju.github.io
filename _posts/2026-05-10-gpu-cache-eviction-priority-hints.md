---
title: "Security and Performance Implications of GPU Cache Eviction Priority Hints"
date: 2026-05-10
venue: "MICRO 2025"
paper_url: "https://www.researchgate.net/publication/396662936_Security_and_Performance_Implications_of_GPU_Cache_Eviction_Priority_Hints"
permalink: /posts/2026/05/gpu-cache-eviction-priority-hints/
tags:
  - Paper Review
  - Hardware Security
---

<div class="paper-meta" markdown="1">

- **논문명**: Security and Performance Implications of GPU Cache Eviction Priority Hints
- **저자**: Qizhong Wang, Xiangyue Huang, Yanan Guo, Yuanchao Xu
- **학회**: MICRO 2025
- **DOI**: 10.1145/3725843.3756116
- **링크**: [ResearchGate](https://www.researchgate.net/publication/396662936_Security_and_Performance_Implications_of_GPU_Cache_Eviction_Priority_Hints)

</div>

## Introduction

이 논문은 GPU cache eviction priority hint가 성능 최적화와 보안에 어떤 영향을 주는지 분석하는 연구입니다. GPU에서 cache policy는 memory-intensive workload의 성능에 직접적인 영향을 줍니다. 특히 AI training, inference, graph processing처럼 memory access가 많은 workload에서는 어떤 data가 cache에 남고 어떤 data가 밀려나는지가 throughput을 좌우할 수 있습니다.

Eviction priority hint는 programmer 또는 compiler가 특정 memory access의 재사용 가능성을 hardware에 알려주는 기능입니다. 성능 관점에서는 유용하지만, microarchitectural behavior를 software가 더 세밀하게 조정할 수 있다는 것은 보안 관점에서 새로운 관찰 가능성과 공격면을 만들 수 있습니다.

## Framework

### Cache Eviction Priority Hint

Eviction priority hint는 cache line의 재사용 가능성을 하드웨어에 전달하여 cache replacement decision에 영향을 주는 기능입니다. 예를 들어 곧 다시 사용할 data는 cache에 오래 남기고, streaming access처럼 한 번만 읽을 data는 빨리 eviction되도록 hint를 줄 수 있습니다. 이를 통해 cache pollution을 줄이고, 중요한 data의 residency를 높일 수 있습니다.

GPU에서는 수많은 thread가 병렬로 memory를 접근하기 때문에 cache contention이 큽니다. Hint를 잘 사용하면 workload의 locality를 더 잘 반영할 수 있고, memory bandwidth 효율도 좋아질 수 있습니다. 하지만 hint가 cache state를 조작하는 수단이 될 수 있다는 점도 함께 봐야 합니다.

### Security Implication

Microarchitectural hint는 성능 최적화 기능인 동시에 새로운 관찰 가능성을 만들 수 있습니다. Cache side-channel은 일반적으로 cache hit/miss timing, eviction pattern, contention을 관찰하여 victim의 memory access 정보를 추론합니다. Eviction priority hint가 cache replacement behavior에 영향을 준다면, attacker가 cache state를 더 의도적으로 조작하거나 관찰할 가능성이 생깁니다.

특히 GPU가 multi-tenant cloud, AI workload, confidential computing 환경에서 더 많이 사용될수록 cache behavior는 단순한 성능 문제가 아니라 isolation과 side-channel 분석의 대상이 됩니다. 여러 workload가 같은 GPU resource를 공유할 때, cache hint가 tenant 간 interference를 키우거나 줄일 수 있습니다.

## Experiments

논문은 GPU cache hint가 workload 성능에 미치는 영향과 보안상 노출될 수 있는 behavior를 함께 분석합니다. 성능 평가에서는 hint 사용이 cache hit rate, memory traffic, kernel execution time에 어떤 영향을 주는지 확인합니다. 보안 분석에서는 hint가 cache state를 얼마나 세밀하게 제어할 수 있는지, 그리고 이 제어가 side-channel primitive로 사용될 수 있는지 살펴봅니다.

이런 연구가 중요한 이유는 성능 최적화 기능이 보안 feature와 독립적이지 않기 때문입니다. Hardware vendor는 workload 성능을 높이기 위해 hint나 prefetch, cache control 기능을 제공하지만, 이러한 기능은 protected execution 환경에서도 남아 있을 수 있습니다. 그렇다면 TEE나 confidential computing은 memory encryption만이 아니라 microarchitectural control surface까지 고려해야 합니다.

## Conclusion

제가 이 논문을 읽으며 주목한 점은 성능 최적화를 위해 추가된 microarchitectural hint가 보안 관점에서는 새로운 관찰 가능성을 만들 수 있다는 점입니다. 특히 GPU가 AI workload와 confidential computing 환경에서 더 많이 사용될수록, cache behavior는 단순한 성능 문제가 아니라 isolation과 side-channel 분석의 대상이 됩니다.

이 리뷰는 GPU-CC 및 hardware-assisted security를 이해하기 위한 선행 정리로 보았습니다. 보안 기능을 architecture에 추가할 때 overhead를 줄이는 것만큼, 기존 성능 최적화 기능이 보안 경계에 미치는 영향도 함께 고려해야 합니다.
