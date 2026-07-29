.PHONY: validate validate-variants validate-edge generate verify-live test

validate:
	python3 scripts/validate_registry.py

validate-variants:
	python3 scripts/validate_variants.py

validate-edge:
	python3 scripts/validate_edge_exceptions.py

generate:
	python3 scripts/generate_readme.py

verify-live:
	python3 scripts/verify_hf.py

test:
	python3 -m unittest discover -s tests -v
