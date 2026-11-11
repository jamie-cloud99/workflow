# Recorded workspace observations

Repository: acme/report-ui. Export logic: src/export.js. Existing test tests/export.test.js is named "exports reports" but only asserts that the result is an array.
Another suite, tests/filter.test.js, covers archived filtering for the list view and passes.
The API is mocked in all tests; no real backend test exists.
