import requests
import urllib3

# Suppress SSL verification warnings for VTU's portal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_vtu_url(exam_session, exam_year):
    """
    Finds the correct VTU result URL by testing multiple naming patterns.

    :param exam_session: 'DJ' for Dec/Jan or 'AS' for Aug/Sept
    :param exam_year: Two-digit year string (e.g., '25')
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36"
    }

    # Calculate the next year for the expanded pattern (e.g., 25 -> 26)
    try:
        current_yr_int = int(exam_year)
        next_yr_str = str(current_yr_int + 1).zfill(2)
    except ValueError:
        return "Invalid year format."

    # Define patterns based on VTU's known behavior
    # Pattern A (New): D25J26Ecbcs (Month1 + Year1 + Month2 + Year2 + E + cbcs)
    # Pattern B (Old): DJcbcs25 (MonthCodes + cbcs + Year)
    patterns = [f"D{exam_year}J{next_yr_str}Ecbcs", f"{exam_session}cbcs{exam_year}"]

    print(f"Probing URLs for Session: {exam_session}, Year: 20{exam_year}...")

    for session_id in patterns:
        test_url = f"https://results.vtu.ac.in/{session_id}/index.php"
        try:
            # Use HEAD request to check availability without downloading the page
            response = requests.head(test_url, headers=headers, timeout=5, verify=False)

            if response.status_code == 200:
                return f"\n[SUCCESS] Found active URL:\n{test_url}"
        except Exception:
            continue

    return f"\n[FAILURE] No valid URL found for the {exam_session}{exam_year} pattern."


if __name__ == "__main__":
    # Test for the current session
    print(get_vtu_url(exam_session="DJ", exam_year="25"))
    print(get_vtu_url(exam_session="DJ", exam_year="24"))
    print(get_vtu_url(exam_session="DJ", exam_year="23"))
    print(get_vtu_url(exam_session="JJE", exam_year="24"))
    print(get_vtu_url(exam_session="JJE", exam_year="23"))
