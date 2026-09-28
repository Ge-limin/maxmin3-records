#!/bin/bash
# Full run, resumable: a finished n leaves logs/done_n{n}; rerunning skips it.
# Usage: ./pipeline.sh [WORKERS]   (default 4)
set -u
cd "$(dirname "$0")"
PY=.venv/bin/python
W=${1:-4}
SEARCH=360    # seconds of random multistart per worker per n
IMPROVE=840   # seconds of basin hopping per worker per n
SWEEP=300     # seconds per worker in the final pass over unconverged n

run() {  # run SCRIPT N SECONDS TAG on W workers and wait
  for s in $(seq 1 "$W"); do
    $PY "$1" "$2" "$3" $(( $2 * 100 + $4 * 10 + s )) >> "logs/n$2.log" 2>&1 &
  done
  wait
}

for n in $(seq 30 50); do
  [ -f "logs/done_n$n" ] && continue
  echo "$(date '+%F %T') n=$n start" >> logs/pipeline.log
  run search.py "$n" "$SEARCH" 1
  run improve.py "$n" "$IMPROVE" 2
  $PY verify.py "bests/n$n.npy" >> logs/pipeline.log
  touch "logs/done_n$n"
done

if [ ! -f logs/done_sweep ]; then
  for n in $($PY report.py --loose); do
    echo "$(date '+%F %T') sweep n=$n" >> logs/pipeline.log
    run improve.py "$n" "$SWEEP" 3
  done
  touch logs/done_sweep
fi
$PY report.py >> logs/pipeline.log
echo "$(date '+%F %T') ALL DONE" >> logs/pipeline.log
touch logs/DONE
