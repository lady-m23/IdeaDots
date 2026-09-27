# IdeaDots — Monetization, Limits and Server Cost Plan

**Version:** 1.0 · **Date:** 2026-09-28 · **Status:** owner decisions M1–M9 applied (M6–M9 on 2026-09-28); proposed defaults Q10–Q11 await confirmation
**Parent:** `docs/PLAN.md` §7–§9 (PLAN.md wins on conflict; this file holds the numbers and the reasoning)
**Audience:** the owner (decisions) and the coding agent (P16 Monetization, P4 schema).

Currency: ₩1,400 = US$1 for every estimate. Prices are Supabase's public list prices checked on 2026-09-28.

---

## 1. Decisions and proposals

| # | Status | Rule |
|---|---|---|
| M1 | **Decided** | **7-day Pro reverse trial** starts at the account's first sign-in, on any platform. No payment method needed. Once per person. It replaces "7-day trial on first Mac sign-in". |
| M2 | **Decided** | **Free: 5 groups** (was 10). |
| M3 | **Decided** | **No lifetime purchase.** Pro is a subscription only (monthly / yearly). |
| M4 | **Decided** | **Ads only on Free.** Pro and the trial are ad-free. Free shows a banner (iOS: AdMob; macOS: house banner). |
| M5 | **Decided** | The 90-day Free search window is dropped. Free is limited by **data per group** instead (amount: Q10). Search covers the full history on every plan. |
| M6 | **Decided** (was Q9) | **Free storage 500 MB** (D23 kept; the 200 MB proposal is not adopted); 10 MB per file. |
| Q10 | Proposed | **Free: 1,000 items per group** (5,000 in total). Pro: no product limit (abuse guard 50,000 per group). |
| Q11 | Proposed | **Pro storage 20 GB** (was 30 GB); 200 MB per file unchanged. |
| M7 | **Decided** (was Q12) | **Occasional interstitial ads on iOS Free from launch**, under the moments and caps of §6.2. The remote flag stays as a kill switch; a 10% holdout measures the effect (§6.3). |
| M8 | **Decided** | **macOS: in-house/promotional ads only**, never third-party: house banner + occasional house interstitial with the same rules as M7. No third-party ad SDK in the Mac app. |
| M9 | **Decided** | **Android / Windows** (later platforms, out of scope now): banner + occasional interstitial, same rules as iOS. |

---

## 2. How Supabase charges

| Meter | Free plan (dev only) | Pro plan ($25/month) | Overage on Pro |
|---|---|---|---|
| **Uploads (ingress)** | Free | **Free** | — |
| **Egress** (all data sent *to* clients: DB/API responses, Storage downloads, Realtime, Edge Functions, Auth) | 5 GB | 250 GB | **$0.09 / GB** |
| Cached egress (Storage served from the CDN cache) | 5 GB | 250 GB | $0.03 / GB |
| File storage (stored bytes, billed every month the data exists) | 1 GB | 100 GB | **$0.0213 / GB-month** |
| Database disk | 500 MB | 8 GB | $0.125 / GB-month |
| Monthly active users (Auth) | 50,000 | 100,000 | $0.00325 / MAU |
| Realtime messages | 2 M | 5 M | $2.50 / million |
| Edge Function invocations | 0.5 M | 2 M | $2 / million |
| Compute | shared | $10 credit = Micro | Small +$5, Medium +$50 per month |
| Pausing | Paused after 1 week idle | Never | — |

What this means:

1. **Uploads cost nothing to transfer.** They do cost money for as long as the file is kept:
   **storage** at $0.0213 per GB per month. Storage is a **stock** cost. It grows with every
   file kept, including files of users who stopped using the app.
2. **Downloads are the transfer cost.** Every file download, and every list, search result and
   realtime event sent to a device, counts as **egress** ($0.09/GB after 250 GB).
3. Production needs the **Pro plan from day one**, because Free projects pause after a week of
   inactivity. Fixed floor: **$25/month (₩35,000)**.
4. Text is almost free. Files are what cost money.

### 2.1 Unit sizes used below

