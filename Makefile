.PHONY: autoformat

autoformat:
	git ls-files | grep -P '\.py$$' | xargs isort
	git ls-files | grep -P '\.py$$' | xargs black -S
