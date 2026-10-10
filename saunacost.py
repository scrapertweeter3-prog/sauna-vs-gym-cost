#!/usr/bin/env python3
"""sauna-cost-per-session: cost-per-session math for home recovery gear."""
import argparse
import json
import sys

KWH_DEFAULT = 2.0


def utility_cost(kwh_per_session: float, rate_per_kwh: float) -> float:
    return kwh_per_session * rate_per_kwh


def annual_sessions(sessions_per_week: float) -> float:
    return sessions_per_week * 52.0


def session_cost(gear_cost: float, total_sessions: float, utility: float) -> float:
    if total_sessions <= 0:
        return float("inf")
    return gear_cost / total_sessions + utility


def break_even_sessions(gear_cost: float, alt_per_visit: float, utility: float) -> float:
    gap = alt_per_visit - utility
    if gap <= 0:
        return float("inf")
    return gear_cost / gap


def main() -> int:
    p = argparse.ArgumentParser(description="cost-per-session math for home recovery gear")
    p.add_argument("--gear", type=float, default=None, help="total gear cost")
    p.add_argument("--week", type=float, default=None, help="sessions per week")
    p.add_argument("--kwh", type=float, default=KWH_DEFAULT, help="kWh per session")
    p.add_argument("--rate", type=float, default=0.17, help="electric rate per kWh")
    p.add_argument("--alt", type=float, default=None, help="alternative cost per visit")
    p.add_argument("--months", type=int, default=36, help="ownership window in months")
    p.add_argument("--compare", nargs=2, type=float, metavar=("A", "B"),
                   help="compare two weekly habits")
    p.add_argument("--json", action="store_true", help="machine output")
    args = p.parse_args()

    if args.compare:
        args.gear = args.gear if args.gear is not None else 2500.0
        args.alt = args.alt if args.alt is not None else 22.0
        args.months = args.months or 36
    else:
        missing = [f for f, v in (("--gear", args.gear), ("--week", args.week),
                                  ("--alt", args.alt)) if v is None]
        if missing:
            p.error(f"the following arguments are required: {', '.join(missing)}")

    util = utility_cost(args.kwh, args.rate)
    be = break_even_sessions(args.gear, args.alt, util)

    if args.compare:
        rows = []
        for wk in args.compare:
            total = wk * 4.345 * args.months
            sc = session_cost(args.gear, total, util)
            rows.append((wk, sc))
        if args.json:
            print(json.dumps({"utility_per_session": round(util, 4),
                              "compare": [{"week": w, "cost_per_session": round(c, 4)}
                                          for w, c in rows]}))
            return 0
        for w, c in rows:
            print(f"at {w:g} sessions/week  -> ${c:,.2f}/session at month {args.months}")
        best = min(rows, key=lambda r: r[1])
        worst = max(rows, key=lambda r: r[1])
        print(f"{best[0]:g} sessions/week wins, saves "
              f"${worst[1] - best[1]:,.2f}/session")
        return 0

    total = args.week * 4.345 * args.months
    sc = session_cost(args.gear, total, util)
    if args.json:
        print(json.dumps({"utility_per_session": round(util, 4),
                          "annual_sessions": round(annual_sessions(args.week), 1),
                          "sessions_in_window": round(total, 1),
                          "amortized_cost_per_session": round(sc, 4),
                          "break_even_visits": None if be == float("inf") else round(be, 1)}))
        return 0
    print(f"Sessions/week                    {args.week:>10g}")
    print(f"Annual sessions                  {annual_sessions(args.week):>10,.0f}")
    print(f"Sessions in window               {total:>10,.0f}")
    print(f"Utility/session                 ${util:>9,.2f}")
    print(f"Amortized cost/session          ${sc:>9,.2f}")
    if be == float("inf"):
        print("Break-even                       never (alternative beats your utility line)")
    else:
        print(f"Break-even vs ${args.alt:g}/visit      {be:>10,.0f} visits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
