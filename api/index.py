# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "fastapi",
#   "uvicorn",
#   "requests",
#   "beautifulsoup4",
# ]
# ///


import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup

# import markdown

app = FastAPI()

# Enable CORS for all origins
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from fastapi.responses import PlainTextResponse


@app.get("/api/outline", response_class=PlainTextResponse)
async def generate_markdown_outline(country: str = Query(..., title="Country")):
    # Fetch Wikipedia page for the country
    print("Request received for: {country}")
    wikipedia_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"

    try:
        response = requests.get(wikipedia_url)
        response.raise_for_status()  # Will raise an exception for bad responses
    except requests.exceptions.RequestException as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error fetching Wikipedia page: {str(e)}"},
        )

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract headings (H1 to H6)
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    # Create the Markdown outline
    # markdown_outline = "## Contents\n\n"
    markdown_outline = ""

    print(headings)

    last_level = 1  # To keep track of heading levels (H1-H6)
    for heading in headings:
        level = int(heading.name[1])  # H1 -> 1, H2 -> 2, ..., H6 -> 6
        text = heading.get_text(strip=True)

        # Ensure markdown format by adding appropriate number of '#'
        # markdown_heading = f"{'#' * level} {text}"

        # Adjust heading levels based on the last heading level
        if level == 1:
            markdown_outline += f"\n# {text}\n"
        elif level == 2:
            markdown_outline += f"\n## {text}\n"
        elif level == 3:
            markdown_outline += f"\n### {text}\n"
        elif level == 4:
            markdown_outline += f"\n#### {text}\n"
        elif level == 5:
            markdown_outline += f"\n##### {text}\n"
        elif level == 6:
            markdown_outline += f"\n###### {text}\n"

    # return JSONResponse(content={"markdown_outline": markdown_outline})
    return markdown_outline


# if __name__ == "__main__":
#     import uvicorn

#     print("URL:")
#     port = 5000
#     print(f"http://localhost:{port}/api/outline")

#     uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")
