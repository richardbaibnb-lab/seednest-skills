"""Read-only comparison of QuickBooks bank-feed CSV snapshots (stdlib only)."""
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = ('Date', 'Bank description', 'Amount', 'GST', 'From/To', 'Match/Categorise')

def text(value):
    return re.sub(r'\s+', ' ', value or '').strip()

def amount(value):
    cleaned = text(value).replace(',', '').replace('A$', '').replace('$', '')
    if cleaned.startswith('(') and cleaned.endswith(')'):
        cleaned = '-' + cleaned[1:-1]
    try:
        return str(Decimal(cleaned).quantize(Decimal('0.01')))
    except InvalidOperation as exc:
        raise ValueError(f'Unrecognised amount: {value!r}') from exc

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        missing = set(REQUIRED) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'{path}: missing CSV columns: {sorted(missing)}')
        rows = []
        for number, row in enumerate(reader, 2):
            if None in row:
                raise ValueError(f'{path}: malformed CSV row {number}')
            rows.append({key: text(value) for key, value in row.items()})
        return rows

def key(row):
    return row['Date'], row['Bank description'], amount(row['Amount'])

def grouped(rows):
    result = defaultdict(list)
    for row in rows:
        result[key(row)].append(row)
    return result

def compare(before, after):
    old, new = grouped(before), grouped(after)
    duplicate = sorted(k for k in old.keys() | new.keys() if len(old[k]) > 1 or len(new[k]) > 1)
    added = [{'key': k, 'count': len(new[k]) - len(old[k])} for k in sorted(new) if len(new[k]) > len(old[k])]
    removed = [{'key': k, 'count': len(old[k]) - len(new[k])} for k in sorted(old) if len(old[k]) > len(new[k])]
    changes = []
    fields = Counter()
    for k in sorted(old.keys() & new.keys()):
        if len(old[k]) != 1 or len(new[k]) != 1:
            continue  # Never guess which of identical bank rows was changed.
        a, b = old[k][0], new[k][0]
        differences = {f: {'before': a.get(f, ''), 'after': b.get(f, '')}
                       for f in sorted(a.keys() | b.keys()) if a.get(f, '') != b.get(f, '')}
        if differences:
            changes.append({'key': k, 'fields': differences})
            fields.update(differences.keys())
    return {
        'before_count': len(before), 'after_count': len(after),
        'added': added, 'removed': removed,
        'ambiguous_duplicate_keys': duplicate,
        'same_transaction_multiset': not added and not removed,
        'unique_pairing_complete': not duplicate and not added and not removed,
        'changed_unique_rows': len(changes), 'changed_fields': dict(fields),
        'changes': changes,
        'note': 'A difference report only; not confirmation of correct categories or GST. Changed identity fields appear as removed/added records.'
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.out and args.out.resolve() in {args.before.resolve(), args.after.resolve()}:
        parser.error('--out must not overwrite an input file')
    result = compare(read(args.before), read(args.after))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + '\n', encoding='utf-8')
    print(payload)

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
