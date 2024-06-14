.. _parsing-label:

Parsing
=======
Under the hood, |project_name| parses source code into **Syntax Trees**.

|project_name| can work with two types of **Syntax Trees**:

* Concrete Syntax Trees (CST)
* Abstract Syntax Trees (AST)

CSTs capture all syntactic and grammar information without any loss of information.

ASTs capture the hierarchical flow of operations in the code but loses information in terms
of syntax. Because of this, using the AST parser can result in unexpected changes to the original code.

Simple Example
..............

Consider the expression ``a + b * c``.

CST would represent this expression as:

.. code-block:: text

        Expression
    ├── Term
    │   ├── Factor (a)
    ├── +
    ├── Term
    │   ├── Factor (b)
    │   ├── *
    │   ├── Factor (c)

Every character in the expression and the relationships between characters is represented.

AST might something like:

.. code-block:: text

    +
    ├── a
    └── *
        ├── b
        └── c

Python Example
..............

Lets consider the following function:

.. code-block:: python

    def add(x, y):
        # summing function
        return x + y


The AST tree would created using the python ``ast`` library would look like:

.. code-block:: python

    ast.Module(
        body=[
            ast.FunctionDef(
                decorator_list=[],
                returns=None,
                name="add",
                args=ast.arguments(
                    args=[
                        ast.arg(
                            arg="x"
                        ),
                        ast.arg(
                            arg="y"
                        )
                    ]
                ),
                body=[
                    ast.Return(
                        value=ast.BinOp(
                            left=ast.Name(
                                id="x"
                            ),
                            right=ast.Name(
                                id="y"
                            ),
                            op=ast.Add()
                        )
                    )
                ]
            )
        ]
    )

This AST tree is enough to robustly capture the fact that the function takes two values and adds them.
However, the comment is lost and whitespaces and line breaks might not be preserved.

Here is the CST for the same simple function:

.. code-block:: python

    Module(
        body=[
            FunctionDef(
                name=Name(
                    value='add',
                    lpar=[],
                    rpar=[],
                ),
                params=Parameters(
                    params=[
                        Param(
                            name=Name(
                                value='x',
                                lpar=[],
                                rpar=[],
                            ),
                            annotation=None,
                            equal=MaybeSentinel.DEFAULT,
                            default=None,
                            comma=Comma(
                                whitespace_before=SimpleWhitespace(
                                    value='',
                                ),
                                whitespace_after=SimpleWhitespace(
                                    value=' ',
                                ),
                            ),
                            star='',
                            whitespace_after_star=SimpleWhitespace(
                                value='',
                            ),
                            whitespace_after_param=SimpleWhitespace(
                                value='',
                            ),
                        ),
                        Param(
                            name=Name(
                                value='y',
                                lpar=[],
                                rpar=[],
                            ),
                            annotation=None,
                            equal=MaybeSentinel.DEFAULT,
                            default=None,
                            comma=MaybeSentinel.DEFAULT,
                            star='',
                            whitespace_after_star=SimpleWhitespace(
                                value='',
                            ),
                            whitespace_after_param=SimpleWhitespace(
                                value='',
                            ),
                        ),
                    ],
                    star_arg=MaybeSentinel.DEFAULT,
                    kwonly_params=[],
                    star_kwarg=None,
                    posonly_params=[],
                    posonly_ind=MaybeSentinel.DEFAULT,
                ),
                body=IndentedBlock(
                    body=[
                        SimpleStatementLine(
                            body=[
                                Return(
                                    value=BinaryOperation(
                                        left=Name(
                                            value='x',
                                            lpar=[],
                                            rpar=[],
                                        ),
                                        operator=Add(
                                            whitespace_before=SimpleWhitespace(
                                                value=' ',
                                            ),
                                            whitespace_after=SimpleWhitespace(
                                                value=' ',
                                            ),
                                        ),
                                        right=Name(
                                            value='y',
                                            lpar=[],
                                            rpar=[],
                                        ),
                                        lpar=[],
                                        rpar=[],
                                    ),
                                    whitespace_after_return=SimpleWhitespace(
                                        value=' ',
                                    ),
                                    semicolon=MaybeSentinel.DEFAULT,
                                ),
                            ],
                            leading_lines=[
                                EmptyLine(
                                    indent=True,
                                    whitespace=SimpleWhitespace(
                                        value='',
                                    ),
                                    comment=Comment(
                                        value='# summing function',
                                    ),
                                    newline=Newline(
                                        value=None,
                                    ),
                                ),
                            ],
                            trailing_whitespace=TrailingWhitespace(
                                whitespace=SimpleWhitespace(
                                    value='',
                                ),
                                comment=None,
                                newline=Newline(
                                    value=None,
                                ),
                            ),
                        ),
                    ],
                    header=TrailingWhitespace(
                        whitespace=SimpleWhitespace(
                            value='',
                        ),
                        comment=None,
                        newline=Newline(
                            value=None,
                        ),
                    ),
                    indent=None,
                    footer=[],
                ),
                decorators=[],
                returns=None,
                asynchronous=None,
                leading_lines=[],
                lines_after_decorators=[],
                whitespace_after_def=SimpleWhitespace(
                    value=' ',
                ),
                whitespace_after_name=SimpleWhitespace(
                    value='',
                ),
                whitespace_before_params=SimpleWhitespace(
                    value='',
                ),
                whitespace_before_colon=SimpleWhitespace(
                    value='',
                ),
                type_parameters=None,
                whitespace_after_type_parameters=SimpleWhitespace(
                    value='',
                ),
            ),
        ],
        header=[
            EmptyLine(
                indent=True,
                whitespace=SimpleWhitespace(
                    value='',
                ),
                comment=None,
                newline=Newline(
                    value=None,
                ),
            ),
        ],
        footer=[],
        encoding='utf-8',
        default_indent='    ',
        default_newline='\n',
        has_trailing_newline=True,
    )

The CST is considerably longer and more complex but holds information about syntax, formatting and comments.

By default, |project_name| uses the ``libcst`` python library to parse source code into a python friendly CST.
The parser can be changed to AST by using the ``--parser=ast`` option on the command line.

**It is strongly recommended to use the default CST parser**
