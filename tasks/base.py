from invoke import task


@task
def clean(ctx):
    """clean - remove build artifacts."""
    ctx.run('rm -rf build/')
    ctx.run('rm -rf dist/')
    ctx.run('rm -rf sirbot.egg-info')
    ctx.run('find . -name __pycache__ -delete')
    ctx.run('find . -name *.pyc -delete')
    ctx.run('find . -name *.pyo -delete')
    ctx.run('find . -name *~ -delete')


@task
def test(ctx):
    """test - run the test runner."""
    ctx.run('py.test --flakes --cov-report html --cov sirbot tests/',
            "dsome other foo")
    ctx.run('open htmlcov/index.html')


@task
def lint(ctx):
    """lint - check style with flake8."""
    ctx.run('flake8 sirbot tests')


@task(clean)
def publish(ctx):
    """publish - package and upload a release to the cheeseshop."""
    ctx.run('python setup.py sdist upload', pty=True)
    ctx.run('python setup.py bdist_wheel upload', pty=True)


@task
def fmt(ctx):
    ctx.run('find . -name helpers.py -exec autopep8 --recursive '
            '--aggressive --aggressive --experimental --in-place {} +')


@task
def fmt_dry(ctx):
    ctx.run('find . -name helpers.py '
            '-exec autopep8 --recursive --aggressive --aggressive '
            '--experimental -d {} +')


@task
def swagger(ctx):
    ctx.run('swagger project edit swagger')
