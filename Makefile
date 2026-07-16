.PHONY: validate validate-variants generate verify-live test

validate:
	python3 scripts/validate_registry.py

validate-variants:
	python3 scripts/validate_variants.py

generate:
	python3 scripts/generate_readme.py

verify-live:
	python3 scripts/verify_hf.py

test:
	python3 -m unittest discover -s tests -v
