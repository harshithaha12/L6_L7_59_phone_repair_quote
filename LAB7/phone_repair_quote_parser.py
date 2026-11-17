def mask_imei(imei):
    """
    Removes dashes and spaces, then hides all but the last four digits.
    Handles None, empty, or short strings safely without crashing.
    """
    if not isinstance(imei, str):
        return ""
    imei = imei.replace('-', '').replace(' ', '')
    if len(imei) <= 4:
        return imei
    return '*' * (len(imei) - 4) + imei[-4:]


def parse_parts_order(text):
    """
    Parses 'screen x1; battery x2' into a {part: quantity} dictionary.
    Handles malformed items, non-strings, and invalid numbers safely without crashing.
    """
    order = {}
    if not isinstance(text, str):
        return order
    for item in text.split(';'):
        item = item.strip()
        if not item or 'x' not in item:
            continue
        parts = item.rsplit('x', 1)
        if len(parts) != 2:
            continue
        part, qty_str = parts[0].strip(), parts[1].strip()
        if not part:
            continue
        try:
            qty = int(qty_str)
            order[part] = qty
        except (ValueError, TypeError):
            continue
    return order


def parse_model(text):
    """
    Splits 'Brand Model name' into a (brand, model) tuple.
    Handles missing models, non-strings, or empty input safely without crashing.
    """
    if not isinstance(text, str):
        return ("", "")
    cleaned = text.strip()
    if not cleaned:
        return ("", "")
    parts = cleaned.split(' ', 1)
    brand = parts[0].title()
    model = parts[1].strip() if len(parts) > 1 else ""
    return brand, model


def main():
    print("==== Running mask_imei ====")
    value = input("Enter an IMEI number (e.g. 35-209900-176148-1): ")
    print("Masked IMEI:", mask_imei(value))

    print("\n==== Running parse_parts_order ====")
    value = input("Enter parts and quantities as PART xQTY separated by ; (e.g. screen x1; battery x2): ")
    print("Parts order:", parse_parts_order(value))

    print("\n==== Running parse_model ====")
    value = input("Enter the phone brand and model (e.g. Samsung Galaxy S23): ")
    print("Brand and model:", parse_model(value))


if __name__ == "__main__":
    main()
