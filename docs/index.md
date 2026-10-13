# sauna-vs-gym-cost

A one-file terminal calculator for the home recovery gear decision:
what a sauna, cold plunge, or gym heat-lounge habit costs per session
once the sticker price is spread over the sessions you take, the
electricity line is added on top, and the visit count where owning
finally beats paying per visit is printed. It prices two usage
habits against each other from the same gear, and it says plainly
when the math never closes.

sauna-vs-gym-cost is built and maintained by [Hackedself](https://hackedself.com),
a site that prices recovery gear the same way: cost-per-session
teardowns, protocol doses, and evidence-first caveats.

## Install

Python 3.8+, standard library only. No install step, no network,
nothing leaves your machine:

    curl -O https://raw.githubusercontent.com/scrapertweeter3-prog/sauna-vs-gym-cost/main/saunacost.py

## Usage

    $ python3 saunacost.py --gear 2500 --week 3 --kwh 2.0 \
        --rate 0.17 --alt 22 --months 36
Sessions/week                             3
Annual sessions                         156
Sessions in window                      469
Utility/session                 $     0.34
Amortized cost/session          $     5.67
Break-even vs $22/visit             115 visits

The printout moves in the order a purchase decision does: the usage
habit you committed to, what the gear works out to per session over
a three-year window, and the visit count that pays it off. At three
sessions a week a $2,500 unit lands at $5.67 a sit against a $22
gym lounge, and pays for itself around visit 115.

## Two habits, one gear

Usage rate is the whole lever. The same $2,500 unit priced at two
habits:

    $ python3 saunacost.py --compare 2 5
at 2 sessions/week  -> $8.33/session at month 36
at 5 sessions/week  -> $3.54/session at month 36
5 sessions/week wins, saves $4.79/session

The gear never changed. The extra three sessions a week are what
the savings line is made of, which is why the honest denominator is
a session counter you keep, not the one on the sales page.

## When the math never closes

--alt is the per-visit price you would really pay. If a cheap gym
membership beats the electricity line alone, the gap goes negative
and no visit count closes it; the tool prints that instead of a
break-even number that looks like a win.

## JSON output

Add --json for the machine-readable form of the same run:

    $ python3 saunacost.py --gear 2500 --week 3 --kwh 2.0 \
        --rate 0.17 --alt 22 --months 36 --json
{"utility_per_session": 0.34, "annual_sessions": 156.0, "sessions_in_window": 469.3, "amortized_cost_per_session": 5.6675, "break_even_visits": 115.4}

## Honest limits

The tool treats the electric rate as flat, ignores install and
electrical work, and assumes the per-visit alternative is a real
option you would otherwise pay for. The README links the full
cost-per-session teardown method behind these numbers.

## License

MIT
