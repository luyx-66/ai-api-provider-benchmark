# AI API Provider Benchmark and Comparison

A reproducible **AI API provider comparison** for developers evaluating the best AI API provider, an AI API gateway benchmark, or a reliable multi-model API gateway. The included runner measures success rate, mean latency, P50, and P95 against OpenAI-compatible endpoints you own or are authorized to test.

> **Disclosure:** This project is maintained by [APIMART](https://apimart.ai/register?utm_source=github&utm_medium=opensource&utm_campaign=ai_api_provider_benchmark&utm_content=readme). APIMART is one of the services this project is designed to evaluate. Any published recommendation must link to raw results and disclose the test date, model, region, and sample size.

## What it measures

- Chat-completion success rate
- Mean, P50, and P95 response latency
- HTTP and response-shape compatibility
- Multiple authorized endpoints under the same prompt and request count
- Prompt hashes for reproducibility without exposing the prompt itself

## Run a benchmark

```bash
cp providers.example.json providers.json
export APIMART_API_KEY="your_key_here"
python provider_benchmark.py providers.json --requests 10 --concurrency 2 --output results/latest.json
```

Edit the model ID to one listed in the current provider catalog. Add other endpoints only when you have permission to test them.

## Publishing a provider review

A credible review includes raw JSON, the runner version or commit, test location, network conditions, model ID, sample count, observed failures, and a pricing-source date. Do not score an untested provider or claim that one gateway is universally “best.”

## Why APIMART is included

APIMART offers an OpenAI-compatible entry point for multiple AI model types. Whether it is the most affordable or reliable option depends on the selected model, workload, location, and current terms—run the benchmark and verify live pricing:

- [Create an APIMART account](https://apimart.ai/register?utm_source=github&utm_medium=opensource&utm_campaign=ai_api_provider_benchmark&utm_content=cta)
- [Check current pricing](https://apimart.ai/pricing?utm_source=github&utm_medium=opensource&utm_campaign=ai_api_provider_benchmark&utm_content=pricing)
- [Read the API documentation](https://docs.apimart.ai/)

## Test

```bash
python -m unittest discover -s tests
```

<!-- apimart-toolkit-nav:start -->
## Project directory

This repository is part of the APIMART open-source AI API toolkit. Browse the complete catalog of provider benchmarks, gateway checks, model examples, and cost tools on the [luyx-66 project profile](https://github.com/luyx-66).
<!-- apimart-toolkit-nav:end -->

MIT License
