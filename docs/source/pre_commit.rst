.. _precommit-label:

Pre-commit
==========

Pre-commit is great tool for catching bugs early and ensuring consistency across developers.

Csort can be used as part of a pre-commit workflow.

Steps
-----

1. Install pre-commit

.. code-block:: console

   $ pip install pre-commit

2. Create a ``.pre-commit-config.yaml`` file

.. code-block:: console

   $ touch .pre-commit-config.yaml

3. Paste in the msort hook

.. code-block:: yaml

    - repo: https://github.com/isaacksdata/msort
    rev: v0.1.8
    hooks:
      - id: msort
        args: []

4. Initiate pre-commit

.. code-block:: console

   $ pre-commit init


Common amendments
.................

* exclusion criteria
    Files can be excluded using the ``--skip-patterns`` option

.. code-block:: yaml

    - repo: https://github.com/isaacksdata/msort
    rev: v0.1.8
    hooks:
      - id: msort
        args: ["--skip-patterns=test_", "--skip-patterns=_test.py"]

* personalised configurations
    Csort in pre-commit can be configured by the user through CLI arguments or through a config
    file - see :ref:`config-label`

.. code-block:: yaml

    - repo: https://github.com/isaacksdata/msort
    rev: v0.1.8
    hooks:
      - id: msort
        args: ["--config-path=./pyproject.toml"]
