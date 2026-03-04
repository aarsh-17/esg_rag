from backend.vectorstore.table_engine import TableEngine

engine = TableEngine()

result = engine.find_value(
    metric_keyword="Cash capital expenditure",
    column_keyword="Renewables"
)

print(result)