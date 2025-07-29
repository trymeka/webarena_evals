# WebArena Benchmark Evaluation Analysis for Meka v1

This folder contains source data & analysis scripts for our WebArena evaluation methodology, specifically documenting the 161 tasks that were excluded from our final results and why. For a full read-up on our evaluation methodology and set-up, read [here](https://blog.withmeka.com/meka-achieves-state-of-the-art-performance-for-computer-use/).

## Overview

Meka achieved a **72.7% success rate** on WebArena. This result was calculated from **651 possible tasks** after excluding **161 impossible tasks** from the original 812-task benchmark.

This folder contains the full audit trail showing which tasks were excluded and the rationale behind each exclusion, ensuring complete reproducibility and transparency for the research community. To learn more about our open source agent framework that achieved these benchmarks, check out our repo [here](https://github.com/trymeka/agent).

## Key Statistics

**Total Original Tasks**: 812  
**Impossible Tasks Excluded**: 161 (19.8% exclusion rate)
- Invalid Environment: 128 tasks  
- Invalid Answer: 33 tasks

**Final Evaluation Set**: 651 tasks  
**Meka Success Rate**: 72.7% (473/651 tasks passed)  
**Failure Rate**: 27.3% (178/651 tasks failed)

## Exclusion Categories

We excluded 161 tasks that could not be properly evaluated:

### Invalid Environment (128 tasks)
Tasks that cannot be run due to environment configuration limitations:
- **Map-related tests**: The map tiling URL in the provided Docker container was broken, making these tasks impossible to complete

### Invalid Answer (33 tasks)  
Tasks with provably incorrect expected outcomes in the original benchmark:
- **Factual errors**: Expected answers that contradict the actual data in the test environment
- **Specification mismatches**: Tasks where the expected outcome doesn't match what's achievable given the environment setup

## Files in This Analysis

### Core Analysis Files
- **`impossible_exclusions_analysis.json`** - Complete detailed analysis with all task data, including full evaluation criteria from the original WebArena test definitions
- **`impossible_exclusions_summary.json`** - High-level statistics for quick reference
- **`analyze_impossible_exclusions.py`** - Python script that generates the analysis 

### Source Data
- **`Latest_Runs_Dataset.csv`** - Complete dataset of all 812 test runs with results
- **`webarena_tests.json`** - Original WebArena evaluation test definitions with expected outcomes

## Methodology Alignment

- **Environment Issues**: Documented infrastructure problems that made certain tasks impossible
- **Answer Validation**: Manual review process that identified incorrect expected outcomes
- **Conservative Approach**: Only excluded tasks with clear, demonstrable issues

## Usage

To reproduce this analysis:

```bash
python analyze_impossible_exclusions.py
```

This will regenerate both JSON files from the source data, allowing you to verify our exclusion decisions independently.

## Research Use

This dataset is provided for the research community to:
- Understand which WebArena tasks may have evaluation issues
- Reproduce our results with the same exclusion criteria  
- Develop improved versions of the benchmark
- Compare agent performance on the same 651-task subset
