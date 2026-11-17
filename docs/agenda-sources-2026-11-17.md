# Lombok agenda — 17 November 2026

Primary sources: Ola Ola weekly yoga/Pilates page; Flowers & Fire schedule; Ashtari class and Aspire to Inspire pages; Mana yoga and mini-retreat pages; Gili Yoga; Zora agenda; Xanadu yoga immersion page. All source URLs and check dates are stored with each listing in `data/agenda.json`.

Ola Ola: explicit Monday–Saturday timetable. Copied times are shown until 17 December, after which visitors use the linked live studio timetable. Flowers & Fire: the page calls its workshop times “this week”; those entries are shown only through Sunday 22 November. Daily studio cards do not invent fixed start times. Zora special events have explicit dates and locations, including Kenza’s Garden for Yoga & Brunch. Multi-day Xanadu, Mana and Ashtari dates are published by the organisers. No public source check is presented as personal confirmation by a provider.

Replaced the previous dated feed, including May–September events and the unconfirmed old Ashtari November training. No old class has been promoted to a recurring entry. Ended events hide automatically, using Asia/Makassar and explicit end times when available. Multi-day events remain visible through their final day and are marked as in progress after starting. Weekly programme cutoffs prevent copied timetables from remaining current indefinitely. All event pages link directly to organisers for current availability; no claim of bookable capacity is made.

Edit `data/agenda.json` as the source of truth, then run `python3 scripts/render-agenda-data.py`. HTML and navigation updates also persist in `scripts/render-island-pages.py`.
