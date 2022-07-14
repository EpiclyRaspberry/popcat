from setuptools import setup, find_packages
extras={
    "dpy":["discord.py>=1.0.0"],
    "pillow":["pillow"]
}
setup(
   name="popcat",
   version="0.0.1",
   author="EpiclyRaspberry",
   author_email="raspberryepicly@gmail.com",
   description="An asynchronous api wrapper for popcat.xyz",
   long_description="An asynchronous api wrapper for popcat.xyz",
   packages=find_packages(),
   install_requires=["aiohttp","aiofiles"],
   extras_require=extras,
   classifiers=[
   "Development Status :: 2 - Pre-Alpha",
   "License :: OSI Approved :: MIT License",
   "Operating System :: OS Independent",
   "Topic :: Internet",
   "Topic :: Software Development :: Libraries",
   "Topic :: Software Development :: Libraries :: Python Modules",
   "Topic :: Utilities",
   "Programming Language :: Python :: 3",
   "Intended Audience :: Developers",
   "Natural Language :: English"
   ]
   )