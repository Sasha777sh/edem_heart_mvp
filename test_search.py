from googlesearch import search

query = "site:wildberries.ru/catalog/222931981/detail.aspx pricing cost"
print(f"Testing search for: {query}")

try:
    for result in search(query, num_results=1, advanced=True):
        print(f"Found: {result.title} - {result.description}")
except Exception as e:
    print(f"Error: {e}")

print("Done.")
