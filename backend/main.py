from backend.graph import app

if __name__ == "__main__":
    result = app.invoke({
        "query": "How many GPUs were used during training?"
    })

    print("\nFINAL ANSWER:")
    print(result["answer"])
    print("result:\n", result["citations"])
    print("\nSOURCES:")

    best = min(result["citations"], key=lambda x: float(x["score"]))

    print("\nMOST RELEVANT SOURCE:")
    print(
        f"- {best['source']} (page {best['page']}, score {float(best['score']):.3f})"
    )
