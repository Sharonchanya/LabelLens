import re


def extract_net_quantity(ocr_results):
    for item in ocr_results:
        text = item["text"]

        match = re.search(
            r"\b\d+(?:\.\d+)?\s*(g|kg|ml|l|litre|litres)\b",
            text,
            re.IGNORECASE
        )

        if match:
            return match.group()

    return None


def extract_mrp(ocr_results):
    for index, item in enumerate(ocr_results):
        text = item["text"]

        match = re.search(
            r"(?:MRP|M\.R\.P\.?)\s*(?:RS\.?|₹)?\s*(\d+(?:\.\d+)?)",
            text,
            re.IGNORECASE
        )

        if match:
            return f"₹{match.group(1)}"

        if re.search(r"\bMRP\b", text, re.IGNORECASE):

            if index + 1 < len(ocr_results):
                next_text = ocr_results[index + 1]["text"]

                price_match = re.search(
                    r"\b(\d+(?:\.\d+)?)\b",
                    next_text
                )

                if price_match:
                    return f"₹{price_match.group(1)}"

    return None


def extract_manufacturer(ocr_results):
    manufacturer_keywords = [
        "manufactured by",
        "manufactured for",
        "manufacturer",
        "packed by",
        "marketed by"
    ]

    for index, item in enumerate(ocr_results):
        text = item["text"].lower()

        for keyword in manufacturer_keywords:
            if keyword in text:

                manufacturer_text = []

                for next_index in range(
                    index + 1,
                    min(index + 4, len(ocr_results))
                ):
                    next_text = ocr_results[next_index]["text"]
                    manufacturer_text.append(next_text)

                if manufacturer_text:
                    return " ".join(manufacturer_text)

    return None


def extract_date_information(ocr_results):
    date_keywords = [
        "manufacturing",
        "manufactured",
        "mfg",
        "mfd",
        "packing",
        "packed",
        "pkd",
        "best before",
        "expiry",
        "exp",
        "use by"
    ]

    for index, item in enumerate(ocr_results):
        text = item["text"]

        for keyword in date_keywords:

            if keyword in text.lower():

                # Check whether the current text contains a number
                if any(char.isdigit() for char in text):
                    return text

                # Otherwise, check the next OCR result
                if index + 1 < len(ocr_results):
                    next_text = ocr_results[index + 1]["text"]

                    if any(char.isdigit() for char in next_text):
                        return f"{text} {next_text}"

    return None