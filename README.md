# EcoPull: Sustainable IoT Image Retrieval Empowered by TinyML Models

This is a research-oriented code package that is primarily intended to allow readers to replicate the results of the paper mentioned below and also encourage and accelerate further research on this topic:

M. Thorsager, V. Croisfelt, J. Shiraishi, and P. Popovski, **“EcoPull: Sustainable IoT Image Retrieval Empowered by TinyML Models,”** GLOBECOM 2024 - 2024 IEEE Global Communications Conference, Cape Town, South Africa, 2024, pp. 5066-5071, doi: 10.1109/GLOBECOM52923.2024.10901782.

A pre-print version is available on arXiv: [https://arxiv.org/abs/2304.10858](https://arxiv.org/abs/2404.14236).

We hope this content helps in your research and contributes to building the precepts behind open science. Remarkably, to boost the idea of open science and further drive the evolution of science, we also motivate you to share your published results with the public.

If you have any questions or if you have encountered any inconsistencies, please do not hesitate to contact me via victorcroisfelt@gmail.com.

## Abstract
This paper introduces EcoPull, a sustainable Internet of Things (IoT) framework powered by Tiny Machine Learning (TinyML) models for efficient image retrieval from multiple devices. The devices are equipped with two types of TinyML models: i) a behavior model and ii) an image compressor model. The behavior model filters out irrelevant images based on the current task, minimizing unnecessary data transmission and reducing communication resource competition among devices. The image compressor model enables devices to communicate with the edge server (ES) using latent representations of images, thereby reducing communication bandwidth usage. While integrating TinyML models into IoT devices does increase energy consumption due to the inference process, this cost is carefully accounted for in our design. Numerical results show that the proposed framework can achieve over 77% and 43% energy savings compared to the simple offloading and a state-of-the-art baseline while still maintaining the quality of the retrieved images at the ES.

## Content
This package includes three main scripts that simulate energy consumption using the integrated communication-computation energy consumption model introduced in the paper under three different scenarios:
- `energy_cost_HiFiC.py`: simulates baseline energy consumption.
- `energy_cost_IoT.py`: simulates the energy consumption of a single IoT user within the EcoPull framework.
- `energy_cost_multi_IoT.py`: simulates the energy consumption of multiple IoT transmitting users within the EcoPull framework, while also evaluating the random access scheme triggered by semantic queries.

## Citing this Repository and License
This code is subject to the MIT license. If you use any part of this repository for research, please consider citing our work.

```bibtex
@INPROCEEDINGS{10901782,
  author={Thorsager, Mathias and Croisfelt, Victor and Shiraishi, Junya and Popovski, Petar},
  booktitle={GLOBECOM 2024 - 2024 IEEE Global Communications Conference}, 
  title={EcoPull: Sustainable IoT Image Retrieval Empowered by TinyML Models}, 
  year={2024},
  volume={},
  number={},
  pages={5066-5071},
  keywords={Energy consumption;Image coding;Biological system modeling;Tiny machine learning;Image retrieval;Mathematical models;Data models;Numerical models;Internet of Things;Data communication;IoT Networks;TinyML;image retrieval;generative AI;medium access control},
  doi={10.1109/GLOBECOM52923.2024.10901782}
}
```

## Acknowledgement
This work was supported by the Villum Investigator Grant “WATER” from the Velux Foundation, Denmark, and by the SNS JU project 6G-GOALS under the EU's Horizon Europe program under Grant Agreement No. 101139232.
