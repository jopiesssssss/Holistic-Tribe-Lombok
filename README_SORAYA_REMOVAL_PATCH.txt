Holistic Tribe Lombok - Soraya Yoga removal patch

What changed:
- Removed Soraya Yoga from data/facilitators.json.
- Removed Soraya Yoga from data/site-data.js, while preserving the Sunset Beach Yoga changes from the previous patch.
- Removed the Soraya Yoga URL from sitemap.xml.
- Removed the Soraya .html clean-URL redirect from vercel.json.
- Replaced the old Soraya profile page files with noindex redirects to /facilitators/.

Optional cleanup in GitHub:
After uploading this patch, you may also delete this old folder and file manually if you want the repo completely clean:
- facilitators/soraya-yoga-wellness-center-gili-trawangan/
- facilitators/soraya-yoga-wellness-center-gili-trawangan.html

The patch already makes the profile invisible in listings and redirects the old URL, so manual deletion is optional.
