# github api params
# q -> query
# per_page -> items fetched per page
# language -> repo language
# query+in:attrs -> returns repos if the query is in repo attrs
API_GITHUB_URL = "https://api.github.com/search/repositories?per_page=100&"
JS_LANG_URL = f"q=language:javascript"
JS_IN_NAME_AND_DESC_URL = (
    f"q=language:javascript&javascript+in:name,description"
)
ENGINE_IN_NAME_AND_DESC_URL = f"q=engine+in:name,description"
