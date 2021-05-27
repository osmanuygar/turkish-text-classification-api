from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    name='advanced-analytic-platform',
    version='1.0.0',
    description='Advanced analytic platform is a broad category of inquiry that can be used to help drive changes and '
                'improvements in business practices.', 

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    include_package_data=True,
    install_requires=['flask-restplus==0.9.2', 'Flask-SQLAlchemy==2.1'],

)
