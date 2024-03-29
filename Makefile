.PHONY: autoformat build run

autoformat:
	git ls-files | grep -P '\.py$$' | xargs isort
	git ls-files | grep -P '\.py$$' | xargs black -S

build:
	docker build -t kyokley/battleship .

run:
	docker run --rm -t -v $(pwd):/code/BattlePyAI kyokley/battleship --vis
