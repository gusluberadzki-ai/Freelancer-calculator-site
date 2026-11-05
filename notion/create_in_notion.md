# Creating the Notion templates for real

Specs live in `templates.py` (and `notion-specs.json` in the project files at `income/notion/`).
They need a session with the **Notion connector** connected to Gustaw's workspace.

## Steps for the session
1. Create a top-level page "Template Shop" (private).
2. For each template in `T`:
   - Create a child page with the template's icon and name. Add an intro paragraph (`intro`), a "How to use" bulleted list (`features`), and a callout "Delete the sample entries when you're ready."
   - Create each database in `dbs` inline on that page, with properties exactly as listed
     (type in position 1, options in position 2; `relation` targets the named database on the same page;
     `rollup` is "Database.Property function"; `formula` uses Notion formula 2.0 syntax).
   - Add the sample `rows` (relations matched by title; checkbox "Yes" = checked).
   - Add the views listed in `views` where the connector supports it (Board by X, Calendar by date, Gallery, filtered "This month"/"This week"/"Unpaid").
3. Ask Gustaw to open each template page, click **Share > Publish**, and switch on **Allow duplicate as template**. Collect the 8 public links. (This toggle is the one step the API can't do.)
4. With the links:
   - Make a one-page PDF per template ("Click here to duplicate your template" + link + 3 steps) for Etsy's digital file.
   - Gumroad: create a product per template (and the bundle) with the link in the content, using covers from `income/notion/<slug>/images/`.
   - Notion Marketplace: submit at notion.com/templates/creators with the cover and listing copy in `listing.md`.

## Fallback without the connector
`<slug>-notion-import.zip` (Markdown + CSV) imports via Notion Settings > Import > Markdown/CSV, but property types
(select, date, checkbox, formulas, relations) must then be set by hand, so it is for building, not for selling.
