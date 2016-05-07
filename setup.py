from distutils.core import setup

setup(name='cartman',
      packages=['cartman'],
      version='1.0.0',
      description='Framework agnostic, redis backed, cart system, Python library ',
      author='Nimesh Kiran Verma, Rohit khatana',
      author_email='nimesh.aug11@gmail.com, rohitkhatana.khatana@gmail.com',
      url='https://github.com/nimeshkverma/cartman',
      download_url='https://github.com/nimeshkverma/cartman/tarball/1.0.0',
      py_modules=['cartman'],
      install_requires=['pymongo'],
      keywords=['cartman', 'cart', 'redis', 'E-commerce', 'webservices'],
      classifiers=[],
      )
