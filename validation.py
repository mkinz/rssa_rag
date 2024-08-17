from llm_interface import LLMProvider


def validate_llm_responses(llm_provider: LLMProvider):
    test_cases = [
        {
            "input": "Who was the first president of the United States?",
            "expected_output": "George Washington",
            "description": "Basic historical fact",
        },
        {
            "input": "Analyze this data: Age: 65, Annual Income: $50,000, Years Worked: 40, Retirement Savings: $500,000",
            # We expect the word "retirement" to be in the response
            "expected_output": "retirement",
            "description": "Simple financial analysis",
        },
    ]

    print("Running LLM Validation Tests:")
    for i, test in enumerate(test_cases, 1):
        response = llm_provider.analyze(test["input"])
        if isinstance(test["expected_output"], str):
            passed = test["expected_output"].lower() in response.lower()
        else:
            passed = test["expected_output"](response)

        print(f"Test {i} ({'Passed' if passed else 'Failed'}): {
              test['description']}")
        if not passed:
            print(f"  Input: {test['input']}")
            # Print first 100 characters of response
            print(f"  Response: {response[:100]}...")
        print()

    return all(
        test["expected_output"].lower() in llm_provider.analyze(
            test["input"]).lower()
        for test in test_cases
    )
