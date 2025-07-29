#!/usr/bin/env python3
"""
Analyze Impossible Task Exclusions
===================================

This script analyzes the Latest_Runs_Dataset.csv to:
1. Identify tasks that cannot be run due to environment configuration or have incorrect expected outcomes
2. Calculate pass/fail statistics for possible tasks only (excluding impossible tasks)
3. Output detailed JSON reports for auditing purposes
"""

import pandas as pd
import json
from datetime import datetime

def load_webarena_tests():
    """Load the webarena tests to get expected answers"""
    with open('webarena_tests.json', 'r', encoding='utf-8') as f:
        tests = json.load(f)
    
    # Create mapping from task_id to expected answer
    expected_answers = {}
    for test in tests:
        task_id = test['task_id']
        eval_info = test.get('eval', {})
        
        # Store the full eval blob as expected answer
        if eval_info:
            expected_answers[task_id] = eval_info
        else:
            expected_answers[task_id] = {"eval_types": [], "note": "No eval data"}
    
    return expected_answers

def analyze_impossible_exclusions():
    """Main analysis function"""
    print("🔍 ANALYZING IMPOSSIBLE TASK EXCLUSIONS")
    print("=" * 50)
    
    # Load the expected answers from webarena tests
    expected_answers = load_webarena_tests()
    
    # Load the dataset
    df = pd.read_csv('Latest_Runs_Dataset.csv')
    
    print(f"Total tasks in dataset: {len(df)}")
    
    # Identify impossible tasks (Exclude - Invalid Answer or Exclude - Invalid Environment)
    impossible_tasks = df[df['result'].isin(['Exclude - Invalid Answer', 'Exclude - Invalid Environment'])]
    possible_tasks = df[~df['result'].isin(['Exclude - Invalid Answer', 'Exclude - Invalid Environment'])]
    
    print(f"Impossible tasks (Invalid Answer/Invalid Environment): {len(impossible_tasks)}")
    print(f"Possible tasks: {len(possible_tasks)}")
    
    # Show breakdown of impossible tasks
    impossible_breakdown = impossible_tasks['result'].value_counts()
    print(f"\nImpossible task breakdown:")
    for result, count in impossible_breakdown.items():
        print(f"  {result}: {count}")
    
    # Calculate statistics for possible tasks only
    print(f"\n📊 STATISTICS FOR POSSIBLE TASKS ONLY")
    print("=" * 50)
    
    possible_results = possible_tasks['result'].value_counts()
    print("Result distribution:")
    for result, count in possible_results.items():
        percentage = count / len(possible_tasks) * 100
        print(f"  {result}: {count} ({percentage:.1f}%)")
    
    # Calculate pass/fail rates (assuming PASS = pass, everything else = fail)
    pass_count = possible_results.get('PASS', 0)
    total_possible = len(possible_tasks)
    fail_count = total_possible - pass_count
    
    print(f"\nPass/Fail Analysis (Possible Tasks Only):")
    print(f"  PASS: {pass_count} ({pass_count/total_possible*100:.1f}%)")
    print(f"  FAIL: {fail_count} ({fail_count/total_possible*100:.1f}%)")
    
    # Prepare data for JSON output
    excluded_tasks = []
    included_tasks = []
    
    print(f"\n📝 PREPARING AUDIT DATA")
    print("=" * 50)
    
    # Process impossible tasks (excluded)
    for _, row in impossible_tasks.iterrows():
        task_id = int(row['task_id'])
        excluded_task = {
            "task_id": task_id,
            "result": str(row['result']),
            "site": str(row['site']),
            "intent": str(row['intent']),
            "created_at": str(row['created_at']),
            "run_id": str(row['run_id']),
            "result_override_reason": str(row['result_override_reason']) if pd.notna(row['result_override_reason']) else None,
            "expected_answer": expected_answers.get(task_id, "Unknown")
        }
        excluded_tasks.append(excluded_task)
    
    # Process possible tasks (included)
    for _, row in possible_tasks.iterrows():
        task_id = int(row['task_id'])
        included_task = {
            "task_id": task_id,
            "result": str(row['result']),
            "site": str(row['site']),
            "intent": str(row['intent']),
            "created_at": str(row['created_at']),
            "run_id": str(row['run_id']),
            "result_override_reason": str(row['result_override_reason']) if pd.notna(row['result_override_reason']) else None,
            "expected_answer": expected_answers.get(task_id, "Unknown")
        }
        included_tasks.append(included_task)
    
    # Create comprehensive analysis report
    analysis_report = {
        "analysis_metadata": {
            "analysis_date": datetime.now().isoformat(),
            "dataset_file": "Latest_Runs_Dataset.csv",
            "total_tasks": int(len(df)),
            "analysis_purpose": "Exclude tasks that cannot be run due to environment configuration & have incorrect expected outcomes. Calculate pass/fail for possible tasks only."
        },
        "summary_statistics": {
            "total_tasks": int(len(df)),
            "impossible_tasks": int(len(impossible_tasks)),
            "possible_tasks": int(len(possible_tasks)),
            "exclusion_rate": float(len(impossible_tasks) / len(df) * 100)
        },
        "impossible_task_breakdown": {str(k): int(v) for k, v in impossible_breakdown.items()},
        "possible_tasks_results": {
            "total_count": int(len(possible_tasks)),
            "pass_count": int(pass_count),
            "fail_count": int(fail_count),
            "pass_rate": float(pass_count / total_possible * 100),
            "fail_rate": float(fail_count / total_possible * 100),
            "result_breakdown": {str(k): int(v) for k, v in possible_results.items()}
        },
        "excluded_tasks": excluded_tasks,
        "included_tasks": included_tasks
    }
    
    # Save detailed analysis report
    with open('impossible_exclusions_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_report, f, indent=2, ensure_ascii=False)
    
    # Save summary for quick reference
    summary = {
        "analysis_date": datetime.now().isoformat(),
        "total_tasks": int(len(df)),
        "excluded_count": int(len(impossible_tasks)),
        "included_count": int(len(possible_tasks)),
        "pass_rate_possible_only": float(pass_count / total_possible * 100),
        "fail_rate_possible_only": float(fail_count / total_possible * 100)
    }
    
    with open('impossible_exclusions_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Analysis complete!")
    print(f"   - Detailed report saved to: impossible_exclusions_analysis.json")
    print(f"   - Summary saved to: impossible_exclusions_summary.json")
    print(f"   - Excluded {len(impossible_tasks)} impossible tasks")
    print(f"   - Included {len(possible_tasks)} possible tasks")
    print(f"   - Pass rate (possible tasks only): {pass_count/total_possible*100:.1f}%")
    
    # Show some examples of excluded tasks
    print(f"\n🔍 SAMPLE EXCLUDED TASKS (IMPOSSIBLE)")
    print("=" * 50)
    
    sample_excluded = impossible_tasks.head(3)
    for i, (_, row) in enumerate(sample_excluded.iterrows(), 1):
        print(f"\nExample {i}:")
        print(f"  Task ID: {row['task_id']}")
        print(f"  Result: {row['result']}")
        print(f"  Site: {row['site']}")
        print(f"  Intent: {str(row['intent'])[:80]}...")
        if pd.notna(row['result_override_reason']):
            print(f"  Override Reason: {str(row['result_override_reason'])[:80]}...")
    
    return analysis_report

if __name__ == "__main__":
    analyze_impossible_exclusions()