| Object | Size | Basis |
|---|---|---|
| Text item row incl. indexes | **~1 KB** | ~100 Korean chars × 3 bytes + row overhead + `pg_trgm` GIN index (2–3× the text) |
| Photo, full size | **~400 KB** | 2048 px long edge, WebP ~80% (§4.9 of PLAN) |
| Photo thumbnail | **~40 KB** | 480 px long edge |
| List page | **~30 KB** | 50 items, first 1,500 chars each, JSON overhead |

---

## 3. Cost per user

### 3.1 Free storage: 200 MB vs 500 MB (Q9)

| | 200 MB | 500 MB |
|---|---|---|
| Photos that fit (≈400 KB) | ~500 | ~1,250 |
| Storage cost of a **full** account | $0.0043/month (**₩6**) | $0.0107/month (**₩15**) |
| Realistic average fill (20–30%) | 40–60 MB → ₩1–2 | 100–150 MB → ₩3–4 |
| One-time egress if a full account syncs to a new device | 0.2 GB × $0.09 = ₩25 | 0.5 GB × $0.09 = ₩63 |
| 10,000 Free users, realistic fill | ~$11/month (₩15k) | ~$27/month (₩38k) |

**Conclusion:** at the storage prices above, the choice between 200 MB and 500 MB changes cost by
only about ₩10 per user per month. The choice should be made on **conversion**:
- 200 MB (≈500 photos) is enough to build the habit, and a regular photo user reaches it in 6–12
  months, which is when an upgrade makes sense.
- 500 MB rarely runs out, so storage stops working as a reason to upgrade.

The 200 MB recommendation was not adopted: **the owner chose 500 MB (M6)**, so storage is a
comfort limit rather than the main upgrade lever; groups (M2) and items per group (Q10) carry that role.

### 3.2 Egress per active user

| Traffic | Typical Free DAU / month | Heavy user / month |
|---|---|---|
| Lists, search, realtime (text) | ~30 MB (10 opens × 3 groups × 30 KB) | ~100 MB |
| Files: thumbnails + opened originals on the *other* device | ~20–40 MB | ~200–400 MB |
| **Total** | **~60 MB → $0.005 (₩7)** | **~0.5 GB → $0.045 (₩63)** |

Egress becomes a real cost only above 250 GB/month in total, roughly 4,000 typical daily users.

### 3.3 Text per group (Q10)

A Free account at the proposed cap holds 5 groups × 1,000 items × 1 KB = **5 MB of database**. That
costs **$0.0006/month (₩1)**. Text limits are **a product lever, not a cost control**. That is why
the proposal counts items, which is easy to understand ("그룹당 메모 1,000개"), and not
characters. The 20,000-character limit per item (I1) stays the same on every plan.

What counts toward the 1,000:
- memos, tasks, links, files, images and **replies**
- **not** separators
- **not** items in the trash

The first 1,000 items take ~4–6 months per group for a heavy "나와의 채팅" user (5–10 memos/day), and
longer for most users.

### 3.4 Pro worst case (Q11)

| | 30 GB | 20 GB |
|---|---|---|
| Storage of a full Pro account | $0.64/month (₩900) | $0.43/month (₩600) |
| One full re-sync to a new device | $2.70 (₩3,800) | $1.80 (₩2,500) |
| Net revenue of a yearly Pro per month (§5.1) | ₩1,545 | ₩1,545 |

A full 30 GB account on a yearly plan leaves only about ₩600 of margin per month, and one device
re-sync erases several months of it.

20 GB is still roughly 50,000 photos. **Recommendation: 20 GB.** The per-day upload cap and the
on-device cache (§7) protect the rest.

---

## 4. Plans after this change

| | Trial (7 days) | Free | Pro |
|---|---|---|---|
| Price | ₩0, no payment method | ₩0 | ₩2,900/month or ₩24,000/year ($2.49 / $19.99) |
| Ads | None | iOS: AdMob banner + occasional interstitial (M7) · Mac: house banner + occasional house interstitial (M8) | None |
| Groups | Unlimited | **5** | Unlimited |
| Items per group | Unlimited | **1,000** (Q10) | Unlimited (guard 50,000) |
| Storage / per file | 20 GB / 200 MB | **500 MB** (M6) / 10 MB | **20 GB** (Q11) / 200 MB |
| Upload cap per day | 2 GB | 50 MB | 2 GB |
| Search | Full history | Full history (M5) | Full history |
| Trash | 30 days | 7 days | 30 days |
| Everything else | Included | Included | Included |

