from distutils.core import setup

setup(name='ecart',
      packages=['ecart'],
      version='1.0.0',
      description='Framework agnostic, redis backed, cart system, Python library ',
      author='Nimesh Kiran Verma, Rohit khatana',
      author_email='nimesh.aug11@gmail.com, rohitkhatana.khatana@gmail.com',
      url='https://github.com/nimeshkverma/ecart',
      download_url='https://github.com/nimeshkverma/ecart/tarball/1.0.0',
      py_modules=['ecart'],
      install_requires=['redis'],
      keywords=['ecart', 'cart', 'redis', 'E-commerce', 'webservices'],
      classifiers=[],
      )
