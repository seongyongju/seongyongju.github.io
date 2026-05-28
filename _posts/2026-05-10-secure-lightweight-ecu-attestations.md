---
title: "Secure and Lightweight ECU Attestations for Resilient Over-the-Air Updates in Connected Vehicles"
date: 2026-05-10
venue: "ACSAC 2023"
paper_url: "https://publica.fraunhofer.de/handle/publica/458448"
permalink: /posts/2026/05/secure-lightweight-ecu-attestations/
tags:
  - Paper Review
  - Hardware Security
---

<div class="paper-meta" markdown="1">

- **논문명**: Secure and Lightweight ECU Attestations for Resilient Over-the-Air Updates in Connected Vehicles
- **저자**: Christian Plappert, Andreas Fuchs
- **학회**: ACSAC 2023
- **링크**: [Fraunhofer Publica](https://publica.fraunhofer.de/handle/publica/458448)

</div>
<figure class="article-figure">
  <img src="/images/articles/secure-lightweight-ecu-attestations.svg" alt="Secure and Lightweight ECU Attestations for Resilient Over-the-Air Updates in Connected Vehicles 개념도">
  <figcaption>이 글은 하드웨어 신뢰 경계로 무엇을 보호하고, 그 대가로 어떤 성능 비용이 생기는지를 중심으로 읽으면 된다.</figcaption>
</figure>

<div class="figure-note" markdown="1">
그림은 하드웨어 보안 논문의 공통 구조입니다. 어떤 작업을 보호할지 정하고, 신뢰할 수 있는 영역과 그렇지 않은 영역을 나눕니다. 이후 메모리, 캐시, TEE 같은 요소가 보안성과 성능에 어떤 영향을 주는지 비교합니다.
</div>

## Introduction

Connected vehicle에서는 OTA(Over-the-Air) update가 보안 패치와 기능 업데이트를 빠르게 배포하기 위한 필수 기능이 되었습니다. 차량이 점점 software-defined vehicle 구조로 이동하면서, ECU(Electronic Control Unit)에 배포되는 software의 양도 많아지고 업데이트 주기도 짧아지고 있습니다. 이때 중요한 문제는 update package를 안전하게 전달하는 것만으로는 충분하지 않다는 점입니다. Package가 암호학적으로 보호되어 전달되더라도, 실제 ECU가 올바른 software를 실행하고 있는지 확인하지 못하면 차량은 여전히 취약한 상태로 운행될 수 있습니다.

기존 secure update mechanism은 주로 update image의 authenticity와 integrity를 보장하는 데 초점을 둡니다. 하지만 update가 실패했거나, 일부 ECU가 rollback되었거나, 공격자가 특정 ECU의 software state를 조작한 경우에는 update distribution만으로 전체 차량 상태를 판단하기 어렵습니다. 특히 차량은 여러 ECU가 동시에 협력하는 cyber-physical system이기 때문에, 하나의 ECU만 기대와 다른 상태여도 안전 기능이나 제어 흐름에 영향을 줄 수 있습니다.

이 논문은 OTA update 이후 각 in-vehicle component가 어떤 software state에 있는지 lightweight하게 attest하는 구조를 제안합니다. 핵심은 모든 ECU에 무거운 TPM을 넣는 것이 아니라, 차량 내부에 존재하는 heterogeneous hardware capability를 고려하여 TPM 2.0과 DICE(Device Identifier Composition Engine)를 조합하는 것입니다. 이를 통해 update 이후 차량이 정상 주행 상태로 돌아가도 되는지 판단할 수 있는 추가 검증 계층을 제공합니다.

## Framework

### TPM 2.0 and DICE

논문은 차량 내부의 overall hardware trust anchor로 TPM 2.0을 사용하고, resource-constrained controller에는 DICE를 사용합니다. TPM 2.0은 secure storage, measurement, signing 등 신뢰 루트를 구성하기 위한 기능을 제공하지만, 모든 ECU에 TPM을 넣는 것은 비용과 자원 측면에서 부담이 큽니다. 차량 내부에는 고성능 gateway나 domain controller도 있지만, 매우 제한적인 microcontroller 기반 ECU도 많기 때문에 동일한 보안 모듈을 전부 적용하기 어렵습니다.

DICE는 이런 제한적인 환경에서 software identity를 형성하기 위한 lightweight mechanism입니다. Boot 과정에서 실행되는 code와 configuration이 다음 단계의 identity derivation에 반영되고, 그 결과 device가 현재 어떤 software를 실행하고 있는지 증명할 수 있는 기반을 만듭니다. 즉 DICE는 TPM처럼 풍부한 기능을 제공하지는 않지만, 작은 ECU에서도 boot measurement와 identity binding을 가능하게 해 줍니다.

이 구조에서 TPM은 차량 내부의 중앙 trust anchor처럼 동작하고, DICE-enabled ECU들은 자신의 software state를 TPM 또는 verifier가 이해할 수 있는 형태로 보고합니다. 따라서 전체 차량은 하나의 강한 trust anchor와 여러 lightweight attestation source가 결합된 형태가 됩니다.

### ECU Attestation for OTA

OTA update 과정에서 차량은 일시적으로 update-ready state에 들어가고, update가 끝난 뒤 fully functional drive mode로 돌아가야 합니다. 이 전환 지점에서 attestation이 필요합니다. 각 ECU는 현재 실행 중인 software version, boot measurement, configuration state를 기반으로 자신의 상태를 증명합니다. Verifier는 이 evidence를 기대값과 비교하여 update가 실제로 반영되었는지 판단합니다.

이 방식의 장점은 update 실패를 단순히 software installation log에 의존해 판단하지 않는다는 점입니다. 공격자가 update manager나 일부 software component를 속이더라도, ECU의 measured state가 기대값과 다르면 차량은 정상 상태로 전환되지 않아야 합니다. 즉 attestation은 update distribution 이후의 post-update validation 역할을 합니다.

또한 이 논문에서 중요한 부분은 resilient OTA입니다. 차량 update는 네트워크 상태, 전원 상태, ECU별 dependency 때문에 실패 가능성이 항상 존재합니다. 따라서 attestation mechanism은 update가 모두 성공했다는 이상적인 상황만 처리하는 것이 아니라, 일부 component가 기대 상태와 다를 때 이를 탐지하고 안전한 decision을 내릴 수 있어야 합니다.

## Experiments

논문은 제안한 attestation concept를 구현하고, OTA update 과정에 추가되는 성능 부담과 보안 속성을 평가합니다. 평가의 핵심은 attestation이 실제 차량 환경에서 사용할 수 있을 만큼 가벼운지, 그리고 resource-constrained ECU에서도 적용 가능한지 확인하는 것입니다.

Attestation은 cryptographic operation과 communication을 포함하기 때문에, 단순히 보안적으로 타당하다는 것만으로는 충분하지 않습니다. 차량 내부 네트워크는 bandwidth가 제한적일 수 있고, 일부 ECU는 연산 능력이 낮으며, update 과정은 사용자의 차량 이용성과도 연결됩니다. 따라서 attestation은 update flow를 지나치게 지연시키지 않으면서 필요한 신뢰 정보를 제공해야 합니다.

이 논문의 결과는 TPM 2.0과 DICE를 결합하면 OTA update 이후의 verification layer를 비교적 낮은 overhead로 구성할 수 있음을 보여줍니다. 중요한 점은 이것이 secure update distribution을 대체하는 것이 아니라 보완한다는 것입니다. Update image의 signature verification은 여전히 필요하고, 이 논문은 그 이후 단계에서 “정말로 차량 내부 ECU들이 기대한 상태로 실행되고 있는가”를 검증합니다.

## Conclusion

이 논문은 차량 OTA update에서 software distribution만 보호하는 것으로는 충분하지 않다는 점을 보여줍니다. 실제 update가 ECU에 반영되었는지, 각 controller가 기대한 software state인지 검증하는 과정이 필요합니다. 특히 connected vehicle에서는 update 실패나 부분 compromise가 안전 문제로 이어질 수 있으므로, post-update attestation은 단순한 보안 기능이 아니라 차량 상태 전환을 위한 신뢰 판단 절차가 됩니다.

제가 이 논문에서 중요하게 본 부분은 hardware trust anchor를 현실적인 ECU 구성에 맞게 나누어 적용한다는 점입니다. 모든 controller에 동일한 TEE나 TPM을 요구하는 방식은 실제 차량 architecture에서 비용과 자원 문제에 부딪힐 수 있습니다. 반면 TPM 2.0과 DICE를 조합하는 방식은 강한 중앙 trust anchor와 lightweight local identity를 함께 활용합니다. 이는 SDV controller architecture에서 보안 기능을 넣을 때, 보안 강도와 overhead 사이의 균형을 어떻게 잡을지 생각하게 해 줍니다.