### 4.1 Reverse trial (M1)

- **Start:** the first successful sign-in of the account, on any platform. The server sets
  `plan = 'trial'` and `trial_ends_at = now() + 7 days`. The client never decides.
- **Once per person:**
  - At trial start the server stores `sha256(pepper ‖ identity)` in `trial_ledger`. The identity
    is the Apple `sub`, or the lower-cased email for email sign-in.
  - The ledger survives account deletion, so deleting and signing up again gives no second trial.
  - The privacy policy states this. The hash cannot be reversed to an identity.
- **Welcome sheet** after the first sign-in: "7일 동안 Pro를 무료로 써보세요 — 결제 정보 필요 없음". It
  lists what Pro adds and has a single OK button.
- **During the trial:**
  - The Settings → Plan row shows "Pro 체험 · N일 남음".
  - On day 5 an in-app notice appears once.
  - If notification permission is already granted (for alarms), one local notification is sent
    24 h before the end. The app never asks for permission for this.
- **Buying during the trial:** the RevenueCat entitlement wins and the trial ends immediately. There
  is **no App Store introductory offer**, because the reverse trial already gave the free week.
- **End:** see the downgrade rules in §4.2. The next launch shows the downgrade sheet (screen spec
  board to add: "Trial ended"):
  - what changes
  - the group picker, if the account has more than 5 groups
  - **Upgrade** and **Continue with Free**

### 4.2 Downgrade rules: nothing is lost, nothing is hidden

| Over the limit | What happens |
|---|---|
| **More than 5 groups** | The user picks 5 **active** groups. The others become **paused**: readable, searchable, exportable, and items can be selected, deleted or moved out. A paused group can't receive new items. The header shows a small lock chip and the input bar is replaced by "일시정지된 그룹 · Pro에서 다시 사용" with **Change active groups**. The active set can be changed **once per 24 h**; without that limit, swapping groups would give unlimited groups for free. |
| **More than 1,000 items in a group** | The group stays active. New items are refused in that group until it is under the cap. The input bar shows "이 그룹이 가득 찼어요 (1,000/1,000)" with **Upgrade** and **Select to clean up**. A counter appears from 900. |
| **Storage over 500 MB** | Every file stays viewable and downloadable. New attachments are refused until usage is under the limit. Text, tasks, links, separators and alarms keep working (PLAN §7). |
| Group creation | The 6th group on Free opens the Pro sheet. |
| Upgrading again | Every paused group becomes active immediately; nothing needs restoring. |

---

## 5. Revenue model

### 5.1 Net revenue per Pro subscriber (Korea)

App Store prices in Korea include 10% VAT. Apple's Small Business Program takes 15%.

| Plan | Price | Net per month |
|---|---|---|
| Monthly | ₩2,900 | ₩2,900 ÷ 1.1 × 0.85 = **₩2,241** |
| Yearly | ₩24,000 | ₩24,000 ÷ 1.1 × 0.85 ÷ 12 = **₩1,545** |
| Blend (40% monthly / 60% yearly) | | **₩1,823** |

RevenueCat is free up to $2,500 of monthly tracked revenue and charges 1% above that.

### 5.2 Ad revenue per iOS Free daily user

Assumptions:
- Korea (Tier 2)
- iOS without an ATT prompt, so no IDFA and lower bids
- Fill rate 85–95%
- The banner is hidden while the keyboard is up, so it is visible only part of a ~3–5 minute daily session

| Format | Impressions / DAU / month | eCPM (KR iOS, no IDFA) | Revenue / DAU / month |
|---|---|---|---|
| Banner (adaptive, 60 s refresh) | 90–180 | $0.15–0.40 | $0.014–0.072 · **mid ₩50** |
| Interstitial (rules in §6.2; 0.2–0.6 per day) | 6–18 | $3–7 | $0.018–0.126 · **mid ₩84** |
| Mac house banner | — | — | ₩0 (conversion and cross-promotion only) |

