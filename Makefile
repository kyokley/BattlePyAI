.PHONY: autoformat build run

autoformat:
	git ls-files | grep -P '\.py$$' | xargs isort
	git ls-files | grep -P '\.py$$' | xargs black -S

build:
	docker build -t kyokley/battleship .

run:
	docker run --rm -t -v $(pwd):/code/BattlePyAI kyokley/battleship --vis

tournament:
	docker run --rm -t -v $$(pwd):/code/BattlePyAI --entrypoint "python" kyokley/battleship tournament.py --vis $$(find ./solutions -name '*.py' | grep -v __init__ | sed -e 's/^.\{2\}//' | sed -e 's/\.py$$//' | sed 's!/!.!g')
