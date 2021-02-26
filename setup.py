from setuptools import setup

setup(
    name='mft',
    version='0.0.1',
    description="A package to facilitate sharing files via SolarWinds Managed File Transfer.",
    url='https://github.com/GitPushPullLegs/contextualmft',
    author='Joe Aguilar',
    author_email='Jose.Aguilar.6694@gmail.com',
    license='GNU General Public License',
    packages=[],
    install_requires=['mft @ git+https://github.com/GitPushPullLegs/mft.git',
                      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)