One blended Pro subscriber (₩1,823/month) is worth about **36 iOS Free daily users' banner revenue**,
or about **13 users' banner + interstitial revenue**.

### 5.3 Monthly scenarios (steady state)

Shared assumptions:
- DAU/MAU 40%
- 85% of Free daily use happens on iPhone
- Free users hold ~60 MB each and Pro users ~2 GB each

The Conservative row assumes 2% conversion with low eCPM; the other rows assume 4% conversion with mid eCPM.

| | Pro subs | Pro net | Banner | Interstitial (if on) | Supabase + fixed costs | **Net, banner only** | **Net, + interstitial** |
|---|---|---|---|---|---|---|---|
| 1k MAU | 40 | ₩73k | ₩16k | ₩27k | ₩50k ($25 + Apple ₩11k) | **₩39k** | **₩66k** |
| 10k MAU, conservative | 200 | ₩365k | ₩65k | ₩82k | ₩120k | **₩310k** | **₩392k** |
| 10k MAU, base | 400 | ₩729k | ₩163k | ₩274k | ₩120k | **₩772k** | **₩1,046k** |
| 50k MAU, base | 2,000 | ₩3.65M | ₩816k | ₩1.37M | ₩450k | **₩4.02M** | **₩5.39M** |

How the cost column is built:
- **10k:** $25 Pro plan, +$5 Small compute, ~$27 storage (≈1.4 TB), ~$10 egress, Apple ₩11k/month.
- **50k:** Medium compute, ~6.8 TB storage (~$143), ~1.2 TB egress (~$86).

What the numbers say:
1. **Subscriptions carry the business.** Pro is 60–85% of revenue in every row.
2. **At the base case the banner adds ~20%.** The interstitial would add a further ~20–30%. The
   interstitial is the only lever above that changes the result by more than a rounding error.
3. **Break-even:**
   - The fixed floor (~₩50k) is covered by **~28 Pro subscribers**, or ~1,000 iOS Free daily
     users on banners alone.
   - Above ~10k MAU, total cost stays near 10% of revenue. Below that, the fixed $25 floor dominates,
     because storage and egress per user are pennies.
4. **The interstitial pays for itself financially** under almost any assumption. Losing one Pro
   subscriber costs as much as the interstitial income of ~22 Free daily users, and interstitials
   usually *raise* ad-free upgrades rather than lower them.
   Its real risks are ones the model can't price:
   - App Store ratings ("광고 너무 많아요")
   - Weaker word of mouth
   - Harm to the core promise of **fast capture**

   The owner chose to launch it on (M7), so these risks are handled by strict placement rules,
   caps, a 10% holdout for measurement and the remote kill switch (§6.3).

---

## 6. Advertising specification

### 6.1 Banner (Free only; unchanged from PLAN §8 except the trial)

- **iOS:** AdMob anchored adaptive banner in the 50 pt slot under the input bar, with an 8 pt gap
  and a hairline above it. Hidden while the keyboard is up.
- **Consent:** no ATT prompt at launch; UMP for EEA/UK.
- **macOS:** house banner in the same slot, rotating:
  - Pro pitch
  - Tips
  - **Cross-promotion of TaskHolder**, the owner's other app
- **Hidden** during the trial and on Pro.

### 6.2 Interstitial (Free: AdMob on iOS, house card on macOS; flag `ads.interstitial.enabled`, on at launch)

Shown only **after the user finishes something**, never before or during an action.

| Allowed moments | Never shown |
|---|---|
| Closing Search after a query | In a session opened from the widget, quick capture, share sheet, notification or any deep link |
| After the Export share sheet is dismissed | Within 120 s of the app coming to the foreground |
| Leaving the Reorder groups page | While the keyboard is up, during selection mode, or while an alarm toast is showing |
| After a multi-select action completes (move, merge, delete) | During the trial or on Pro |
| | During the first 3 days after the trial ends |

Rules:
- **Frequency caps:**
  - at least 3 h between interstitials (`ads.interstitial.min_gap_min`, default 180)
  - at most 2 per day (`ads.interstitial.max_per_day`)
