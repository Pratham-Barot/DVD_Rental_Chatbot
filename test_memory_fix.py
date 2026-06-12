from graph.workflow import app

config = {
    "configurable": {
        "thread_id": "memory_fix_test"
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

    result = app.invoke(
        {
            "question": question
        },
        config=config
    )

    print("\nQUESTION:", question)

    print(
        "MESSAGE COUNT:",
        len(
            result.get(
                "messages",
                []
            )
        )
    )