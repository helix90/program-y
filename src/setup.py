from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

version = None
with open(path.join(here, "version.txt"), encoding="utf-8") as f:
    version = f.read()
version = version.strip()
print("Building PyPi Package for version %s" % version)

if version is None:
    print("No version.txt found")

long_description = ""
with open(path.join(here, path.join(here, "README.md")), encoding="utf-8") as f:
    long_description = f.read()

download_url = "https://github.com/keiffster/program-y/%s.tar.gz" % version

setup(
    name="programy",
    packages=find_packages(),
    package_data={"": ["*.conf", "*.aiml"]},
    include_package_data=True,
    version=version,
    description="AIML Framework and Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Keith Sterling",
    author_email="keiffster@gmail.com",
    url="https://github.com/keiffster/program-y.git",
    download_url=download_url,
    keywords=["aiml", "chatbot", "virtual assistant", "ai"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "python-dateutil==2.8.1",
        "wget==3.2",
        "urllib3==1.26.19",
        "beautifulsoup4==4.8",
        "lxml==4.9.1",
        "PyYAML==6.0.1",
        "Flask==2.3.2",
        "Flask-SocketIO==4.2.1",
        "tweepy==3.8.0",
        "slixmpp==1.8.5",
        "python-telegram-bot==21.4",
        "pymessenger==0.0.7.0",
        "twilio==9.2.3",
        "slackclient==2.9.3",
        "viberbot==1.0.11",
        "line-bot-sdk==1.15.0",
        "discord.py==2.4.0",
        "botbuilder-core==4.16.1",
        "botbuilder-schema>=4.16.1",
        "wikipedia==1.4.0",
        "MetOffer==1.3.2",
        "APScheduler==3.7.0",
        "emoji==0.5.4",
        "autocorrect==0.4.4",
        "textblob==0.15.3",
        "redis==4.4.4",
        "pymongo==3.10.0",
        "SQLAlchemy==1.3.12",
        "PyMySQL==0.9.3",
    ],
)
