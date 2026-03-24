# import json
# from backend.vectorstore.retriever import retriever
# from backend.llm import llm
# import time


# K = 3


# def evidence_judge(claim, context):
#     prompt = f"""
# You are evaluating retrieval quality.

# Does the CONTEXT provide concrete factual support,
# quantitative evidence, or direct elaboration for the CLAIM?

# Only answer YES if the context materially supports
# or verifies the claim.

# If it is only thematically related, answer NO.

# Respond with YES or NO only.

# CLAIM:
# {claim}

# CONTEXT:
# {context}
# """
#     response = llm.invoke(prompt).strip().upper()
#     return response == "YES"


# def evaluate():
#     with open("backend/retrieval_test.json", "r") as f:
#         test_data = json.load(f)

#     total = len(test_data)
#     hits = 0
#     similarity_scores = []
#     total_precision = 0  # NEW

#     for i, sample in enumerate(test_data):
#         claim = sample["claim"]
#         query = "Represent this sentence for searching relevant passages: " + claim

#         docs_with_scores = retriever.vectorstore.similarity_search_with_score(
#             query, k=K
#         )

#         found_support = False
#         relevant_count = 0  # NEW

#         print(f"\nClaim {i+1}: {claim}")

#         for doc, score in docs_with_scores:
#             similarity_scores.append(score)

#             print(
#                 f"Score: {round(score, 3)} | Page: {doc.metadata.get('page')}\n"
#                 f"Text: {doc.page_content[:300]}..."
#             )

#             supports = evidence_judge(claim, doc.page_content)

#             print("LLM verdict:", "SUPPORTS" if supports else "NOT_RELEVANT")
#             print("------")

#             if supports:
#                 relevant_count += 1  # NEW
#                 found_support = True

#         # ---- Recall logic (unchanged) ----
#         if found_support:
#             hits += 1

#         # ---- Precision logic (NEW) ----
#         precision_k = relevant_count / K
#         total_precision += precision_k

#         print(f"Precision@{K} for this claim: {round(precision_k, 2)}")

#         time.sleep(0.2)

#     recall_at_k = hits / total
#     avg_precision_at_k = total_precision / total  # NEW
#     avg_similarity = sum(similarity_scores) / len(similarity_scores)

#     print("\n==============================")
#     print(f"LLM-Validated Recall@{K}: {recall_at_k:.2f}")
#     print(f"Precision@{K}: {avg_precision_at_k:.2f}")
#     print(f"Average Similarity Score: {round(avg_similarity, 3)}")
#     print("==============================")


# if __name__ == "__main__":
#     evaluate()

# # from backend.vectorstore.retriever import retriever
# # from backend.llm import llm

# # K = 5


# # def evidence_judge(claim, context):
# #     prompt = f"""
# # Does the CONTEXT explicitly confirm, restate, or clearly elaborate the CLAIM?

# # If the context contains a statement that directly affirms the claim,
# # answer YES.

# # If it only discusses a related theme but does not clearly confirm the claim,
# # answer NO.

# # CLAIM:
# # {claim}

# # CONTEXT:
# # {context}
# # """
# #     response = llm.invoke(prompt).strip().upper()
# #     return response == "YES"


# # def evaluate_single_claim(claim):
# #     query = "Represent this sentence for searching relevant passages: " + claim

# #     docs_with_scores = retriever.vectorstore.similarity_search_with_score(
# #         query, k=K
# #     )

# #     found_support = False
# #     similarity_scores = []

# #     print(f"\nClaim: {claim}")
# #     print("=" * 50)

# #     for doc, score in docs_with_scores:
# #         similarity_scores.append(score)

# #         print(f"Score: {round(score, 3)}")
# #         print(f"Page: {doc.metadata.get('page')}")
# #         print(f"Text: {doc.page_content[:-1]}...\n")

# #         supports = evidence_judge(claim, doc.page_content)

# #         print("LLM verdict:", "SUPPORTS" if supports else "NOT_RELEVANT")
# #         print("-" * 50)

# #         if supports:
# #             found_support = True

# #     recall_at_k = 1.0 if found_support else 0.0
# #     avg_similarity = sum(similarity_scores) / len(similarity_scores)

# #     print("\nSummary")
# #     print("=" * 50)
# #     print(f"LLM-Validated Recall@{K}: {recall_at_k:.2f}")
# #     print(f"Average Similarity Score: {round(avg_similarity, 3)}")


# # if __name__ == "__main__":
# #     claim = "In 2023, about 94% of the oil spills of more than 100 kilograms from the SPDC-operated facilities were caused by the illegal activities of third parties."
# #     evaluate_single_claim(claim)

import requests
print(requests.get("https://huggingface.co").status_code)