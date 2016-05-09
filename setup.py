from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


setup(name='ecart',
      packages=['ecart'],
      version='1.0.2',
      description='Framework agnostic, redis backed, cart system, Python library ',
      long_description=long_description,
      author='Nimesh Kiran Verma, Rohit khatana',
      author_email='nimesh.aug11@gmail.com, rohitkhatana.khatana@gmail.com',
      url='https://github.com/nimeshkverma/ecart',
      download_url='https://github.com/nimeshkverma/ecart/tarball/1.0.2',
      py_modules=['ecart'],
      install_requires=['redis'],
      keywords=['ecart', 'cart', 'redis', 'E-commerce', 'webservices'],
      classifiers=[],
      )
