# Integrating Local Models Deployed with IPEX-LLM

[IPEX-LLM](https://github.com/intel-analytics/ipex-llm) is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency. 

Dify supports integrating LLM and Text Embedding capabilities of large language models deployed with IPEX-LLM on Intel platforms.

## Quick Integration

### Install and Run Ollama with IPEX-LLM

Follow the instructions in [IPEX-LLM Ollama Quickstart guide](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/ollama_quickstart.html) to start Ollama service on Intel CPUs and GPUs. 

### Integrate IPEX-LLM accelerated Ollama with Dify

Next, integrate IPEX-LLM accelerated Ollama with Dify following the same steps as in [Ollama integration guide](https://docs.dify.ai/tutorials/model-configuration/ollama).