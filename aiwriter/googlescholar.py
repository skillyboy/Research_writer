# from serpapi import GoogleSearch
# from urllib.parse import urlsplit, parse_qsl
# import pandas as pd
# import os, json

# # def scrape_google_scholar_author():

# params = {
#     "api_key": os.getenv("6c3ee40b5c5be9e4b533d695500d9e3d61ee184ab14babad48a431831c4cb618"),       #SerpApi API key
#     "engine": "google_scholar_author",    # author results search engine
#     "author_id": "VxOmZDgAAAAJ",          # search query
#     "hl": "en"                             #language
# }

# search = GoogleSearch(params)
# results = search.get_dict()

# author_results_data = {
#     "author_data": {},
#     "author_articles": []
# }

# author_results_data["author_data"]["name"] = results.get("author").get("name")
# author_results_data["author_data"]["email"] = results.get("author").get("email")
# author_results_data["author_data"]["website"] = results.get("author").get("website")
# author_results_data["author_data"]["interests"] = results.get("author").get("interests")
# author_results_data["author_data"]["affiliations"] = results.get("author").get("affiliations")
# author_results_data["author_data"]["thumbnail"] = results.get("author").get("thumbnail")

# author_results_data["author_data"]["cited_by_table"] = results.get("cited_by", {}).get("table")
# author_results_data["author_data"]["cited_by_graph"] = results.get("cited_by", {}).get("graph")

# author_results_data["author_data"]["public_access_link"] = results.get("public_access", {}).get("link")
# author_results_data["author_data"]["public_access_available"] = results.get("public_access", {}).get("available")
# author_results_data["author_data"]["public_access_not_available"] = results.get("public_access", {}).get("not_available")
# author_results_data["author_data"]["co_authors"] = results.get("co_authors")

# #extracting all author articles
# while True:
#     results = search.get_dict()

#     for article in results.get("articles", []):

#         print(f"Extracting article: {article.get('title')} ")

#         author_results_data["author_articles"].append({
#             "article_title": article.get("title"),
#             "article_link": article.get("link"),
#             "article_year": article.get("citation_id"),
#             "article_citation_id": article.get("authors"),
#             "article_authors": article.get("publication"),
#             "article_publication": article.get("cited_by", {}).get("value"),
#             "article_cited_by_value": article.get("cited_by", {}).get("link"),
#             "article_cited_by_link": article.get("cited_by", {}).get("cites_id"),
#             "article_cited_by_cites_id": article.get("year")
#         })

#     if "next" in results.get("serpapi_pagination", []):
#         search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))
#     else:
#         break

# print(json.dumps(author_results_data, indent=2, ensure_ascii=False))
# print(f"Done. Extracted {len(author_results_data['author_articles'])-1} articles.")  #counts extra empty line, that's why -1.

# # #masatoshi_nei_author_articles.csv
# # pd.DataFrame(data=author_results_data["author_articles"]).to_csv(
# #     f"{author_results_data['author_data']['name'].lower().replace(' ', '_')}_author_articles.csv", 
# #     encoding="utf-8"
# # )

# # return author_results_data

