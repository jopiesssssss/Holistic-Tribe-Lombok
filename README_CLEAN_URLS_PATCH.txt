Holistic Tribe Lombok clean URLs patch

Upload this patch into the root of your GitHub repository and overwrite existing files.

What this patch does:
- Creates clean directory URLs for all .html pages, for example:
  /about/
  /facilitators/
  /facilitators/kuara-lombok-south-lombok/
  /holistic-practices/breathwork/
  /holistic-travel-guides/best-holistic-things-to-do-in-lombok-after-bali/

- Updates internal navigation/card/data links to use clean URLs.
- Keeps old .html URLs working by replacing them with redirect pages.
- Adds vercel.json redirects for proper permanent redirects on Vercel.
- Updates sitemap.xml to clean canonical URLs.

Important:
- Upload this after the latest Kuara patch.
- Do not delete folders such as assets/ or data/.
- After deploying, test the homepage, facilitators page, Kuara page, practice guides and travel guides.
