"""Chippy's menu as a web page: writes menu.html beside this file."""
from html import escape
from pathlib import Path

MENU = [("Chips", 320), ("Cod", 790), ("Haddock", 850),
        ("Chicken parmo", 990)]


def menu_rows(menu):
    """Return one table row of HTML for each item on the menu.

    Args:
        menu: a list of (item, price in pence) pairs.

    Returns:
        The rows as one string, each item's name escaped.
    """
    rows = []
    for item, pence in menu:
        rows.append(f"<tr><td>{escape(item)}</td>"
                    f"<td>£{pence / 100:.2f}</td></tr>")
    return "\n".join(rows)


def menu_page(menu):
    """Return the whole page: the template's skeleton around the rows.

    Args:
        menu: a list of (item, price in pence) pairs.

    Returns:
        The page as one string of HTML.
    """
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1">
  <title>Chippy: menu</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>Chippy</h1>
    <p>Fish and chips, fried fresh</p>
  </header>
  <main>
    <h2>Menu</h2>
    <table>
      <caption>Prices for one portion</caption>
      <thead>
        <tr><th>Item</th><th>Price</th></tr>
      </thead>
      <tbody>
{menu_rows(menu)}
      </tbody>
    </table>
  </main>
  <footer>
    <p>Chippy, Teesside</p>
  </footer>
</body>
</html>
"""


def main():
    """Write menu.html beside this file, then say where it is."""
    page = Path(__file__).with_name("menu.html")
    page.write_text(menu_page(MENU), encoding="utf-8")
    print(f"Written: {page}")


if __name__ == "__main__":
    main()
