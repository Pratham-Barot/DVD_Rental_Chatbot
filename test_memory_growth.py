from graph.workflow import app

config = {
    "configurable": {
        "thread_id": "memory_test"
    }
}

questions = [
    "What is AI?",
    "Explain in one sentence",
    "Give an example",
    "What columns are in actor table?",
    "How many actors are there?"
]

for question in questions:

    print("\n" + "=" * 50)
    print("QUESTION:", question)
    print("=" * 50)

    result = app.invoke(
        {
            "question": question
        },
        config=config
    )

    print(
        "\nANSWER:",
        result["answer"]
    )