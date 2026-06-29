# Weather Shopper — Selenium + pytest (Python)

End-to-end automation of the [Weather Shopper](https://weathershopper.pythonanywhere.com/) test app using **Selenium WebDriver**, **pytest** and the **Page Object Model**.

## Flow automated
1. Read temperature; buy moisturizers (<19 °C) or sunscreens (>34 °C).
2. Add cheapest *Aloe* + *Almond* (or *SPF-50* + *SPF-30*).
3. Cart → Stripe iframe checkout → pay with public test card.
4. Assert `PAYMENT SUCCESS`.

> Card `4242 4242 4242 4242` is Stripe's public test card — not a real card.

## Setup & run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest            # report at reports/report.html
```

## Stack
Selenium 4 · pytest · POM · webdriver-manager · pytest-html · GitHub Actions CI.
