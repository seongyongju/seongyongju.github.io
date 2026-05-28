---
title: "vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention"
date: 2026-05-10
venue: "ASPLOS 2025"
paper_url: "https://www.microsoft.com/en-us/research/publication/vattention-dynamic-memory-management-for-serving-llms-without-pagedattention/"
permalink: /posts/2026/05/vattention/
tags:
  - Paper Review
  - Hardware Security
---

<div class="paper-meta" markdown="1">

- **논문명**: vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention
- **저자**: Ramya Prabhu, Ajay Nayak, Jayashree Mohan, Ramachandran Ramjee, Ashish Panwar
- **학회**: ASPLOS 2025
- **링크**: [Microsoft Research](https://www.microsoft.com/en-us/research/publication/vattention-dynamic-memory-management-for-serving-llms-without-pagedattention/?locale=ko-kr)

</div>

## Introduction

LLM serving에서는 요청마다 prompt 길이와 생성 길이가 다르고, 이에 따라 KV-cache 메모리 사용량도 동적으로 변합니다. KV-cache는 이전 token들의 key/value representation을 저장하여 다음 token 생성 시 attention 계산을 빠르게 하기 위한 구조입니다. 요청이 길어질수록 KV-cache도 커지고, 동시에 여러 사용자의 요청을 batch로 처리하면 GPU memory 관리가 전체 serving 성능에 직접적인 영향을 줍니다.

기존 PagedAttention 방식은 KV-cache를 page 단위로 쪼개어 물리 메모리를 필요한 만큼 할당함으로써 fragmentation 문제를 줄입니다. 하지만 이 방식은 KV-cache가 non-contiguous layout으로 관리되기 때문에 attention kernel과 serving framework가 paging을 직접 이해해야 합니다. 즉 memory management 문제가 application/runtime/kernel stack 전체로 퍼지고, 구현 복잡도가 증가합니다.

이 논문은 PagedAttention 없이도 LLM serving에서 동적 메모리 관리를 수행할 수 있는 vAttention을 제안합니다. 핵심은 GPU의 virtual memory abstraction을 이용해 application이 보는 주소 공간은 contiguous하게 유지하면서, 실제 physical memory는 필요할 때 동적으로 할당하는 것입니다. 이를 통해 기존 attention kernel을 크게 바꾸지 않으면서도 dynamic memory allocation의 장점을 얻으려 합니다.

## Framework

### Virtual Memory 기반 KV-cache 관리

vAttention의 핵심 아이디어는 CUDA virtual memory API를 활용하여 KV-cache를 가상 주소 공간에서는 contiguous하게 유지하고, 실제 물리 메모리는 필요한 시점에 demand paging 방식으로 할당하는 것입니다. Attention kernel 입장에서는 KV-cache가 연속된 배열처럼 보이기 때문에, 기존 contiguous KV-cache를 가정한 kernel을 그대로 사용하거나 최소한의 수정만으로 사용할 수 있습니다.

반면 runtime은 가상 주소와 물리 메모리의 mapping을 관리합니다. 요청이 처음 들어왔을 때 최대 생성 길이에 맞춰 physical memory를 모두 할당할 필요가 없고, 실제 token이 생성되면서 필요한 부분에만 memory를 commit할 수 있습니다. 이 방식은 over-allocation을 줄이고, 요청마다 다른 sequence length가 만들어내는 memory fragmentation을 완화합니다.

중요한 점은 vAttention이 memory abstraction의 위치를 바꾼다는 것입니다. PagedAttention은 serving framework와 attention kernel이 page table 또는 block table을 직접 다루는 쪽에 가깝습니다. vAttention은 그 복잡도를 virtual memory layer에 맡기고, 상위 computation은 contiguous memory를 보는 것처럼 유지합니다.

### PagedAttention과의 차이

PagedAttention은 KV-cache를 page 단위로 관리하기 때문에 serving system과 attention kernel이 page table을 이해해야 합니다. 이 방식은 memory utilization 측면에서 효과적이지만, attention computation이 non-contiguous block들을 따라가야 하므로 kernel 설계가 복잡해질 수 있습니다. 또한 새로운 attention optimization이 나올 때마다 paging-aware하게 다시 구현해야 할 수 있습니다.

반면 vAttention은 virtual memory layer에서 연속성을 제공합니다. 물리적으로는 필요할 때 할당되지만, 가상 주소상으로는 연속적이기 때문에 computation layer는 단순한 memory view를 유지합니다. 이 접근은 abstraction boundary를 잘 활용한 사례입니다. Dynamic memory management는 runtime과 virtual memory system이 담당하고, attention kernel은 본래의 계산 구조에 집중할 수 있습니다.

이 차이는 보안 시스템 설계에서도 중요하게 볼 수 있습니다. 어떤 기능을 어느 계층에 넣느냐에 따라 성능과 구현 복잡도가 달라집니다. vAttention은 memory management policy를 kernel computation에 직접 섞기보다, virtual memory abstraction으로 분리합니다.

## Experiments

논문은 vAttention이 LLM serving 환경에서 memory allocation overhead를 줄이고, PagedAttention 기반 구현과 비교해 competitive한 성능을 낼 수 있음을 보입니다. 평가에서는 다양한 request length, batch size, serving workload에서 throughput과 memory utilization을 비교합니다. LLM serving은 요청 길이 분포가 불규칙하기 때문에, 평균 성능뿐 아니라 worst-case memory waste와 fragmentation도 중요합니다.

vAttention은 가상 주소 공간을 크게 예약해 두고 실제 physical memory는 필요한 만큼만 commit하는 방식으로, 긴 sequence를 대비한 과도한 pre-allocation을 줄입니다. 동시에 attention kernel은 contiguous memory를 사용하는 것처럼 동작하므로, paging-aware kernel이 필요로 하는 복잡한 indirection을 줄일 수 있습니다.

이 결과는 LLM serving에서 memory management가 단순한 implementation detail이 아니라 성능을 좌우하는 핵심 요소임을 보여줍니다. 특히 GPU memory는 제한적이고 비싸기 때문에, 같은 GPU에서 더 많은 request를 처리하려면 KV-cache를 효율적으로 관리해야 합니다.

## Conclusion

제가 이 논문에서 중요하게 본 부분은 보안 기능 자체보다도, 시스템 수준의 abstraction을 잘 설계하면 성능과 구현 복잡도 사이의 trade-off를 줄일 수 있다는 점입니다. vAttention은 KV-cache memory management를 attention kernel 안으로 밀어 넣지 않고 virtual memory abstraction으로 처리합니다. 이 덕분에 dynamic allocation의 장점과 contiguous memory view의 장점을 동시에 얻습니다.

TEE나 TrustZone과 같은 보호 메커니즘을 controller architecture에 넣을 때도 비슷한 문제가 발생합니다. 보안 경계를 어느 계층에 둘지, protected memory를 어떤 abstraction으로 노출할지, world switch나 memory copy overhead를 어디에서 흡수할지에 따라 전체 시스템 복잡도와 성능이 달라집니다. vAttention은 직접적인 보안 논문은 아니지만, architecture-level abstraction을 통해 overhead를 줄이는 방식이라는 점에서 참고할 가치가 있습니다.
