# 📥 Installation 


**Prerequisites:**

- 🐍 Python 3.10 or higher 
- 📦 pip or [Poetry] 


## 📦 pip

**PLUTUS** is published as a python package and can be installed with
`pip`, ideally by using a [virtual environment]. Open up a terminal and install with:

=== "Latest"

    ``` sh
    pip install plutus-pairtrading
    ```

=== "1.x"

    ``` sh
    pip install plutus-pairtrading=="1.*" # (1)!
    ```

    1.  PLUTUS uses [semantic versioning].

        This will make sure that you don't accidentally [upgrade to the next
        major version], which may include breaking changes that silently corrupt
        your site. Additionally, you can use `pip freeze` to create a lockfile,
        so builds are reproducible at all times:

        ```
        pip freeze > requirements.txt
        ```

        Now, the lockfile can be used for installation:

        ```
        pip install -r requirements.txt
        ```

This will automatically install compatible versions of all dependencies. **PLUTUS** always strives to support the latest versions, so there's no need to install the dependencies separately. PLUTUS dependencies are listed below: 

  [numpy] | [pandas] | [plotly] | [requests] | [matplotlib] | [yfinance] | [arch] | [seaborn]

---

!!! tip

    If you don't have prior experience with Python, we recommend reading
    [Using Python's pip to Manage Your Projects' Dependencies], which is a
    really good introduction on the mechanics of Python package management and
    helps you troubleshoot if you run into errors.

  [Python package]: https://pypi.org/project/plutus-pairtrading/
  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
  [semantic versioning]: https://semver.org/
  [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/


## 🐙 Git

**PLUTUS** can be directly used from [GitHub] by cloning the
repository into a subfolder of your project root which might be useful if you
want to use the very latest version:

```
git clone https://github.com/fox-techniques/plutus-pairtrading.git
```

Next, install the theme and its dependencies with:

```
pip install -e plutus-pairtrading
```

## 🎭 Poetry


Installing **PLUTUS**:

```bash
poetry add plutus-pairtrading
```

This command downloads and installs the package and its dependencies and adds the package as a dependency in your `pyproject.toml`.

Using the Package:

After installation, you can start using the package in your project. If you need to enter the virtual environment managed by Poetry, run:

```bash
poetry shell
```

Verify the Installation:

```bash
poetry show plutus-pairtrading
```

Updating the Package:

```bash
poetry update plutus-pairtrading
```

Add packages to a group:

```bash
poetry add --group notebook jupyter ipykernel
```

Install the dependencies from a group:
```bash
poetry install --with notebook
```


  [GitHub]: https://github.com/fox-techniques/plutus-pairtrading
  [numpy]: https://pypi.org/project/numpy/
  [pandas]: https://pypi.org/project/pandas/
  [plotly]: https://pypi.org/project/plotly/
  [requests]: https://pypi.org/project/requests/
  [matplotlib]: https://pypi.org/project/matplotlib
  [yfinance]: https://pypi.org/project/yfinance
  [arch]: https://pypi.org/project/arch
  [seaborn]: https://pypi.org/project/seaborn
  [Poetry]: https://python-poetry.org/docs/#installation