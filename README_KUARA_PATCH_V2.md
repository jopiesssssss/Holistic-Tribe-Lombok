# Kuara Resort Lombok profile patch v2

This patch updates the existing Kuara listing in the current Holistic Tribe Lombok website.

## What changed

- Replaced the existing Kuara profile page at `facilitators/kuara-lombok-south-lombok.html`.
- Added a small redirect page at `facilitators/kuara-resort-lombok.html`, so the earlier shorter URL also works.
- Added optimized Kuara images in `assets/images/kuara/`.
- Added all 24 supplied photos to a gallery slider with thumbnails.
- Added the Kuara logo to the profile page.
- Updated `data/site-data.js` and `data/facilitators.json`, so the cards on the homepage and facilitators page automatically show the new Kuara name, photo, description and profile link.

## Brochure decision

The brochure/PDF is not included in this patch. For now the page sends visitors to Kuara's official website for the latest brochure, experiences, availability and booking details.

This keeps the website lighter and avoids publishing a large sales presentation as a public download.

## Upload instructions

Upload the contents of this patch into the root of your GitHub repository and let it overwrite the existing files when asked.

After deployment, the main profile URL is:

`/facilitators/kuara-lombok-south-lombok.html`