- **Loading:** preload in the background when a moment becomes likely. If no ad is loaded at the
  moment, **skip it; never wait or show a spinner**.
- **macOS (M8):** the same moments, exclusions and caps show a **house interstitial**: a
  dismissible promo card over the window (Pro benefits, price, **Upgrade**, **Not now**; close
  visible at once). It is bundled with the app; no ad network, no tracking.
- **Rejected formats:**
  - **App-open ads**: they delay capture, the main promise.
  - **Rewarded ads for extra quota**: too complex for the gain.

### 6.3 Launch and monitoring of the interstitial (M7)

1. Launch with interstitials **on** for iOS Free users (`ads.interstitial.enabled` = `{"pct": 90}`).
   The server assigns a stable `ab_bucket` per user; the 10% outside `pct` never sees an
   interstitial and is the **holdout** used to measure the effect. The owner may set `pct` to 100.
2. Review weekly, then after 4 weeks compare exposed users with the holdout:
   - D7 and D30 retention of Free users
   - trial→paid conversion
   - banner + interstitial ARPDAU
   - App Store rating and reviews that mention ads
3. Keep it if exposed D30 retention is within **2 points** of the holdout, conversion does not
   drop, and the rating holds. Otherwise lower the caps or switch it off remotely. No app release is
   needed for either.

---

## 7. Cost guardrails

| Guardrail | Rule |
|---|---|
| Uploads | On-device compression (PLAN §4.9). The daily upload caps in §4. No video (C9). |
| Downloads | The uploading device seeds its own disk cache, so it never downloads its own upload. LRU disk cache for originals: iOS 500 MB, Mac 2 GB. Thumbnails in lists. Signed URLs are cacheable for the URL lifetime, so CDN hits bill as cached egress ($0.03). |
| Lists | Only the first 1,500 characters of each body per row (PLAN §6). Pages of 50. Refetch since the cursor, not full reloads. |
| Supabase Spend Cap | **On** until 1k MAU. After that turn it **off**, because hitting the cap restricts service, and check usage weekly. |
| Dormant data | Revisit in year 2 once the storage stock can be measured. Option: attachments of Free accounts idle > 12 months are removed after two emails; text is kept. Not adopted now. |
| Storage backend (Q5) | Stay on Supabase Storage. Move files to **Cloudflare R2** (no egress fees, $0.015/GB) when Storage egress overage passes **$50/month** or stored files pass **3 TB**. |

---

## 8. Data model changes (P4 schema; P16 behavior)

```sql
-- Limits live in data, so changing a number is an UPDATE, not a migration.
create table plan_limits (
  plan text primary key check (plan in ('free','trial','pro')),
  max_groups int,                 -- null = unlimited
  max_items_per_group int,        -- Free 1000, Pro/trial 50000 (guard)
  storage_bytes bigint,           -- Free 500 MB, Pro/trial 20 GB
  max_file_bytes bigint,          -- 10 MB / 200 MB
  daily_upload_bytes bigint,      -- 50 MB / 2 GB
  trash_days int,                 -- 7 / 30
  ads boolean
);

alter table entitlements
  add column trial_started_at timestamptz,
  add column trial_ends_at timestamptz,
  add column pro_expires_at timestamptz,        -- written by revenuecat-webhook
  add column active_groups_changed_at timestamptz,
  add column ab_bucket smallint default (floor(random()*100))::smallint;

create table trial_ledger (identity_hash text primary key, first_trial_at timestamptz not null);

alter table groups
  add column paused boolean not null default false,
  add column item_count int not null default 0;   -- maintained by trigger; no count(*) on insert

create table app_config (key text primary key, value jsonb not null);  -- remote flags, read-only to clients
```

- `effective_plan(uid)` (SQL, `stable`) returns `'pro'` if `pro_expires_at > now()`, else
  `'trial'` if `trial_ends_at > now()`, else `'free'`. Every limit check calls it. Nothing is
  stored as "current plan", so expiry needs no cron job.
- **Insert trigger on `items`:**
  - rejects inserts into a paused group
  - rejects inserts when `item_count >= max_items_per_group` for the effective plan
  - separators and trashed rows don't count
  - error code `P0001 item_limit`, mapped to the full-group bar
