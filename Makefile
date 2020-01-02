.PHONY: autoformat tests

autoformat:
	git ls-files | grep -P '\.py$$' | xargs isort
	git ls-files | grep -P '\.py$$' | xargs black -S

tests:
	pytest
	git ls-files | grep -P '\.py$$' | xargs black -S --check
