import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


HEADERS = {"User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")}


def extract_fashion_data(fashion):
  """
    extract fashion data from the HTML content, which includes: title, price, rating, colors, size, gender
  """
  try:
    # get the title directly
    fashion_title = fashion.find('h3').text.strip()

    # extract price
    prices = fashion.find('div', class_='price-container')
    if prices:
      price = prices.find('span', class_='price')
      price = price.text.strip() if price is not None else ''
    else:
      prices_NA = fashion.find('p', class_='price')
      price = prices_NA.text if prices_NA else ''

    # extract product detail from <p>
    fashion_elements = fashion.find('div', class_='product-details')

    fashion_data = {}
    # extract Rating
    rating_tag = fashion_elements.find('p', string=lambda string: string and 'Rating:' in string)
    rating_match = re.search(r'Rating:\s*⭐\s*(.*?)\s*/', rating_tag.text)
    fashion_data["Rating"] = rating_match.group(1) if rating_match else None

    # Extract Colors
    color_tag = fashion_elements.find('p', string=lambda string: string and 'Colors' in string)
    color_match = re.search(r'\d+', color_tag.string)
    fashion_data["Colors"] = color_match.group(0)

    # Extract Size
    size_tag = fashion_elements.find('p', string=lambda string: string and 'Size:' in string)
    size_match = re.search(r'Size:\s*([A-Z]+)', size_tag.text)
    fashion_data["Size"] = size_match.group(1) if size_match else None

    # Extract Gender
    gender_tag = fashion_elements.find('p', string=lambda string: string and 'Gender:' in string)
    gender_match = re.search(r'Gender:\s*(\w+)', gender_tag.text)
    fashion_data["Gender"] = gender_match.group(1) if gender_match else None

    # add timestamp column
    fashion_data["Timestamp"] = pd.Timestamp.now()

    # add default values for keys that might not be found
    fashion_data.setdefault("Rating", "")
    fashion_data.setdefault("Colors", "")
    fashion_data.setdefault("Size", "")
    fashion_data.setdefault("Gender", "")

    # append the result
    fashion = {
            "Title": fashion_title,
            "Price": price,
            "Rating": fashion_data["Rating"],
            "Colors": fashion_data["Colors"],
            "Size": fashion_data["Size"],
            "Gender": fashion_data["Gender"],
            "Timestamp": fashion_data["Timestamp"]}
    return fashion

  except Exception as e:
    print(f"Error extracting fashion data: {e}")
    return None


def scrape_fashion_data(BASE_URL, delay=5):
  """
    fetch all required fashion data
  """
  pages = 50
  result = []

  for i in range(1, pages + 1):
    print(f"Scraping page {i}")
    if i == 1:
      url = BASE_URL # handle special case for the first page
    else:
      url = f"{BASE_URL}page{i}"

    try:
      response = requests.get(url, headers=HEADERS, timeout=delay)
      response.raise_for_status()  # raise HTTPError for bad responses (4xx or 5xx)

      content = response.content
      parser = BeautifulSoup(content, 'html.parser')
      elements = parser.find_all("div", class_="collection-card")

      # check if the page is empty
      if not elements:
        print(f"No products found on page {i}, stopping scraping.")
        break

      for fashion in elements:
        fashion_data = extract_fashion_data(fashion)
        if fashion_data:
          result.append(fashion_data)
          print(f"   ---> {len(result)} total products")

    except Exception as e:
      print(f"An unexpected error occurred on page {i}: {e}")
      break

  return result