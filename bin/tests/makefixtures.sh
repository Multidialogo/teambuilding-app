#!/usr/bin/env bash

fixtures_dir="./tests/fixtures"
fixture_filename="fixture.yaml"

(
  set -o errexit
  set -o pipefail
  set -o nounset

  mkdir -p "${fixtures_dir}"

  python manage.py dumpdata --format yaml -e auth.permission \
    -e contenttypes.contenttype -e sessions.session \
    -e postaladdress.country -e postaladdress.countryadminlevelmapping \
    >"${fixtures_dir}/${fixture_filename}"
)
