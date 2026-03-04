from backend.graph import app

claim = "Shell achieved more than 60% of its target to halve Scope 1 and 2 emissions by 2030 compared with 2016 levels."

result = app.invoke({
    "query": claim,
})

print(result["verdict"])
print(result["grounded"])
print(result["citations"])