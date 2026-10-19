# Italian Finds V6

This version keeps the V4/V5 numbered folder structure (`assets/01/`, `assets/02/`, etc.) and supports any number of cars through `cars.json`.

## Add a car
1. Create the next numbered folder, e.g. `assets/13/`.
2. Put its main image inside using `PREFIX-Main.jpg`.
3. Put gallery images in sequence: `PREFIX-01.jpg`, `PREFIX-02.jpg`, etc. Use consecutive numbering without gaps.
4. Add one entry to `cars.json` with `folder`, `prefix`, `year`, and `name`. Example:

```json
{ "folder": "13", "prefix": "GTJunior", "year": "1970", "name": "Alfa Romeo GT 1300 Junior" }
```

The code loads each car in the catalogue, and discovers gallery photographs until the first missing number. It creates no placeholder tiles.

## Optional videos
Videos are appended after photographs. Name them `PREFIX-VIDEO-01.mp4`, `PREFIX-VIDEO-02.mp4`, etc., in the same numbered car folder.

## Important static-hosting limitation
GitHub Pages does not provide a directory-listing API to browser JavaScript, so the site cannot discover newly created folders by itself. `cars.json` is the small catalogue that tells it which folders exist and each car's display name. Add one entry per car when adding a folder.
