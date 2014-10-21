python build_pdf.py -p 1 --hw 6 --landscape --chars-per-line=165 -o hw6/searchout --to-ps - hw6/searchout.txt
echo "built search out"
# python build_pdf.py --hw 6 -o hw6/code --to-ps hw6/search.py witschey/base.py witschey/basic_stats.py witschey/log/log.py witschey/log/numberlog.py witschey/models/__init__.py witschey/models/model.py witschey/models/independent_variable.py witschey/models/dtlz7.py witschey/models/fonseca.py witschey/models/kursawe.py witschey/models/schaffer.py witschey/models/viennet3.py witschey/models/zdt1.py witschey/models/zdt3.py  witschey/searchers/searcher.py witschey/searchers/simulated_annealer.py witschey/searchers/maxwalksat.py witschey/searchers/genetic_algorithm.py  witschey/rdiv.py

ps2pdf @hw6/hw6.in hw6/witschey.pdf
