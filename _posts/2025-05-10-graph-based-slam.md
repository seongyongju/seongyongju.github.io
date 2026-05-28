---
title: "A Tutorial on Graph-Based SLAM"
date: 2025-05-10
venue: "IEEE ITS Magazine, 2010"
paper_url: "https://www.researchgate.net/publication/231575337_A_tutorial_on_graph-based_SLAM"
permalink: /posts/2025/05/graph-based-slam/
tags:
  - Paper Review
  - Machine Learning
---

<div class="paper-meta" markdown="1">

- **논문명**: A Tutorial on Graph-Based SLAM
- **저자**: Giorgio Grisetti, Rainer Kummerle, Cyrill Stachniss, Wolfram Burgard
- **저널**: IEEE Intelligent Transportation Systems Magazine, 2010
- **DOI**: 10.1109/MITS.2010.939925
- **링크**: [ResearchGate](https://www.researchgate.net/publication/231575337_A_tutorial_on_graph-based_SLAM)

</div>
<figure class="article-figure">
  <img src="/images/articles/graph-based-slam.svg" alt="A Tutorial on Graph-Based SLAM 개념도">
  <figcaption>이 글은 문제 설정에서 출발해 제안 방법, 실험 구성, 핵심 결과 순서로 이해하면 된다.</figcaption>
</figure>

<div class="figure-note" markdown="1">
그림은 SLAM의 기본 흐름입니다. 센서 관측을 노드와 제약으로 바꾸고, 그래프 최적화를 통해 위치와 지도를 함께 개선합니다.
</div>

## Introduction

이 논문은 SLAM, 즉 Simultaneous Localization and Mapping 문제를 graph-based formulation으로 설명하는 tutorial paper입니다. SLAM은 로봇이 미지의 환경에서 이동하면서 자신의 위치를 추정하고 동시에 지도를 구성하는 문제입니다. 로봇은 odometry, camera, LiDAR, IMU 같은 센서로부터 정보를 얻지만, 이 측정값에는 항상 noise와 drift가 포함됩니다.

SLAM이 어려운 이유는 위치 추정과 지도 작성이 서로 의존하기 때문입니다. 정확한 지도가 있어야 위치를 잘 추정할 수 있고, 정확한 위치를 알아야 지도를 잘 만들 수 있습니다. Graph-based SLAM은 이 상호 의존 관계를 graph optimization 문제로 바꾸어 다룹니다.

## Framework

### Graph-based SLAM

Graph-based SLAM에서는 robot pose와 landmark를 node로 표현하고, odometry나 sensor measurement에서 얻은 spatial constraint를 edge로 표현합니다. 예를 들어 로봇이 시간 `t`에서 `t+1`로 이동했다는 odometry measurement는 두 pose node 사이의 edge가 됩니다. 특정 위치에서 landmark를 관측했다면 pose node와 landmark node 사이에 edge가 생깁니다.

각 edge는 measurement와 uncertainty를 포함합니다. Optimization의 목표는 모든 edge constraint를 가장 잘 만족하는 node configuration을 찾는 것입니다. 즉 SLAM 문제는 “센서 측정값들과 가장 일관적인 trajectory와 map은 무엇인가”라는 least-squares optimization 문제로 바뀝니다.

이 방식은 loop closure를 자연스럽게 반영할 수 있습니다. 로봇이 이전에 방문한 장소를 다시 인식하면, 현재 pose와 과거 pose 사이에 새로운 constraint가 추가됩니다. 이 constraint는 누적된 odometry drift를 줄이고 전체 trajectory를 보정하는 데 중요한 역할을 합니다.

### Filtering and Smoothing

논문은 filtering과 smoothing의 차이도 설명합니다. Filtering은 현재 상태와 지도를 online으로 추정하는 접근입니다. 과거 상태를 marginalize하고 현재 state를 계속 업데이트하기 때문에 실시간 처리에 적합하지만, 과거 trajectory 전체를 다시 보정하는 데에는 한계가 있습니다.

Smoothing은 전체 measurement set을 사용하여 전체 trajectory를 추정하는 접근입니다. Graph-based SLAM은 smoothing 관점과 잘 맞습니다. 과거 pose도 graph node로 유지하고, 새로운 constraint가 들어오면 전체 graph를 다시 최적화하여 trajectory를 보정할 수 있습니다.

또한 Graph-based SLAM은 front-end와 back-end를 분리한다는 점에서 유용합니다. Front-end는 sensor data로부터 feature matching, scan matching, loop closure detection을 수행하여 graph를 만들고, back-end는 graph optimization을 수행합니다. 이 분리는 시스템을 이해하고 개선하기 쉽게 만듭니다.

## Discussion

Graph-based SLAM의 장점은 SLAM 문제를 확률적 상태 추정 문제에서 graph optimization 문제로 명확하게 바꿔 볼 수 있다는 점입니다. 센서 측정값이 만들어내는 제약 조건을 edge로 표현하면, 누적 오차가 발생한 trajectory도 optimization을 통해 보정할 수 있습니다.

이 구조는 cyber-physical system에서 중요한 insight를 줍니다. 물리 세계에서 들어오는 센서 데이터는 불확실하고 noisy하지만, 여러 측정값 사이의 관계를 constraint로 표현하면 전체 상태를 더 안정적으로 추정할 수 있습니다. 따라서 state estimation은 단순 sensor reading이 아니라 optimization과 consistency checking의 문제입니다.

## Conclusion

제가 이 논문을 리뷰한 이유는 cyber-physical system에서 sensing, localization, optimization이 어떻게 연결되는지 이해하기 위해서입니다. 특히 mobility system에서는 controller architecture의 보안뿐 아니라, sensor measurement와 state estimation 과정의 신뢰성도 중요합니다.

SDV나 autonomous mobility 환경에서는 공격자가 sensor input을 조작하거나 localization pipeline에 영향을 주는 경우도 생각해야 합니다. Graph-based SLAM의 구조를 이해하면 어떤 measurement가 어떤 constraint를 만들고, 잘못된 constraint가 전체 state estimate에 어떤 영향을 주는지 분석할 수 있습니다.
