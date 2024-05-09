import setuptools

DEPENDENCIES = ["ast_comments==1.2.2", "astor==0.8.1", "libcst==1.3.1"]
EXCLUDE_FROM_PACKAGES = ["tests*"]

if __name__ == "__main__":
    setuptools.setup(
        packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGES),
        install_requires=DEPENDENCIES,
        entry_points={
            "console_scripts": [
                "csort = src.main:main",
            ]
        },
    )
