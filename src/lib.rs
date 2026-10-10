//! Cost-per-session math for home recovery gear.
//!
//! A home sauna or cold plunge is a gear price, a usage habit, and an
//! electricity line. These functions restate that into dollars per
//! session and the visit count where the gear beats a gym membership.

/// Per-session utility cost from kilowatt-hours and a rate.
///
/// ```
/// let u = sauna_vs_gym_cost::utility_cost(2.0, 0.17);
/// assert!((u - 0.34).abs() < 1e-9);
/// ```
pub fn utility_cost(kwh_per_session: f64, rate_per_kwh: f64) -> f64 {
    kwh_per_session * rate_per_kwh
}

/// Sessions a weekly habit adds up to over a year.
///
/// ```
/// let s = sauna_vs_gym_cost::annual_sessions(4.0);
/// assert!((s - 208.0).abs() < 1e-9);
/// ```
pub fn annual_sessions(sessions_per_week: f64) -> f64 {
    sessions_per_week * 52.0
}

/// Amortized cost of one session: gear price spread over total sessions,
/// plus the utility line.
///
/// ```
/// let c = sauna_vs_gym_cost::session_cost(2_500.0, 1_000.0, 1.40);
/// assert!((c - 3.9).abs() < 1e-9);
/// ```
pub fn session_cost(gear_cost: f64, total_sessions: f64, utility_per_session: f64) -> f64 {
    if total_sessions <= 0.0 {
        return f64::INFINITY;
    }
    gear_cost / total_sessions + utility_per_session
}

/// Visits until the gear has paid for itself against a per-visit
/// alternative. Infinite when the alternative is cheaper than the
/// electricity alone, because usage then never closes the gap.
///
/// ```
/// let b = sauna_vs_gym_cost::break_even_sessions(2_500.0, 22.0, 1.40);
/// assert!((b - 2_500.0 / 20.6).abs() < 1e-9);
/// ```
pub fn break_even_sessions(gear_cost: f64, alternative_per_visit: f64, utility_per_session: f64) -> f64 {
    let gap = alternative_per_visit - utility_per_session;
    if gap <= 0.0 {
        return f64::INFINITY;
    }
    gear_cost / gap
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn amortization_falls_as_sessions_stack() {
        let early = session_cost(2_500.0, 100.0, 1.40);
        let late = session_cost(2_500.0, 1_000.0, 1.40);
        assert!(late < early);
    }

    #[test]
    fn pricier_gym_shortens_break_even() {
        let cheap = break_even_sessions(2_500.0, 15.0, 1.40);
        let pricey = break_even_sessions(2_500.0, 30.0, 1.40);
        assert!(pricey < cheap);
    }

    #[test]
    fn never_breaks_even_when_utility_covers_the_visit() {
        assert!(break_even_sessions(2_500.0, 1.00, 1.40).is_infinite());
    }

    #[test]
    fn annual_scales_linearly() {
        assert!(annual_sessions(6.0) > annual_sessions(3.0));
    }

    #[test]
    fn zero_sessions_is_infinite_not_a_crash() {
        assert!(session_cost(2_500.0, 0.0, 1.40).is_infinite());
    }
}
