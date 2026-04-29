# Holistic Tribe Lombok — static site

This folder is ready to upload to a new GitHub repository and deploy with Vercel as a static website.

## What is included

- Shared header and footer across all pages
- Homepage with facilitator cards, practice browsing and agenda preview
- Separate pages for Facilitators, Agenda, About and Contact
- 16 facilitator profile pages with the existing external photo links and information carried over
- Data files for facilitators and events
- Smarter agenda behavior: multi-day retreats/trainings are shown as one date-range listing instead of repeated every day
- Contact page with separate flows for visitors, facilitators and event updates

## File structure

```text
index.html
facilitators.html
agenda.html
about.html
contact.html
facilitators/
assets/css/styles.css
assets/js/main.js
data/site-data.js
data/facilitators.json
data/events.json
assets/images/general/holistic-tribe-lombok-hero.webp
```

## How to deploy with GitHub + Vercel

1. Create a new empty GitHub repository.
2. Upload all files and folders from this folder into the repository root.
3. In Vercel, choose **Add New Project**.
4. Import the GitHub repository.
5. Use the default static settings. No build command is required.
6. Deploy.

## How to update facilitators

For quick data updates, edit:

- `data/site-data.js` for the live JavaScript data used by the site
- `data/facilitators.json` as a clean reference copy

At the moment, facilitator profile pages are generated as static HTML. If you change a facilitator heavily in the data, also update the matching file in `facilitators/`.

## How to update agenda events

Edit the events inside:

- `data/site-data.js`
- `data/events.json` as reference

For multi-day retreats or trainings, use both `date` and `endDate`. Example:

```json
{
  "title": "200H Yoga Teacher Training",
  "date": "2026-04-06",
  "endDate": "2026-04-28",
  "time": "Multi-day program",
  "type": "Training"
}
```

The agenda will show this as one date-range event.

## Photos

This version uses the existing external image URLs. Later, when facilitators send you photos, place them in something like:

```text
assets/images/facilitators/
```

Then update the image URLs in `data/site-data.js` and the matching profile HTML page.
