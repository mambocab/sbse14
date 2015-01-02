python build_pdf.py -p 1 --hw 7 --landscape --chars-per-line=210 -o hw7/searchout --to-ps - hw7/searchout.txt
echo "built search out"
python build_pdf.py --hw 7 -o hw7/code --to-ps hw7/search.py witschey/base.py witschey/basic_stats.py witschey/log/log.py witschey/log/numberlog.py witschey/models/__init__.py witschey/models/model.py witschey/models/independent_variable.py witschey/models/dtlz7.py witschey/models/fonseca.py witschey/models/kursawe.py witschey/models/schaffer.py witschey/models/viennet3.py witschey/models/zdt1.py witschey/models/zdt3.py witschey/models/osyczka.py witschey/searchers/searcher.py witschey/searchers/simulated_annealer.py witschey/searchers/maxwalksat.py witschey/searchers/genetic_algorithm.py witschey/searchers/particle_swarm_optimizer.py witschey/rdiv.py

ps2pdf @hw7/hw7.in hw7/witschey.pdf
