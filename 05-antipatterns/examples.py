"""Examples of common Python anti-patterns — Python Patrol demo."""


def process_items(items=[]):
    """PP001: Mutable default argument."""
    items.append("new")
    return items


def check_status(code):
    """PP002: List membership check — should use set."""
    if code in [200, 201, 204, 301, 302, 400, 401, 403, 404, 500]:
        return True
    return False


def build_query(parts):
    """PP003: String concatenation in a loop."""
    query = ""
    for part in parts:
        query += part + " AND "
    return query


def total_score(records):
    """PP005: Unnecessary list comprehension in sum()."""
    return sum([r.score for r in records])


def find_user(users, target):
    """PC005: Comparison with None using ==."""
    for user in users:
        if user.name == None:
            continue
        if user.name == target:
            return user
    return None


API_KEY = "sk-abc123secret456"  # PS001: Hardcoded secret


def dangerous_eval(user_input):
    """PS002: eval() on user input."""
    return eval(user_input)


def load_config(path):
    """PC001: Bare except."""
    try:
        with open(path) as f:
            return f.read()
    except:
        return None
