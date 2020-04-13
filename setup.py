from distutils.core import setup

setup(
    name='MangroveConservation',
    version='0.1dev',
    description='use twitter data to measure public perception related to mangrove conservation and deforestation',
    autor='Mimi Gong',
    author_email='gongmimi@msu.edu',
    packages=['MangroveConservation',],
    license='MIT',
    #long_description=open('README.md').read(),
    install_requires=[
        'jupyter',
        'spacy',
        'pandas',
        'pyyaml',
        'pylint', 
        'matplotlib',
        'lxml',
        'gensim',
        'scikit-learn',
        'nltk',
        'textblob',
        'json_lines',
        'pyLDAvis',
        'wordcloud',
        'numpy',
        'pdoc3',
        'autopep8',
        'pytest',
        'pip'
    ])
