from setuptools import setup

setup(
    name='gcalendar',
    version='0.0.4',
    description='An google calendar wrapper to integrate with the Getting Things Done framework.',
    url='https://github.com/GTDSL-GCalendar',
    author='Yeboster',
    author_email='yeboster@gmail.com',
    license='MIT',
    packages=['gcalendar'],
    install_requires=['google-api-python-client',
                      'google-auth-httplib2',
                      'google-auth-oauthlib'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Productivity',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
)