- **Group insert trigger:** rejects when active groups reach `max_groups`.
- **`start_trial()` RPC:**
  - called once after sign-in
  - idempotent
  - checks `trial_ledger` first
- **`set_active_groups(ids uuid[])` RPC:**
  - enforces 5 and the 24 h rule
  - flips `paused`
- **On downgrade** (first Free read after expiry), when groups > 5: the most recently opened 5
  stay active until the user chooses otherwise.
- `app_config` keys:
  - `ads.interstitial.enabled` (`{"pct":90}` at launch, M7)
  - `ads.interstitial.min_gap_min`
  - `ads.interstitial.max_per_day`
  - `ads.interstitial.grace_days`

---

## 9. Implementation tasks (replace P16 tasks 16.1–16.3; add 16.4–16.6)

| Task | Scope | Acceptance |
|---|---|---|
| 16.1 Entitlements and gating | `plan_limits`, `effective_plan`, triggers above; `EntitlementsRepo` exposes the plan, the limits and `trialDaysLeft`; every gate reads it | Editing `plan_limits`, or moving `trial_ends_at` into the past, flips every gate without a restart; pgTAP tests: 6th group rejected on Free, 1,001st item rejected, a separator still accepted at the cap, a paused group rejects inserts |
| 16.2 Banner ads | As PLAN §8, plus hidden during the trial | Test ads on iOS; no slot on the trial or Pro; house banner on Mac |
| 16.3 RevenueCat purchase | `pro_monthly` / `pro_yearly`, no introductory offer, Restore, webhook writes `pro_expires_at`, universal purchase | Sandbox purchase on iPhone unlocks the Mac within one realtime event |
| 16.4 Reverse trial | `start_trial()`, `trial_ledger`, welcome sheet, Plan row countdown, day-5 notice, optional 24 h local notification | New account → trial; delete account + sign up again → no trial; clock moved past the end → downgrade sheet |
| 16.5 Downgrade flow | Trial-ended sheet, group picker, paused-group header and input bar, `set_active_groups` with the 24 h rule, full-group bar, 900+ counter | Account with 8 groups, 1,200 items in one group and 300 MB: nothing lost, every rule of §4.2 is visible |
| 16.6 Interstitials (M7, M8) | `google_mobile_ads` interstitial on iOS; house interstitial card on macOS; one `InterstitialGate` enforcing §6.2 (moments, caps, grace, deep-link sessions) on both; `app_config` read, `ab_bucket` holdout | Flag off → never shown; flag on → shown only at the listed moments, never twice within the gap, never in a widget-opened session, never for the holdout; the macOS bundle contains no third-party ad SDK |

**Owner inputs:**
- AdMob interstitial unit id
- App Store Connect products without an introductory offer
- A privacy-policy line about the trial ledger
- A privacy-label check (no change while there is no ATT)

---

## 10. Risks

| Risk | Mitigation |
|---|---|
| App Review questions a server-granted trial that doesn't go through IAP (Guideline 3.1.1) | Pro is unlocked only through IAP. The trial is a promotional period with no purchase. State this in the review notes. Fallback: remove the reverse trial and use an App Store 7-day introductory free trial on `pro_yearly`. |
| Users feel the 5-group drop after the trial as a loss | Nothing is deleted or hidden. The downgrade sheet explains the rules before anything changes. Paused groups stay fully readable. |
| The interstitial hurts ratings | Strict moments and caps, 10% holdout to measure it, remote kill switch (§6.3). |
| Storage stock grows with churned users | Measure it in year 2; dormant-data option in §7. The R2 trigger in §7. |
| Low eCPM without ATT | Accepted for a privacy-first memo app. Revisit an ATT pre-prompt only if ad revenue matters more than the current model assumes. |

---

## Sources (checked 2026-09-28)

- Supabase pricing: https://supabase.com/pricing
- Supabase egress: https://supabase.com/docs/guides/platform/manage-your-usage/egress
- AdMob eCPM benchmarks 2026: https://www.revenuelab.fyi/blog/admob-ecpm-benchmarks-2026
- RevenueCat State of Subscription Apps 2026: https://www.revenuecat.com/state-of-subscription-apps
