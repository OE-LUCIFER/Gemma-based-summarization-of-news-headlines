import requests
from headlines import Headlines

class SpaceWebScoutHeadlines(Headlines):
    def _format_headlines(self, response, max_headlines: int = 100):
        headlines = []
        for idx, article in enumerate(response):
            if idx >= max_headlines:
                break

            new_headline = f"{idx + 1}. {article['title'].strip()} "
            new_headline += f"(URL: {article['url'].strip()}) "
            new_headline += f"{article['body'].strip()}"
            new_headline += "\n"
            headlines.append(new_headline)

        headlines = "\n".join(headlines)
        return headlines

    def get_headlines(self, max_headlines: int = 20):
        url = f"https://oevortex-webscout.hf.space/api/news?q=latest AI news&max_results={max_headlines}&safesearch=moderate&region=wt-wt"
        response = requests.get(url)
        
        if response.status_code == 200:
            return self._format_headlines(response.json()['results'], max_headlines)
        else:
            return f"Failed to fetch headlines. Status code: {response.status_code}"

# Example usage:
headlines_provider = SpaceWebScoutHeadlines()
print(headlines_provider.get_headlines(max_headlines=10))
