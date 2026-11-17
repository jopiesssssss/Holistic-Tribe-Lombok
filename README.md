# Holistic Tribe Lombok — static site

This folder is ready to upload to a new GitHub repository and deploy with Vercel as a static website.

## What is included

- Shared header and footer across all pages
- Homepage with facilitator cards, practice browsing and agenda preview
- Separate pages for Facilitators, Agenda, About, Contact and Holistic Travel Guides
- 16 facilitator profile pages with the existing external photo links and information carried over
- Data files for facilitators and events, refreshed for the live agenda
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
holistic-travel-guides/
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


## Live-ready patch notes

This version removes the About page hero image, adds non-profit language in key places, refreshes agenda behavior so it starts from current/upcoming events, adds new researched events and adds three SEO travel guide pages linked from the homepage.

The travel guide pages are located in:

```text
holistic-travel-guides/
```

After upload, check these URLs:

```text
/holistic-travel-guides/
/holistic-travel-guides/bali-or-lombok-yoga-wellness.html
/holistic-travel-guides/best-holistic-things-to-do-in-lombok-after-bali.html
/holistic-travel-guides/tetebatu-lombok-nature-meditation-slow-travel.html
```


## Source-reviewed provider profiles

New profiles with `profileTemplate: "source-v1"` are generated from `data/facilitators.json` using `python3 scripts/render-source-profiles.py`. Update the same provider in `data/site-data.js`, then rerun the renderer. Custom legacy profiles are preserved. Public source checks are not provider confirmations. Do not add seasonal classes or guessed map coordinates as verified availability.

## Refreshed profiles and discovery pages (17 November 2026)

Build the static pages in this order:

```sh
python3 scripts/render-island-pages.py
python3 scripts/render-discovery-pages.py
python3 scripts/render-agenda-data.py
python3 scripts/render-practice-guides.py
python3 scripts/finalize-discovery-seo.py
```

The data in `data/facilitators.json` remains the provider source. The new renderer updates 21 profiles. Sunset retains its separate photo design, and Kuara retains its complete checked main HTML; its refresh uses scoped CSS only. `data/agenda.json` remains the calendar source. Discovery pages select real published providers by their recorded categories and area; held-for-review profiles stay excluded.

Finalization adds canonical metadata, provider/site/breadcrumb/list structured data, crawlable directory cards, internal links, redirects and a sitemap. Run finalization after rendering before publication. `data/seo-pages.json` records the indexable pages. No ratings, invented opening hours, guessed addresses, availability claims or guaranteed search rankings are added.

## Practice library

The seven English practice guides are maintained in `data/practice-guides.json`. Run `python3 scripts/render-practice-guides.py` after profile/homepage renderers and before SEO finalization. This also adds relevant guide links to published profiles, preserving the complete checked Kuara profile. Existing mandalas are retained; four new covers are in `assets/images/practices/`.

Agenda listings carry explicit `practices` tags: a workshop can be tagged Breathwork without changing its event type or a provider’s permanent categories. `/agenda/?practice=Breathwork&view=events` opens a visible practice filter. Guide previews share the agenda’s WITA date and expiry logic. Unverified or expired weekly times stay hidden; provider timetables and appointment links remain available.

Validate with `node scripts/test-practice-agenda.cjs` and `python3 scripts/check-practice-guides.py`.
