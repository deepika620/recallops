from memory import recall


def _dedupe(result, top_n):
    matches = []
    seen = set()
    for m in result.results:
        text = m.text.strip()
        if text in seen:
            continue
        seen.add(text)
        matches.append(text)
        if len(matches) == top_n:
            break
    return matches


def search_alert(alert_text, top_n=6):
    """One Hindsight recall per alert."""
    return _dedupe(recall(alert_text), top_n)


if __name__ == "__main__":
    alert = input("Paste an alert: ")
    for i, text in enumerate(search_alert(alert), start=1):
        print(f"{i}. {text}")