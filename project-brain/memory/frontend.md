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
  - `SubscriptionForm` and `SubscriptionList` components.
  - Typed client `lib/api.ts` connecting to `/api/v1/subscriptions`.
- Phase 3 Authentication UI implemented:
  - Global `AuthProvider` & `useAuth` hook managing token persistence in `localStorage`, user state, and auth actions.
  - Sticky `Navbar` component with brand logo, links, dynamic user profile badge, and Sign Out action.
  - `/login` page with email & password authentication, show/hide password toggle, and 1-click Demo Account switchers (Alice vs Bob) for testing multi-user isolation.
  - `/signup` page with email, full name, password, and password confirmation validation.
  - Upgraded `/subscriptions` page to enforce JWT Bearer tokens and display live tenant isolation status.
  - Linked Clerk application `app_3KNcbw5uhM7VcS1DfaCN6zllJc8` via Clerk CLI.
  - Configured `@clerk/nextjs` with shadcn theme (`@clerk/ui`), `clerkMiddleware()` with auto-proxy matcher (`/__clerk/:path*`), and Clerk UI controls (`SignInButton`, `SignUpButton`, `UserButton`, `SignedIn`, `SignedOut`) in `Navbar`.
  - Added Clerk auth routes `/sign-in/[[...sign-in]]` and `/sign-up/[[...sign-up]]`.
  - `clerk doctor` passed with 100% green checkmarks; production build (`next build`) passing.

