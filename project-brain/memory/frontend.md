# Subsfolio — Frontend Architecture

## 1. Stack & Tools
- **Framework**: Next.js (App Router), React, TypeScript.
- **Styling**: Tailwind CSS, shadcn/ui component library, Lucide Icons.
- **State & Data Fetching**: TanStack Query / React Hooks.

## 2. Planned Pages & Routes
- `/` — Landing Page (Marketing, Value Proposition)
- `/login` & `/signup` — Authentication entrypoints
- `/dashboard` — Main Analytics & Renewals Dashboard
- `/subscriptions` — Subscription list and management
- `/subscriptions/new` — Add subscription form
- `/subscriptions/[id]` — Subscription detail & edit view
- `/subscriptions/import` — Email/receipt extraction staging & confirmation
- `/assistant` — AI Natural-language subscription query chat
- `/settings` — User profile, reminder preferences, integrations

## 3. UI Components & Modules
- `DashboardStats` — KPI metrics cards (monthly spend, active count, upcoming renewals) (Phase 4)
- `SubscriptionList` — List of user subscriptions with status badges, price, renewal date, edit/archive actions
- `SubscriptionForm` — Create and edit modal form with validation
- `lib/api.ts` — Typed fetch client for backend API with development user support
- `SpendingChart` — Category breakdown & monthly expense trends (Phase 4)
- `UpcomingRenewalsList` — Timeline of upcoming charges (Phase 5)
- `ExtractionReviewCard` — Staged AI extraction confirmation card (Phase 6)

## 4. Implementation Status
- Phase 1 Foundation implemented: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, shadcn/ui readiness (`components.json`, `lib/utils.ts`).
- Phase 2 Subscription Management UI implemented:
  - `/subscriptions` management page with create, edit, filter, and archive capabilities.
  - Development identity switcher allowing testing of user isolation directly in the browser.
  - `SubscriptionForm` and `SubscriptionList` components.
  - Typed client `lib/api.ts` connecting to `/api/v1/subscriptions`.
  - Zero ESLint warnings, TypeScript passing (`tsc --noEmit`), and optimized production build (`next build`) passing.

