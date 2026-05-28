---
title: "Intel SGX Explained"
date: 2026-05-10
venue: "IACR ePrint, 2016"
paper_url: "https://www.sciweavers.org/publications/intel-sgx-explained"
permalink: /posts/2026/05/intel-sgx-explained/
tags:
  - Paper Review
  - Hardware Security
---

<div class="paper-meta" markdown="1">

- **논문명**: Intel SGX Explained
- **저자**: Victor Costan, Srinivas Devadas
- **출판 형태**: IACR ePrint, 2016
- **링크**: [Sciweavers](https://www.sciweavers.org/publications/intel-sgx-explained)

</div>

## Introduction

Intel SGX Explained는 Intel Software Guard Extensions의 구조와 보안 모델을 정리한 문헌입니다. SGX는 운영체제나 hypervisor와 같은 privileged software를 완전히 신뢰하지 않는 환경에서도, enclave라는 격리된 실행 영역을 통해 code와 data의 confidentiality 및 integrity를 보호하려는 기술입니다.

TEE를 이해할 때 SGX는 중요한 기준점입니다. TrustZone, SEV, TDX, GPU confidential computing처럼 다양한 trusted execution mechanism이 있지만, 모두 공통적으로 “무엇을 신뢰하고 무엇을 신뢰하지 않는가”, “보호되는 memory boundary가 어디인가”, “remote verifier가 실행 상태를 어떻게 확인하는가”라는 질문을 가집니다. SGX는 이 질문들을 비교적 명확한 enclave model로 제시합니다.

## Framework

### Enclave Model

이 논문은 SGX의 architectural detail, enclave memory 관리, address translation, attestation, launch control 등 SGX를 이해하는 데 필요한 세부 요소를 체계적으로 설명합니다. Enclave는 일반 application address space 안에 존재하지만, CPU가 memory access rule을 강제하여 enclave 외부 code가 enclave memory를 직접 읽거나 쓸 수 없도록 합니다.

SGX에서 중요한 개념은 EPC(Enclave Page Cache)와 measurement입니다. Enclave page는 보호된 memory 영역에 배치되고, enclave가 생성될 때 code와 data의 measurement가 계산됩니다. 이 measurement는 나중에 attestation 과정에서 “어떤 code가 enclave 안에 올라갔는지”를 증명하는 근거가 됩니다.

또한 enclave transition도 중요합니다. Application은 enclave entry를 통해 trusted code를 호출하고, enclave는 제한된 interface를 통해 외부와 상호작용합니다. 이 interface가 너무 넓거나 검증이 부족하면 enclave 내부가 안전해도 Iago attack이나 confused deputy 문제가 생길 수 있습니다.

### Threat Model

SGX는 운영체제나 hypervisor가 악의적일 수 있다는 강한 threat model을 가정합니다. 대신 CPU package 내부의 하드웨어와 SGX mechanism은 신뢰합니다. 이 구분은 trusted computing base를 어디까지 둘 것인지 판단하는 데 중요합니다.

하지만 SGX가 모든 것을 보호하는 것은 아닙니다. OS가 page fault pattern을 관찰하거나 scheduling을 조작하거나, cache side channel을 통해 정보를 추론할 수 있습니다. 또한 enclave가 외부 system call이나 untrusted memory를 사용할 때는 interface validation이 필요합니다. 따라서 SGX의 보안 속성은 confidentiality와 integrity의 강한 기반을 제공하지만, side-channel과 boundary interaction은 별도로 설계해야 합니다.

## Discussion

SGX는 TEE의 대표적인 예시이지만, 모든 공격을 막는 완전한 보호 기술은 아닙니다. 특히 side-channel, enclave interface, memory access pattern 등은 별도의 분석과 완화가 필요합니다. 따라서 SGX를 이해할 때는 제공하는 보안 속성과 남아 있는 공격면을 함께 보는 것이 중요합니다.

이 점은 다른 TEE에도 그대로 적용됩니다. TrustZone을 vehicle controller에 넣거나 GPU-CC를 AI workload에 적용할 때도, hardware boundary가 생겼다고 해서 전체 system이 자동으로 안전해지는 것은 아닙니다. Protected world와 normal world 사이의 interface, shared memory, interrupt, DMA, cache behavior까지 함께 봐야 합니다.

## Conclusion

제가 이 논문을 리뷰한 이유는 TEE의 기본 구조를 이해하기 위해서입니다. TrustZone이나 GPU-CC처럼 다른 형태의 trusted execution mechanism을 볼 때도, SGX의 enclave model은 보안 경계와 trusted computing base를 비교하는 기준점이 됩니다.

특히 제 연구 관심인 controller architecture에 TEE를 도입하는 문제에서는 SGX가 보여주는 교훈이 중요합니다. TEE는 강한 격리 primitive를 제공하지만, 실제 overhead와 interface complexity를 줄이려면 어떤 code를 enclave에 넣을지, 어떤 data path를 보호할지, attestation을 언제 수행할지 세밀하게 설계해야 합니다.
